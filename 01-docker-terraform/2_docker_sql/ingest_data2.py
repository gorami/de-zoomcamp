#!/usr/bin/env python
# coding: utf-8

# In[1]:

from time import time
import pandas as pd
from sqlalchemy import create_engine
import argparse
import os




def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv'

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_csv(csv_name, nrows=100)


    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True: 
        t_start = time()

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='Ingest CSV Data 2 Postgres',
                        description='What the program does',
                        epilog='Text at the bottom of help')

    #user, password, host, port, database name, table name, url of the CSV

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres') 
    parser.add_argument('--host', help='host for postgres') 
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name') 
    parser.add_argument('--table_name', help='table name')
    parser.add_argument('--url', help='CSV file url')

    args = parser.parse_args()

    main(args)