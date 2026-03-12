import streamlit as st
import streamlit.components.v1 as components

def show_current_location_map():
    # Simple Leaflet implementation to show ONLY current location
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map { height: 500px; width: 100%; border-radius: 10px; }
        body { font-family: sans-serif; margin: 0; }
    </style>
    </head>
    <body>
    <p id="status" style="padding: 10px;">📡 Detecting your location...</p>
    <div id="map"></div>

    <script>
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          const lat = position.coords.latitude;
          const lon = position.coords.longitude;

          document.getElementById("status").innerHTML = "📍 <b>Current Location:</b> " + lat.toFixed(5) + ", " + lon.toFixed(5);

          var map = L.map('map').setView([lat, lon], 16);

          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap'
          }).addTo(map);

          // Add a marker for the current location
          L.marker([lat, lon]).addTo(map)
            .bindPopup('You are here')
            .openPopup();
        },
        function(error) {
          document.getElementById("status").innerHTML = "❌ Error: " + error.message;
        }
      );
    } else {
      document.getElementById("status").innerHTML = "❌ Geolocation not supported by this browser";
    }
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

# Streamlit App UI
st.title("📍 Current Location Map")
st.write("This map will pinpoint your exact location once permissions are granted.")

show_current_location_map()
