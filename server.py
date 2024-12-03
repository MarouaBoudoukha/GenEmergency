from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Example endpoint that returns a simple message # Example endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

# Endpoint to get the location of a phone # Another endpoint with parameters
@app.route('/locate/<phone>', methods=['GET'])
def greet(phone):
    client_id = 'ZzY7UmVlAntH292fkTk4LXBJt9buTd3z'
    client_secret = 'anhlnJYM6CAEs27uma7DXtz3TMsoUXaHEQBbQmJUEAvc'
    scope = "" # Scope for the API (can be empty)
    return call_api(get_access_token(client_id,client_secret,""), phone)

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


# POST endpoint
# @app.route('/add', methods=['POST'])
# def add():
    # data = request.json
    # x = data.get('x')
    # y = data.get('y')
    # if x is not None and y is not None:
        # return jsonify(result=x + y)
    # return jsonify(error="Please provide both 'x' and 'y'"), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
