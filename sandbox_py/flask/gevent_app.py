"""gevent_app.py
    Starts the flask web application in a gevent production server.

    cd into the folder where this file is, and issue ``python gevent_app.py``"""

from gevent.pywsgi import WSGIServer
from file_upload import app

http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
