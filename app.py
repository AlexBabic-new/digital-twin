import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from log import log_event, get_last_events
from database import init_db, insert_reading, fetch_all_readings

# === Fetch weather data from OpenWeather API ===
def get_weather(city="Perth"):
    try:
        api_key = st.secrets["weather_api_key"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        temp = res["main"]["temp"]
        desc = res["weather"][0]["main"].lower()
        return temp, desc
    except Exception as e:
        return None, "Weather data unavailable"

# === Load an image from a URL ===
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# === Initialize database ===
init_db()

# === Image URLs for visualization ===
sun_image_url = "https://i.imgur.com/V7xQwOw.png"
snow_image_url = "https://i.imgur.com/Nz5X28P.png"
rain_image_url = "https://i.imgur.com/N6Z8X4h.png"
cloud_image_url = "https://i.imgur.com/hKnpvK2.png"
animal_image_url = "https://i.imgur.com/64lAFmE.png"
field_image_url = "https://i.imgur.com/PGqQ8td.png"

# === Create two main tabs: Home and Settings Info ===
tab1, tab2 = st.tabs(["🏡 Home", "⚙️ Settings Info"])

# === TAB 1: Home (Clickable dashboard icons) ===
with tab1:
    st.title("🌾 Digital Twin - Smart Farm Dashboard")
    st.markdown("### Click an icon for more information:")

    current_temp, current_desc = get_weather("Perth")

    col1, col2, col3 = st.columns(3)

    # Weather Icon
    with col1:
        if st.button("🌤️ Weather Info"):
            if current_temp is not None:
                if current_temp < 10:
                    img = load_image(snow_image_url)
                elif "rain" in current_desc:
                    img = load_image(rain_image_url)
                elif "cloud" in current_desc:
                    img = load_image(cloud_image_url)
                else:
                    img = load_image(sun_image_url)
                st.image(img, caption=f"{current_temp} °C, {current_desc.capitalize()}")
                st.info(f"Temperature: {current_temp} °C | Condition: {current_desc.capitalize()}")
                if st.button("⬅️ Back", key="weather_back"):
                    st.experimental_rerun()

    # Soil Moisture Icon
    with col2:
        if st.button("🌾 Soil Moisture"):
            img_field = load_image(field_image_url)
            st.image(img_field, caption="Soil Moisture Status")
            st.warning("⚠️ Soil moisture is decreasing. Irrigation recommended soon!")
            if st.button("⬅️ Back", key="field_back"):
                st.experimental_rerun()

    # Animal Detection Icon
    with col3:
        if st.button("🐾 Animal Presence"):
            img_animal = load_image(animal_image_url)
            st.image(img_animal, caption="Animal Detection")
            st.success("✅ Animal 1 at 07:00 | Animal 2 at 08:15")
            if st.button("⬅️ Back", key="animal_back"):
                st.experimental_rerun()

# === TAB 2: Settings Info (Original sensor dashboard) ===
with tab2:
    st.sidebar.title("🌦️ Current Weather")
    if current_temp is not None:
        st.sidebar.write(f"{current_temp} °C, {current_desc.capitalize()}")
    else:
        st.sidebar.warning("Weather data unavailable.")

    st.header("📈 Real-Time Sensor Dashboard")

    # Load sensor data from the database
    data = fetch_all_readings()
    df = pd.DataFrame(data, columns=["ID", "Timestamp", "Temperature (°C)", "Humidity (%)", "pH"])

    if not df.empty:
        latest = df.iloc[-1]
        temp = latest["Temperature (°C)"]
        humidity = latest["Humidity (%)"]
        ph = latest["pH"]

        # Alert users when readings are out of optimal range
        if temp < 10 or temp > 35:
            st.error(f"🔥 CRITICAL: Temperature out of range ({temp} °C)")
            st.toast(f"🔥 Temperature alert: {temp} °C")
        if humidity < 30 or humidity > 70:
            st.warning(f"⚠️ WARNING: Humidity out of range ({humidity}%)")
            st.toast(f"💧 Humidity alert: {humidity}%")
        if ph < 5.5 or ph > 7.5:
            st.info(f"ℹ️ INFO: pH slightly off the ideal range ({ph})")
            st.toast(f"🧪 pH alert: {ph}")

        st.dataframe(df)
    else:
        st.info("No sensor data available yet.")
