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

import sys
import os
from analysis import helpers
from analysis.parse import getDataMatrix
from exparser.DataMatrix import DataMatrix

dm = getDataMatrix(cacheId='data')
# First filter the data and then perform all operations that have been specified
# on the command line.
dm = helpers.filter(dm, cacheId='cache')
for i in sys.argv:
	if hasattr(helpers, i):
		retval = getattr(helpers, i)(dm)
		if retval != None:
			dm = retval

