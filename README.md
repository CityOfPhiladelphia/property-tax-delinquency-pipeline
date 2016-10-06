# property-tax-delinquency-pipeline
Python workflow for property tax data transformation


```bash
cat input/sample.txt | python tax_clean.py > input/cleaned.csv

cat input/cleaned.csv | python delq_geocode.py oracle-stgeom://...
```
