from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Endpoint to receive data
@app.route('/api/data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Log the received heart rate # Log the received data
    heart_rate = data.get('heart_rate')
    print(f"Heart rate: {heart_rate}")
    
    #print(f"Heart rate: {data.get('heart_rate')}, Car velocity: {data.get('car_velocity')}")
    #if data.get('heart_rate') < 50: #or data.get('car_velocity') == 0:
    if heart_rate < 50:
        print(requests.get("http://127.0.0.1:5004/locate/+33699901032").json())

    # Return a success response
    return jsonify({"message": "Data received successfully"}), 200

if __name__ == "__main__":
    # Run the server on localhost at port 5001 # Run the server on localhost at port 5000
    app.run(host="0.0.0.0", port=5001)
