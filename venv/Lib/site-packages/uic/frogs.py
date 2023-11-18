#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2014-2023 Daniel Jung
# Contact: proggy@mailbox.org
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""Frog definitions for this package."""
# 2014-02-01
from frog import Frog, sentence
import uic


# wagonnumbers
f = Frog(inmap=dict(wagonnumber_pattern='$@'),
    preproc=dict(wagonnumber_pattern=sentence), outmap={0: '#@'},
    usage='wagonnumbers [options] WAGONNUMBER_PATTERN')
f(uic.wagonnumbers)
