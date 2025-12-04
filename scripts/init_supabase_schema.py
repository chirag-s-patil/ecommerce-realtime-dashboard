# scripts/init_supabase_schema.py
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("Set DATABASE_URL environment variable before running this script.")

engine = create_engine(DATABASE_URL, future=True)

create_sql = """
CREATE TABLE IF NOT EXISTS orders (
  invoiceno TEXT,
  stockcode TEXT,
  description TEXT,
  quantity INTEGER,
  invoicedate TIMESTAMP,
  unitprice DOUBLE PRECISION,
  customerid TEXT,
  country TEXT
);
"""

with engine.begin() as conn:
    conn.execute(text(create_sql))
    print("✅ orders table ensured (created if not exists).")
