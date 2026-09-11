import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="911 Call Volume Predictor", layout="wide")

st.title("🚨 911 Call Volume Predictor")
st.markdown("Predict Seattle Fire Department 911 call volume by hour")

st.divider()

col1, col2 = st.columns(2)

with col1:
    year = st.selectbox("Year", [2024, 2025, 2026, 2027], index=2)
    month = st.selectbox("Month", list(range(1, 13)), index=8)
    
with col2:
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_name = st.selectbox("Day of Week", days)
    day_of_week = days.index(day_name)
    hour = st.slider("Hour", 0, 23, 17)

if st.button("Predict", type="primary"):
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={
            "year": year,
            "month": month,
            "day_of_week": day_of_week,
            "hour": hour
        }
    )
    
    if response.status_code == 200:
        prediction = response.json()["predicted_calls"]
        st.metric("Predicted Calls This Hour", f"{prediction:.1f}")
    else:
        st.error("API Error")