# 🗽 NYC Taxi DBT Project – Module 4 Homework
This mini-project/workshop focuses on transforming and analysing NYC Taxi data using **DBT** and **BigQuery**.
## Project Summary

We process and model NYC Taxi trip data from 2019 and 2020, including:
- Green Taxi
- Yellow Taxi
- For-Hire Vehicles (FHV)

  ### Objective
- Load raw data from URL to GCS, then to BigQuery native tables  
- Build **staging models** to clean and standardize schema  
- Build **fact/dimension models** using **star schema**  
- Perform analytical tasks such as revenue analysis, trip duration percentiles, and quarterly comparisons

  ---

## Data Sources

- Green Taxi: 7,778,101 records  
- Yellow Taxi: 109,047,518 records  
- FHV: 43,244,696 records

Stored as BigQuery native tables.
### Workflow
![DBT Data Lineage](https://user-images.githubusercontent.com/4315804/148699280-964c4e0b-e685-4c0f-a266-4f3e097156c9.png)


The following are answers to the homework questions:

### 1. `sources.yml` file
## DBT Configuration

### sources.yml
yaml
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema: "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi
`

### Environment Variables
bash
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
### Example SQL Model
sql
select *
from {{ source('raw_nyc_tripdata', 'ext_green_taxi') }}
### Explanation

The `source()` macro pulls metadata from `sources.yml` and uses environment variables to determine the actual BigQuery table to query.
In `sources.yml`, the source called `raw_nyc_tripdata` defines the project ID and dataset, configurable via environment variables.
The table `ext_green_taxi` is also defined there.
Exporting the variables overrides the default values in `sources.yml`.

The SQL model compiles to:
sql
select * from myproject.my_nyc_tripdata.ext_green_taxi
---

## 1. DBT Variables and Dynamic Models

To modify the dbt model (`fct_recent_taxi_trips.sql`) to dynamically control the date range:

* **In development:** process only the last **7 days** of trips
* **In production:** process the last **30 days** for analytics

Example:
sql
select *
from {{ ref('fact_taxi_trips') }}
where pickup_datetime >= CURRENT_DATE - INTERVAL '30' DAY
### Precedence for configuration resolution

When resolving configurations such as `env_var()`, the precedence order is:

1. Command line arguments
2. Environment variables
3. Default values in the `env_var()` macro call

Note: `env_var()` only looks at **real environment variables**, not dbt `vars`.

DBT `vars` have high precedence only for `var()`, **not** for `env_var()`.

### Combining `var()` and `env_var()`

For values that might change, combine `var()` and `env_var()`:
sql
pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY
* The CLI var: `--vars '{"days_back": "7"}'`
* Else the environment variable `DAYS_BACK`
* Else fallback to 30 days

In development, pass:
bash
--vars '{"days_back": "7"}'
In production, set:
bash
export DAYS_BACK=30
Or rely on default value.

---

## 2. DBT Data Lineage and Execution

![DBT Data Lineage](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/04-analytics-engineering/homework_q2.png)

In the lineage above:

* `taxi_zone_lookup` is the **only** materialization build (from a `.csv` seed file).

### Commands to materialize `fct_taxi_monthly_zone_revenue`

* `dbt run` — runs all models
* `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`
  (runs model `dim_taxi_trips`, all ancestors feeding it, and descendants it feeds into)
* `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`
  (selects fact model and all its dependencies)
* `dbt run --select +models/core/`
  (runs whole core and its ancestors)
* `dbt run --select models/staging/+`
  (selects models downstream of staging; dbt does NOT traverse multiple layers unless explicitly included)

---

## 3. DBT Macros and Jinja

### Use Case

You are dealing with sensitive data only available to your team in the `raw` layer of your data warehouse (e.g., a specific BigQuery dataset or PostgreSQL schema).

You decide to:

* Obfuscate/masquerade data in staging models and make it available in a different schema (`staging` layer) for Data/Analytics Engineers.
* Optionally build another layer (`service` layer) with dimension (`dim_`) and fact (`fct_`) tables using **Star Schema** dimensional modeling for dashboards and product owners/managers.

### Macro Example
jinja
{% macro resolve_schema_for(model_type) -%}
{%- set target_env_var = 'DBT_BIGQUERY_TARGET_DATASET'  -%}
{%- set stging_env_var = 'DBT_BIGQUERY_STAGING_DATASET' -%}

{%- if model_type == 'core' -%} 
  {{- env_var(target_env_var) -}}
{%- else -%}                    
  {{- env_var(stging_env_var, env_var(target_env_var)) -}}
{%- endif -%}
{%- endmacro %}
### Usage in models
sql
{{ config(
  schema=resolve_schema_for('core'),
) }}
---

### True statements about the macro:

* Setting `DBT_BIGQUERY_TARGET_DATASET` env var is **mandatory** or it will fail to compile
* Setting `DBT_BIGQUERY_STAGING_DATASET` env var is **not mandatory**; it defaults to `DBT_BIGQUERY_TARGET_DATASET`
* When using `'core'`, models materialize in dataset defined by `DBT_BIGQUERY_TARGET_DATASET`
* When using `'stg'` or `'staging'`, models materialize in dataset defined by `DBT_BIGQUERY_STAGING_DATASET` if set, else default to `DBT_BIGQUERY_TARGET_DATASET`

---

## 4. SQL Questions and Answers

### 4.1 Quarterly Revenue Model: `fct_taxi_trips_quarterly_revenue.sql`

Computes quarterly revenue by year based on `total_amount`.

**YoY Growth in 2020:**

| Taxi Type | Best Quarter | Worst Quarter |
| --------- | ------------ | ------------- |
| Green     | 2020/Q1      | 2020/Q2       |
| Yellow    | 2020/Q1      | 2020/Q2       |

---

### 4.2 Taxi Monthly Fare Percentiles: P97, P95, P90 `fct_taxi_trips_monthly_fare_p95.sql`
Computes the **continuous percentile** of `fare_amount` partitioned by `service_type`, `year`, and `month`.
Filtering conditions:

* `fare_amount > 0`
* `trip_distance > 0`
* `payment_type_description` in ('Cash', 'Credit card')

| Taxi Type | P97  | P95  | P90  |
| --------- | ---- | ---- | ---- |
| Green     | 55.0 | 45.0 | 26.5 |
| Yellow    | 31.5 | 25.5 | 19.0 |

---

### 4.3 Staging Model: `dim_fhv_tripdata.sql` and core model `fct_fhv_monthly_zone_traveltime_p90.sql` 
Computes the timestamp difference in seconds between dropoff_datetime and pickup_datetime.

Compute the continous p90 of trip_duration partitioning by year, month, pickup_location_id, and dropoff_location_id
---
