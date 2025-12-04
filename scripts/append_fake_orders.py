# scripts/append_fake_orders.py
import os
import random
import uuid
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Read DATABASE_URL from env
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("Set DATABASE_URL environment variable before running this script.")

# Create engine
engine = create_engine(DATABASE_URL, future=True)

def make_order():
    return {
        "invoiceno": str(uuid.uuid4())[:8],
        "stockcode": str(random.randint(10000, 99999)),
        "description": f"Sample product {random.randint(1,999)}",
        "quantity": random.choice([1,1,1,2,3]),
        "invoicedate": datetime.utcnow(),
        "unitprice": round(random.uniform(5,100), 2),
        "customerid": str(random.randint(10000,99999)),
        "country": random.choice(["United Kingdom","United States","India","Germany","France"])
    }

def main(n=5):
    rows = [make_order() for _ in range(n)]
    df = pd.DataFrame(rows)
    # Use pandas.to_sql to append
    with engine.begin() as conn:
        df.to_sql("orders", conn, if_exists="append", index=False, method="multi")
    print(f"Inserted {len(rows)} rows.")

if __name__ == "__main__":
    # You can pass number of rows via env var APPEND_COUNT if you like
    n = int(os.environ.get("APPEND_COUNT", "5"))
    main(n)
