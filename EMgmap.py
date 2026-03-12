import streamlit as st
import streamlit.components.v1 as components
import json

# Page Config
st.set_page_config(page_title="Live GPS Tracker", page_icon="📍")

def show_live_map():
    # We use a unique key for the component to capture return values
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Location</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            #map { height: 500px; width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
            #status-bar { background: #f0f2f6; padding: 10px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; color: #31333F; display: flex; justify-content: space-between; }
            .loading-pulse { height: 10px; width: 10px; background: #ff4b4b; border-radius: 50%; display: inline-block; animation: pulse 1.5s infinite; }
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
            }
        </style>
    </head>
    <body>
    <div id="status-bar">
        <span><span class="loading-pulse"></span> <b>GPS Status:</b> <span id="msg">Initializing...</span></span>
        <span id="coords">0.00, 0.00</span>
    </div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <script>
        var map, marker, circle;
        var firstLoad = true;

        function updatePosition() {
            if (!navigator.geolocation) {
                document.getElementById("msg").innerHTML = "Not supported by browser";
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const accuracy = position.coords.accuracy;

                    document.getElementById("msg").innerHTML = "Live Tracking Active";
                    document.getElementById("coords").innerHTML = lat.toFixed(5) + ", " + lon.toFixed(5);

                    // --- NEW: SEND DATA TO PYTHON ---
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: {lat: lat, lon: lon}
                    }, '*');
                    // --------------------------------

                    if (firstLoad) {
                        map = L.map('map').setView([lat, lon], 16);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            attribution: '© OpenStreetMap contributors'
                        }).addTo(map);
                        marker = L.marker([lat, lon]).addTo(map).bindPopup("<b>You are here</b>").openPopup();
                        circle = L.circle([lat, lon], { radius: accuracy, color: '#007bff', fillOpacity: 0.1 }).addTo(map);
                        firstLoad = false;
                    } else {
                        marker.setLatLng([lat, lon]);
                        circle.setLatLng([lat, lon]);
                        circle.setRadius(accuracy);
                        map.panTo([lat, lon]);
                    }
                },
                (error) => { document.getElementById("msg").innerHTML = "Error: " + error.message; },
                { enableHighAccuracy: true }
            );
        }
        updatePosition();
        setInterval(updatePosition, 5000);
    </script>
    </body>
    </html>
    """
    # We assign the return value of the component to a variable
    return components.html(html_code, height=600)

# --- Main App ---
st.title("🛰️ Live Locator")

# Display the map and capture the return value
data_from_js = show_live_map()

# Print the coordinates using Python
if data_from_js:
    st.subheader("Python Output")
    col1, col2 = st.columns(2)
    col1.metric("Latitude", data_from_js['lat'])
    col2.metric("Longitude", data_from_js['lon'])
    
    # Standard print for console/logs
    print(f"Python captured: Lat {data_from_js['lat']}, Lon {data_from_js['lon']}")

st.markdown("""
    This module fetches your browser's GPS coordinates and updates your position 
    on the map every **5 seconds**. 
""")

with st.expander("ℹ️ Troubleshooting"):
    st.write("1. Ensure you are using **HTTPS** or **localhost**.")
    st.write("2. Click 'Allow' when the browser asks for Location permissions.")

st.divider()
st.caption("Developed for Smart Parking System | Powered by Leaflet.js")
