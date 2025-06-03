import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time
import gzip
import shutil

def main(params):
    print("Ingestion process started.")
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    print(f"Connecting to database {db} at {host}:{port} as user {user}...")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    file_name = url.split('/')[-1]

    is_zipped = file_name.endswith('.gz')


    #download the file
    gz_name = 'output.csv.gz'
    csv_name = 'output.csv'
    
    os.system(f'wget {url} -O {gz_name if is_zipped else csv_name}')

    if is_zipped:
        with gzip.open(gz_name, 'rb') as file_in:
            with open(csv_name, 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)


    df_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000)

    df = next(df_iter)


    df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime =pd.to_datetime(df.lpep_dropoff_datetime )

    df.head(n=0).to_sql(name = table_name, con= engine,if_exists='replace')

    while True:
        try:
            t_start = time()
            df =  next(df_iter)
            df.lpep_pickup_datetime=pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime =pd.to_datetime(df.lpep_dropoff_datetime )
            df.to_sql(name = table_name, con= engine,if_exists='append')
            t_end = time()
            print('inserted another chunk ..., took %.3f second' % (t_end - t_start))

        except StopIteration:
            print('all the data is ingested')
            break

    print("Ingestion process completed.")
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    #user,password,host,port,db,table name,url of the csv

    parser.add_argument('--user', help='User name to connect to Postgres')
    parser.add_argument('--password', help='Password to connect to Postgres')
    parser.add_argument('--host', help='Host to connect to Postgres')
    parser.add_argument('--port', help='Port to connect to Postgres')
    parser.add_argument('--db', help='Database name to connect to Postgres')
    parser.add_argument('--table_name', help='Table name to connect to Postgres')
    parser.add_argument('--url', help='URL of the CSV file')

    args = parser.parse_args()
    #print(args.accumulate(args.integers))

    main(args)
