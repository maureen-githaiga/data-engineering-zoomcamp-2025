# Docker, SQL, and Terraform

Objective: Gain hands-on experience with local development environments using Docker, perform basic data exploration with SQL, and provision cloud infrastructure using Terraform on Google Cloud Platform (GCP).

### 🐳 Docker & PostgreSQL

- Used the `python:3.12.8` Docker image to explore Docker fundamentals.
- Configured a multi-service environment with `docker-compose` to run:
  - **PostgreSQL** database
  - **pgAdmin** for web-based database access and inspection
- Downloaded and loaded the following datasets into PostgreSQL:
  - Green Taxi Trip Data – October 2019
  - Taxi Zone Lookup Table

### 📊 Data Analysis (SQL)

Performed analytical queries on the green taxi trip data to:

- Count trips segmented by trip distance
- Identify the longest trip per day
- Determine top pickup zones by total fare amount
- Find the drop-off location with the highest tip from a specific zone

### ☁ Terraform & GCP

- Installed and configured **Terraform** to manage infrastructure as code
- Cloned and updated course-provided Terraform scripts to:
  - Create a **Google Cloud Storage (GCS)** bucket
  - Create a **BigQuery** dataset
- Followed Terraform workflow: `terraform init`, `terraform apply`, `terraform destroy`

## Datasets

- [Green Taxi Trips – October 2019](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz)
- [Taxi Zone Lookup Table](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)
  
# Homework Solutions

## Running docker with the python:3.12.8 image in an interactive mode, using the entrypoint bash.

docker run -it --entrypoint=bash python:3.12.8  
to check the version run command  pip --version

## Docker networking and docker-compose
In the `docker-compose.yaml` file, the two containers **Postgres** and **pgAdmin** are connected through a **Docker network**.
The hostname and port that **pgAdmin** should use to connect to **Postgres** are:

- **Hostname:** `postgres` (this is the name of the Postgres container)
- **Port:** `5432` (this is the default Postgres port exposed internally in the container)

Docker Compose creates a **default network** for all services defined in the same `docker-compose.yaml`, which allows them to refer to each other by **service name** as a hostname.

## Trip Segmentation Count
Trips occurring within different distance segments in October 2019?

``` sql
SELECT
  CASE
    WHEN trip_distance <= 1 THEN 'Up to 1 mile'
    WHEN trip_distance > 1 AND trip_distance <= 3 THEN '1-3 miles'
    WHEN trip_distance > 3 AND trip_distance <= 7 THEN '3-7 miles'
    WHEN trip_distance > 7 AND trip_distance <= 10 THEN '7-10 miles'
    ELSE 'Over 10 miles'
  END AS distance_levels,
  COUNT(*) AS trip_count
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
GROUP BY distance_levels
ORDER BY trip_count DESC;
```

## Longest Trip Per Day

```sql
SELECT lpep_pickup_datetime::date AS pickup_day, MAX(trip_distance) AS max_distance
FROM green_taxi_trips
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;
```

## Top Pickup Zones on 2019-10-18

```sql
SELECT tz."Zone", SUM(g.total_amount) AS total
FROM green_taxi_trips g
INNER JOIN taxi_zones tz ON tz."LocationID" = g."PULocationID"
WHERE g.lpep_pickup_datetime::date = '2019-10-18'
GROUP BY tz."Zone"
ORDER BY total DESC
LIMIT 3;
```

## Largest Tip for East Harlem North

```sql
SELECT dropoffzone."Zone", g.tip_amount
FROM green_taxi_trips g
INNER JOIN taxi_zones pickupzone ON pickupzone."LocationID" = g."PULocationID"
INNER JOIN taxi_zones dropoffzone ON dropoffzone."LocationID" = g."DOLocationID"
WHERE g.lpep_pickup_datetime >= '2019-10-01' 
  AND g.lpep_pickup_datetime < '2019-11-01'
  AND pickupzone."Zone" = 'East Harlem North'
ORDER BY g.tip_amount DESC
LIMIT 1;
```

## Terraform Workflow
To prepare an environment by creating resources in GCP with Terraform.  
The sequence to:

- Downloading the provider plugins and setting up backend: `terraform init`  
- Generating proposed changes and auto-executing the plan: `terraform apply -auto-approve`  
- Remove all resources managed by terraform: `terraform destroy`
