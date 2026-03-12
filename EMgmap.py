import streamlit as st
import streamlit.components.v1 as components

def show_road_route_map():
    # Leaflet and Leaflet Routing Machine implementation
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js"></script>
    <style>
        #map { height: 500px; width: 100%; border-radius: 10px; }
        body { font-family: sans-serif; }
    </style>
    </head>
    <body>
    <p id="status">📡 Requesting GPS access...</p>
    <div id="map"></div>

    <script>
    const destination = [16.704987, 74.243252]; // Kolhapur Bus Stand

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          const userLat = position.coords.latitude;
          const userLon = position.coords.longitude;

          document.getElementById("status").innerHTML = 
            "<b>Route Found:</b> From your location to Kolhapur Bus Stand";

          var map = L.map('map').setView(destination, 13);

          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
          }).addTo(map);

          // Routing logic
          L.Routing.control({
            waypoints: [
              L.latLng(userLat, userLon),
              L.latLng(destination[0], destination[1])
            ],
            routeWhileDragging: false,
            addWaypoints: false,
            show: true // Set to true to see turn-by-turn directions
          }).addTo(map);
        },
        function(error) {
          document.getElementById("status").innerHTML = "❌ Error: " + error.message;
        }
      );
    } else {
      document.getElementById("status").innerHTML = "❌ Geolocation not supported";
    }
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

# Streamlit UI
st.title("📍 Real-time Navigation")
st.info("Allow browser location permissions to see the route.")

if st.button("Reload Map"):
    st.rerun()

show_road_route_map()
