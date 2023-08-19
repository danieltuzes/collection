from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import datetime
import platform
import re
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    server = request.json['server']
    ip_address = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{ip_address}_{timestamp}.txt"
    
    if platform.system().lower() == "windows":
        cmd = ['ping', '-n', '1', server]
    else:
        cmd = ['ping', '-c', '1', server]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8')

    if platform.system().lower() == "windows":
        match = re.search(r'Average = (\d+)ms', output)
        if match:
            time = float(match.group(1))
        else:
            time = None
    else:
        match = re.search(r'time=(\d+\.\d+) ms', output)
        if match:
            time = float(match.group(1))
        else:
            time = None

    if time is not None:
        with open(os.path.join('logs', filename), "a") as file:
            file.write(f"{datetime.datetime.now()} - {time}\n")
    
    return jsonify({"time": time, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(directory='logs', path=filename)

if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.mkdir('logs')
    app.run(host='0.0.0.0', port=5000)
