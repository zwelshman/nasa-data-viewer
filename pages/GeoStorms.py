import streamlit as st
import requests
from datetime import datetime, timedelta

import os
API_KEY = os.environ['NASA_API_KEY']

st.title("NASA DONKI Geomagnetic Storm (GST) Viewer with Storm Magnitude")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", datetime.now())

def fetch_gst_data(start_date, end_date, api_key):
    url = "https://api.nasa.gov/DONKI/GST"
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

def get_storm_magnitude(kp_index):
    if kp_index >= 9:
        return "G5 - Extreme"
    elif kp_index >= 8:
        return "G4 - Severe"
    elif kp_index >= 7:
        return "G3 - Strong"
    elif kp_index >= 6:
        return "G2 - Moderate"
    elif kp_index >= 5:
        return "G1 - Minor"
    else:
        return "Below storm level"

data = fetch_gst_data(start_date, end_date, API_KEY)

if data:
    st.success(f"Found {len(data)} geomagnetic storm event(s)")
    for storm in data:
        st.subheader(f"Geomagnetic Storm: {storm['gstID']}")
        st.write(f"**Start Time:** {storm['startTime']}")
        
        if 'allKpIndex' in storm and storm['allKpIndex']:
            st.write("**Kp Index Information:**")
            for kp in storm['allKpIndex']:
                kp_value = kp['kpIndex']
                magnitude = get_storm_magnitude(kp_value)
                st.write(f"- Time: {kp['observedTime']}, Kp Index: {kp_value}, Source : {kp['source']}, Magnitude: {magnitude}, Link: {storm['link']}")
        if 'linkedEvents' in storm and storm['linkedEvents']:
            st.write("**Linked Events:**")
            for event in storm['linkedEvents']:
                st.write(f"- {event['activityID']}")
        st.write("---")
else:
    st.warning("No geomagnetic storm data available for the selected date range.")

st.info("Data source: NASA DONKI Geomagnetic Storm (GST) API")
