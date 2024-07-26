import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.point import Point
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

API_KEY = os.environ['NASA_API_KEY']

@st.cache_data(ttl=3600)
def fetch_data(url):
    response = requests.get(url)
    return response.json()

def fetch_earth_events(api_key):
    return fetch_data(f"https://eonet.gsfc.nasa.gov/api/v3/events?limit=250&api_key={api_key}")

def fetch_categories(api_key):
    return fetch_data(f"https://eonet.gsfc.nasa.gov/api/v3/categories?api_key={api_key}")

@lru_cache(maxsize=100)
def coordinates_to_location(lat, lon):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.reverse(f"{lat}, {lon}", zoom=2)
    return location.address if location else f"Coordinates: {lat}, {lon}"

category_colors = {
    "Wildfires": "red", "Severe Storms": "blue", "Volcanoes": "orange",
    "Earthquakes": "purple", "Floods": "green", "Landslides": "brown",
    "Manmade": "black", "Sea and Lake Ice": "cyan", "Snow": "lightblue",
    "Temperature Extremes": "pink", "Water Color": "darkblue",
    "Drought": "yellow", "Dust and Haze": "gray"
}

st.set_page_config(layout="wide", page_title="Earth Observatory Natural Event Tracker")
st.title("Earth Observatory Natural Event Tracker")

@st.cache_data(ttl=3600)
def load_and_process_data(api_key, selected_categories):
    earth_events_data = fetch_earth_events(api_key)
    event_data = []
    for event in earth_events_data['events']:
        if any(category['title'] in selected_categories for category in event['categories']):
            for geometry in event['geometry']:
                event_data.append({
                    'title': event['title'],
                    'category': event['categories'][0]['title'],
                    'date': pd.to_datetime(geometry['date']),
                    'coordinates': geometry['coordinates']
                })
    df = pd.DataFrame(event_data)
    return df.sort_values('date', ascending=False).groupby('category').head().reset_index(drop=True)

categories_data = fetch_categories(API_KEY)
category_titles = [category['title'] for category in categories_data['categories']]
selected_categories = st.multiselect("Select categories to display:", category_titles, default=category_titles)

df = load_and_process_data(API_KEY, selected_categories)

col1, col2 = st.columns([3, 1])

with col1:
    m = folium.Map(location=[30, 10], zoom_start=1)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['coordinates'][1], row['coordinates'][0]],
            popup=f"{row['title']} ({row['date'].strftime('%Y-%m-%d')})",
            tooltip=row['category'],
            icon=folium.Icon(color=category_colors.get(row['category'], "blue"))
        ).add_to(m)
    st_folium(m, width=700, height=300)

    st.write("### Recent Earth Events")
    for _, row in df.iterrows():
        with st.expander(f"**{row['title']}** - {row['date'].strftime('%Y-%m-%d')}"):
            st.write(f"Category: {row['category']}")
            lon, lat = row['coordinates']
            st.write(f"Location: {coordinates_to_location(lat, lon)}")

with col2:
    st.write("### Category Colors")
    for category, color in category_colors.items():
        st.markdown(f"<span style='color:{color}; font-size: 12px;'>⬤</span> <span style='font-size: 12px;'>{category}</span>", unsafe_allow_html=True)

st.write(f"Total events displayed: {len(df)}")