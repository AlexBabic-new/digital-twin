from cryptography.fernet import Fernet

# Učitaj ključ
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Učitaj enkriptovani fajl
with open("events_encrypted.log", "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()

# Dekriptuj
decrypted_data = cipher.decrypt(encrypted_data)

# Sačuvaj dekriptovani fajl (opciono)
with open("events_decrypted.log", "wb") as decrypted_file:
    decrypted_file.write(decrypted_data)

print("✅ Decryption complete. Saved as 'events_decrypted.log'")
