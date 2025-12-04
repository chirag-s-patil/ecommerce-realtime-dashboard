import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

DB = r"D:/Timepass Projects/Ecommerce Realtime/duckdb/ecommerce.duckdb"

@st.cache_data(ttl=60)
def load_data():
    con = duckdb.connect(DB)
    try:
        df = con.execute("SELECT * FROM marts.mart_daily_sales").df()
    except:
        df = con.execute("SELECT * FROM mart_daily_sales").df()
    return df

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📊 E-Commerce Sales Dashboard")

df = load_data()

# KPIs
total_revenue = df["revenue"].sum()
total_orders = df["orders"].sum()
unique_customers = df["unique_customers"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{unique_customers:,}")

# Charts
st.markdown("---")
st.subheader("Revenue Trend Over Time")

fig = px.line(df, x="day", y="revenue")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Orders Over Time")
fig2 = px.bar(df, x="day", y="orders")
st.plotly_chart(fig2, use_container_width=True)

# Show recent rows
st.subheader("Recent Daily Metrics")
st.dataframe(df.sort_values("day", ascending=False).head(15))
