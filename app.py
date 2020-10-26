import json
import logging
from flask import Flask, request

app = Flask(__name__)


@app.route("/marusya", methods=["POST", "GET"])
def marusya():
    return "Marusya"

@app.route("/visa", methods=['POST'])
def vise():
    return "Visa post"

@app.route("/")
def home():
    return "Welcome page!"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)