#!/usr/bin/env python
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

from exparser import Tools
from analysis import helpers, parse
Tools.analysisLoop(
	parse.getDataMatrix(cacheId='data'),
	mods=[helpers],
	pre=['filter'],
	full=[
		'dontShow',
		'descriptives',
		'lmeBehavior',
		'trialPlot100',
		'trialPlot1000',
		'trialPlot2500',
		'corrPlot100_100',
		'corrPlot100_1000',
		'corrPlot100_2500',
		'corrPlot1000_100',
		'corrPlot1000_2500',
		'corrPlot1000',
		'corrPlot2500',
		'corrPlot2500_100',
		'corrPlot2500_1000'
		]
	)
