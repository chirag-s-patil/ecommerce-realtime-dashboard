import os, pandas as pd
from sqlalchemy import create_engine
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, future=True)
df = pd.read_sql("SELECT COUNT(*) as c FROM orders;", engine)
print("rows in orders:", int(df['c'].iloc[0]))