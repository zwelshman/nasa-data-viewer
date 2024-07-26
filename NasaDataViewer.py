import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta
from datetime import datetime
from dotenv import load_dotenv
load_dotenv() 

st.set_page_config(initial_sidebar_state="auto")

import os
API_KEY = os.environ['NASA_API_KEY']

st.title("NASA Data Viewer")

st.write("Welcome to the NASA Data Viewer app. This application provides access to various NASA data sources and space weather information.")

# Navigation buttons
col1, col2, col3 = st.columns(3)
container_height = 175

with col1:
    with st.container(height = container_height, border=True):
        st.page_link("pages/Nasa Picture of the Day.py", label="NASA Photo of the Day", icon="🌠")
        st.markdown("""View NASA's daily featured space image along with its explanation.""")
    with st.container(height = container_height, border=True):    
        st.page_link("pages/Near Earth Objects.py", label="Near Earth Objects", icon="☄️")
        st.markdown("""Explore data on asteroids and comets that pass close to Earth, including their sizes and potential hazards.""")

with col2:
    with st.container(height = container_height,border=True):
        st.page_link("pages/Mars_Rover_Photos.py", label="Mars Rover", icon="🔴")
        st.markdown("""Browse through images captured by NASA's Mars rovers, offering a glimpse of the Martian landscape.""")
    with st.container(height = container_height,border=True):
        st.page_link("pages/Earth_Events.py", label="Natural Disaster Events", icon="🌍")
        st.markdown("""Track natural events occurring on Earth using NASA's Earth Observatory Natural Event Tracker.""")

with col3:
    with st.container(height = container_height,border=True):
        st.page_link("pages/Geomagnetic Storms.py", label="Geomagnetic Storms", icon="⚡")
        st.markdown("""Monitor geomagnetic storm activity and their potential impacts on Earth.""")

# st.markdown("## Current Space Weather Summary")

# def fetch_space_weather_data():
#     today = datetime.now().strftime("%Y-%m-%d")
#     yesterday = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
#     url = f"https://api.nasa.gov/DONKI/GST?startDate={yesterday}&endDate={today}&api_key={API_KEY}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None

# space_weather_data = fetch_space_weather_data()

# if space_weather_data:
#     if len(space_weather_data) > 0:
#         st.write("Recent Geomagnetic Storm Activity in last 30 days:")
#         for storm in space_weather_data:
#             st.write(f"- Storm ID: {storm['gstID']}")
#             st.write(f"  Start Time: {storm['startTime']}")
#             if 'allKpIndex' in storm and storm['allKpIndex']:
#                 max_kp = max(kp['kpIndex'] for kp in storm['allKpIndex'])
#                 st.write(f"  Maximum Kp Index: {max_kp}")
#             st.write("  ")
#     else:
#         st.write("No significant geomagnetic storm activity in the past 24 hours.")
# else:
#     st.write("Unable to fetch current space weather data. Please try again later.")

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
