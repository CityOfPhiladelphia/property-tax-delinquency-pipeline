#!/usr/bin/env python

from __future__ import print_function
import petl
import phila_delinquents
import sys
import unicodecsv

import logging


# Import dataset
rows = [row for row in unicodecsv.reader(sys.stdin, delimiter="|")]
if rows[0][0].startswith(u'\ufeff'):
    rows[0][0] = rows[0][0][1:]
table = petl.wrap(rows)

# Verify sure that the header is as we expect
for name in table.header():
    print(name)
header = tuple(name.strip() for name in table.header())
if header != phila_delinquents.HEADER:
    logging.error('Unexpected table header: {}'.format(header))
    sys.exit(1)


# Apply the transformations:
# 1) replace the header.
# 2) replace occurrences of "NULL" with None.
# 3) apply hyphenate to select cols.

def hyphenate(dtstr):
    '''format a string with hyphens'''
    if dtstr and len(dtstr) > 6:
        assert 1 <= int(dtstr[4:6]) <= 12
        return '{}-{}-{}'.format(dtstr[0:4], dtstr[4:6], dtstr[6:])
    else:
        return dtstr

def NULL_to_None(val):
    '''Convert "NULL" values to None.'''
    return None if val == 'NULL' else val

clean = table.setheader(phila_delinquents.HEADER)\
             .convert(phila_delinquents.HEADER, 'strip')\
             .convert(phila_delinquents.HEADER, NULL_to_None)\
             .convert(("Most_Recent_Yr_Owed",
                       "Oldest_Yr_Owed",
                       "Most_Recent_Payment_Date",
                       "Coll_Agency_Most_Recent_Yr",
                       "Coll_Agency_Oldest_Yr",
                       "Most_Recent_Bankrupt_Yr",
                       "Yr_of_Last_Assessment",
                       "Oldest_Bankrupt_Yr"), hyphenate)

# Export transormation to csv
clean.progress().tocsv()
