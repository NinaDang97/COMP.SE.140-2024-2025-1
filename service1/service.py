from flask import Flask, jsonify, request
import os
import requests
import socket
import time
import sys
import subprocess
import time
import datetime

app = Flask(__name__)

def getIP():
    hostname = socket.gethostname()
    IPAddress = socket.gethostbyname(hostname)
    return IPAddress

def get_container_info():
    info = {
        "IP_address": getIP(),
        "processes": os.popen("ps -o pid,comm").read(),
        "disk_space": os.popen("df -h /").read(),
        "uptime": os.popen("uptime").read().strip(),
    }
    return info

def get_service2():
    try:
        service2_response = requests.get("http://service2:5002")
        service2_response.raise_for_status() # Raise an error for non-2xx responses
        service2_data = service2_response.json()
    except requests.RequestException as e:
        service2_data = {"error": "Service2 not available"}
    return service2_data

def get_info_data():
    service1_data = get_container_info()
    service2_data = get_service2()
    return {
        "Service1": service1_data,
        "Service2": service2_data
    }

@app.route('/request', methods=['GET'])
def get_info():
    time.sleep(2) # Delay 2 seconds
    return jsonify(get_info_data())

def stop():
    print("Service stop requested, shutting down all containers.", file=sys.stderr)
    
    # Respond to client immediately before shutdown
    response = jsonify({"message": "Service is stopping all containers."})
    response.status_code = 200
    
    # Shut down the Docker Compose process after sending the response
    # Use a subprocess to run the shutdown command
    shutdown_cmd = "docker-compose down"
    try:
        subprocess.Popen(shutdown_cmd, shell=True)
    except Exception as e:
        print(f"Failed to shut down: {e}", file=sys.stderr)
    
    return response

# Global state variable
state = "INIT"
state_log = [] # Log of state changes

@app.route('/state', methods=['GET'])
def get_state():
    """Return the current state of the service."""
    return jsonify(state)

@app.route('/state', methods=['PUT'])
def update_state():
    """Update the state of the service."""
    global state

    new_state = request.data.decode("utf-8").strip()
    
    valid_states = ["INIT", "PAUSED", "RUNNING", "SHUTDOWN"]
    if new_state not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    if state != new_state:
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        state_log.append(f"{timestamp}: {state}->{new_state}")
        state = new_state

    if new_state == "SHUTDOWN":
        # Shut down the service
        stop()

    return jsonify(new_state)

@app.route('/run-log', methods=['GET'])
def get_run_log():
    """Retrieve the log of state transitions."""
    return "\n".join(state_log), 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8197)