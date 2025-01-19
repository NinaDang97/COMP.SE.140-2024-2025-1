from flask import Flask, jsonify
import os
import requests
import socket
import time
import sys
import subprocess

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
        service2_data = service2_response.json()
    except:
        service2_data = {"error": "Service2 not available"}
    return service2_data

@app.route('/', methods=['GET'])
def get_info():
    service1_data = get_container_info()
    service2_data = get_service2()
    time.sleep(2) # Delay 2 seconds
    response = {
        "Service1": service1_data,
        "Service2": service2_data
    }
    return jsonify(response)

@app.route('/stop', methods=['POST'])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8199)