# property-tax-delinquency-pipeline
Python workflow for property tax data transformation


```bash
(env) Andrews-MacBook-Pro:property-tax-delinquency-pipeline amadonna$ python tax_delinquency.py 
Usage: tax_delinquency.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cleanup         Normalizes headers, trims text, normalizes...
  merge_geocodes  Any fields that were not geocoded using AIS,...
```

First run the cleanup command:

```bash
cat raw_tax_delinquency_data.txt | python tax_delinquency.py cleanup > tax_delinquency_clean.csv
```

Then run it through the [batch-geocoder](https://github.com/CityOfPhiladelphia/batch-geocoder) using the AIS geocoder:

```bash
cat tax_delinquency_clean.csv | batch_geocoder ais --ais-url http://ais.example.com --query-fields opa_number --ais-fields lat,lon,street_address,zip_code,zip_4,unit_type,unit_num > tax_delinquency_geocoded.csv
```

Once it's geocoded, attempt to fill in the misses (rows AIS could not geocode) using the original address and lat/longs:

```bash
cat tax_delinquency_geocoded.csv | python tax_delinquency.py merge_geocodes > tax_delinquency.csv
```
