from flask import Flask, send_from_directory, request, jsonify
import datetime
import os
import requests

app = Flask(__name__, static_folder='.')

@app.route("/")
def index():
    return app.send_static_file("index.html")

def get_server_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return f"{data['city']}, {data['region']}, {data['country']}"
    except:
        return "Unknown Location"

@app.route('/location')
def get_location():
    server_location = get_server_location()
    return server_location

@app.route("/app.js")
def serve_js():
    return app.send_static_file("app.js")

@app.route('/ping')
def ping():
    return datetime.datetime.now().strftime('%H:%M:%S')

@app.route('/store_latency', methods=['POST'])
def store_latency():
    data = request.json
    rtt = data['rtt']
    serverTime = data['serverTime']

    ip_address = request.remote_addr
    filename = f"{ip_address}_{datetime.datetime.now().date()}.txt"
    folder = "data"
    if not os.path.exists(folder):
        os.mkdir(folder)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'a') as file:
        file.write(f"{serverTime}: {rtt} ms\n")

    return jsonify(status="success")

@app.route('/download')
def download():
    ip_address = request.remote_addr
    filename = f"{ip_address}_{datetime.datetime.now().date()}.txt"
    folder = "data"
    return send_from_directory(folder, filename, as_attachment=True)

if __name__ == "__main__":
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(('0.0.0.0', 5432), app)
    http_server.serve_forever()