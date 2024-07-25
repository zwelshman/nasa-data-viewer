import streamlit as st
import requests

import os
API_KEY = os.environ['NASA_API_KEY']

def fetch_apod(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    return response.json()

st.title("Astronomy Picture of the Day")

apod_data = fetch_apod(API_KEY)
st.image(apod_data['url'], caption=apod_data['title'])
st.write(apod_data['explanation'])
