ORIGINAL_HEADER = (
    'legalname',
    'OPANumber',
    'Street_Code',
    'House#',
    'PrincipalDue',
    'PenaltyDue',
    'InterestDue',
    'OtherChargesDue',
    'TotalDue',
    '#YearsOwed',
    'mostRecentYearOwed',
    'oldestYearOwed',
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
    'homestd_value',
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
    'Bankr_RcvTotal',
    'Bankr_CalcTotal',
    'Sheriff_Sale',
    'OLD_LIENS',
    'LIEN_SALE',
    'APPEAL',
)

CLEAN_HEADER = (
    'legal_name',
    'opa_number',
    'street_code',
    'house_num',
    'principal_due',
    'penalty_due',
    'interest_due',
    'other_charges_due',
    'total_due',
    'num_years_owed',
    'most_recent_year_owed',
    'oldest_year_owed',
    'most_recent_payment_date',
    'return_mail',
    'case_status',
    'collection_agency_years',
    'collection_agency_most_recent',
    'collection_agency_oldest_year',
    'collection_agency_principal',
    'collection_agency_calc_total',
    'year_of_last_assessment',
    'total_assessment',
    'taxable_assessment',
    'exempt_abate_assessment',
    'homestd_value',
    'net_tax_value_after_homestd',
    'building_code',
    'building_description',
    'building_group_1',
    'building_group_2',
    'property_address',
    'city',
    'state',
    'zip_5',
    'owner_2_name',
    'mailing_addr',
    'mailing_city',
    'mailing_state',
    'mailing_zip',
    'council_district',
    'x_long',
    'y_lat',
    'pay_agreement',
    'agree_agency',
    'agree_org',
    'agree_status',
    'sequestration',
    'bankruptcy',
    'bankruptcy_count',
    'bankruptcy_max',
    'bankruptcy_min',
    'bankruptcy_principal',
    'bankruptcy_rcv_total',
    'bankruptcy_calc_total',
    'sheriff_sale',
    'old_liens',
    'lien_sale',
    'appeal',
)

DB_TABLE = 'TaxDelinquencyFC'

GEOCODE_SQL = '''
    UPDATE TaxDelinquencyFC
    SET shape = (
        SELECT shape FROM address_summary
        WHERE opa_account = opanumber
        AND ROWNUM = 1
    )
    WHERE shape IS NULL
'''