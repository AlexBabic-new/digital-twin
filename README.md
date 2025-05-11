# 🌾 Bhutan Digital Twin – Smart Farming Dashboard

This project is a simulated digital twin system for monitoring rice field conditions, designed as a prototype for future IoT integration. It includes a Streamlit-based dashboard, image-driven animal detection, and modular architecture for eventual connection to real sensors (e.g., via MQTT or LoRaWAN).


##  Project Structure

```plaintext
digital-twin/
├── app.py                  # Streamlit frontend dashboard
├── set_animal.py           # CLI script to simulate animal presence
├── animal.txt              # Control file used to reflect current animal
├── log.py                  # Event logging module
├── database.py             # SQLite storage for sensor readings
├── requirements.txt        # Python dependencies
├── split_images/           # Animal and environment image assets
│   ├── monkey.jpg.webp
│   ├── deer.jpg
│   └── boar.jpg
└── .streamlit/secrets.toml # Contains weather API key (if used)
```


##  Technologies Used

###  Currently used:
- **Streamlit** – interactive dashboard UI
- **Python** – logic and backend handling
- **Local image-based simulation** – for prototyping detection flow

###  Planned for integration:
- **Raspberry Pi + BME688 sensors**
- **LoRaWAN** – for long-range transmission
- **MQTT (Mosquitto)** – for real-time sensor messaging
- **Eclipse Ditto** – digital twin modeling
- **Fly.io or Streamlit Cloud** – for deployment


##  Animal Detection Logic (Updated: May 2025)

This prototype simulates animal presence on a farm using static image placeholders and a simple control file.

###  Features
- Dashboard loads animal images dynamically based on the value in `animal.txt`
- CLI script `set_animal.py` simulates detection (choose: Monkey, Deer, Boar)
- Automatically updates image in dashboard
- Compatible with future sensor-based triggers or AI models


##  How to Use the Simulation

### ▶ Step 1: Start the Dashboard

```bash
streamlit run app.py
```

### ▶ Step 2: Simulate Animal Detection

Open a second terminal and run:

```bash
python3 set_animal.py
# Enter one of: monkey, deer, boar
```

After a few seconds, the dashboard will refresh and display the selected animal image.


##  Future Enhancements

-  Replace `set_animal.py` with MQTT-based sensor input
-  Integrate AI model for real-time animal classification
-  Add Fly.io or Streamlit Cloud auto-deploy
-  Store detection events and timestamps in a structured database


##  How to Run Locally

```bash
git clone https://github.com/your-username/digital-twin.git
cd digital-twin
pip install -r requirements.txt
streamlit run app.py
```


##  Notes

- This project currently **does not connect to physical sensors**.
- The logic is structured to allow easy integration of sensor data in the next phase.
- It is intended for **demonstration and educational purposes**.


##  Created by Aleksandar Babić – May 2025
