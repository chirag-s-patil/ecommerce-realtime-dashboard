# extract_to_parquet.py

import os
import pandas as pd
from sqlalchemy import create_engine
import duckdb

PG_URL = "postgresql://postgres:password@localhost:5432/ecommerce"

PARQUET_DIR = "parquet"
DUCKDB_FILE = r"duckdb\ecommerce.duckdb"  # Windows-friendly path

os.makedirs(PARQUET_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DUCKDB_FILE), exist_ok=True)

def read_table(table_name):
    engine = create_engine(PG_URL)
    print(f"Reading {table_name} from Postgres...")
    df = pd.read_sql_table(table_name, engine)
    return df

def write_parquet(df, name):
    path = os.path.join(PARQUET_DIR, f"{name}.parquet")
    df.to_parquet(path, index=False)
    print(f"Written: {path}")
    return path

def create_duckdb_table(parquet_path, table_name):
    con = duckdb.connect(DUCKDB_FILE)
    parquet_path = parquet_path.replace("\\", "/")  # Important for Windows path
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_parquet('{parquet_path}')")
    con.close()
    print(f"Created DuckDB table `{table_name}` in {DUCKDB_FILE}")

def main():
    table = "orders"

    df = read_table(table)
    p = write_parquet(df, table)
    create_duckdb_table(p, table)

    print("ETL complete!")

if __name__ == "__main__":
    main()
