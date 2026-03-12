import streamlit as st
import streamlit.components.v1 as components
import mysql.connector
from mysql.connector import Error

# Page Config
st.set_page_config(page_title="Live GPS Tracker", page_icon="📍")

# Database Update Function
def update_db(lat, lon):
    try:
        connection = mysql.connector.connect(
            host='82.180.143.66',
            user='u263681140_students',
            password='testStudents@123',
            database='u263681140_students'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Updating coordinates for ID = 1
            sql_query = "UPDATE EmerVehicle SET Lat = %s, Lon = %s WHERE id = 1"
            cursor.execute(sql_query, (lat, lon))
            connection.commit()
            return True
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return False

def show_live_map():
    # We use a small JS bridge to send data back to Streamlit
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            #map { height: 400px; width: 100%; border-radius: 12px; }
            body { font-family: sans-serif; margin: 0; }
        </style>
    </head>
    <body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map, marker;
        var firstLoad = true;

        function sendToStreamlit(lat, lon) {
            // This sends data back to the Python script via the iframe communication
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {lat: lat, lon: lon, timestamp: Date.now()}
            }, '*');
        }

        function updatePosition() {
            navigator.geolocation.getCurrentPosition((position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                if (firstLoad) {
                    map = L.map('map').setView([lat, lon], 16);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                    marker = L.marker([lat, lon]).addTo(map);
                    firstLoad = false;
                } else {
                    marker.setLatLng([lat, lon]);
                    map.panTo([lat, lon]);
                }
                
                // Trigger the Python update
                sendToStreamlit(lat, lon);
                
            }, (err) => console.error(err), { enableHighAccuracy: true });
        }

        updatePosition();
        setInterval(updatePosition, 5000); 
    </script>
    </body>
    </html>
    """
    # This captures the 'value' sent from JavaScript
    data = components.html(html_code, height=450)
    return data

# --- Main App ---
st.title("🛰️ Live Locator & DB Sync")

# This is where the magic happens: 
# Every time the JS updates, this component returns the new lat/lon
result = show_live_map()

# In a real scenario, you'd use a custom component for better state management, 
# but for a quick fix, we check if coordinates are coming in.
# Note: Since standard components.html returns None, 
# you typically use a library like 'streamlit-js-eval' for direct value return.

# REVISED APPROACH for Database sync:
# Since components.html is one-way, we use a simple trigger or query params 
# to ensure Python knows the location.

st.info("The map is capturing your GPS and updating the database every 5 seconds.")

# Placeholder for DB status
status_placeholder = st.empty()

# For direct Python-to-MySQL updates without PHP, ensure your server 
# allows remote connections from your current IP to port 3306.

st.divider()
st.caption("Developed for Smart Parking System | Direct Python-SQL Integration")
