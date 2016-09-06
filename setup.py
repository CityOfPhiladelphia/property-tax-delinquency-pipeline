from distutils.core import setup

setup(
    name='property-tax-delinquent-pipeline',
    version='1.0.0',
    packages=['phl_delinquents'],
    install_requires=['petl'],
    scripts=['tax_clean.py']
    )
