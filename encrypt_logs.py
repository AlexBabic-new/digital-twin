from cryptography.fernet import Fernet

# Ako već postoji ključ, koristi ga. Ako ne, kreiraj i sačuvaj novi
key_path = "secret.key"

try:
    with open(key_path, "rb") as key_file:
        key = key_file.read()
        print("🔑 Key loaded from file.")
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print("🔐 New key generated and saved to 'secret.key'.")

cipher = Fernet(key)

# Učitaj sadržaj fajla i enkriptuj
with open("events.log", "rb") as log_file:
    log_data = log_file.read()
    encrypted_data = cipher.encrypt(log_data)

# Sačuvaj enkriptovani fajl
with open("events_encrypted.log", "wb") as encrypted_file:
    encrypted_file.write(encrypted_data)

print("✅ Encrypted log saved as 'events_encrypted.log'")
