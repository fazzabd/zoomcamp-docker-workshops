#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default='01', type=str, help='Month of the data')
@click.option('--targettable', default='yellow_taxi_data', type=str, help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for data ingestion')
@click.option('--pg_user', default='root', type=str, help='PostgreSQL user')
@click.option('--pg_pass', default='root', type=str, help='PostgreSQL password')
@click.option('--pg_host', default='localhost', type=str, help='PostgreSQL host')
@click.option('--pg_port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg_db', default='ny_taxi', type=str, help='PostgreSQL database')
def run(year, month, targettable, chunksize, pg_user, pg_pass, pg_host, pg_port, pg_db):
    # Read a sample of the data
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month}.csv.gz'

    df = pd.read_csv(
        url.format(year=year, month=month),
        nrows=100,
        dtype=dtype,
        parse_dates=parse_dates
    )

    engine = create_engine('postgresql://{root}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'.format(
        root=pg_user,
        pg_pass=pg_pass,
        pg_host=pg_host,
        pg_port=pg_port,
        pg_db=pg_db
    ))

    df_iter = pd.read_csv(
        url.format(year=year, month=month),
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )
    first_chunk = next(df_iter)

    first_chunk.head(0).to_sql(
        name=targettable,
        con=engine,
        if_exists="replace"
    )

    print("Table created")

    for df_chunk in tqdm(df_iter):
    # for df_chunk in df_iter:
        df_chunk.to_sql(
            name=targettable,
            con=engine,
            if_exists="append"
        )
        print("Inserted chunk:", len(df_chunk))

if __name__ == '__main__':
    run()