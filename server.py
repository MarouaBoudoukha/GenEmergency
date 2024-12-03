from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

latitude = 0.0
longitude = 0.0
heart_rate = 0

# Endpoint to get the location of a phone # Another endpoint with parameters
@app.route('/locate/<phone>', methods=['GET'])
def greet(phone):
    client_id = 'ZzY7UmVlAntH292fkTk4LXBJt9buTd3z'
    client_secret = 'anhlnJYM6CAEs27uma7DXtz3TMsoUXaHEQBbQmJUEAvc'
    scope = "" # Scope for the API (can be empty)
    response = call_api(get_access_token(client_id,client_secret,""), phone)
    return response

# Function to obtain an OAuth access token
def get_access_token(client_id, client_secret, scope):
    token_url = 'https://api.orange.com/oauth/v3/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()
    access_token = response_data.get('access_token')
    return response_data['access_token']

# Function to call the location API with the access token and phone number
def call_api(access_token, phone_number):
    api_url = 'https://api.orange.com/camara/location-retrieval/orange-lab/v0/retrieve'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-correlator': 'your_correlator'
    }
    data = {
        "device": {
            "phoneNumber": phone_number # Phone number to locate
        },
        "maxAge": 60 # Maximum age of the location data
    }
    response = requests.post(api_url, headers=headers, json=data) # POST request to get the location
    return response.json()

@app.route('/api/data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    global heart_rate
    global latitude
    global longitude

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Log the received heart rate # Log the received data
    heart_rate = data.get('heart_rate')
    
    if heart_rate < 40:
        response = requests.get("http://localhost:5001/locate/+33699901032").json()
        latitude = response['area']['center']['latitude']
        longitude = response['area']['center']['longitude']
        print(response)

    return jsonify({"message": "Data received successfully"}),  200

@app.route('/position')
def position():
    return jsonify({'latitude': latitude, 'longitude': longitude})

@app.route('/heart')
def heart():
    return {'heart': heart_rate}

if __name__ == "__main__":
    # Run the server on localhost at port 5001 # Run the server on localhost at port 5000
    app.run(host="0.0.0.0", port=5001)