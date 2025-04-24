from datetime import datetime

HONEYPOT_TOKEN = "https://fakeurl.example.com/api/secret/ABCD1234XYZ"

def get_honeypot_token():
    return HONEYPOT_TOKEN

def log_honeypot_access(ip_address="Unknown IP"):
    with open("events.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🔐 Honeypot accessed from {ip_address}\n")
