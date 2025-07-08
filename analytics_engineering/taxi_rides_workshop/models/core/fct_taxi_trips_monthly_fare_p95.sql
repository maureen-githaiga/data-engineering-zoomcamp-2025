{{ config(materialized="table") }}

with
    trips_data as (

        select *
        from {{ ref("fact_trips") }}
        where
            month = 4 and
            year = 2020 and
            fare_amount > 0
            and trip_distance > 0
            and payment_type_description in ('Cash', 'Credit card')
            and service_type = 'Green'

    )
select
    service_type,
    year,
    month,
    {{ bigquery__quantile('fare_amount', 0.9, 'service_type, year, month') }} as p90_fare_amount ,
    {{ bigquery__quantile('fare_amount', 0.95, 'service_type, year, month') }} as p95_fare_amount ,
    {{ bigquery__quantile('fare_amount', 0.97, 'service_type, year, month') }} as p97_fare_amount 
from trips_data


