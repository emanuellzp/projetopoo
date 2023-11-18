#!/usr/bin/env python3
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
"""Self-check digit calculator for UIC wagon numbers.  Tools around UIC wagon
numbers. Check validity of self-check digits, calculate self-check digits.

Examples:

>>> check_wagonnumber('371 015-9')
True
>>> cdigit('371 015')
9
>>> wagonnumbers('371 0??-9')
['371 001-9', '371 015-9', '371 020-9', '371 039-9', '371 044-9', '371 058-9', '371 063-9', '371 077-9', '371 082-9', '371 096-9']


Background information
----------------------

http://en.wikipedia.org/wiki/UIC_wagon_numbers"""
#
# 2014-01-31 - 2023-04-17
__version__ = '0.0.1'

import os
import sys


def wagonnumbers(wagonnumber_pattern, fromfile=None):
    """Return all valid combinations of UIC wagon numbers based on the given
    pattern.  The pattern has to be of the form "xxxxxxx-s". The number of
    digits before the dash is arbitrary. "s" is the self-check digit. Any
    digit, including the self-check digit, may be replaced by a placeholder
    "?". Whitespace is ignored.

    If *fromfile* is not *None*, filter the output by the given digit blocks
    found in the text file *fromfile*. The file must contain one block of
    digits per line, where the number of digits must match the number of
    placeholders "?" in the wagonnumber pattern. Dashes "-" are ignored, so the
    file may contain lines of the form "xxx-s".

    Example usage:

    >>> wagonnumbers('21 80 014 0 272-?')
    ['21 80 014 0 272-4']
    >>> wagonnumbers('33 80 076 5 11?-?')
    ['33 80 076 5 110-6',
     '33 80 076 5 111-4',
     '33 80 076 5 112-2',
     '33 80 076 5 113-0',
     '33 80 076 5 114-8',
     '33 80 076 5 115-5',
     '33 80 076 5 116-3',
     '33 80 076 5 117-1',
     '33 80 076 5 118-9',
     '33 80 076 5 119-7']
    >>> wagonnumbers('33 80 076 5 115-4')
    []
    >>> wagonnumbers('33 80 076 5 115-5')
    ['33 80 076 5 115-5']
    >>> wagonnumbers('31 80 437 3 ???-?', fromfile='era4-white')
    ['31 80 437 3 300-1',
     '31 80 437 3 811-7',
     '31 80 437 3 217-7',
     '31 80 437 3 797-8',
     '31 80 437 3 354-8',
     '31 80 437 3 565-9']

    Background information:
    http://en.wikipedia.org/wiki/UIC_wagon_numbers"""
    # 2014-01-31 - 2014-02-01
    wagonnumbers = []
    qnum = wagonnumber_pattern.count('?')
    if qnum == 0:
        if check_wagonnumber(wagonnumber_pattern):
            wagonnumbers = [wagonnumber_pattern]
        else:
            wagonnumbers = []
    else:
        if fromfile:
            # consider only combinations given in the file
            fromfile = os.path.expanduser(fromfile)
            with open(fromfile, 'r') as f:
                digitblocks = f.readlines()
                for i in range(len(digitblocks)):
                    digitblocks[i] = digitblocks[i].strip().replace('-', '')
                #import columnize
                #print(columnize.columnize(digitblocks))
            digitblocks
            combinds = []
            for digitblock in digitblocks:
                if len(digitblock) != qnum:
                    print(f'wagonnumbers: {fromfile}: found block with ' +
                          'wrong number of digits', file=sys.stderr)
                    sys.exit(1)
                comb = [int(char) for char in digitblock]
                wagonnumber = create_wagonnumber(wagonnumber_pattern, comb)
                if check_wagonnumber(wagonnumber):
                    wagonnumbers.append(wagonnumber)
        else:
            # consider all possible combinations
            for combind in range(10**qnum):
                combstr = '%0*i' % (qnum, combind)
                comb = [int(char) for char in combstr]
                wagonnumber = create_wagonnumber(wagonnumber_pattern, comb)
                if check_wagonnumber(wagonnumber):
                    wagonnumbers.append(wagonnumber)
    return wagonnumbers


def check_wagonnumber(wagonnumber):
    """Check the given wagonnumber for integrity (if it has the right
    self-check digit). The wagon number must be of the form "xxxxxxx-x", where
    each "x" stands for a digit. The number of digits before the dash is
    arbitrary.  If the self-check digit after the dash is valid, return True,
    otherwise, return False.

    Example usage:

    >>> check_wagonnumber('120 002-2')
    False
    >>> check_wagonnumber('120 002-1')
    True"""
    # 2013-01-31
    digits, cdig = parse_wagonnumber(wagonnumber)
    return cdigit(digits) == cdig


def cdigit(short_wagonnumber):
    """Compute self-check digit for the given short wagon number.  By short
    wagon number we mean one without the self-check digit (and without the
    dash) at the end.

    Example usage:

    >>> cdigit('120 002')
    1"""
    # 2014-01-31
    digits = parse_short_wagonnumber(short_wagonnumber)
    return diff10(total_digitsum(multiply21(digits)))


def create_wagonnumber(wagonnumber_pattern, comb):
    """Create a wagonnumber by replacing the questionmarks "?" in a given
    wagonnumber pattern by the digits given by the list *comb*. The number of
    questionmarks and the length of *comb* have to agree.

    Note: The resulting wagon number is not checked for integrity.

    Example usage:

    >>> create_wagonnumber('12? 00?-1', [0, 2])
    '120 002-1'"""
    # 2014-02-01
    qnum = wagonnumber_pattern.count('?')
    if qnum != len(comb):
        raise ValueError('unexpected number of placeholders "?" in ' +
                         'wagonnumber pattern')
    out = ''
    for char in wagonnumber_pattern:
        if char == '?':
            out += str(comb[0])
            comb = comb[1:]
        else:
            out += char
    return out


def parse_short_wagonnumber(short_wagonnumber):
    """Parse given short wagon number (excluding the check digit).

    Example usage:

    >>> parse_short_wagonnumber('120 002')
    [1, 2, 0, 0, 0, 2]"""
    # 2014-01-31
    if isinstance(short_wagonnumber, list):
        return short_wagonnumber
    short_wagonnumber = str(short_wagonnumber)
    digits = []
    for char in short_wagonnumber:
        if char in '1234567890':
            digits.append(int(char))
        elif char == ' ':
            continue
        else:
            raise ValueError('invalid wagon number')
    return digits


def parse_wagonnumber(wagonnumber):
    """Parse given complete wagon number (including the check digit) of the
    form "xxxxxxx-x". The number of digits before the dash is arbitrary.

    Example usage:

    >>> parse_wagonnumber('120 002-1')
    ([1, 2, 0, 0, 0, 2], 1)"""
    # 2014-01-31
    wagonnumber = str(wagonnumber)
    if wagonnumber.count('-') != 1:
        raise ValueError('invalid wagon number')
    left, right = wagonnumber.split('-')
    if len(right) != 1:
        raise ValueError('invalid wagon number')
    digits = []
    for char in wagonnumber:
        if char in '1234567890':
            digits.append(int(char))
        elif char == '-':
            continue
        elif char == ' ':
            continue
        else:
            raise ValueError('invalid wagon number')
    cdigit = digits[-1]
    digits = digits[:-1]
    return digits, cdigit


def parse_wagonnumber_pattern(wagonnumber_pattern):
    """Parse given wagon number pattern of the form "xxxxxxx-x" where each of
    the digits "x" may also be replaced by a questionmark "?". The number of
    digits before the dash "-" is arbitrary.

    Example usage:

    >>> parse_wagonnumber_pattern('120 002-1')
    (7, [1, 2, 0, 0, 0, 2, 1], [0, 1, 2, 3, 4, 5, 6], [])
    >>> parse_wagonnumber_pattern('120 002-?')
    (7, [1, 2, 0, 0, 0, 2], [0, 1, 2, 3, 4, 5], [6])
    >>> parse_wagonnumber_pattern('120 00?-?')
    (7, [1, 2, 0, 0, 0], [0, 1, 2, 3, 4], [5, 6])"""
    wagonnumber_pattern = str(wagonnumber_pattern)
    if wagonnumber_pattern.count('-') != 1:
        raise ValueError('invalid wagon number pattern')
    left, right = wagonnumber_pattern.split('-')
    if len(right) != 1:
        raise ValueError('invalid wagon number pattern')
    count = 0
    digits = []
    inds = []
    missinds = []
    ind = 0
    for char in wagonnumber_pattern:
        if char in '1234567890':
            count += 1
            digits.append(int(char))
            inds.append(ind)
        elif char == '?':
            count += 1
            missinds.append(ind)
        elif char in ' -':
            continue
        else:
            raise ValueError('invalid wagon number pattern')
        ind += 1
    return count, digits, inds, missinds


def total_digitsum(l):
    """Compute the total digit sum of the given list of numbers.

    Example usage:

    >>> total_digitsum([1, 2, 34])
    10
    >>> total_digitsum([1, 4, 0, 0, 0, 4])
    9

    (because 1+2+3+4 == 10)"""
    # 2014-01-31
    return sum([digitsum(n) for n in l])


def digitsum(n):
    """Compute the digit sum of the given number.

    Example usage:

    >>> digitsum(123)
    6

    Courtesy to
    http://stackoverflow.com/questions/14939953/sum-the-digits-of-a-number-python
    """
    # 2014-01-31
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r


def diff10(n):
    """Return difference of the given number to the next multiple of ten.

    Example usage:

    >>> diff10(1)
    9
    >>> diff10(8)
    2
    >>> diff10(10)
    0"""
    return ((n-1)//10+1)*10 - n


def multiply21(l):
    """Multiply each of the given list of numbers individually from right to
    left alternately by 2 and 1.

    Example usage:

    >>> multiply21([1, 1, 1, 1])
    [1, 2, 1, 2]
    >>> multiply21([1, 2, 0, 0, 0, 2])
    [1, 4, 0, 0, 0, 4]"""
    out = []
    for i in range(len(l)):
        n = l[i]
        if (len(l)-i) % 2 == 1:
            n *= 2
        out.append(n)
    return out


def __main__():
    import doctest
    doctest.testmod()
