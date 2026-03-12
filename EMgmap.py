import streamlit as st
import streamlit.components.v1 as components
import mysql.connector

# ================= DATABASE CONFIG =================
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students"
}

def update_db_location(lat, lon):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Updating row with id=1 (Emergency Vehicle)
        query = "UPDATE EmerVehicle SET Lat = %s, Lon = %s WHERE id = 1"
        cursor.execute(query, (str(lat), str(lon)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"DB Error: {e}")
        return False

# ================= UI & LOGIC =================
st.title("🚑 Emergency Vehicle Tracker")

# 1. This hidden component executes JS and sends data back to Streamlit
# We use a unique key to prevent unnecessary re-renders
location_data = components.html(
    """
    <script>
    function sendLocation() {
        navigator.geolocation.getCurrentPosition((pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            
            // Send data to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {lat: lat, lon: lon, timestamp: Date.now()}
            }, '*');
        });
    }

    // Initial send
    sendLocation();
    // Repeat every 5 seconds
    setInterval(sendLocation, 5000);
    </script>
    """,
    height=0,
)

# 2. Capture data from the JavaScript "postMessage"
# Note: In standard Streamlit, we check query params or session state for the return value
# For this specific implementation, we'll use a listener approach or a button-less update

if "last_lat" not in st.session_state:
    st.session_state.last_lat = None

# Using a placeholder to show status
status_placeholder = st.empty()

# For a seamless update, we can use a query param trick or a simple button 
# But for 'auto' update without refreshing UI, we use the following:

st.info("The system is tracking your location and updating the 'EmerVehicle' table every 5 seconds.")

# Logic to handle the incoming JS data
# Since components.html doesn't return values directly to variables easily, 
# we often use a small custom component or streamlit-js-eval.
# Here is the robust version using streamlit-js-eval:

from streamlit_js_eval import streamlit_js_eval

loc = streamlit_js_eval(
    js_expressions="done(navigator.geolocation.getCurrentPosition(pos => done({lat:pos.coords.latitude, lon:pos.coords.longitude})))",
    key="track",
    want_output=True
)

if loc:
    lat, lon = loc['lat'], loc['lon']
    success = update_db_location(lat, lon)
    if success:
        status_placeholder.success(f"✅ Database Updated: Lat {lat}, Lon {lon}")
    
    # Simple Map Display
    st.map({
        'latitude': [float(lat)],
        'longitude': [float(lon)]
    })

# Auto-refresh the Streamlit script to catch the next JS interval
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="db_update_timer")
