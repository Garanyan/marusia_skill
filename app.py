import json
import logging
from flask import Flask, request

app = Flask(__name__)


@app.route("/marusya", methods=["POST", "GET"])
def marusya():
	return "Marusya"

@app.route("/visa", methods=['POST'])
	return "Visa post"