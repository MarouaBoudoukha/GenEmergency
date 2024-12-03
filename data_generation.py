import requests
import time
import random

# Server configuration
SERVER_URL = "http://localhost:5001/api/data"  # Replace with your server's URL

# Types d'urgences disponibles
TYPES_URGENCE = [
    "accident_de_voiture",
    "accident_randonnee",
    "chute_personnes_agees",
    "incendie"
]

# Function to simulate heart rate and car velocity
def generate_data():
    # Simulate normal heart rate (60–100 bpm) with occasional very low BPM (30–50 bpm)
    if random.random() < 0.1:  # 10% chance for very low BPM
        heart_rate = random.randint(30, 50)
    else:
        heart_rate = random.randint(60, 100)

    # Simulate car velocity (0–120 km/h)
    car_velocity = round(random.uniform(0, 120), 2)

    # Sélection aléatoire d'un type d'urgence
    type_urgence = random.choices(
        TYPES_URGENCE,
        weights=[0.4, 0.3, 0.2, 0.1],  # Ajustez les probabilités selon vos besoins
        k=1
    )[0]

    # Générer des coordonnées aléatoires (par exemple, autour de Paris)
    latitude = round(random.uniform(48.80, 48.90), 6)
    longitude = round(random.uniform(2.30, 2.40), 6)

    return {
        "type_urgence": type_urgence,
        "heart_rate": heart_rate,
        "car_velocity": car_velocity,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    }

# Function to send data to the server
def send_data(data):
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
            # Afficher la réponse du serveur
            print(f"Réponse du serveur : {response.json()}")
        else:
            print(f"Failed to send data: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

# Main loop to send data continually
def main():
    interval = 2  # Interval between sending data (in seconds)
    print("Starting heart rate and car velocity sender... Press Ctrl+C to stop.")

    try:
        while True:
            data = generate_data()
            print(f"Envoi des données : {data}")  # Ajouté pour débogage
            send_data(data)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nData sender stopped.")

if __name__ == "__main__":
    main()
