from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, base64, os

app = Flask(__name__)
CORS(app)  # ← REQUIRED

ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
WORKFLOW_URL = os.environ.get("WORKFLOW_URL")

@app.route("/", methods=["GET"])
def health():
    return "Backend is running"

@app.route("/", methods=["POST"])
def run():
    try:
        image_input = None

        # FILE UPLOAD
        if "file" in request.files:
            file = request.files["file"]
            image_input = {
                "type": "base64",
                "value": base64.b64encode(file.read()).decode("utf-8")
            }

        # JSON INPUT
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

        rf_res = requests.post(
            WORKFLOW_URL,
            json={
                "api_key": ROBOFLOW_API_KEY,
                "inputs": { "image": image_input }
            },
            timeout=30
        )

        return jsonify(rf_res.json())

    except Exception as e:
        return jsonify({ "error": str(e) }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
