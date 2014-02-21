#-*- coding:utf-8 -*-

"""
This file is part of P0009.1.

P0009.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0009.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0009.1.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import numpy as np
import warnings
from analysis import plot
from matplotlib import pyplot as plt
from exparser import TraceKit as tk
from exparser.PivotMatrix import PivotMatrix
from exparser.TangoPalette import *

# The parameters to extract the pupil trace for the various epochs
trialParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'trial',
	'baseline'		: 'baseline',
	'baselineLock'	: 'end',
	'traceLen'		: 3000
	}

# The window size for the lme. (production value: 1)
winSize = 250
# The number of simulations for the lme. (production value: 10000)
nsim = 10
# Stimulus durations.
cueDur = 50
targetDur = 50

def filter(dm):

	"""
	Performs data pre-processing, including outlier removal, and recoding.

	Arguments:
	dm		--	A DataMatrix.

	Returns:
	A DataMatrix.
	"""

	# Select columns
	dm = dm.select('practice == "no"')
	dm = dm.select('maxHGazeErr <= 100')
	dm = dm.selectByStdDev(['file'], 'response_time')
	print 'N(trials) = %d' % len(dm)
	# Add cued luminance field for easy processing later on
	dm = dm.addField('cueLum', dtype=str)
	dm['cueLum'] = 'dark'
	i = dm['brightSide'] == dm['cueSide']
	dm['cueLum'][i] = 'bright'
	return dm

def behavior(dm):

	"""
	Analysis of the behavioral results.

	Arguments:
	dm		--	A DataMatrix.

	Returns:
	A DataMatrix.
	"""

	dmc = dm.select('correct == 1')

	pm = PivotMatrix(dm, ['soa'], ['subject_nr'], dv='ctoa')
	pm._print('CTOA')
	pm.save('output/ctoa.csv')
	pm = PivotMatrix(dmc, ['cueValidity', 'soa'], ['subject_nr'], \
		dv='response_time')
	pm.save('output/rt.csv')
	pm._print('Correct RT')
	pm.linePlot(show=True)
	pm = PivotMatrix(dm, ['cueValidity', 'soa'], ['subject_nr'], \
		dv='correct')
	pm.save('output/acc.csv')
	pm._print('Accuracy')
	pm.linePlot(show=True)

def tracePlot(dm, traceParams=trialParams, suffix='', err=True):

	"""
	A pupil-trace plot for a single epoch.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	traceParams		--	The trace parameters. (default=trialParams)
	suffix			--	A suffix to identify the trace. (default='')
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	"""

	x1, y1, err1 = tk.getTraceAvg(dm.select('cueLum == "bright"'), \
		**traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select('cueLum == "dark"'), **traceParams)
	if err:
		d = y2-y1
		aErr = lmeTrace(dm, traceParams=traceParams, suffix=suffix)
		aP = aErr[:,0]
		aLo = aErr[:,1]
		aHi = aErr[:,2]
		minErr = (d-aLo)/2
		maxErr = (aHi-d)/2
		y1min = y1 - minErr
		y1max = y1 + maxErr
		y2min = y2 - minErr
		y2max = y2 + maxErr
		plt.fill_between(x1, y1min, y1max, color=green[1], alpha=.25)
		plt.fill_between(x2, y2min, y2max, color=blue[1], alpha=.25)
	plt.plot(x1, y1, color=green[1])
	plt.plot(x2, y2, color=blue[1])

def trialPlot(dm, show=True, err=True):

	"""
	A pupil-trace plot for the full trial epoch.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	show			--	Indicates whether the plot should be shown.
						(default=True)
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	"""

	if show:
		plot.new()
	plt.axhline(1, linestyle='--', color='black')
	dm = dm.select('soa == 2445')
	tracePlot(dm, err=err)
	# Cue
	plt.axvspan(0, cueDur, color=blue[1], alpha=.2)
	# Target
	plt.axvspan(2500, 2500+targetDur, color=blue[1], alpha=.2)
	if show:
		plot.save('trialPlot', show=True)

def subjectPlot(dm):

	"""
	Generates a separate trial plot for each subject.

	Arguments:
	dm		--	A DataMatrix.

	"""

	plot.new(size=plot.hi)
	i = 1
	for _dm in dm.group('subject_nr'):
		subject_nr = _dm['subject_nr'][0]
		N = len(_dm)
		plt.subplot(dm.count('subject_nr')/2, 2, i)
		plt.title('%s (%d)' % (subject_nr, N))
		trialPlot(_dm, show=False, err=False)
		i += 1
	plot.save('subjectPlot', show=True)

def lmeTrace(dm, traceParams=trialParams, suffix=''):

	"""
	Performs the lme analysis for the cueLum Bright vs Dark contrast. To speed
	up the analysis, the results are cached.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	traceParams		--	The trace parameters. (default=trialParams)
	suffix			--	A suffix to identify the trace. (default='')

	Returns:
	A 2D array where the columns are [p, ciHi, ciLo] and the rows are the
	samples.
	"""

	cachePath = 'cache/lmeTrace%s.npy' % suffix
	if os.path.exists(cachePath) and not '--no-cache' in sys.argv:
		print 'Retrieving lmeTrace from cache (%s)' % cachePath
		return np.load(cachePath)
	a = tk.mixedModelTrace(dm, ['cueLum'], ['subject_nr'], winSize=winSize, \
		nSim=nsim, **traceParams)
	np.save(cachePath, a)
	return a

# Sanity checks
if winSize != 1:
	warnings.warn('winSize should be 1 for production!')
if nsim != 10000:
	warnings.warn('nsim should be 10000 for production!')
