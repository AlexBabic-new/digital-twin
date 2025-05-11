# set_animal.py

animal = input("Enter animal name (monkey / deer / boar): ").strip().lower()

if animal not in ["monkey", "deer", "boar"]:
    print("❌ Invalid input. Allowed values: monkey, deer, boar")
else:
    with open("animal.txt", "w") as file:
        file.write(animal)
    print(f"✅ Animal set to: {animal.capitalize()}")
