#!/usr/bin/env python
# coding: utf-8

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

def run():
    year = 2021
    month = '01'
    targettable = 'yellow_taxi_data'
    chukksize = 100000

    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'

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
        chunksize=chukksize
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