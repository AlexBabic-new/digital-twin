import sqlite3
from datetime import datetime

DB_NAME = "sensor_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS readings (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT,
                 temperature REAL,
                 humidity REAL,
                 ph REAL
             )''')
    conn.commit()
    conn.close()

def insert_reading(temperature, humidity, ph):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO readings (timestamp, temperature, humidity, ph) VALUES (?, ?, ?, ?)", 
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity, ph))
    conn.commit()
    conn.close()

def fetch_all_readings():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
