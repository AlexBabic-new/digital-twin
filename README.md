# 🌾 Bhutan Digital Twin – Smart Farming Dashboard

This project is a real-time digital twin system for monitoring rice field conditions using sensor data and cloud visualization. It includes Streamlit dashboard, Raspberry Pi devices, LoRaWAN, MQTT communication, and Eclipse Ditto integration.

---

## 📦 Project Structure

- `app.py` – Streamlit frontend for dashboard
- `database.py` – SQLite storage for sensor data
- `log.py` – Event logging module
- `requirements.txt` – Python dependencies
- `Dockerfile` – Optional Docker deployment (for Fly.io)
- `.streamlit/secrets.toml` – Weather API keys
- `README.md` – You're here!

---

## 📡 Technologies Used

- Raspberry Pi + BME688 sensors
- LoRaWAN for long-range data transfer
- MQTT protocol (Mosquitto broker)
- Eclipse Ditto for digital twin model
- Streamlit for web dashboard
- Fly.io for cloud deployment

---
## 🐾 Animal Detection Logic (Updated: May 2025)

This project simulates animal presence detection on a smart farm using images and a control file (`animal.txt`).

### ✅ Features
- The dashboard UI is fully interactive with tabs and metrics.
- Animal image is dynamically loaded based on the value inside `animal.txt`.
- Script `set_animal.py` allows you to manually simulate animal detection (Monkey, Deer, Boar).
- Animal images are stored in the `split_images/` directory.
- Fully compatible with future sensor input integration (e.g., via MQTT).

### 🚀 Example Usage

```bash
# Run the main Streamlit dashboard
streamlit run app.py

# In a separate terminal, run the script and input desired animal
python3 set_animal.py
# Enter: monkey


## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/digital-twin.git
cd digital-twin
pip install -r requirements.txt
streamlit run app.py
