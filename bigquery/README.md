## 🗽 NYC Yellow Taxi Trip Records – 2024 BigQuery Module

This mini-project/workshop objective is to work with **NYC Yellow Taxi Trip Records (Jan–June 2024)**, using **Google Cloud Storage** and **BigQuery** for data querying and optimization.

---

## Overview

In this project, we:

- Load NYC Yellow Taxi data (Parquet format) from January to June 2024 into a **Google Cloud Storage (GCS)** bucket
- Create both an **External Table** and a **Materialized Table** in **BigQuery**
- Perform analytical queries on the data to explore performance and storage characteristics
- Optimize BigQuery performance using **partitioning and clustering**
- Compare query performance across table types

---

## Data Source

**Yellow Taxi Trip Records**  
🗓Date Range: **January 2024 to June 2024**  
Format: Parquet  
Source: [NYC Taxi & Limousine Commission Trip Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

---

## ⚙️ Tools & Technologies

- Google Cloud Storage (GCS)
- BigQuery
- SQL (standard)

> Note: No orchestration tool (Airflow, Prefect, etc.) was used to load data into BigQuery as per assignment instructions. Data was loaded up to GCS only.

---

## BigQuery Setup

- ✅ **External Table**: Created using GCS-hosted Parquet files  
- ✅ **Materialized Table**: Loaded directly from external table, unpartitioned  
- ✅ **Partitioned & Clustered Table**: Created for optimized performance  

---

## SQL Queries

All queries for the homework questions are included in this README under the `Homework Solutions` section below.

- Record counting
- Column-level data scanning analysis
- Fare distribution insights
- Table optimization strategy
- Partitioning vs non-partitioning performance comparison
- Data location verification
- BigQuery best practices


## Homework Solutions

### **Question 1: Count of the records for the 2024 Yellow Taxi Data**

```sql
SELECT COUNT(*) 
FROM `zoomcamp.external_yellow_tripdata_2024`;
```
---

### **Question 2: Distinct PULocationIDs – External vs Materialized Table**

```sql
-- External Table
SELECT DISTINCT COUNT(PULocationID)
FROM `zoomcamp.external_yellow_tripdata_2024`; 

-- Materialized Table
SELECT DISTINCT COUNT(PULocationID)
FROM `zoomcamp.yellow_tripdata_2024_regular`;
```

**Estimated data read**:

* External Table: **0 MB**
* Materialized Table: **155.12 MB**

---

### **Question 3: Bytes Processed – One vs Two Columns**

```sql
-- One column
SELECT PULocationID  
FROM `zoomcamp.yellow_tripdata_2024_regular` LIMIT 5;

-- Two columns
SELECT PULocationID, DOLocationID  
FROM `zoomcamp.yellow_tripdata_2024_regular` LIMIT 5;
```

**Explanation**:
BigQuery is a **columnar database**. It only reads the columns requested. Querying more columns (e.g. both `PULocationID` and `DOLocationID`) increases the number of bytes read.

---

### **Question 4: Number of Records with `fare_amount = 0`**

```sql
SELECT COUNT(*)
FROM `zoomcamp.external_yellow_tripdata_2024`
WHERE fare_amount = 0;
```

---

### **Question 5: Optimizing Table with Partitioning & Clustering**

**Strategy**: Partition by `tpep_pickup_datetime`, Cluster by `VendorID`

```sql
CREATE OR REPLACE TABLE `zoomcamp.yellow_tripdata_2024_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID  
AS
SELECT * FROM `zoomcamp.external_yellow_tripdata_2024`;
```

---

### **Question 6: Distinct VendorIDs Between 2024-03-01 and 2024-03-15**

```sql
-- Materialized Table
SELECT DISTINCT VendorID
FROM `zoomcamp.yellow_tripdata_2024_regular`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned & Clustered Table
SELECT DISTINCT VendorID
FROM `zoomcamp.yellow_tripdata_2024_partitioned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

**Estimated bytes processed**:

* Materialized Table: **310.24 MB**
* Optimized Table: **26.85 MB**

---

### **Question 7: Where is the data stored in the External Table?**

**Answer**: **GCS Bucket**

* External tables read directly from GCS.
* They avoid data duplication and support querying on-demand.
* Costs are based on data scanned from GCS.

---

### **Question 8: Is it best practice to always cluster your data?**

**Answer**: **False**

Clustering is useful when:

* Filtering or sorting by a column frequently
* High cardinality in the clustered column
* Large datasets

Not useful when:

* Table is small
* Few distinct values
* Frequent inserts (reclustering needed)

---

### **Question 9: Why does `SELECT COUNT(*)` show 0 bytes processed?**

BigQuery uses **metadata** for `COUNT(*)` queries on native tables, so no actual table scan occurs.

```sql
SELECT COUNT(*)
FROM `zoomcamp.yellow_tripdata_2024_regular`;
```


