import csv, sys
from collections import defaultdict

Source_COLS = [
    'legalname',
    'OPAnumber',
    'Street_Code',
    'House#',
    'principalDue',
    'penaltyDue',
    'interestDue',
    'otherChargesDue',
    'totalDue',
    '#yearsOwned',
    'mostRecentYearOwned',
    'oldestYearOwned',
    'mostRecentPaymentDate',
    'ReturnMail',
    'CASE_STATUS',
    'CollectionAgency#years',
    'CollectionAgency#mostRecentYear',
    'CollectionAgency#oldestYear',
    'CollAg_PRINCIPAL',
    'CollAg_CalcTotal',
    'YEAR OF LAST ASSESSMENT',
    'TOTAL ASSESSMENT',
    'taxableAssessment',
    'exempt_abateAssessment',
    'homesteadValue',
    'netTaxValueAfterHmstd',
    'buildingCode',
    'BldgDescription',
    'BldgGroup_1',
    'BldgGroup_2',
    'property_address',
    'CITY',
    'ST',
    'ZIP5',
    'OWNER2 NAME',
    'Mailing_Addr',
    'Mailing_City',
    'Mailing_State',
    'Mailing_Zip',
    'Council_District',
    'X_LONG',
    'Y_LAT',
    'Pay_Agreement',
    'Agree_Agency',
        'Agree_Org',
    'Agree_Status',
    'SEQUESTRATION',
    'Bankruptcy',
    'Bankr_count',
    'Bankr_max',
    'Bankr_min',
    'Bankr_PRINCIPAL',
    'Bankr_CaclTotal',
    'Sherrif_Sale',
    'OLD_LIENS',
    'LIEN_SALE',
    'APPEAL'
]


def hyphenate(num):
    '''format a string with hyphens'''
    nums = str(num)
    return '{}-{}-{}'.format(nums[0:4], nums[4:6], nums[6:])


#print hyphenate(20141231)

def reader(filename, d='|'):
    data = []
    with open(filename) as tsvin:
        tax = csv.reader(tsvin, delimiter=d)
        for line in tax:
            data.append(line)
    return data

raw = reader('./input/sample.txt')

#print raw
