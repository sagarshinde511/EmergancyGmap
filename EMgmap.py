import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# Run this at the top: Refreshes the app every 5000ms (5 seconds)
st_autorefresh(interval=5000, key="maprefresh")

def show_simple_map():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>#map { height: 400px; width: 100%; border-radius: 10px; }</style>
    </head>
    <body>
    <div id="map"></div>
    <script>
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            var map = L.map('map').setView([lat, lon], 16);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            L.marker([lat, lon]).addTo(map).bindPopup('Current Location').openPopup();
        });
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=450)

st.title("📍 Auto-Refreshing Location")
show_simple_map()
