#!/usr/bin/env python

import datum
import phl_delinquents

@click.command()
@click.option(dbconn)
def main(dbconn):
    with datum.connect(dbconn) as db:
        table = db.table(phl_delinquents.DB_TABLE)
        table.delete()
        table.load()
        db.execute(phl_delinquents.GEOCODE_SQL)

if __name__ == '__main__':
    main()