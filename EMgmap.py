import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval # Added this

# Page Config
st.set_page_config(page_title="Live GPS Tracker", page_icon="📍")

def show_live_map():
    # ... [Your existing html_code remains exactly the same] ...
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            #map { height: 500px; width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            body { font-family: sans-serif; }
            #status-bar { background: #f0f2f6; padding: 10px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; display: flex; justify-content: space-between; }
        </style>
    </head>
    <body>
    <div id="status-bar">
        <span><b>GPS Status:</b> <span id="msg">Initializing...</span></span>
        <span id="coords">0.00, 0.00</span>
    </div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map, marker, circle;
        var firstLoad = true;
        function updatePosition() {
            if (!navigator.geolocation) return;
            navigator.geolocation.getCurrentPosition((position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                document.getElementById("msg").innerHTML = "Live Tracking Active";
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
            }, (error) => {}, { enableHighAccuracy: true });
        }
        updatePosition();
        setInterval(updatePosition, 5000);
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

# --- Main App ---
st.title("🛰️ Live Locator")

# NEW: Fetch location directly into Python
loc = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(pos => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: pos.coords.latitude + ',' + pos.coords.longitude}, '*'); });", key='get_loc')

if loc:
    lat_py, lon_py = loc.split(",")
    st.success(f"**Python Received:** Latitude: {lat_py}, Longitude: {lon_py}")
else:
    st.warning("Awaiting GPS coordinates for Python module...")

st.markdown("""
    This module fetches your browser's GPS coordinates and updates your position 
    on the map every **5 seconds**. 
""")

# Display the map
show_live_map()

st.divider()
st.caption("Developed for Smart Parking System | Powered by Leaflet.js")
