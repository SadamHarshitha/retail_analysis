import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session  # Ee line add cheyali
import pandas as pd
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="SmartMart Executive Dashboard", layout="wide")

# --- SESSION INITIALIZATION ---
def create_session():
    try:
        # Check if running inside Snowflake
        return get_active_session()
    except Exception:
        # External connection (GitHub/Streamlit Cloud)
        # Ee logic work avvali ante st.secrets set chesi undali
        return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()
# ... rest of your code stays the same ...

# --- HELPER FUNCTION ---
def run_query(query):
    # Snowflake Streamlit uses Snowpark dataframes
    return session.sql(query).to_pandas()

# --- 1. DATA LOADING ---
# Pulling directly from your Gold Views
df_prod = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_PRODUCT_PERFORMANCE")
df_reg = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_REGIONAL_INSIGHTS")
df_cust = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_CUSTOMER_SEGMENTATION")
df_inv = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_INVENTORY_OPERATIONS")
df_chan = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_CHANNEL_ANALYSIS")
df_time = run_query("SELECT * FROM RETAIL_DB.RETAIL_SCHEMA_GOLD.REPORT_TIME_TRENDS")

# --- 2. HEADER & FILTERS ---
st.title("🛍️ SmartMart Executive Dashboard")
st.markdown("### Real-time Intelligence from Gold Layer")

with st.sidebar:
    st.header("🎯 Filters")
    all_regions = df_reg['REGION'].unique().tolist()
    selected_regions = st.multiselect("Select Regions", options=all_regions, default=all_regions)

# Filtering logic
filtered_reg = df_reg[df_reg['REGION'].isin(selected_regions)]

# --- 3. ROW 1: KPI SCORECARDS ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_rev = df_prod['TOTAL_REVENUE'].sum()
total_qty = df_prod['TOTAL_QUANTITY_SOLD'].sum()
avg_order = df_cust['AVG_REVENUE_PER_ORDER'].mean()
loyalty_pct = (len(df_cust[df_cust['LOYALTY_STATUS'] == 'Repeat Customer']) / len(df_cust)) * 100

kpi1.metric("Total Revenue", f"${total_rev:,.0f}")
kpi2.metric("Units Sold", f"{total_qty:,.0f}")
kpi3.metric("Avg Order Value", f"${avg_order:,.2f}")
kpi4.metric("Retention Rate", f"{loyalty_pct:.1f}%")

st.divider()

# --- 4. ROW 2: SALES TRENDS & PRODUCTS ---
col_a, col_b = st.columns([3, 2])

with col_a:
    st.subheader("📈 Revenue Growth Trend")
    # Using st.area_chart (Native)
    trend_plot = df_time.set_index('SALE_DATE')['DAILY_REVENUE']
    st.area_chart(trend_plot, color="#00CC96")

with col_b:
    st.subheader("🏆 Top 10 Products")
    top_10 = df_prod.nlargest(10, 'TOTAL_REVENUE').set_index('PRODUCT_NAME')['TOTAL_REVENUE']
    st.bar_chart(top_10, color="#1f77b4")

# --- 5. ROW 3: SEGMENTATION & CHANNELS ---
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🌐 Channel Revenue")
    chan_data = df_chan.groupby('SALES_CHANNEL')['TOTAL_REVENUE'].sum()
    st.bar_chart(chan_data)

with c2:
    st.subheader("👥 Age Group Split")
    age_data = df_chan.groupby('AGE_GROUP')['ORDER_VOLUME'].sum()
    st.bar_chart(age_data, color="#ff7f0e")

with c3:
    st.subheader("📍 Regional Performance")
    reg_data = filtered_reg.groupby('REGION')['TOTAL_REVENUE'].sum()
    st.bar_chart(reg_data, color="#9467bd")

# --- 6. ROW 4: OPERATIONAL INSIGHTS ---
st.divider()
st.subheader("⚡ Inventory Velocity & Operations")
# Using st.scatter_chart (Native)
st.scatter_chart(
    data=df_inv,
    x='TOTAL_QTY_SOLD',
    y='SALES_VELOCITY_PER_DAY',
    color='CATEGORY',
    size='AVG_BASKET_SIZE'
)

st.success("✅ Dashboard directly connected to Snowflake Gold Layer.")