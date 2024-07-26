import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv() 

api_key = os.environ['NASA_API_KEY']

@st.cache_data(ttl=43200)  # Cache for 24 hours
def fetch_apod(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    return response.json()

st.set_page_config(page_title="Astronomy Picture of the Day", layout="wide")

st.title("Astronomy Picture of the Day")

apod_data = fetch_apod(api_key)
import pprint 
st.image(apod_data['hdurl'], caption=apod_data['title'], use_column_width=True)
st.write(apod_data['explanation'])