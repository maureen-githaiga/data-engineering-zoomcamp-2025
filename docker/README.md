# Docker, SQL, and Terraform

----

## ✅Running docker with the python:3.12.8 image in an interactive mode, using the entrypoint bash.

docker run -it --entrypoint=bash python:3.12.8
to check the version run command  pip --version

## Docker networking and docker-compose
In the Docker Compose.yaml file the two contsiners postgres and pg admin are connected through networking
the port that hostname and port that pgAdmin should use to connect to Postgres is postgres:5432 postgres is the container name and 5432 is the internal port of the database container.

## Trip Segmentation Count
How many trips occurred within different distance segments in October 2019?

Query: 

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

# Longest Trip Per Day

SELECT lpep_pickup_datetime::date AS pickup_day, MAX(trip_distance) AS max_distance
FROM green_taxi_trips
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;

#Top Pickup Zones on 2019-10-18

SELECT tz."Zone", SUM(g.total_amount) AS total
FROM green_taxi_trips g
INNER JOIN taxi_zones tz ON tz."LocationID" = g."PULocationID"
WHERE g.lpep_pickup_datetime::date = '2019-10-18'
GROUP BY tz."Zone"
ORDER BY total DESC
LIMIT 3;
#Largest Tip for East Harlem North
SELECT dropoffzone."Zone", g.tip_amount
FROM green_taxi_trips g
INNER JOIN taxi_zones pickupzone ON pickupzone."LocationID" = g."PULocationID"
INNER JOIN taxi_zones dropoffzone ON dropoffzone."LocationID" = g."DOLocationID"
WHERE g.lpep_pickup_datetime >= '2019-10-01' 
  AND g.lpep_pickup_datetime < '2019-11-01'
  AND pickupzone."Zone" = 'East Harlem North'
ORDER BY g.tip_amount DESC
LIMIT 1;

#Terraform Workflow
 To prepare an environment by creating resources in GCP with Terraform.
 the sequence to : 
Downloading the provider plugins and setting up backend  terraform init,  
Generating proposed changes and auto-executing the plan ...terraform apply -auto-approve,
Remove all resources managed by terraform` terraform destroy
