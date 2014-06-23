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
respLockParams = {
	'signal'		: 'pupil',
	'lock'			: 'start',
	'phase'			: 'trial',
	'baseline'		: 'baseline',
	'baselineLock'	: 'end',
	'traceLen'		: 1500
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
	corrPlot100_100(dm)
	corrPlot100_1000(dm)
	corrPlot100_2500(dm)
	corrPlot1000_2500(dm)
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

	Plot.new(size=(3,3))
	plt.title('SOA: %d ms (behavior), %d ms (pupil)' % (soaBehav+55, \
		soaPupil+55))
	Plot.regress(xData, yData)
	plt.text(0.05, 0.90, 'Sample = %d' % bestSample, ha='left', \
			va='top', transform=plt.gca().transAxes)
	plt.axhline(0, linestyle='--', color='black')
	plt.axvline(0, linestyle='--', color='black')
	plt.plot(xData, yData, 'o', color='black')
	plt.ylabel('Behav. cuing effect (%)')
	plt.xlabel('Pupil cuing effect (norm.)')
	Plot.save('corrExample.%d.%d' % (soaBehav, soaPupil), 'corrAnalysis',
		show=show)

def corrPlot(dm, soaBehav, soaPupil, suffix=''):

	"""
	Plots and analyzes the correlation between the cuing effect in behavior and
	pupil size.

	Arguments:
	dm			--	A DataMatrix.
	soaBehav	--	The SOA to analyze for the behavioral effect.
	soaPupil	--	The SOA to analyze for the pupil effect.

	Keyword arguments:
	suffix		--	A suffix for the plot filename. (default='')
	"""

	Plot.new(size=Plot.ws)
	plt.title('SOA: %d ms (behavior), %d ms (pupil)' % (soaBehav+55, \
		soaPupil+55))
	plt.ylim(-.2, 1)
	plt.xlabel('Time since cue onset (ms)')
	plt.ylabel('Behavior - pupil correlation (r)')
	plt.axhline(0, linestyle='--', color='black')
	# Cue shading
	plt.axvspan(0, cueDur, color=blue[1], alpha=.2)
	# Target shading
	targetOnset = soaPupil+55
	plt.axvspan(targetOnset, targetOnset+targetDur, color=blue[1], alpha=.2)
	plt.xlim(0, 2550)
	# Accuracy
	a = corrTrace(dm, soaBehav, soaPupil, dv='correct', suffix='acc', \
		cacheId='corrTrace.correct.%d.%d%s' % (soaBehav, soaPupil, suffix))
	tk.markStats(plt.gca(), a[:,1])
	plt.plot(a[:,0], label='Accuracy', color=blue[1])
	# RTs
	a = corrTrace(dm, soaBehav, soaPupil, dv='response_time', suffix='rt', \
		cacheId='corrTrace.rt.%d.%d%s' % (soaBehav, soaPupil, suffix))
	tk.markStats(plt.gca(), a[:,1])
	plt.plot(a[:,0], label='Response times', color=orange[1])
	plt.legend(frameon=False, loc='upper left')
	Plot.save('corrAnalysis.%d.%d%s' % (soaBehav, soaPupil, suffix),
		'corrAnalysis', show=show)

def corrPlot100_100(dm):

	"""
	A correlation plot between the behavioral response in the 100 ms SOA and
	the pupil trace in 2500 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 45, 45)
	corrExample(dm, 45, 45)

def corrPlot100_1000(dm):

	"""
	A correlation plot between the behavioral response in the 100 ms SOA and
	the pupil trace in 1000 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 45, 945)
	corrExample(dm, 45, 945)

def corrPlot100_2500(dm):

	"""
	A correlation plot between the behavioral response in the 100 ms SOA and
	the pupil trace in 2500 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 45, 2445)
	corrExample(dm, 45, 2445)

def corrPlot1000_2500(dm):

	"""
	A correlation plot between the behavioral response in the 100 ms SOA and
	the pupil trace in 2500 ms SOA.

	Arguments:
	dm				--	A DataMatrix.
	"""

	corrPlot(dm, 945, 2445)
	corrExample(dm, 945, 2445)

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
def corrTrace(dm, soaBehav, soaPupil, dv='correct', suffix='', \
	traceParams=trialParams):

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
	nSubject = dmPupil.count('subject_nr')
	# Determine the trace length and create the trace plot
	traceLen = soaPupil + 105
	traceParams = trialParams.copy()
	traceParams['traceLen'] = traceLen
	# First determine the behavioral cuing effect for each participant
	print 'Determining behavioral cuing effect ...'
	aCuingEffect = np.empty(nSubject)
	for _dm in dmBehav.group('subject_nr'):
		i = _dm['subject_nr'][0]
		aCuingEffect[i] = cuingEffectBehav(_dm, dv=dv)
	print aCuingEffect
	print 'M = %.4f (%.4f)' % (aCuingEffect.mean(), aCuingEffect.std())
	print 'Done'
	# Next create 2 dimensional array with pupil-effect traces for each
	# participant over time
	print 'Creating pupil-effect traces ...'
	aPupilEffect = np.empty( (nSubject, traceLen) )
	for _dm in dmPupil.group('subject_nr'):
		i = _dm['subject_nr'][0]
		print 'Subject %d' % i
		x1, y1, err1 = tk.getTraceAvg(_dm.select('cueLum == "bright"', \
			verbose=False), **traceParams)
		x2, y2, err2 = tk.getTraceAvg(_dm.select('cueLum == "dark"', \
			verbose=False), **traceParams)
		d = y2-y1
		aPupilEffect[i] = d
	print 'Done'
	# Now walk through the pupil-effect array sample by sample and determine
	# the correlation with the behavioral cuing effect.
	print 'Determine correlations ...'
	aStats = np.empty( (traceLen, 2) )
	for i in range(traceLen):
		s, _i, r, p, se = linregress(aCuingEffect, aPupilEffect[:,i])
		print 'soaBehav: %d, soaPupil: %d' % (soaBehav, soaPupil)
		print '%d: r = %.4f, p = %.4f' % (i, r, p)
		aStats[i,0] = r
		aStats[i,1] = p
	print 'Done'
	return aStats

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
	pm = PivotMatrix(dm, ['cueValidity', 'soa', 'cueLum'], ['subject_nr'], \
		dv=lambda x: len(x))
	pm._print('Cell count')
	pm.save('output/cellcount.cueValidity.soa.cueLum.csv')
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

def tracePlot(dm, traceParams=trialParams, suffix='', err=True, \
	lumVar='cueLum', minSmp=200):

	"""
	A pupil-trace plot for a single epoch.

	Arguments:
	dm				--	A DataMatrix.

	Keyword arguments:
	traceParams		--	The trace parameters. (default=trialParams)
	suffix			--	A suffix to identify the trace. (default='')
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	lumVar			--	The variable that contains the luminance information.
						(default='cueLum')
	"""

	# At the moment we can only determine error bars for cueLum
	assert(not err or lumVar == 'cueLum')
	assert(lumVar in ['cueLum', 'targetLum'])
	x1, y1, err1 = tk.getTraceAvg(dm.select('%s == "bright"' % lumVar), \
		**traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select('%s == "dark"' % lumVar), \
		**traceParams)
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
		tk.markStats(plt.gca(), np.abs(aT), below=False, thr=2, minSmp=minSmp)
	if lumVar == 'cueLum':
		plt.plot(x1, y1, color=green[1], label='Cue on bright')
		plt.plot(x2, y2, color=blue[1], label='Cue on dark')
	elif lumVar == 'targetLum':
		plt.plot(x1, y1, color=green[1], label='Target on bright')
		plt.plot(x2, y2, color=blue[1], label='Target on dark')

def traceDiffPlot(dm, traceParams=trialParams, suffix='', err=True, \
	color=blue[1], label=None):

	"""
	A pupil-trace plot for a single epoch.

	Arguments:
	dm				--	A DataMatrix.

	Keyword arguments:
	traceParams		--	The trace parameters. (default=trialParams)
	suffix			--	A suffix to identify the trace. (default='')
	err				--	Indicates whether error bars should be drawn.
						(default=True) Note: UNUSED
	color			--	The line color. (default=blue[1])
	label			--	The line label. (default=None)
	"""

	x1, y1, err1 = tk.getTraceAvg(dm.select('cueLum == "bright"'), \
		**traceParams)
	x2, y2, err2 = tk.getTraceAvg(dm.select('cueLum == "dark"'), **traceParams)
	d = y2-y1
	plt.plot(d, color=color, label=label)

def trialPlot(dm, soa, _show=show, err=True, minSmp=200, suffix=''):

	"""
	A pupil-trace plot for the full trial epoch.

	Arguments:
	dm				--	A DataMatrix.
	soa				--	The SOA to select.

	Keyword arguments:
	_show			--	Indicates whether the plot should be shown.
						(default=True)
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	suffix			--	A suffix to identify the trace. (default='')
	"""

	assert(soa in dm.unique('soa'))
	if _show:
		Plot.new(size=Plot.ws)
		plt.title('SOA: %d ms' % (soa+55))
	plt.axhline(1, linestyle='--', color='black')
	dm = dm.select('soa == %d' % soa)
	# Determine the trace length and create the trace plot
	traceLen = soa + 105
	traceParams = trialParams.copy()
	traceParams['traceLen'] = traceLen
	tracePlot(dm, traceParams=traceParams, err=err, suffix='.%d%s' % (soa, \
		suffix), minSmp=minSmp)
	# Cue
	plt.axvspan(0, cueDur, color=blue[1], alpha=.2)
	# Target. Take into account to cue duration in determining the target onset.
	targetOnset = soa+55
	plt.axvspan(targetOnset, targetOnset+targetDur, color=blue[1], alpha=.2)
	plt.xlim(0, 2550)
	plt.legend(frameon=False)
	plt.xlabel('Time since cue onset (ms)')
	plt.ylabel('Pupil size (norm.)')
	if _show:
		plt.ylim(.98, 1.07)
	plt.yticks([1,1.025, 1.05])
	plt.xticks(range(0, 2501, 500))
	if _show:
		Plot.save('trialPlot.%d' % soa, 'trialPlot', show=show)

def trialPlot100(dm):

	"""
	A pupil-trace plot for the full trial epoch in 100 ms SOA condition.

	Arguments:
	dm				--	A DataMatrix.
	"""

	trialPlot(dm, soa=45)

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

	global R
	try:
		R
	except:
		R = RBridge()

	i = 1
	Plot.new(size=Plot.ws)
	for dv in ['correct', 'irt']:
		# Also analyze the grouped 945 and 2445 SOAs, which gives more power
		# than analyzing them separately.
		R.load(dm.select('soa != 45'))
		lm = R.lmer('%s ~ cueValidity * soa + (1|subject_nr)' % dv)
		lm.save('output/lmeBehavior.longInteract.%s.csv' % dv)
		lm._print(title='Long: %s' % dv, sign=10)
		lm = R.lmer('%s ~ cueValidity + (1|subject_nr)' % dv)
		lm.save('output/lmeBehavior.longNoInteract.%s.csv' % dv)
		lm._print(title='Long: %s' % dv, sign=10)
		# Loop over SOAs
		lSoa = []
		lVal = []
		lInv = []
		for soa in [45, 945, 2445]:
			_dm = dm.select('soa == %d' % soa, verbose=False)
			R.load(_dm)
			lm = R.lmer('%s ~ cueValidity + (1|subject_nr)' % dv)
			lm.save('output/lmeBehavior.%s.%s.csv' % (dv, soa))
			lm._print(title='%s (%s)' % (dv, soa), sign=10)
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
	Plot.save('behavior', 'behavior', show=show)

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

def respLockPlot(dm, soa, _show=True, err=True, suffix=''):

	"""
	Generates a response-locked pupil-trace plot.

	Arguments:
	dm		--	A DataMatrix.
	soa		--	The SOA to analyze.

	Keyword arguments:
	_show			--	Indicates whether the plot should be shown.
						(default=True)
	err				--	Indicates whether error bars should be drawn.
						(default=True)
	suffix			--	A suffix to identify the trace. (default='')
	"""

	assert(soa in dm.unique('soa'))
	if _show:
		Plot.new(size=Plot.ws)
		plt.title('SOA: %d ms%s' % (soa+55, suffix))
	dm = dm.select('soa == %d' % soa)
	# Recoding target luminance
	print 'Recoding target luminance ...'
	dm = dm.addField('targetLum', dtype=str)
	for i in dm.range():
		if (dm['cueLum'][i] == 'bright' and dm['cueValidity'][i] == 'valid') \
			or (dm['cueLum'][i] == 'dark' and dm['cueValidity'][i] == \
			'invalid'):
			dm['targetLum'][i] = 'bright'
		else:
			dm['targetLum'][i] = 'dark'
	print 'Done'
	# Draw lines
	plt.axhline(1, linestyle='--', color='black')
	plt.axvline(dm['response_time'].mean(), linestyle='--', color='black')
	# Determine the trace length and create the trace plot
	traceParams = respLockParams.copy()
	traceParams['offset'] = soa+55
	tracePlot(dm, traceParams=traceParams, err=False, suffix='.respLock.%d%s' \
		% (soa, suffix), lumVar='targetLum')
	# Target
	plt.axvspan(0, targetDur, color=blue[1], alpha=.2)
	plt.xlim(0, traceParams['traceLen'])
	plt.legend(frameon=False)
	plt.xlabel('Time since target onset (ms)')
	plt.ylabel('Pupil size (norm.)')
	plt.ylim(.95, 1.4)
	plt.yticks([1, 1.1, 1.2, 1.3])
	plt.xticks(range(0, 1501, 250))
	if _show:
		Plot.save('respLockPlot.%d%s' % (soa, suffix), 'respLock', show=show)

def respLockPlot100(dm):

	"""
	Generates a response-locked pupil-trace plot for 100 ms SOA.

	Arguments:
	dm		--	A DataMatrix.
	"""

	respLockPlot(dm.select('correct == 1'), soa=45, suffix='.correct')
	respLockPlot(dm.select('correct == 0'), soa=45, suffix='.incorrect')

def respLockPlot1000(dm):

	"""
	Generates a response-locked pupil-trace plot for 1000 ms SOA.

	Arguments:
	dm		--	A DataMatrix.
	"""

	respLockPlot(dm.select('correct == 1'), soa=945, suffix='.correct')
	respLockPlot(dm.select('correct == 0'), soa=945, suffix='.incorrect')

def respLockPlot2500(dm):

	"""
	Generates a response-locked pupil-trace plot for 2500 ms SOA.

	Arguments:
	dm		--	A DataMatrix.
	"""

	respLockPlot(dm.select('correct == 1'), soa=2445, suffix='.correct')
	respLockPlot(dm.select('correct == 0'), soa=2445, suffix='.incorrect')

def splitHalfReliabilityCorrect(dm, soa=2445, n=10000):

	"""
	Tests the split-half reliability of the behavioral cuing effect at the peak
	sample. Wrapper for accuracy analysis.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	soa		--	The SOA. (default=2445)
	dv		--	The dependent variable to use. (default='correct')
	n		--	The number of runs. (default=1000)
	"""

	splitHalfReliabilityBehav(dm, soa=soa, dv='correct', n=n)

def splitHalfReliabilityBehav(dm, soa=2445, dv='response_time', n=10000):

	"""
	Tests the split-half reliability of the behavioral cuing effect at the peak
	sample.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	soa		--	The SOA. (default=2445)
	dv		--	The dependent variable to use. (default='correct')
	n		--	The number of runs. (default=1000)
	"""

	@cachedArray
	def corrArray(dm, soa, dv, n):
		import time
		lR = []
		t0 = time.time()
		for i in range(n):
			l1 = []
			l2 = []
			for _dm in dm.group('subject_nr'):
				_dm.shuffle()
				dm1 = _dm[:len(_dm)/2]
				dm2 = _dm[len(_dm)/2:]
				ce1 = cuingEffectBehav(dm1, dv=dv)
				ce2 = cuingEffectBehav(dm2, dv=dv)
				l1.append(ce1)
				l2.append(ce2)
			s, j, r, p, se = linregress(l1, l2)
			print '%d (%d s): r = %.4f, p = %.4f' % (i, time.time()-t0, r, p)
			lR.append(r)
		return np.array(lR)

	assert(soa in dm.unique('soa'))
	dm = dm.select('soa == %d' % soa)
	Plot.new(size=(3,3))
	a = corrArray(dm, soa, dv, n, cacheId='corrArrayBehav.%s' % dv)
	a.sort()
	ci95up = a[np.ceil(.975 * len(a))]
	ci95lo = a[np.floor(.025 * len(a))]
	s = 'M = %.2f, P(r > 0) = %.2f, 95%%: %.2f - %.2f' % (a.mean(),
		np.mean(a > 0), ci95lo, ci95up)
	print s
	plt.hist(a, bins=n/10, color=blue[1])
	plt.title(s)
	plt.axvline(0, color='black')
	plt.xlim(-1, 1)
	plt.xlabel('Split-half correlation (r)')
	plt.ylabel('Frequency (N)')
	Plot.save('splitHalfReliability.behav.%s' % dv, folder='corrAnalysis',
		show=show)

def splitHalfReliabilityPupil(dm, soa=2445, sample=1852, n=10000):

	"""
	Tests the split-half reliability of the pupillary inhibition at the peak
	sample.

	Arguments:
	dm		--	A DataMatrix.

	Keyword arguments:
	soa		--	The SOA. (default=2445)
	sample	--	The pupil-trace sample. (default=1852)
	n		--	The number of runs. (default=1000)
	"""

	@cachedArray
	def corrArray(dm, soa, sample, n):
		import time
		lR = []
		t0 = time.time()
		for i in range(n):
			l1 = []
			l2 = []
			for _dm in dm.group('subject_nr'):
				_dm.shuffle()
				dm1 = _dm[:len(_dm)/2]
				dm2 = _dm[len(_dm)/2:]
				ce1 = cuingEffectPupil(dm1, epoch=(sample, sample+winSize))
				ce2 = cuingEffectPupil(dm2, epoch=(sample, sample+winSize))
				l1.append(ce1)
				l2.append(ce2)
			s, j, r, p, se = linregress(l1, l2)
			print '%d (%d s): r = %.4f, p = %.4f' % (i, time.time()-t0, r, p)
			lR.append(r)
		return np.array(lR)

	assert(soa in dm.unique('soa'))
	dm = dm.select('soa == %d' % soa)
	Plot.new(size=(3,3))
	a = corrArray(dm, soa, sample, n, cacheId='corrArrayPupil')
	a.sort()
	ci95up = a[np.ceil(.975 * len(a))]
	ci95lo = a[np.floor(.025 * len(a))]
	s = 'M = %.2f, P(r > 0) = %.2f, 95%%: %.2f - %.2f' % (a.mean(),
		np.mean(a > 0), ci95lo, ci95up)
	print s
	plt.hist(a, bins=n/10, color=blue[1])
	plt.title(s)
	plt.axvline(0, color='black')
	plt.xlim(-1, 1)
	plt.xlabel('Split-half correlation (r)')
	plt.ylabel('Frequency (N)')
	Plot.save('splitHalfReliability.pupil', folder='corrAnalysis')

def subjectPlot(dm):

	"""
	Generates a separate trial plot for each subject.

	Arguments:
	dm		--	A DataMatrix.
	"""

	Plot.new(size=Plot.xl)
	i = 1
	for _dm in dm.group('subject_nr'):
		subject_nr = _dm['subject_nr'][0]
		N = len(_dm)
		plt.subplot(np.ceil(dm.count('subject_nr')/4.), 5, i)
		plt.title('%s (%d)' % (subject_nr, N))
		trialPlot(_dm, 2445, _show=False, err=False, suffix='.subject%.2d' % \
			subject_nr)
		i += 1
	Plot.save('subjectPlot', 'subject', show=show)

def subjectDiffPlot(dm):

	"""
	Creates a line plot of the pupil effect separately for each subject.

	Arguments:
	dm		--	A DataMatrix.
	"""

	Plot.new(size=Plot.w)
	colors = brightColors * 10
	for _dm in dm.group('subject_nr'):
		print 'Subject %d' % _dm['subject_nr'][0]
		traceDiffPlot(_dm, color=colors.pop())
	plt.axhline(0, linestyle='--', color='black')
	Plot.save('subjectDiffPlot', 'subject', show=show)

# Sanity checks
if winSize != 1:
	warnings.warn('winSize should be 1 for production!')
