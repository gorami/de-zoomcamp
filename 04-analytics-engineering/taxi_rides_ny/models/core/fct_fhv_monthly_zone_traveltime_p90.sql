with trips_data as (select * from `prod.dim_fhv_trips`)
select distinct
    trip_month,
    trip_year,
    pickup_locationid,
    dropoff_locationid,
    percentile_cont(trip_duration, 0.90) over (
        partition by trip_month, trip_year, pickup_locationid, dropoff_locationid
    ) p90
from trips_data