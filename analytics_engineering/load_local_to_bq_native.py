import os
from google.cloud import storage
import pandas as pd
from pandas_gbq import to_gbq

#config
PROJECT_ID = "deep-rainfall-457106-v3"
BUCKET_NAME = "dezoomcamp_bq_hw4_2025"
BQ_DATASET = "zoomcamp"

#initialize storage client
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

datasets = {}
for year in [2019,2020]:
    for month in range(1, 13):
        mm = f"{month:02d}"
        datasets[f"green_{year}_{mm}"] = f"green_tripdata_{year}-{mm}.parquet"
        datasets[f"yellow_{year}_{mm}"] = f"yellow_tripdata_{year}-{mm}.parquet"

for month in range(1, 13):
    mm = f"{month:02d}"
    datasets[f"fhv_2019_{mm}"] = f"fhv_tripdata_2019-{mm}.parquet"


def load_to_bq(local_path, table_name):
    """
    Load a local parquet file to BigQuery.
    """
    df = pd.read_parquet(local_path)
    to_gbq(df, f"{BQ_DATASET}.{table_name}", project_id=PROJECT_ID, if_exists='replace')
    print(f"Loaded {local_path} to BigQuery table {BQ_DATASET}.{table_name}")
    print(f"Loaded to bigquery: {BQ_DATASET}.{table_name}")

def run_pipeline():
    for table_name, file_name in datasets.items():

        local_path = os.path.join(".", file_name)

        #load_to_bq(local_path, table_name)

        if os.path.exists(local_path):
            os.remove(local_path)
            print(f"Deleted local file: {local_path}")

if __name__ == "__main__":
    run_pipeline()
    print("Pipeline completed successfully.")
