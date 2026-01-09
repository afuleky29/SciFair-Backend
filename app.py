from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

ROBOFLOW_API_KEY = os.environ["ROBOFLOW_API_KEY"]
WORKFLOW_URL = "https://app.roboflow.com/science-fair-2526/acacia-koa-vs-acacia-confusa/models/acacia-koa-vs-acacia-confusa/2"

@app.route("/", methods=["POST"])
def run():
    # ---------- IMAGE URL ----------
    if request.is_json:
        data = request.json

        if "image" in data:
            response = requests.post(
                WORKFLOW_URL,
                json={
                    "api_key": ROBOFLOW_API_KEY,
                    "inputs": {
                        "image": {
                            "type": "url",
                            "value": data["image"]
                        }
                    }
                }
            )
            return jsonify(response.json())

        # ---------- BASE64 (WEBCAM) ----------
        if "base64" in data:
            response = requests.post(
                WORKFLOW_URL,
                json={
                    "api_key": ROBOFLOW_API_KEY,
                    "inputs": {
                        "image": {
                            "type": "base64",
                            "value": data["base64"]
                        }
                    }
                }
            )
            return jsonify(response.json())

    # ---------- FILE UPLOAD ----------
    if "file" in request.files:
        file = request.files["file"]
        encoded = base64.b64encode(file.read()).decode("utf-8")

        response = requests.post(
            WORKFLOW_URL,
            json={
                "api_key": ROBOFLOW_API_KEY,
                "inputs": {
                    "image": {
                        "type": "base64",
                        "value": encoded
                    }
                }
            }
        )
        return jsonify(response.json())

    return jsonify({"error": "No image provided"}), 400

if __name__ == "__main__":
    app.run()
