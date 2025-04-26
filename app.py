import streamlit as st
import pandas as pd
from datetime import datetime
from log import log_event, get_last_events
from database import init_db, insert_reading, fetch_all_readings
import matplotlib.pyplot as plt
import requests

# === Weather Function ===
def get_weather(city="Perth"): 
    try:
        api_key = st.secrets["weather_api_key"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"].capitalize()
        return f"{city}: {temp}°C, {desc}"
    except Exception as e:
        return f"Could not fetch weather data: {e}"

# === Initialize database ===
init_db()

# === Sidebar Weather ===
st.sidebar.markdown("☁️ **Current Weather**")
st.sidebar.write(get_weather("Perth"))

# === Load initial data from DB ===
data = fetch_all_readings()
df = pd.DataFrame(data, columns=["ID", "Timestamp", "Temperature (°C)", "Humidity (%)", "pH"])

# === Tabs layout ===
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📜 Logs", "📈 Graphs"])

# === TAB 1: Dashboard ===
with tab1:
    st.subheader("📥 Enter Sensor Data")

    with st.form("sensor_input_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            temperature_input = st.number_input("🌡️ Temperature (°C)", min_value=-50.0, max_value=100.0, value=22.4, step=0.1)
        with col2:
            humidity_input = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        with col3:
            ph_input = st.number_input("🧪 pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)

        submitted = st.form_submit_button("📩 Submit")

    if submitted:
        insert_reading(temperature_input, humidity_input, ph_input)
        log_event(f"Manual input: T={temperature_input}, H={humidity_input}, pH={ph_input}")
        st.success("Sensor data submitted and logged!")
        st.experimental_rerun()

    # Refresh data after submission
    data = fetch_all_readings()
    df = pd.DataFrame(data, columns=["ID", "Timestamp", "Temperature (°C)", "Humidity (%)", "pH"])
    
    # === ALERT SYSTEM BASED ON LAST ENTRY ===
        if not df.empty:
    latest = df.iloc[-1]  # poslednji unos

    temp = latest["Temperature (°C)"]
    humidity = latest["Humidity (%)"]
    ph = latest["pH"]

    if temp > 40:
        st.error(f"🔥 ALERT: Temperature is too high! ({temp}°C)")
    if humidity < 30:
        st.info(f"💧 Low humidity detected: {humidity}%")
    if ph < 5:
        st.warning(f"🧪 Warning: pH is too low! ({ph})")

    st.subheader("📦 Sensor Data Table")
    st.dataframe(df)

    st.subheader("📥 Export Sensor Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="sensor_data.csv",
        mime="text/csv"
    )

# === TAB 2: Logs ===
with tab2:
    st.subheader("🔔 Simulate Event")
    if st.button("Log Simulated Event"):
        log_event("Simulated sensor event")
        st.success("Event logged successfully!")

    st.subheader("📜 Recent Log Events")
    last_logs = get_last_events()
    for line in last_logs:
        st.text(line.strip())

# === TAB 3: Graphs ===
with tab3:
    st.subheader("📈 Temperature Over Time")

    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df["Timestamp"], df["Temperature (°C)"], marker='o', color='tomato')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature Trend")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    else:
        st.info("No data to plot yet.")
            
    st.subheader("📉 Humidity Over Time")

    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df["Timestamp"], df["Humidity (%)"], marker='o', color='skyblue')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Humidity (%)")
        ax.set_title("Humidity Trend")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    else:
        st.info("No humidity data to plot yet.")

