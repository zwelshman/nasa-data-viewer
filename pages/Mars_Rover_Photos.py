import os
API_KEY = os.environ['NASA_API_KEY']

import streamlit as st
import requests
import pandas as pd
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv() 

# NASA API URL
NASA_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

def fetch_mars_photos(earth_date, api_key):
    params = {
        "earth_date": earth_date.strftime("%Y-%m-%d"),
        "api_key": api_key
    }
    response = requests.get(NASA_API_URL, params=params)
    return response.json()

def get_last_5_photos(start_date, api_key):
    photos = []
    current_date = start_date
    
    while len(photos) < 5:
        data = fetch_mars_photos(current_date, api_key)
        if "photos" in data and data["photos"]:
            photos.extend(data["photos"])
            if len(photos) >= 5:
                return photos[-5:]
        current_date -= timedelta(days=1)
    
    return photos[-5:]

st.title("Mars Rover Photos")

earth_date = st.date_input("Select Earth Date", value=pd.to_datetime("2024-02-19"))
api_key = API_KEY

photos = get_last_5_photos(earth_date, api_key)

if photos:
    st.write(f"Displaying the last {len(photos)} photos:")
    
    for photo in photos:
        st.image(photo["img_src"], caption=f"Camera: {photo['camera']['full_name']}", use_column_width=True)
        st.write(f"Taken on: {photo['earth_date']}")
        st.write(f"Rover: {photo['rover']['name']}")
        st.write("---")
else:
    st.error("No photos found even after searching previous dates.")
