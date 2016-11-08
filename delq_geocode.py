#!/usr/bin/env python

import click
import datum
import phila_delinquents
import phila_petl_ext as petl
from pprint import pprint

@click.command()
@click.option('--connection', '-d', required=True)
def main(connection):
    with datum.connect(connection) as db:
        # Truncate the table
        db.table(phila_delinquents.DB_TABLE)\
            .delete()

        # Load the data with a progress indicator via petl
        petl.fromcsv()\
            .progress()\
            .todatum(db, phila_delinquents.DB_TABLE)

        # Run the SQL to geocode the table
        # TODO: It would be nice if we had a datum function that was like:
        #
        #   db.table(...).geocode(...)
        #
        # It would have to take a join condition, and should support bringing
        # other information in from address_summary at the same time (like the
        # standardized address, etc).
        db.execute(phila_delinquents.GEOCODE_SQL)

if __name__ == '__main__':
    main()