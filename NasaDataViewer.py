import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta
from datetime import datetime

st.set_page_config(initial_sidebar_state="expanded")

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color: white;
    height: 3em;
    width: 200px;
    border-radius:10px;
    border:3px solid #000000;
    font-size:20px;
    font-weight: bold;
    margin: 0px 0px 10px 10px;
    display: inline-block;
}

div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)

# st.page_link("pages/APOD.py", label="APOD", icon="🌠")
# st.page_link("pages/NEO.py", label="NEO", icon="☄️")
# st.page_link("pages/Mars_Rover_Photos.py", label="Mars Rover", icon="🔴")
# st.page_link("pages/Earth_Events.py", label="Earth Events", icon="🌍")
# st.page_link("pages/GeoStorms.py", label="GeoStorms", icon="⚡")

import os
API_KEY = os.environ['NASA_API_KEY']

st.title("NASA Data Viewer")

st.write("Welcome to the NASA Data Viewer app. This application provides access to various NASA data sources and space weather information.")

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/APOD.py", label="APOD", icon="🌠")
    st.page_link("pages/NEO.py", label="NEO", icon="☄️")

with col2:
    st.page_link("pages/Mars_Rover_Photos.py", label="Mars Rover", icon="🔴")
    st.page_link("pages/Earth_Events.py", label="Earth Events", icon="🌍")

with col3:
    st.page_link("pages/GeoStorms.py", label="GeoStorms", icon="⚡")

st.markdown("## Available Data")

st.markdown("""
- **APOD (Astronomy Picture of the Day)**: View NASA's daily featured space image along with its explanation.
- **NEO (Near Earth Objects)**: Explore data on asteroids and comets that pass close to Earth, including their sizes and potential hazards.
- **Mars Rover Photos**: Browse through images captured by NASA's Mars rovers, offering a glimpse of the Martian landscape.
- **Earth Events**: Track natural events occurring on Earth using NASA's Earth Observatory Natural Event Tracker.
- **GeoStorms**: Monitor geomagnetic storm activity and their potential impacts on Earth.
""")

st.markdown("## Current Space Weather Summary")

def fetch_space_weather_data():
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://api.nasa.gov/DONKI/GST?startDate={yesterday}&endDate={today}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

space_weather_data = fetch_space_weather_data()

if space_weather_data:
    if len(space_weather_data) > 0:
        st.write("Recent Geomagnetic Storm Activity:")
        for storm in space_weather_data:
            st.write(f"- Storm ID: {storm['gstID']}")
            st.write(f"  Start Time: {storm['startTime']}")
            if 'allKpIndex' in storm and storm['allKpIndex']:
                max_kp = max(kp['kpIndex'] for kp in storm['allKpIndex'])
                st.write(f"  Maximum Kp Index: {max_kp}")
            st.write("  ")
    else:
        st.write("No significant geomagnetic storm activity in the past 24 hours.")
else:
    st.write("Unable to fetch current space weather data. Please try again later.")

st.markdown("""
For more detailed space weather information, including solar activity, geomagnetic conditions, and potential impacts on Earth, please visit the [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/).
""")

st.markdown("## About This App")
st.write("""
This NASA Data Viewer provides a comprehensive look at various aspects of space and Earth science. 
From daily astronomy pictures to near-Earth object tracking, Mars exploration, and Earth event monitoring, 
this app offers a wide range of data visualizations and information. The space weather summary 
gives you an up-to-date overview of current conditions that may affect our planet.

Explore the different pages to dive deeper into each topic!
""")
