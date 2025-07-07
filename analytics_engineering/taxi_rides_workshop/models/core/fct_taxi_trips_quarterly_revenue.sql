{{ config(materialized='table') }}

with trips_data as (
    select 
    service_type,
    year,
    quarter,
    year_quarter,
    sum(total_amount) as quarterly_revenue
    
    from {{ ref('fact_trips') }}
    group by 1,2,3,4
),
lagged as (
    select *,
    lag(quarterly_revenue) over (partition by service_type, quarter order by year) as last_year_revenue
    from trips_data
)
select *,
{{ safe_divide('quarterly_revenue - last_year_revenue', 'last_year_revenue') }} as yoy_growth
from lagged
order by service_type, year, year_quarter