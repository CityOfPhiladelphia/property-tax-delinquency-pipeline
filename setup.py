from distutils.core import setup
from requirements import r

setup(
    name='property-tax-delinquent-pipeline',
    version='1.0.0',
    **r.requirements.txt,
    packages=['phl_delinquents'],
    scripts=['tax_clean.py']
    )
