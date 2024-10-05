from flask import Flask, jsonify
import os
import requests
import socket

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
    response = {
        "Service1": service1_data,
        "Service2": service2_data
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)