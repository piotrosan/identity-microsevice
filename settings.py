import os

APP_ID = 'Hay6wfGtyWE88JHNbabqw2'

root_path = os.path.abspath(os.path.dirname(__file__))

SSL_KEYFILE = None
SSL_CERTFILE = None
HOST = 'localhost'
PORT = 8001

BASE_URL = f"{'https' if SSL_CERTFILE else 'http'}://{HOST}:{PORT}"