# 🚖 NYC Taxi Data Project — Workflow Orchestration with Kestra

This project is part of the workflow orchestration module The goal is to extend existing data ingestion workflows to handle **NYC Yellow and Green Taxi datasets for the year 2021**, using **Kestra**, a modern open-source orchestration platform.

## 📌 Project Description

We build and schedule ETL pipelines that:

- Download monthly taxi trip data in CSV format from a public GitHub release
- Convert the data to Parquet format
- Upload the processed files to a Google Cloud Storage (GCS) bucket
- Load the Parquet files into BigQuery for analytics
  
The workflows are designed to be reusable, parameterized, and support both manual and automated execution using Kestra’s `Schedule`, `ForEach`, and `Subflow` features.

---

## 📦 Datasets Used

- **Green Taxi Trip Data**:  
  [GitHub Release — Green Taxi](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)  

- **Yellow Taxi Trip Data**:  
  [GitHub Release — Yellow Taxi](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)

For `wget`-friendly links, use:  
`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`  
and replace `green` with `yellow` when needed.

---

## ⚙️ Technologies & Tools

- [Kestra](https://kestra.io/) — Workflow orchestration
- Google Cloud Storage (GCS) — Cloud storage for Parquet files
- BigQuery — Data warehouse for querying transformed datasets
- Python / SQL — For transformation and queries

---

