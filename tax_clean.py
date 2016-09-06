import petl as etl

table = etl.fromcsv()

def hyphenate(num):
    '''format a string with hyphens'''
    try:
        nums = str(num)
        return '{}-{}-{}'.format(nums[0:4], nums[4:6], nums[6:])
    except:
        print "error"

clean = table.convert("mostRecentYearOwed", hyphenate)\
                      .convert("oldestYearOwed", hyphenate)\
                      .convert("mostRecentPaymentDate", hyphenate)\
                      .convert("CollectionAgency#mostRecentYear", hyphenate)\
                      .convert("CollectionAgency#oldestYear", hyphenate)


etl.tocsv(clean, './output/out.csv')
