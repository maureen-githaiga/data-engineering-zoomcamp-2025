----Creating external table
CREATE OR REPLACE EXTERNAL TABLE `deep-rainfall-457106-v3.zoomcamp.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_bq_hw3_2025/yellow_tripdata_2024-*.parquet']
);

------Creating materialised table without clustering or partitioning
CREATE OR REPLACE TABLE `deep-rainfall-457106-v3.zoomcamp.yellow_tripdata_2024_regular`
AS SELECT * FROM  `deep-rainfall-457106-v3.zoomcamp.external_yellow_tripdata_2024`;

------count of records for the 2024 Yellow Taxi Data

SELECT COUNT(*) 
FROM `zoomcamp.external_yellow_tripdata_2024`;

---count of distincet number of PULocationIDs from external table to estimate the amount of data read

SELECT  DISTINCT COUNT(PULocationID)
FROM `zoomcamp.external_yellow_tripdata_2024`; 

---count of distincet number of PULocationIDs from materialised table to estimate the amount of data read
SELECT  DISTINCT COUNT(PULocationID)
FROM `zoomcamp.yellow_tripdata_2024_regular`;

---retrieving the PULocationID from the materialised table vs PULocationID and DOLocationID 
SELECT PULocationID  
FROM `zoomcamp.yellow_tripdata_2024_regular` LIMIT 5;

SELECT PULocationID, DOLocationID  
FROM `zoomcamp.yellow_tripdata_2024_regular` LIMIT 5;

---Records have a fare_amount of 0
SELECT COUNT(*)
FROM `zoomcamp.external_yellow_tripdata_2024`
WHERE fare_amount = 0;

---optimized table for query that always filter based on tpep_dropoff_datetime and orders the results by VendorID (Create a new table with this strategy)

CREATE OR REPLACE TABLE `deep-rainfall-457106-v3.zoomcamp.yellow_tripdata_2024_partitioned`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID  AS
SELECT * FROM `zoomcamp.external_yellow_tripdata_2024`;

---retrieving distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive) comparison materialised vs optimised table

SELECT DISTINCT VendorID
FROM `zoomcamp.yellow_tripdata_2024_regular`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `zoomcamp.yellow_tripdata_2024_partitioned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

---
SELECT COUNT(*)
FROM `zoomcamp.yellow_tripdata_2024_regular`;
