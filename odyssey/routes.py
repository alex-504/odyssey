import time
import requests
from flask import Blueprint, render_template, jsonify, request
from datetime import datetime, timezone
import os
import socket

# Define the blueprint 
main = Blueprint('main', __name__)

# API key for Hosted-Graphite
api_key = os.getenv('HOSTED_GRAPHITE_API_KEY')
headers = {"Authorization": f"Bearer {api_key}"}

# Ensure API key is present
if not api_key:
    raise ValueError("HOSTED_GRAPHITE_API_KEY is not set in environment variables")

# Helper function to send metrics
import socket

api_key = os.getenv('HOSTED_GRAPHITE_API_KEY')

def send_metric(metric_name, value):
    try:
        message = f"{api_key}.{metric_name} {value}\n"
        
        # Create a TCP connection to Hosted-Graphite
        conn = socket.create_connection((f"{api_key}.carbon.hostedgraphite.com", 2003))
        conn.send(message.encode('utf-8'))
        conn.close()
        
    except Exception as e:
        print(f"Failed to send metric {metric_name}: {e}")

# HTML Route 1: Home Page
@main.route('/')
def home():
    return render_template('home.html')

# HTML Route 2: About Page
@main.route('/about')
def about():
    return render_template('about.html')

# API Route 1: GET Endpoint (returns JSON data)
@main.route('/api/data', methods=['GET'])
def get_data():
    start_time = time.time()

    response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')
    joke = response.json()[0]

    # Calculate response duration
    duration = time.time() - start_time

    # Send metrics
    send_metric("get_request_count", 1)           # Metric 1: GET request count
    send_metric("get_request_duration", duration) # Metric 2: GET request duration
    send_metric("total_request_count", 1)         # Metric 3: Total API request count

    return jsonify({
        'message': f"{joke['setup']} {joke['punchline']}",
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

# API Route 2: POST Endpoint (handles JSON data)
@main.route('/api/data', methods=['POST'])
def post_data():
    start_time = time.time()

    name = request.form.get('name')
    age = request.form.get('age')

    if not name or not all(part.isalpha() for part in name.split()):
        return jsonify({"error": "Invalid or missing name"}), 400

    if not age or not age.isdigit():
        return jsonify({"error": "Invalid or missing age"}), 400

    duration = time.time() - start_time

    # Send metrics
    send_metric("post_request_count", 1)          # Metric 1: POST request count
    send_metric("post_request_duration", duration)# Metric 2: POST request duration
    send_metric("total_request_count", 1)         # Metric 3: Total API request count

    return jsonify({
        'name': name,
        'age': age,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })