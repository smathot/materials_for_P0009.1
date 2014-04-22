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
from matplotlib import pyplot as plt
from exparser import TraceKit as tk
from exparser.PivotMatrix import PivotMatrix
from exparser.TangoPalette import *
from exparser.RBridge import RBridge
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser import Plot
from scipy.stats import linregress

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
winSize = 1
# Stimulus durations.
cueDur = 50
targetDur = 50
# Determines whether we use sample-based or fixaton-base checking of gaze
# position. Sample-based is better in principle, but leads to a huge loss of
# data.
gazeCheckMethod = 'fixation'
# Some colors for the plots
valColor = green[1]
invColor = red[1]
# The model to be used for the mixed-model trace
traceModel = 'cueLum + (1|subject_nr)'
# Indicates whether plots should be shown or only saved to disk
show = True

def __fullPathway__(dm):

	"""
	Runs the full analysis pathway.

	Arguments:
	dm		--	A DataMatrix.
	"""

	global show
	show = False
	descriptives(dm)
	lmeBehavior(dm)
	trialPlot1000(dm)
	trialPlot2500(dm)
	corrPlot100_2500(dm)
	corrPlot1000(dm)
	corrPlot2500(dm)

def corrExample(dm, soaBehav, soaPupil, dv='correct'):

	"""
	Plots an example of the correlation between behavior and pupil size at the
	most strongly correlating point.

	Arguments:
	dm			--	A DataMatrix.
	soaBehav	--	The SOA to analyze for the behavioral effect.
	soaPupil	--	The SOA to analyze for the pupil effect.

	Keyword arguments:
	dv			--	The dependent variable to use for the behavioral effect.
					(default='correct')
	"""

	assert(soaPupil in dm.unique('soa'))
	assert(soaBehav in dm.unique('soa'))
	a = corrTrace(dm, soaBehav, soaPupil, dv='correct', suffix='acc', \
		cacheId='corrTrace.correct.%d.%d' % (soaBehav, soaPupil))
	bestSample = np.argmax(a[:,0])
	dmBehav = dm.select('soa == %d' % soaBehav)
	dmPupil = dm.select('soa == %d' % soaPupil)
	xData = []
	yData = []
	print 'pp\tbehav\tpupil'
	for subject_nr in dm.unique('subject_nr'):
		ceb = cuingEffectBehav(dmBehav.select('subject_nr == %d' \
			% subject_nr, verbose=False), dv=dv)
		cep = cuingEffectPupil(dmPupil.select('subject_nr == %d' \
			% subject_nr, verbose=False), epoch=(bestSample, \
			bestSample+winSize))
		print '%.2d\t %.4f\t%.4f' % (subject_nr, ceb, cep)
		yData.append(100.*ceb)
		xData.append(cep)
	s, _i, r, p, se = linregress(xData, yData)
	print '%d: r = %.4f, p = %.4f' % (bestSample, r, p)
	xFit = np.array([min(xData), max(xData)])
	yFit = _i + s*xFit
	Plot.new(size=Plot.xs)
	plt.plot(xFit, yFit, '-', color='black')
	plt.axhline(0, linestyle='--', color='black')
	plt.axvline(0, linestyle='--', color='black')
	plt.plot(xData, yData, 'o', color='black')
	plt.ylabel('Behav. cuing effect (%)')
	plt.xlabel('Pupil cuing effect (norm.)')
	Plot.save('corrExample.%d.%d' % (soaBehav, soaPupil), show=show)

def corrPlot(dm, soaBehav, soaPupil):

	"""
	Plots and analyzes the correlation between the cuing effect in behavior and
	pupil size.

	Arguments:
	dm		--	A DataMatrix.
	soaBehav	--	The SOA to analyze for the behavioral effect.
	soaPupil	--	The SOA to analyze for the pupil effect.
	"""

	Plot.new(size=Plot.w)
	plt.ylim(-.2, 1)
	plt.xlabel('Time since cue onset (ms)')
	plt.ylabel('Behavior - pupil correlation (r)')
	plt.axhline(0, linestyle='--', color='black')
	# Cue shading
	plt.axvspan(0, cueDur, color=blue[1], alpha=.2)
	# Target shading
	targetOnset = soaPupil+55
	plt.axvspan(targetOnset, targetOnset+targetDur, color=blue[1], alpha=.2)
	plt.xlim(0, 2500)
	# Accuracy
	a = corrTrace(dm, soaBehav, soaPupil, dv='correct', suffix='acc', \
		cacheId='corrTrace.correct.%d.%d' % (soaBehav, soaPupil))
	tk.markStats(plt.gca(), a[:,1])
	plt.plot(a[:,0], label='Accuracy', color=blue[1])
	# RTs
	a = corrTrace(dm, soaBehav, soaPupil, dv='response_time', suffix='rt', \
		cacheId='corrTrace.rt.%d.%d' % (soaBehav, soaPupil))
	tk.markStats(plt.gca(), a[:,1])
	plt.plot(a[:,0], label='Response times', color=orange[1])
	plt.legend(frameon=False, loc='upper left')
	Plot.save('corrAnalysis.%d.%d' % (soaBehav, soaPupil), show=show)

def corrPlot100_2500(dm):

	"""
	A correlation plot between the behavioral response in the 100 ms SOA and
	the pupil trace in 2500 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 45, 2445)
	corrExample(dm, 45, 2445)

def corrPlot1000(dm):

	"""
	A behavior-pupil correlation plot for the 1000 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 945, 945)
	corrExample(dm, 945, 945)

def corrPlot2500(dm):

	"""
	A behavior-pupil correlation plot for the 2500 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 2445, 2445)
	corrExample(dm, 2445, 2445)

@cachedArray
def corrTrace(dm, soaBehav, soaPupil, dv='correct', suffix=''):

	"""
	Calculates the correlation between the behavioral cuing effect and the
	pupil-size cuing effect.

	Arguments:
	dm			--	A DataMatrix.
	soaBehav	--	The SOA to analyze for the behavioral effect.
	soaPupil	--	The SOA to analyze for the pupil effect.

	Keyword arguments:
	dv			--	The dependent variable to use for the behavioral cuing
					effect. (default='correct')
	suffix		--	A suffix to identify the trace for caching. (default='')

	Returns:
	A 2D numpy array r- and p-values for each sample.
	"""

	assert(soaPupil in dm.unique('soa'))
	assert(soaBehav in dm.unique('soa'))
	dmBehav = dm.select('soa == %d' % soaBehav)
	dmPupil = dm.select('soa == %d' % soaPupil)
	a = np.zeros((soaPupil+55, 2))
	for i in range(0, soaPupil+55, winSize):
		xData = []
		yData = []
		for subject_nr in dm.unique('subject_nr'):
			ceb = cuingEffectBehav(dmBehav.select('subject_nr == %d' \
				% subject_nr, verbose=False), dv=dv)
			cep = cuingEffectPupil(dmPupil.select('subject_nr == %d' \
				% subject_nr, verbose=False), epoch=(i, i+winSize))
			print '%.2d %.4f %.4f' % (subject_nr, ceb, cep)
			yData.append(ceb)
			xData.append(cep)
		s, _i, r, p, se = linregress(xData, yData)
		a[i:i+winSize, 0] = r
		a[i:i+winSize, 1] = p
		print 'soaBehav: %d, soaPupil: %d' % (soaBehav, soaPupil)
		print '%d: r = %.4f, p = %.4f' % (i, r, p)
	return a

def cuingEffectBehav(dm, dv='response_time'):

	"""
	Determines the behavioral cuing effect for a given dataset.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	dv		--	'response_time' or 'correct'. (default='response_time')

	Returns:
	A value reflecting the behavioral cuing effect, with positive values meaning
	a positive cuing effect.
	"""

	assert(dv in ['response_time', 'correct'])
	if dv == 'response_time':
		dm = dm.select('correct == 1', verbose=False)
	_dmVal = dm.select('cueValidity == "valid"', verbose=False)
	_dmInv = dm.select('cueValidity == "invalid"', verbose=False)
	cuingEffect = _dmInv[dv].mean() - _dmVal[dv].mean()
	if dv == 'correct':
		cuingEffect *= -1
	return cuingEffect

def cuingEffectPupil(dm, traceParams=trialParams, epoch=(500,1000)):

	"""
	Determines the pupil cuing effect for a given dataset. This is the mean
	difference between bright and dark trials within a specific epoch.

	Arguments:
	dm				--	A DataMatrix.

	Keyword arguments:
	traceParams		--	The trace parameters. (default=trialParams)
	epoch			--	The time interval for which to estimate the pupil
						effect. (default=(500,1000))

	Returns:
	A value reflecting the pupil cuing effect.
	"""

	x1, y1, err1 = tk.getTraceAvg(dm.select('cueLum == "bright"', verbose= \
		False), **traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select('cueLum == "dark"', verbose= \
		False), **traceParams)
	d = y2-y1
	d = d[epoch[0]:epoch[1]]
	return d.mean()

def descriptives(dm):

	"""
	Tabular analysis of the descriptive results.

	Arguments:
	dm		--	A DataMatrix.

	Returns:
	A DataMatrix.
	"""

	dmc = dm.select('correct == 1')
	pm = PivotMatrix(dm, ['soa'], ['subject_nr'], dv='ctoa')
	pm._print('CTOA')
	pm.save('output/ctoa.csv')
	pm = PivotMatrix(dm, ['subject_nr'], ['subject_nr'], dv=lambda x: len(x))
	pm._print('Cell count')
	pm.save('output/cellcount.csv')
	pm = PivotMatrix(dmc, ['cueValidity', 'soa'], ['subject_nr'], \
		dv='response_time')
	pm.save('output/rt.csv')
	pm._print('Correct RT')
	pm.linePlot(show=show)
	pm = PivotMatrix(dm, ['cueValidity', 'soa'], ['subject_nr'], \
		dv='correct')
	pm.save('output/acc.csv')
	pm._print('Accuracy')
	pm.linePlot(show=show)

@cachedDataMatrix
def filter(dm):

	"""
	Performs data pre-processing, including outlier removal, and recoding.

	Arguments:
	dm		--	A DataMatrix.

	Returns:
	A DataMatrix.
	"""

	dm = dm.select('practice == "no"')
	assert(gazeCheckMethod in ('fixation', 'sample'))
	if gazeCheckMethod == 'fixation':
		dm = dm.select('maxHFixErr <= 100')
	else:
		dm = dm.select('maxHGazeErr <= 100')
	print 'N(trials) = %d' % len(dm)
	# Recode brightSide and cueSide into cueLum for easy processing
	dm = dm.addField('cueLum', dtype=str)
	dm['cueLum'] = 'dark'
	i = dm['brightSide'] == dm['cueSide']
	dm['cueLum'][i] = 'bright'
	# Add inverse-rt field for lme analysis of behavioral data
	dm = dm.addField('irt', dtype=float)
	dm['irt'] = 1./dm['response_time']
	return dm

def tracePlot(dm, traceParams=trialParams, suffix='', err=True):

	"""
	A pupil-trace plot for a single epoch.

	Arguments:
	dm				--	A DataMatrix.

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
		aErr = lmeTrace(dm, traceParams=traceParams, suffix=suffix, \
			cacheId='lmeTrace%s' % suffix)
		aT = aErr[:,0]
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
		tk.markStats(plt.gca(), np.abs(aT), below=False, thr=2, minSmp=200)
	plt.plot(x1, y1, color=green[1], label='Cue on bright')
	plt.plot(x2, y2, color=blue[1], label='Cue on dark')

def trialPlot(dm, soa, _show=show, err=True, suffix=''):

	"""
	A pupil-trace plot for the full trial epoch.

	Arguments:
	dm				--	A DataMatrix.
	soa				--	The SOA to select.

	Keyword arguments:
	show			--	Indicates whether the plot should be shown.
						(default=True)
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	suffix			--	A suffix to identify the trace. (default='')
	"""

	assert(soa in dm.unique('soa'))
	if _show:
		Plot.new(size=Plot.ws)
	plt.axhline(1, linestyle='--', color='black')
	dm = dm.select('soa == %d' % soa)
	# Determine the trace length and create the trace plot
	traceLen = soa + 105
	traceParams = trialParams.copy()
	traceParams['traceLen'] = traceLen
	tracePlot(dm, traceParams=traceParams, err=err, \
		suffix='.%d%s' % (soa, suffix))
	# Cue
	plt.axvspan(0, cueDur, color=blue[1], alpha=.2)
	# Target. Take into account to cue duration in determining the target onset.
	targetOnset = soa+55
	plt.axvspan(targetOnset, targetOnset+targetDur, color=blue[1], alpha=.2)
	plt.xlim(0, 2550)
	plt.legend(frameon=False)
	plt.xlabel('Time since cue onset (ms)')
	plt.ylabel('Pupil size (norm.)')
	plt.ylim(.98, 1.07)
	plt.yticks([1,1.025, 1.05])
	plt.xticks(range(0, 2501, 500))
	if _show:
		Plot.save('trialPlot.%d' % soa, show=show)

def trialPlot1000(dm):

	"""
	A pupil-trace plot for the full trial epoch in 1000 ms SOA condition.

	Arguments:
	dm				--	A DataMatrix.
	"""

	trialPlot(dm, soa=945)

def trialPlot2500(dm):

	"""
	A pupil-trace plot for the full trial epoch in 2500 ms SOA condition.

	Arguments:
	dm				--	A DataMatrix.
	"""

	trialPlot(dm, soa=2445)

def lmeBehavior(dm):

	"""
	Analyzes the behavioral data with mixed effects.

	Arguments:
	dm		--	A DataMatrix.
	"""

	R = RBridge()
	i = 1
	Plot.new(size=Plot.ws)
	for dv in ['correct', 'irt']:
		plt.subplot(1,2,i)
		R.load(dm)
		lm = R.lmer('%s ~ cueValidity * soa + (1|subject_nr)' % dv)
		lm.save('output/lmeBehavior.%s.csv' % dv)
		lm._print(title=dv, sign=10)
		lSoa = []
		lVal = []
		lInv = []
		for soa in [45, 945, 2445]:
			_dm = dm.select('soa == %d' % soa, verbose=False)
			R.load(_dm)
			lm = R.lmer('%s ~ cueValidity + (1|subject_nr)' % dv)
			lm.save('output/lmeBehavior.%s.%d.csv' % (dv, soa))
			lm._print(title='%s (%d)' % (dv, soa), sign=10)
			mInv = lm['est'][0] # Invalid is reference
			mVal = mInv + lm['est'][1] #4Add slope for validity effect
			d = lm['est'][1]
			m = mInv + .5*d
			minD = d - lm['se'][1]
			maxD = d + lm['se'][1]
			# Determine error bars based on the slope CIs
			cInv = [m-minD/2, m-maxD/2]
			cVal = [m+minD/2, m+maxD/2]
			if dv == 'irt':
				mVal = 1./mVal
				mInv = 1./mInv
				cInv = [1./cInv[0], 1./cInv[1]]
				cVal = [1./cVal[0], 1./cVal[1]]
			else:
				mVal = 100.*mVal
				mInv = 100.*mInv
				cInv = [100.*cInv[0], 100.*cInv[1]]
				cVal = [100.*cVal[0], 100.*cVal[1]]
			print cVal, cInv
			# We plot the errorbars separately, because it's a bit easier than
			# passing them onto `plt.errorbar()`.
			plt.plot([soa+55, soa+55], cVal, '-', color=valColor)
			plt.plot([soa+55, soa+55], cInv, '-', color=invColor)
			lSoa.append(soa+55)
			lVal.append(mVal)
			lInv.append(mInv)
		plt.xlim(-100, 2750)
		plt.xticks([100, 1000, 2500])
		plt.xlabel('Cue-target interval (ms)')
		if dv == 'irt':
			plt.ylabel('Respone time (ms)')
			plt.ylim(420, 630)
			plt.yticks([450, 500, 550, 600])
		else:
			plt.ylabel('Accuracy (%)')
			plt.ylim(80, 95)
			plt.yticks([82.5, 85, 87.5, 90, 92.5])
		i += 1
		nVal = len(dm.select('cueValidity == "valid"', verbose=False))
		nInv = len(dm.select('cueValidity == "invalid"', verbose=False))
		plt.plot(lSoa, lVal, 'o-', color=valColor, label='Valid (N=%d)' % nVal)
		plt.plot(lSoa, lInv, 'o-', color=invColor, label='Invalid (N=%d)' % \
			nInv)
		plt.legend(frameon=False)
	Plot.save('behavior', show=show)

@cachedArray
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

	_dm = dm.selectColumns(['cueLum', 'subject_nr', '__trace_trial__', \
		'__trace_baseline__'])
	a = tk.mixedModelTrace(_dm, traceModel, winSize=winSize, **traceParams)
	return a

def subjectPlot(dm):

	"""
	Generates a separate trial plot for each subject.

	Arguments:
	dm		--	A DataMatrix.
	"""

	Plot.new(size=Plot.hi)
	i = 1
	for _dm in dm.group('subject_nr'):
		subject_nr = _dm['subject_nr'][0]
		N = len(_dm)
		plt.subplot(np.ceil(dm.count('subject_nr')/2.), 2, i)
		plt.title('%s (%d)' % (subject_nr, N))
		trialPlot(_dm, show=False, err=False, suffix='.subject%.2d' % \
			subject_nr)
		i += 1
	Plot.save('subjectPlot', show=show)

# Sanity checks
if winSize != 1:
	warnings.warn('winSize should be 1 for production!')
