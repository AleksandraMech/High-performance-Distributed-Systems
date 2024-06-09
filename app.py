from flask import Flask
from views import views
import time
import csv
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import datetime
import json
import sys
import os

app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")


app.secret_key = os.urandom(24)


if __name__ == '__main__':
    app.run(debug=True, port=8000)