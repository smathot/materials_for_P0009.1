#!/usr/bin/env python

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
from academicmarkdown import build, git, tools
import myZoteroCredentials
import time
version = '1.1.3'
build.path += ['svg', 'md', 'tables']
build.zoteroApiKey = myZoteroCredentials.zoteroApiKey
build.zoteroLibraryId = myZoteroCredentials.zoteroLibraryId
build.setStyle('apa')
build.pdfHeader = 'Manuscript in preparation [v%s; %s; %s]' % (version, \
	time.strftime('%c'), git.commitHash())
if '--snapshot' in sys.argv:
	git.snapshot('md/__main__.md', msg=sys.argv[-1])
else:
	build.PDF('md/__main__.md', 'latest-manuscript.pdf')
