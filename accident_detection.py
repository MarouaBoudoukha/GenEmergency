from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to receive data
@app.route('/api/data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Log the received data
    print(f"Received data: {data}")

    # Return a success response
    return jsonify({"message": "Data received successfully"}), 200

if __name__ == "__main__":
    # Run the server on localhost at port 5000
    app.run(host="0.0.0.0", port=5001)
