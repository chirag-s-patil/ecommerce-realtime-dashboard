import pandas as pd
from sqlalchemy import create_engine

PG_URL = "postgresql://postgres:password@localhost:5432/ecommerce"
TABLE = "orders"   # table name used earlier

def main():
    engine = create_engine(PG_URL)

    # count rows
    cnt = pd.read_sql(f"SELECT COUNT(*) AS c FROM {TABLE}", engine)
    print("Row count:", int(cnt['c'].iloc[0]))

    # sample 5 rows
    df = pd.read_sql(f"SELECT * FROM {TABLE} LIMIT 5", engine)
    print("\nSample rows:\n", df.to_string(index=False))

if __name__ == "__main__":
    main()
