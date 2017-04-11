HEADER = (
    'Owner',
    'OPA_Number',
    'Street_Code',
    'House_Number',
    'Principal_Due',
    'Penalty_Due',
    'Interest_Due',
    'Other_Charges_Due',
    'Total_Due',
    'Num_Yrs_Owed',
    'Most_Recent_Yr_Owed',
    'Oldest_Yr_Owed',
    'Most_Recent_Payment_Date',
    'Return_Mail',
    'Coll_Agency_Num_Yrs',
    'Coll_Agency_Most_Recent_Yr',
    'Coll_Agency_Oldest_Yr',
    'Coll_Agency_Principal_Owed',
    'Coll_Agency_Total_Owed',
    'Yr_of_Last_Assessment',
    'Total_Assessment',
    'Taxable_Assessment',
    'Exempt_Abate_Assessment',
    'Homestead_Value',
    'Net_Tax_Value_After_Hmstd',
    'Building_Code',
    'Detail_Bld_Description',
    'General_Building_Description',
    'Building_Category',
    'Property_Address',
    'City',
    'State',
    'Zip_Code',
    'Co_owner',
    'Mailing_Address',
    'Mailing_City',
    'Mailing_State',
    'Mailing_Zip',
    'Council_District',
    'X_LONG', #TODO: These should be lowerecased in the next dataset
    'Y_LAT',
    'Payment_Agreement',
    'Agreement_Agency',
    'Sequestration_Enforcement',
    'Bankruptcy',
    'Yrs_in_Bankruptcy',
    'Most_Recent_Bankrupt_Yr',
    'Oldest_Bankrupt_Yr',
    'Principal_Sum_Bankrupt_Yrs',
    'Total_Amount_Bankrupt_Yrs',
    'Sheriff_Sale',
    'Liens_Sold_1990s',
    'Liens_Sold_2015',
    'Assessment_Under_Appeal',
)


DB_TABLE = 'TaxDelinquency'

GEOCODE_SQL = '''
    UPDATE TaxDelinquency
    SET (shape, property_address) = (
        SELECT shape, street_address FROM GIS_AIS.address_summary
        WHERE opa_account = opanumber
        AND ROWNUM = 1
    )
    WHERE shape IS NULL
'''