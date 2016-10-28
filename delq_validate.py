#!/usr/bin/env python

from __future__ import print_function
import petl
import sys

from phila_delinquents.validation import num_or_null

assertions = [dict(zip(['name', 'field', 'assertion'], vals)) for vals in ()]

tests = [dict(zip(['name', 'field', 'test'], vals)) for vals in (
    ('street_code is num_or_null', 'street_code', num_or_null),
    ('house_num is num_or_null', 'house_num', num_or_null),
    ('principal_due is num_or_null', 'principal_due', num_or_null),
    ('penalty_due is num_or_null', 'penalty_due', num_or_null),
    ('interest_due is num_or_null', 'interest_due', num_or_null),
    ('other_charges_due is num_or_null', 'other_charges_due', num_or_null),
    ('total_due is num_or_null', 'total_due', num_or_null),
    ('num_years_owed is num_or_null', 'num_years_owed', num_or_null),
    ('collection_agency_years is num_or_null', 'collection_agency_years', num_or_null),
    ('collection_agency_principal is num_or_null', 'collection_agency_principal', num_or_null),
    ('collection_agency_calc_total is num_or_null', 'collection_agency_calc_total', num_or_null),
    ('year_of_last_assessment is num_or_null', 'year_of_last_assessment', num_or_null),
    ('total_assessment is num_or_null', 'total_assessment', num_or_null),
    ('taxable_assessment is num_or_null', 'taxable_assessment', num_or_null),
    ('exempt_abate_assessment is num_or_null', 'exempt_abate_assessment', num_or_null),
    ('homestd_value is num_or_null', 'homestd_value', num_or_null),
    ('net_tax_value_after_homestd is num_or_null', 'net_tax_value_after_homestd', num_or_null),
    ('council_district is num_or_null', 'council_district', num_or_null),
    ('x_long is num_or_null', 'x_long', num_or_null),
    ('y_lat is num_or_null', 'y_lat', num_or_null),
    ('bankruptcy_count is num_or_null', 'bankruptcy_count', num_or_null),
    ('bankruptcy_principal is num_or_null', 'bankruptcy_principal', num_or_null),
    ('bankruptcy_rcv_total is num_or_null', 'bankruptcy_rcv_total', num_or_null),
    ('bankruptcy_calc_total is num_or_null', 'bankruptcy_calc_total', num_or_null),
)]

errors = petl.fromcsv()\
             .progress(prefix='Validated ')\
             .validate(constraints=assertions + tests)\
             .cache()

errors.tocsv()
sys.exit(0 if errors.nrows() == 0 else 1)
