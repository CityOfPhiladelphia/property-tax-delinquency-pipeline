#!/usr/bin/env python

import petl as etl

# import dataset
table = etl.fromcsv()

def hyphenate(num):
    '''format a string with hyphens'''
    try:
        nums = str(num)
        return '{}-{}-{}'.format(nums[0:4], nums[4:6], nums[6:])
    except:
        print "error"

# apply hyphenate to select cols.
clean = table.convert("mostRecentYearOwed", hyphenate)\
                      .convert("oldestYearOwed", hyphenate)\
                      .convert("mostRecentPaymentDate", hyphenate)\
                      .convert("CollectionAgency#mostRecentYear", hyphenate)\
                      .convert("CollectionAgency#oldestYear", hyphenate)

# export transormation to csv
etl.tocsv(clean)
