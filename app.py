import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import requests
from PIL import Image
import os
from log import log_event, get_last_events
from database import init_db, insert_reading, fetch_all_readings

# === Pokreni bazu ===
init_db()

# === Putanje do slika ===
image_paths = {
    "monkey": "split_images/monkey.jpg.webp",
    "deer": "split_images/deer.jpg",
    "boar": "split_images/boar.jpg"
}

sun_image_path = "split_images/sun.jpg"
cloud_image_path = "split_images/sun-cloud.jpg.webp"
field_image_path = "split_images/rice_field.png"

# === Učitaj trenutno aktivnu životinju iz animal.txt ===
def get_current_animal():
    if os.path.exists("animal.txt"):
        with open("animal.txt", "r") as f:
            animal = f.read().strip()
            return animal if animal in image_paths else "deer"
    return "deer"

# === Učitaj sliku bez greške ===
def load_image(path):
    try:
        return Image.open(path)
    except:
        return None

# === Dohvati vremensku prognozu (OpenWeather) ===
def get_weather(city="Perth"):
    try:
        api_key = st.secrets["weather_api_key"]
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        current_temp = res["list"][0]["main"]["temp"]
        current_desc = res["list"][0]["weather"][0]["main"].lower()
        forecast = [(res["list"][i]["dt_txt"], res["list"][i]["main"]["temp"]) for i in range(1, 6, 2)]
        return current_temp, current_desc, forecast
    except Exception:
        return None, "unavailable", []

# === UI početak ===
st.set_page_config(page_title="Digital Twin - Smart Farm", layout="centered")
st.title("🌾 Digital Twin – Smart Farm Dashboard")

# === Inicijalizuj stanje ako ne postoji ===
if "view" not in st.session_state:
    st.session_state.view = "home"
if "settings_tab" not in st.session_state:
    st.session_state.settings_tab = ""

# === TABOVI ===
tab1, tab2 = st.tabs(["🏠 Home", "⚙️ Settings Info"])

# === TAB 1: HOME ===
with tab1:
    if st.session_state.view == "home":
        st.markdown("### Click an icon for more information:")
        current_temp, current_desc, _ = get_weather("Perth")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(load_image(sun_image_path))
            st.metric("Temperature", f"{current_temp} °C" if current_temp else "N/A")
            if st.button("Weather Info"):
                st.session_state.view = "weather"

        with col2:
            st.image(load_image(field_image_path))
            st.success("Soil moisture is normal")
            if st.button("Soil Moisture"):
                st.session_state.view = "moisture"

        with col3:
            current_animal = get_current_animal()
            animal_image = load_image(image_paths.get(current_animal))
            st.image(animal_image)
            st.info(f"Animal detected: {current_animal.capitalize()}")
            if st.button("Animal Presence"):
                st.session_state.view = "animals"

    elif st.session_state.view == "weather":
        current_temp, current_desc, forecast = get_weather("Perth")
        st.image(load_image(cloud_image_path))
        st.info(f"Current: {current_temp} °C, {current_desc.capitalize()}")
        st.write("### Forecast")
        for time, temp in forecast:
            st.write(f"{time}: {temp} °C")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    elif st.session_state.view == "moisture":
        st.image(load_image(field_image_path))
        st.warning("⚠️ Soil moisture low. Irrigation needed.")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

    elif st.session_state.view == "animals":
        current_animal = get_current_animal()
        st.image(load_image(image_paths.get(current_animal)))
        st.success(f"Animal detected: {current_animal.capitalize()}")
        if st.button("⬅️ Back"):
            st.session_state.view = "home"

# === TAB 2: SETTINGS ===
with tab2:
    current_temp, current_desc, _ = get_weather("Perth")
    st.sidebar.title("🌤️ Current Weather")
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
