# streamlit_app/app.py
import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard (Live)", layout="wide")

# If a DATABASE_URL is set (Streamlit secrets or env), use Postgres (Supabase).
# Otherwise fall back to local DuckDB file (developer mode).
DATABASE_URL = None
# Streamlit Cloud exposes secrets via st.secrets; local dev may set env var directly.
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    DATABASE_URL = os.environ.get("DATABASE_URL")

def load_from_postgres(db_url: str) -> pd.DataFrame:
    from sqlalchemy import create_engine, text
    engine = create_engine(db_url)
    query = """
    SELECT
      date_trunc('day', invoicedate) as day,
      sum(quantity * unitprice) as revenue,
      count(*) as orders,
      count(distinct customerid) as unique_customers
    FROM orders
    GROUP BY 1
    ORDER BY 1
    """
    df = pd.read_sql(query, engine)
    # day might be Timestamp, convert to date for display
    df['day'] = pd.to_datetime(df['day']).dt.date
    return df

def load_from_duckdb(duckdb_path: str = "duckdb/ecommerce.duckdb") -> pd.DataFrame:
    # Import locally only when needed
    import duckdb
    con = duckdb.connect(duckdb_path)
    # try typical schema names used by dbt; fall back if not present
    for candidate in ["marts.mart_daily_sales", "mart_daily_sales", "marts.mart_daily_sales"]:
        try:
            df = con.execute(f"SELECT * FROM {candidate}").df()
            return df
        except Exception:
            continue
    # fallback to reading any table named mart_daily_sales or orders
    try:
        return con.execute("SELECT * FROM mart_daily_sales").df()
    except Exception:
        try:
            return con.execute("SELECT * FROM orders").df()
        except Exception as e:
            raise RuntimeError("No suitable table found in DuckDB. Run dbt locally or point DATABASE_URL to Supabase.") from e

st.title("📊 E-Commerce Sales Dashboard (Live)")

if DATABASE_URL:
    st.caption("Connected to remote Postgres (live demo)")
    df = load_from_postgres(DATABASE_URL)
else:
    st.caption("Using local DuckDB (developer mode). Set DATABASE_URL in Streamlit secrets or env to enable live mode.")
    try:
        df = load_from_duckdb()
    except Exception as e:
        st.error("Could not load data from DuckDB: " + str(e))
        st.stop()

# Basic KPIs
total_revenue = df["revenue"].sum() if "revenue" in df.columns else 0
total_orders = int(df["orders"].sum()) if "orders" in df.columns else 0
unique_customers = int(df["unique_customers"].sum()) if "unique_customers" in df.columns else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{unique_customers:,}")

st.markdown("---")
st.subheader("Revenue Trend Over Time")
if df.empty:
    st.write("No data available yet.")
else:
    fig = px.line(df, x="day", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Recent Daily Metrics")
st.dataframe(df.sort_values("day", ascending=False).head(15))
