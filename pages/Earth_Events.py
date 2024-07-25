import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

from dotenv import load_dotenv
load_dotenv() 

import os
API_KEY = os.environ['NASA_API_KEY']

def fetch_earth_events(api_key):
    url = f"https://eonet.gsfc.nasa.gov/api/v3/events?limit=250&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def fetch_categories(api_key):
    url = f"https://eonet.gsfc.nasa.gov/api/v3/categories?api_key={api_key}"
    response = requests.get(url)
    return response.json()

category_colors = {
    "Wildfires": "red",
    "Severe Storms": "blue",
    "Volcanoes": "orange",
    "Earthquakes": "purple",
    "Floods": "green",
    "Landslides": "brown",
    "Manmade": "black",
    "Sea and Lake Ice": "cyan",
    "Snow": "lightblue",
    "Temperature Extremes": "pink",
    "Water Color": "darkblue",
    "Drought": "yellow",
    "Dust and Haze": "gray"
}


st.title("Earth Observatory Natural Event Tracker")

earth_events_data = fetch_earth_events(API_KEY)
categories_data = fetch_categories(API_KEY)

category_titles = [category['title'] for category in categories_data['categories']]
selected_categories = st.multiselect("Select categories to display:", category_titles, default=category_titles)

event_data = []
for event in earth_events_data['events']:
    if any(category['title'] in selected_categories for category in event['categories']):
        for geometry in event['geometry']:
            event_data.append({
                'title': event['title'],
                'category': event['categories'][0]['title'],
                'date': pd.to_datetime(geometry['date']),  # Convert to datetime
                'coordinates': geometry['coordinates']
            })

df = pd.DataFrame(event_data)

# Filter to keep only the 50 most recent events per category
df = df.sort_values('date', ascending=False).groupby('category').head().reset_index(drop=True)

col1, col2 = st.columns([2, 1])

m = folium.Map(location=[50, 50], zoom_start=0)

for _, row in df.iterrows():
    category = row['category']
    color = category_colors.get(category, "blue")
    folium.Marker(
        location=[row['coordinates'][1], row['coordinates'][0]],
        popup=f"{row['title']} ({row['date'].strftime('%Y-%m-%d')})",
        tooltip=row['category'],
        icon=folium.Icon(color=color)
    ).add_to(m)

with col1:
    st_folium(m, width=700, height=300)
    st.write("### Recent Earth Events")
    for _, row in df.iterrows():
        st.write(f"**{row['title']}**")
        st.write(f"Category: {row['category']}")
        st.write(f"Date: {row['date'].strftime('%Y-%m-%d')}")
        st.write("---")

st.write(f"Total events displayed: {len(df)}")

with col2:
    st.write("### Category Colors")
    for category, color in category_colors.items():
        st.markdown(f"<span style='color:{color}'>⬤</span> {category}", unsafe_allow_html=True)
