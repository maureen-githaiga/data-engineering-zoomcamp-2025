from google.cloud import bigquery

PROJECT_ID = "deep-rainfall-457106-v3"
DATASET_ID = "zoomcamp"
BUCKET_NAME = "dezoomcamp_bq_hw4_2025"

client = bigquery.Client(project=PROJECT_ID)

tables = {}

# Green & Yellow taxi data: 2019 and 2020
for year in [2019, 2020]:
    for month in range(1, 13):
        mm = f"{month:02d}"
        tables[f"green_{year}_{mm}"] = f"gs://{BUCKET_NAME}/green/green_tripdata_{year}-{mm}.parquet"
        tables[f"yellow_{year}_{mm}"] = f"gs://{BUCKET_NAME}/yellow/yellow_tripdata_{year}-{mm}.parquet"

# FHV data: only 2019
for month in range(1, 13):
    mm = f"{month:02d}"
    tables[f"fhv_2019_{mm}"] = f"gs://{BUCKET_NAME}/fhv/fhv_tripdata_2019-{mm}.parquet"

# Load from GCS to BigQuery
for table_name, gcs_uri in tables.items():
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_uri(
        gcs_uri, table_id, job_config=job_config
    )

    load_job.result()  # Wait for the job to complete
    print(f"✅ Loaded {gcs_uri} into {table_id}")
