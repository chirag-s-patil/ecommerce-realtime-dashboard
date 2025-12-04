
  
    
    

    create  table
      "ecommerce"."main"."mart_daily_sales__dbt_tmp"
  
    as (
      

with raw as (
  select *
  from read_parquet('D:/Timepass Projects/Ecommerce Realtime/parquet/parquet/orders.parquet')
),

clean as (
  select
    try_cast(invoicedate as timestamp) as invoicedate,
    coalesce(try_cast(quantity as double), 0) as quantity,
    coalesce(try_cast(unitprice as double), 0) as unitprice,
    coalesce(try_cast(quantity as double) * try_cast(unitprice as double), 0) as total_amount,
    try_cast(customerid as integer) as customerid
  from raw
)

select
  date_trunc('day', invoicedate)::date as day,
  sum(total_amount) as revenue,
  count(distinct customerid) as unique_customers,
  count(*) as orders
from clean
group by 1
order by 1
    );
  
  