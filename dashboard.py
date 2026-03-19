import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="City Pulse: Bengaluru", layout="wide")
st.title("🏙️ Live City Pulse: Bengaluru")


# 2. Load the data from your CSV
def load_data():
    if os.path.exists("city_data.csv"):
        df = pd.read_csv("city_data.csv")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    return pd.DataFrame()


import os

df = load_data()

if not df.empty:
    # 3. Top Row: Key Metrics
    col1, col2, col3 = st.columns(3)
    latest = df.iloc[-1]

    with col1:
        st.metric("Current Humidity", f"{latest['Humidity']}%")
    with col2:
        st.metric("Current Traffic Speed", f"{latest['Traffic_Speed_KMH']} km/h")
    with col3:
        st.metric("Data Points Collected", len(df))

    # 4. The "Unique Twist" Chart: Correlation Trend
    st.subheader("Traffic Speed vs. Humidity Over Time")

    # Create a line chart with two axes
    fig = px.line(df, x="Timestamp", y=["Humidity", "Traffic_Speed_KMH"],
                  title="Environmental Impact on Urban Mobility",
                  labels={"value": "Value", "variable": "Metric"},
                  template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # 5. Show the raw logs
    with st.expander("View Raw Data Logs"):
        st.dataframe(df.sort_values(by="Timestamp", ascending=False))
else:
    st.warning("No data found yet. Keep your 'app.py' running to collect data!")

st.info("💡 Pro-Tip: Keep 'app.py' running in one terminal and this dashboard in another.")