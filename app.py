import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from log import log_event, get_last_events
from database import init_db, insert_reading, fetch_all_readings

# === Fetch weather data from OpenWeather API ===
def get_weather(city="Perth"):
    try:
        api_key = st.secrets["weather_api_key"]
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        current_temp = res["list"][0]["main"]["temp"]
        current_desc = res["list"][0]["weather"][0]["main"].lower()
        forecast = [(res["list"][i]["dt_txt"], res["list"][i]["main"]["temp"]) for i in range(1, 6, 2)]
        return current_temp, current_desc, forecast
    except Exception as e:
        return None, "Weather data unavailable", []

# === Load an image from a URL safely ===
def load_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except UnidentifiedImageError:
        return None

# === Initialize database ===
init_db()

# === Image URLs for visualization (valid) ===
sun_image_url = "https://i.ibb.co/4W2DGKm/sun.png"
snow_image_url = "https://i.ibb.co/NK4fyH5/snow.png"
rain_image_url = "https://i.ibb.co/hKRcTzw/rain.png"
cloud_image_url = "https://i.ibb.co/mT1v2cJ/cloud.png"
animal_image_url = "https://i.ibb.co/yg3TTZF/animal.png"
field_image_url = "https://i.ibb.co/fMQKZFm/soil.png"

# === Session state setup ===
if "view" not in st.session_state:
    st.session_state.view = "home"
if "settings_tab" not in st.session_state:
    st.session_state.settings_tab = "Temperature"

# === Create two main tabs: Home and Settings Info ===
tab1, tab2 = st.tabs(["🏡 Home", "⚙️ Settings Info"])

# === TAB 1: Main Dashboard ===
with tab1:
    st.title("🌾 Digital Twin - Smart Farm Dashboard")

    # === HOME VIEW ===
    if st.session_state.view == "home":
        st.markdown("### Click an icon for more information:")
        current_temp, current_desc, _ = get_weather("Perth")

        col1, col2, col3 = st.columns(3)

        with col1:
            img = load_image(cloud_image_url)
            if img:
                st.image(img, use_column_width=True)
            st.metric(label="🌡️ Temperature", value=f"{current_temp} °C")
            if st.button("Weather Info"):
                st.session_state.view = "weather"

        with col2:
            img = load_image(field_image_url)
            if img:
                st.image(img, use_column_width=True)
            st.success("✅ Soil moisture is normal")
            if st.button("Soil Moisture"):
                st.session_state.view = "moisture"

        with col3:
            img = load_image(animal_image_url)
            if img:
                st.image(img, use_column_width=True)
            st.info("🟢 No intruder detected")
            if st.button("Animal Presence"):
                st.session_state.view = "animals"

    # === WEATHER DETAIL VIEW ===
    elif st.session_state.view == "weather":
        current_temp, current_desc, forecast = get_weather("Perth")
        if current_temp is not None:
            if current_temp < 10:
                img = load_image(snow_image_url)
            elif "rain" in current_desc:
                img = load_image(rain_image_url)
            elif "cloud" in current_desc:
                img = load_image(cloud_image_url)
            else:
                img = load_image(sun_image_url)
            if img:
                st.image(img)
            st.info(f"Current: {current_temp} °C, {current_desc.capitalize()}")
            st.write("### Forecast:")
            for time, temp in forecast:
                st.write(f"{time}: {temp} °C")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    # === MOISTURE DETAIL VIEW ===
    elif st.session_state.view == "moisture":
        img = load_image(field_image_url)
        if img:
            st.image(img)
        st.warning("⚠️ Soil moisture low. Irrigation required.")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    # === ANIMAL DETAIL VIEW ===
    elif st.session_state.view == "animals":
        img = load_image(animal_image_url)
        if img:
            st.image(img)
        st.success("Animal detected at 07:00 - Animal 2")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

# === TAB 2: Settings Info ===
with tab2:
    st.sidebar.title("🌦️ Current Weather")
    current_temp, current_desc, _ = get_weather("Perth")
    if current_temp is not None:
        st.sidebar.write(f"{current_temp} °C, {current_desc.capitalize()}")
    else:
        st.sidebar.warning("Weather data unavailable.")

    tabs = st.radio("Select Data View", ["Temperature", "Humidity", "pH", "Soil Quality", "Logs"])

    data = fetch_all_readings()
    df = pd.DataFrame(data, columns=["ID", "Timestamp", "Temperature (°C)", "Humidity (%)", "pH"])

    if tabs == "Temperature" and not df.empty:
        st.subheader("🌡️ Temperature Overview")
        st.line_chart(df.set_index("Timestamp")["Temperature (°C)"])

    elif tabs == "Humidity" and not df.empty:
        st.subheader("💧 Humidity Overview")
        st.line_chart(df.set_index("Timestamp")["Humidity (%)"])

    elif tabs == "pH" and not df.empty:
        st.subheader("🧪 pH Values")
        st.line_chart(df.set_index("Timestamp")["pH"])

    elif tabs == "Soil Quality":
        st.subheader("🌱 Soil Quality Info")
        st.info("(Placeholder for future implementation of soil quality assessments)")

    elif tabs == "Logs":
        st.subheader("📜 Event Logs")
        logs = get_last_events()
        for log in logs:
            st.text(log)

    if st.button("⬅️ Back to Home"):
        st.session_state.view = "home"
        st.experimental_rerun()