#!/usr/bin/env python

from __future__ import print_function
import petl
import phila_delinquents
import sys
import unicodecsv

import goodtables
import logging


# Import dataset
rows = [row for row in unicodecsv.reader(sys.stdin, delimiter="|")]
if rows[0][0].startswith(u'\ufeff'):
    rows[0][0] = rows[0][0][1:]
table = petl.wrap(rows)

# Verify that the header is as we expect
header = tuple(name.strip() for name in table.header())
if header != phila_delinquents.ORIGINAL_HEADER:
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

def extract_year(val):
    '''Convert EOY date to just a 4 digit year'''
    return val[0:4] if val else val

def normalize_philadelphia(val):
    if val == "PHILA":
        return "PHILADELPHIA"
    else:
        return val

clean = table.setheader(phila_delinquents.CLEAN_HEADER)\
             .convert(phila_delinquents.CLEAN_HEADER, 'strip')\
             .convert(phila_delinquents.CLEAN_HEADER, NULL_to_None)\
             .convert(("most_recent_year_owed",
                      "oldest_year_owed",
                      "collection_agency_most_recent_year",
                      "collection_agency_oldest_year",
                      "most_recent_bankrupt_year",
                      "oldest_bankrupt_year"), extract_year)\
             .convert(("most_recent_payment_date",), hyphenate)\
             .convert(("city",
                       "mailing_city"), normalize_philadelphia)\
             .convert(('bankruptcy',), lambda x: True if x == "bankrupt" else False)\
             .convert(('liens_sold_2015',), lambda x: None if x == "N" else x)

# Export transormation to csv
clean.progress().tocsv()

