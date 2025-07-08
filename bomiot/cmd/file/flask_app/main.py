from flask import Flask, jsonify
from django.contrib.auth import get_user_model

User = get_user_model()

flask_app = Flask(__name__)

@flask_app.route("/test/")
def test():
    return jsonify({"msg": "This is a Flask API"})