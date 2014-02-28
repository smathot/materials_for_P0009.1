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

import sys
import numpy as np
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from matplotlib import pyplot as plt

# Display center
xc = 512
yc = 384

class MyReader(EyelinkAscFolderReader):

	"""A custom reader to parse the EyeLink data files."""

	def initTrial(self, trialDict):

		"""
		Do some pre-trial initialization.

		Arguments:
		trialDict	--	A `dict` with trial info.
		"""

		trialDict['maxHGazeErr'] = 0
		trialDict['maxHFixErr'] = 0
		# We set the baseline tracePhase already here, because for some reason
		# the start_phase and start_trial messages got flipped in the datafile
		# on some trials.
		self.tracePhase = 'baseline'

	def finishTrial(self, trialDict):

		"""
		Do some post-trial calculations.

		Arguments:
		trialDict	--	A `dict` with trial info.
		"""

		trialDict['ctoa'] = self.targetTime - self.cueTime

	def parseLine(self, trialDict, l):

		"""
		Parse a single line from the EyeLink data file.

		Arguments:
		trialDict	--	A `dict` with trial info.
		l			--	A list that corresponds to the white-space-splitted
						line.
		"""

		# We record the entire trace under the name 'trial'
		if 'start_phase' in l:
			if 'cue' in l:
				self.cueTime = l[1]
				self.tracePhase = 'trial'
			elif 'target' in l:
				self.targetTime = l[1]
		elif 'end_phase' in l:
			if 'feedback' in l:
				self.tracePhase = None
		# Keep track of the maximum horizontal gaze error in the crucial part of
		# the trial.
		if self.tracePhase != None:
			smp = self.toSample(l)
			if smp != None:
				trialDict['maxHGazeErr'] = max(abs(smp['x'] - xc), \
					trialDict['maxHGazeErr'])
			fix = self.toFixation(l)
			if fix != None:
				trialDict['maxHFixErr'] = max(abs(fix['x'] - xc), \
					trialDict['maxHFixErr'])
