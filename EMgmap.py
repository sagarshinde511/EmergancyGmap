import streamlit as st
import streamlit.components.v1 as components

def get_location():
    # JavaScript to fetch coordinates and send them to Streamlit
    js_code = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            // Send data back to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {lat: lat, lon: lon}
            }, '*');
        },
        (error) => {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {error: error.message}
            }, '*');
        }
    );
    </script>
    """
    # Use a small height so it doesn't take up space
    return components.html(js_code, height=0)

st.title("📍 Real-time Geolocation")

if st.button("Get My Location"):
    location_data = get_location()
    st.info("Requesting permission...")

# This listener catches the 'value' sent from the JS postMessage
# Note: In a real app, you might use a custom component for better state management
