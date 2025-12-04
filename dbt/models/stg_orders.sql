{{ config(materialized='view') }}

with raw as (
  select *
  from read_parquet('D:/Timepass Projects/Ecommerce Realtime/parquet/parquet/orders.parquet')
)

select
  invoiceno,
  stockcode,
  description,
  try_cast(quantity as integer) as quantity,
  try_cast(invoicedate as timestamp) as invoicedate,
  try_cast(unitprice as double) as unitprice,
  try_cast(customerid as integer) as customerid,
  country
from raw
