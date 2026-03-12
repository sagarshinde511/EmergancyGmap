import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import folium
from streamlit_folium import st_folium

st.title("Auto-Loading Map & Location")

# JavaScript call to get geolocation
location = streamlit_js_eval(
    js_expressions="done(navigator.geolocation.getCurrentPosition(pos => { \
        const {latitude, longitude} = pos.coords; \
        done({latitude, longitude}); \
    }))", 
    want_output=True,
    key="get_location"
)

if location:
    lat = location['latitude']
    lon = location['longitude']
    
    st.success(f"Location found: {lat}, {lon}")
    
    # Create and display the map centered on the current location
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="You are here").add_to(m)
    
    st_folium(m, width=700, height=500)
else:
    st.info("Please allow location access in your browser to load the map.")
