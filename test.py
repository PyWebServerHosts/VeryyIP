from flask import Flask, jsonify
from veryyip import VeryyIP
import requests

# Initialize the Flask app
app = Flask(__name__)

# Initialize VeryyIP
ip = VeryyIP()

# Route to get the private (local) IP address
@app.route('/api/local-ip', methods=['GET'])
def get_local_ip():
    local_ip = ip.get('private')
    return jsonify({'local_ip': local_ip})

# Route to get the public IP address
@app.route('/api/public-ip', methods=['GET'])
def get_public_ip():
    public_ip = ip.get('public')
    return jsonify({'public_ip': public_ip})

# Route to display the IP addresses on the root path
@app.route('/', methods=['GET'])
def index():
    # Get local IP address by calling /api/local-ip
    local_ip_response = requests.get('http://localhost:5000/api/local-ip')
    local_ip = local_ip_response.json().get('local_ip')

    # Get public IP address by calling /api/public-ip
    public_ip_response = requests.get('http://localhost:5000/api/public-ip')
    public_ip = public_ip_response.json().get('public_ip')

    # Display both IP addresses on the root page
    return f'''
    <h1>IP Address Information</h1>
    <p><strong>Local IP Address:</strong> {local_ip}</p>
    <p><strong>Public IP Address:</strong> {public_ip}</p>
    '''

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

