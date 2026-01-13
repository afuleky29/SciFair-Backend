from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, base64, os

app = Flask(__name__)
CORS(app)

ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
WORKFLOW_URL = os.environ.get("WORKFLOW_URL")


@app.route("/", methods=["GET"])
def health():
    return "Backend is running"


@app.route("/", methods=["POST"])
def run():
    try:
        # 🔴 Validate env vars
        if not ROBOFLOW_API_KEY or not WORKFLOW_URL:
            return jsonify({
                "error": "Missing ROBOFLOW_API_KEY or WORKFLOW_URL"
            }), 500

        image_input = None

        # 1️⃣ FILE UPLOAD (multipart/form-data)
        if "file" in request.files:
            file = request.files["file"]
            image_input = {
                "type": "base64",
                "value": base64.b64encode(file.read()).decode("utf-8")
            }

        # 2️⃣ JSON INPUT (URL or BASE64)
        elif request.is_json:
            data = request.json

            if "url" in data:
                image_input = {
                    "type": "url",
                    "value": data["url"]
                }

            elif "base64" in data:
                image_input = {
                    "type": "base64",
                    "value": data["base64"].split(",")[-1]
                }

        if not image_input:
            return jsonify({"error": "No image provided"}), 400

        # 🔵 DEBUG INPUT
        print("IMAGE INPUT TYPE:", image_input["type"])

        # 3️⃣ SEND TO ROBOFLOW
        rf_res = requests.post(
            WORKFLOW_URL,
            json={
                "api_key": ROBOFLOW_API_KEY,
                "inputs": {
                    "image": image_input
                }
            },
            timeout=30
        )

        # 🔴 HANDLE ROBOFLOW FAILURE
        if rf_res.status_code != 200:
            return jsonify({
                "error": "Roboflow request failed",
                "status": rf_res.status_code,
                "details": rf_res.text
            }), 500

        return jsonify(rf_res.json())

    except
