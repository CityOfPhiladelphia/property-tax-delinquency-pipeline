from datetime import datetime
from functools import partial
from collections import OrderedDict
import logging
import sys

import petl
import click
import pyproj

logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)-15s] %(levelname)s [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

header_map = OrderedDict([
    ('OPA_Number', 'opa_number'),
    ('Owner', 'owner'),
    ('Co_owner', 'co_owner'),
    ('Principal_Due', 'principal_due'),
    ('Penalty_Due', 'penalty_due'),
    ('Interest_Due', 'interest_due'),
    ('Other_Charges_Due', 'other_charges_due'),
    ('Total_Due', 'total_due'),
    ('\ufeffIs_Actionable', 'is_actionable'),
    ('Payment_Agreement', 'payment_agreement'),
    ('Num_Yrs_Owed', 'num_years_owed'),
    ('Most_Recent_Yr_Owed', 'most_recent_year_owed'),
    ('Oldest_Yr_Owed', 'oldest_year_owed'),
    ('Most_Recent_Payment_Date', 'most_recent_payment_date'),
    ('Yr_of_Last_Assessment', 'year_of_last_assessment'),
    ('Total_Assessment', 'total_assessment'),
    ('Taxable_Assessment', 'taxable_assessment'),
    ('Mailing_Address', 'mailing_address'),
    ('Mailing_City', 'mailing_city'),
    ('Mailing_State', 'mailing_state'),
    ('Mailing_Zip', 'mailing_zip'),
    ('Return_Mail', 'return_mail'),
    ('Building_Code', 'building_code'),
    ('Detail_Bld_Description', 'detail_building_description'),
    ('General_Building_Description', 'general_building_description'),
    ('Building_Category', 'building_category'),
    ('Coll_Agency_Num_Yrs', 'coll_agency_num_years'),
    ('Coll_Agency_Most_Recent_Yr', 'coll_agency_most_recent_year'),
    ('Coll_Agency_Oldest_Yr', 'coll_agency_oldest_year'),
    ('Coll_Agency_Principal_Owed', 'coll_agency_principal_owed'),
    ('Coll_Agency_Total_Owed', 'coll_agency_total_owed'),
    ('Exempt_Abate_Assessment', 'exempt_abatement_assessment'),
    ('Homestead_Value', 'homestead_value'),
    ('Net_Tax_Value_After_Hmstd', 'net_tax_value_after_homestead'),
    ('Agreement_Agency', 'agreement_agency'),
    ('Sequestration_Enforcement', 'sequestration_enforcement'),
    ('Bankruptcy', 'bankruptcy'),
    ('Yrs_in_Bankruptcy', 'years_in_bankruptcy'),
    ('Most_Recent_Bankrupt_Yr', 'most_recent_bankrupt_year'),
    ('Oldest_Bankrupt_Yr', 'oldest_bankrupt_year'),
    ('Principal_Sum_Bankrupt_Yrs', 'principal_sum_bankrupt_years'),
    ('Total_Amount_Bankrupt_Yrs', 'total_amount_bankrupt_years'),
    ('Sheriff_Sale', 'sheriff_sale'),
    ('Liens_Sold_1990s', 'liens_sold_1990s'),
    ('Liens_Sold_2015', 'liens_sold_2015'),
    ('Assessment_Under_Appeal', 'assessment_under_appeal'),
    ## original address fields, to be replaced by geocoding
    ('Property_Address', 'orig_property_address'),
    ('Zip_Code', 'orig_zip_code'),
    ('X_Long', 'orig_lon'),
    ('Y_Lat', 'orig_lat')
])

year_fields = ['coll_agency_most_recent_year',
               'coll_agency_oldest_year',
               'most_recent_year_owed',
               'most_recent_bankrupt_year',
               'oldest_bankrupt_year',
               'oldest_year_owed']

date_fields = ['most_recent_payment_date']

boolean_fields = ['is_actionable',
                  'return_mail',
                  'payment_agreement',
                  'sequestration_enforcement',
                  'bankruptcy',
                  'liens_sold_1990s',
                  'assessment_under_appeal']

orig_address_fields = ['orig_property_address',
                       'orig_zip_code',
                       'orig_lon',
                       'orig_lat']

ais_fields = ['lat',
              'lon',
              'street_address',
              'zip_code',
              'zip_4',
              'unit_type',
              'unit_num']

## Hack to not include two rows at the end with "Affected row" text
class FinishException(Exception):
    pass

def cleanup_row(row):
    if all(field == None for field in row):
        raise FinishException()

    out = []
    for i in range(0, len(row)):
        field = row[i]
        field = field.strip()
        if field == '':
            field = 'NULL'

        if field != 'NULL':
            key = row.flds[i]
            if key in year_fields:
                field = field[:4]
            elif key in date_fields:
                field = datetime.strptime(field, '%Y%m%d').strftime('%Y-%m-%d')
            elif key in boolean_fields:
                if field == 'Y' or field == 'bankrupt' or field == 'yes':
                    field = 'true'
                else:
                    field = 'false'
        out.append(field)

    return out

transformer = None

geom_template = '{{"crs": {{"type": "name", "properties": {{"name": "EPSG:4326"}}}}, "type": "Point", "coordinates": [{}, {}]}}'

def merge_geocodes_row(row):
    out = list(row)
    if (not row['street_address'] or row['street_address'] == '') and row['orig_property_address'] != 'NULL':
        logger.info('`{}` not geocoded. Reverting to original info'.format(row['opa_number']))

        out[row.flds.index('street_address')] = row['orig_property_address']
        out[row.flds.index('zip_code')] = row['orig_zip_code']
        out[row.flds.index('zip_4')] = 'NULL'
        out[row.flds.index('unit_type')] = 'NULL'
        out[row.flds.index('unit_num')] = 'NULL'

        if row['orig_lon'] != 'NULL' and row['orig_lat'] != 'NULL':
            lon, lat = transformer(row['orig_lon'], row['orig_lat'])
            out[row.flds.index('lon')] = lon
            out[row.flds.index('lat')] = lat
        else:
            out[row.flds.index('lon')] = 'NULL'
            out[row.flds.index('lat')] = 'NULL'
    else:
        for key in ais_fields:
            if row[key] == '':
                out[row.flds.index(key)] = 'NULL'

    if out[row.flds.index('lat')] != 'NULL' and out[row.flds.index('lon')] != 'NULL':
        out.append(geom_template.format(out[row.flds.index('lon')], out[row.flds.index('lat')]))
    else:
        out.append('NULL')

    return out

@click.group()
def main():
    pass

@main.command()
def cleanup():
    """
    Normalizes headers, trims text, normalizes dates / years, normalizes booleans
    """

    try:
        petl\
        .fromcsv(delimiter='|')\
        .cut(*list(header_map.keys()))\
        .rename(header_map)\
        .rowmap(cleanup_row, list(header_map.values()), failonerror=True)\
        .tocsv()
    except FinishException:
        pass

@main.command()
def merge_geocodes():
    """
    Any fields that were not geocoded using AIS, use the orig_* fields
    """

    global transformer

    transformer = partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:2272', preserve_units=True),
        pyproj.Proj(init='EPSG:4326')
    )

    headers = list(header_map.values())

    final_headers = [
        'opa_number',
        'street_address',
        'zip_code',
        'zip_4',
        'unit_type',
        'unit_num'
    ]

    for header in headers:
        if header == 'opa_number' or header in orig_address_fields:
            continue
        final_headers.append(header)
    final_headers += ['lat', 'lon', 'shape']

    petl\
    .fromcsv()\
    .rowmap(merge_geocodes_row, headers + ais_fields + ['shape'], failonerror=True)\
    .cut(*final_headers)\
    .tocsv()

if __name__ == '__main__':
    main()
