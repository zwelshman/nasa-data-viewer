import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import date, timedelta

import os
API_KEY = os.environ['NASA_API_KEY']

def fetch_neo_data(api_key, start_date, end_date):
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def plot_neo_diameters(neo_list):
    names = [neo['name'] for neo in neo_list]
    diameters = [neo['estimated_diameter']['kilometers']['estimated_diameter_max'] for neo in neo_list]
    plt.figure(figsize=(10, 5))
    plt.barh(names, diameters, color='skyblue')
    plt.xlabel('Estimated Diameter (km)')
    plt.title('Estimated Diameters of Near Earth Objects')
    st.pyplot(plt)

st.title("Near Earth Objects")

today = date.today()
yesterday = today - timedelta(1)
neo_data = fetch_neo_data(API_KEY, yesterday, today)

neo_count = neo_data['element_count']
st.write(f"Number of Near Earth Objects today {str(today)} is: {neo_count}")

neo_list = neo_data['near_earth_objects'][str(yesterday)]
for neo in neo_list:
    st.write(f"Name: {neo['name']}")
    st.write(f"Estimated Diameter (km): {neo['estimated_diameter']['kilometers']['estimated_diameter_max']:.2f}")
    st.write(f"Potentially Hazardous: {neo['is_potentially_hazardous_asteroid']}")
    if neo['is_potentially_hazardous_asteroid']:
        st.write(f"Potential Impact Location: {neo['close_approach_data']}")
    st.write("---")

plot_neo_diameters(neo_list)
