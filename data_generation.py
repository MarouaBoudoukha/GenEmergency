import requests
import time
import random

# Server configuration
SERVER_URL = "http://localhost:5001/api/data"  # Replace with your server's URL

isAttack = False

# Function to simulate heart rate and car velocity
def generate_data():
    global isAttack  # Declare isAttack as a global variable
    # Simulate normal heart rate (60–100 bpm) with occasional very low BPM (30–50 bpm)
    if isAttack or random.random() < 0.1:  # 10% chance for very low BPM
        heart_rate = random.randint(10, 40)
        isAttack = True
    else:
        heart_rate = random.randint(60, 100)
    
    # Simulate car velocity (0–120 km/h)
    car_velocity = round(random.uniform(0, 120), 2)
    
    return {
        "heart_rate": heart_rate
    }

# Function to send data to the server
def send_data(data):
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
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
            send_data(data)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nData sender stopped.")

if __name__ == "__main__":
    main()
