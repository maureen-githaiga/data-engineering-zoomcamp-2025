{{ config(materialized="table") }}

with
    trips_data as (

        select * ,
        timestamp_diff(dropoff_datetime, pickup_datetime,second ) as trip_duration
        from {{ ref("dim_fhv_trips") }} 
        where month = 11 and year = 2019 and pickup_zone in ("Newark Airport", "SoHo", "Yorkville East")

    ),
    p90_by_pair as (
        select *,
        {{ bigquery__quantile('trip_duration', 0.9, 'year, month,pickup_locationid,dropoff_locationid') }} as p90_trip_duration
        from trips_data
    ),
    ranked as (
        select *,
        row_number() over (partition by pickup_zone order by p90_trip_duration desc) as rn
        from p90_by_pair

    )
    select pickup_zone,
    dropoff_zone,
    p90_trip_duration
from ranked
where rn = 2

