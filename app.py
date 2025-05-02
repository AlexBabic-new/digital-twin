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
    except:
        return None

# === Initialize database ===
init_db()

# === Image URLs ===
sun_image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e0/SNice.svg"
snow_image_url = "https://upload.wikimedia.org/wikipedia/commons/9/9e/Snow_flake_icon.svg"
rain_image_url = "https://upload.wikimedia.org/wikipedia/commons/5/5b/Rain_icon.svg"
cloud_image_url = "https://upload.wikimedia.org/wikipedia/commons/7/75/Weather-few-clouds.svg"
monkey_image_url = "https://upload.wikimedia.org/wikipedia/commons/5/5f/Monkey_portrait_02.jpg"
deer_image_url = "https://upload.wikimedia.org/wikipedia/commons/3/34/White-tailed_deer.jpg"
boar_image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b7/Wild_boar_Bieszczady.jpg"
field_image_url = "https://upload.wikimedia.org/wikipedia/commons/1/1d/Wheat_field_2013.jpg"

# === Session state ===
if "view" not in st.session_state:
    st.session_state.view = "home"
if "settings_tab" not in st.session_state:
    st.session_state.settings_tab = ""

# === Tabs ===
tab1, tab2 = st.tabs(["🏡 Home", "⚙️ Settings Info"])

# === TAB 1: HOME ===
with tab1:
    st.title("🌾 Digital Twin - Smart Farm Dashboard")

    if st.session_state.view == "home":
        st.markdown("### Click an icon for more information:")
        current_temp, current_desc, _ = get_weather("Perth")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(sun_image_url)
            st.metric("Temperature", f"{current_temp} °C")
            if st.button("Weather Info"):
                st.session_state.view = "weather"

        with col2:
            st.image(field_image_url)
            st.success("Soil moisture is normal")
            if st.button("Soil Moisture"):
                st.session_state.view = "moisture"

        with col3:
            st.image(monkey_image_url)
            st.info("No intruder detected")
            if st.button("Animal Presence"):
                st.session_state.view = "animals"

    elif st.session_state.view == "weather":
        current_temp, current_desc, forecast = get_weather("Perth")
        st.image(cloud_image_url)
        st.info(f"Current: {current_temp} °C, {current_desc.capitalize()}")
        st.write("### Forecast")
        for time, temp in forecast:
            st.write(f"{time}: {temp} °C")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    elif st.session_state.view == "moisture":
        st.image(field_image_url)
        st.warning("⚠️ Soil moisture low. Irrigation needed.")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    elif st.session_state.view == "animals":
        st.image(deer_image_url)
        st.success("Animal detected at 07:00 - Deer")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

# === TAB 2: SETTINGS ===
with tab2:
    current_temp, current_desc, _ = get_weather("Perth")
    st.sidebar.title("🌦️ Current Weather")
    if current_temp:
        st.sidebar.write(f"{current_temp} °C, {current_desc.capitalize()}")

    selection = st.radio("Select Data View", ["Temperature", "Humidity", "pH", "Soil Quality", "Logs"])
    st.session_state.settings_tab = selection

    data = fetch_all_readings()
    df = pd.DataFrame(data, columns=["ID", "Timestamp", "Temperature (°C)", "Humidity (%)", "pH"])

    if selection == "Temperature" and not df.empty:
        st.subheader("🌡️ Temperature Overview")
        st.line_chart(df.set_index("Timestamp")["Temperature (°C)"])

    elif selection == "Humidity" and not df.empty:
        st.subheader("💧 Humidity Overview")
        st.line_chart(df.set_index("Timestamp")["Humidity (%)"])

    elif selection == "pH" and not df.empty:
        st.subheader("🧪 pH Values")
        st.line_chart(df.set_index("Timestamp")["pH"])

    elif selection == "Soil Quality":
        st.subheader("🌱 Soil Quality Info")
        st.info("(Placeholder for future implementation of soil quality assessments)")

    elif selection == "Logs":
        st.subheader("📜 Event Logs")
        logs = get_last_events()
        for log in logs:
            st.text(log)

    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.session_state.view = "home"
