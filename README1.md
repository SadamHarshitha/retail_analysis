# 🛍️ SmartMart 360° Retail Analytics Dashboard

An executive-level business intelligence dashboard built with **Streamlit** and **Snowflake**, utilizing the **Medallion Architecture (Gold Layer)** for real-time retail insights.

## 🚀 Features
* **Executive KPIs:** Total Revenue, Units Sold, Avg Order Value, and Customer Retention.
* **Sales Trends:** Interactive area charts showing monthly revenue growth.
* **Product Analytics:** Top 10 performing products by revenue.
* **Regional Insights:** Geographical performance breakdown across different stores and cities.
* **Inventory Ops:** Analysis of sales velocity and average basket sizes.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Database:** Snowflake (Gold Schema Views)
* **Frontend:** Streamlit
* **Visualization:** Altair & Native Streamlit Charts
* **Data Processing:** Snowpark Python API

## 📂 Project Structure
* `streamlit_app.py`: Main application code with hybrid session logic.
* `requirements.txt`: Python dependencies.
* `README.md`: Project documentation.

## ⚙️ Setup & Deployment

### 1. Snowflake Tables
Ensure your Snowflake account has the `RETAIL_DB.RETAIL_SCHEMA_GOLD` views created from the Fact and Dimension tables.

### 2. Local Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with your Snowflake credentials.
4. Run: `streamlit run streamlit_app.py`

### 3. Streamlit Cloud Deployment
1. Connect your GitHub repo to [Streamlit Cloud](https://share.streamlit.io).
2. Add your Snowflake credentials to the **Secrets** section in the app settings.

---
*Developed by Harshitha Sadam*
