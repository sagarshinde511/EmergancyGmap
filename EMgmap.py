import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# Page Config
st.set_page_config(page_title="Live GPS Tracker", page_icon="📍")

def show_live_map():
    # Keep your HTML exactly as it was
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            #map { height: 500px; width: 100%; border-radius: 12px; }
            #status-bar { background: #f0f2f6; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
        </style>
    </head>
    <body>
    <div id="status-bar"><b>GPS Status:</b> <span id="msg">Initializing...</span> | <span id="coords">0.00, 0.00</span></div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map, marker, circle, firstLoad = true;
        function updatePosition() {
            navigator.geolocation.getCurrentPosition((position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById("coords").innerHTML = lat.toFixed(5) + ", " + lon.toFixed(5);
                if (firstLoad) {
                    map = L.map('map').setView([lat, lon], 16);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                    marker = L.marker([lat, lon]).addTo(map);
                    circle = L.circle([lat, lon], { radius: position.coords.accuracy }).addTo(map);
                    firstLoad = false;
                } else {
                    marker.setLatLng([lat, lon]);
                    circle.setLatLng([lat, lon]);
                    map.panTo([lat, lon]);
                }
            }, (err) => {}, { enableHighAccuracy: true });
        }
        updatePosition();
        setInterval(updatePosition, 5000);
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

st.title("🛰️ Live Locator")

# --- FETCH FROM JS TO PYTHON ---
# This line runs a small JS snippet to return the location to Python
location_data = streamlit_js_eval(
    js_expressions="navigator.geolocation.getCurrentPosition(pos => { "
                   "window.parent.postMessage({type: 'streamlit:setComponentValue', "
                   "value: {lat: pos.coords.latitude, lon: pos.coords.longitude}}, '*'); });",
    key="get_location"
)

# Print the values in Python if they exist
if location_data:
    st.subheader("Python Output")
    col1, col2 = st.columns(2)
    col1.metric("Latitude", location_data['lat'])
    col2.metric("Longitude", location_data['lon'])
else:
    st.info("Waiting for GPS permission/signal...")

# Display the map
show_live_map()
