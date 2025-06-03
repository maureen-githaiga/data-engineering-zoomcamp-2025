import pandas as pd
from sqlalchemy import create_engine
import argparse

def ingest_csv(params):
    engine = create_engine(f'postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}')

    print(f"Ingesting '{params.csv}' into table '{params.table_name}'...")

    df = pd.read_csv(params.csv)
    df.to_sql(name=params.table_name, con=engine, if_exists='replace', index=False)

    print("Ingestion complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV to PostgreSQL")

    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--db', required=True)
    parser.add_argument('--table_name', required=True)
    parser.add_argument('--csv', required=True)

    args = parser.parse_args()
    ingest_csv(args)

