from datetime import datetime

LOG_FILE = "events.log"

def log_event(event: str):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")

def get_last_events(n=5):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        return lines[-n:] if len(lines) >= n else lines
    except FileNotFoundError:
        return []
