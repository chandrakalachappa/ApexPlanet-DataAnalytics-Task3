import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="ApexPlanet Task 3 Dashboard", layout="wide")
st.title("ApexPlanet Data Analytics — Task 3")
st.subheader("Deep-Dive Sales Analysis")
st.caption("Built from the cleaned Task 1 dataset and extending the Task 2 EDA themes.")

DATA_PATH ="ApexPlanet_Task1_Cleaned_Dataset.csv" 

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Total_Sales", "Quantity", "Age"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()
required = {"Total_Sales"}
if not required.issubset(df.columns):
    st.error("The dataset must contain a Total_Sales column.")
    st.stop()

filtered = df.copy()
with st.sidebar:
    st.header("Dashboard Filters")
    if "Order_Date" in filtered.columns and filtered["Order_Date"].notna().any():
        valid_dates = filtered["Order_Date"].dropna()
        start = valid_dates.min().date()
        end = valid_dates.max().date()
        chosen = st.date_input("Order date range", value=(start, end), min_value=start, max_value=end)
        if isinstance(chosen, tuple) and len(chosen) == 2:
            filtered = filtered[
                filtered["Order_Date"].dt.date.between(chosen[0], chosen[1]) |
                filtered["Order_Date"].isna()
            ]
    for col, label in [("Category", "Category"), ("City", "City"), ("Age_Group", "Age group"), ("Gender", "Gender")]:
        if col in filtered.columns:
            options = sorted(filtered[col].dropna().astype(str).unique().tolist())
            selected = st.multiselect(label, options, default=options)
            if selected:
                filtered = filtered[filtered[col].astype(str).isin(selected)]

total_sales = filtered["Total_Sales"].sum()
order_count = filtered["Order_ID"].nunique() if "Order_ID" in filtered.columns else len(filtered)
avg_order = total_sales / order_count if order_count else 0
units = filtered["Quantity"].sum() if "Quantity" in filtered.columns else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"{total_sales:,.2f}")
c2.metric("Unique Orders", f"{order_count:,}")
c3.metric("Average Sales / Order", f"{avg_order:,.2f}")
c4.metric("Units Sold", f"{units:,.0f}")

st.markdown("---")
left, right = st.columns(2)

if "Category" in filtered.columns:
    cat = filtered.groupby("Category", dropna=False)["Total_Sales"].sum().reset_index().sort_values("Total_Sales", ascending=False)
    left.subheader("Sales by Category")
    left.plotly_chart(px.bar(cat, x="Category", y="Total_Sales", title="Total sales by category"), use_container_width=True)
else:
    left.info("Category column not found in dataset.")

if "Order_Date" in filtered.columns:
    monthly = filtered.dropna(subset=["Order_Date"]).copy()
    monthly["Month"] = monthly["Order_Date"].dt.to_period("M").astype(str)
    monthly = monthly.groupby("Month")["Total_Sales"].sum().reset_index()
    right.subheader("Monthly Sales Trend")
    right.plotly_chart(px.line(monthly, x="Month", y="Total_Sales", markers=True, title="Sales by month"), use_container_width=True)
else:
    right.info("Order_Date column not found in dataset.")

left2, right2 = st.columns(2)
if "Product" in filtered.columns:
    top_products = filtered.groupby("Product", dropna=False)["Total_Sales"].sum().reset_index().sort_values("Total_Sales", ascending=False).head(10)
    left2.subheader("Top 10 Products")
    left2.plotly_chart(px.bar(top_products.sort_values("Total_Sales"), x="Total_Sales", y="Product", orientation="h", title="Top products by sales"), use_container_width=True)

if "City" in filtered.columns:
    cities = filtered.groupby("City", dropna=False)["Total_Sales"].sum().reset_index().sort_values("Total_Sales", ascending=False).head(10)
    right2.subheader("Top 10 Cities")
    right2.plotly_chart(px.bar(cities, x="City", y="Total_Sales", title="Top cities by sales"), use_container_width=True)

st.subheader("Filtered Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales_data.csv", "text/csv")

st.caption("Note: sales values are shown without a currency symbol because the dataset's currency was not confirmed.")
