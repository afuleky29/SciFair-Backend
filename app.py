from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# ENV VARS (set these in Render)
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
WORKFLOW_URL = os.environ.get("WORKFLOW_URL")

# ---------- HEALTH CHECK ----------
@app.route("/", methods=["GET"])
def health():
    return "Backend is running"

# ---------- MAIN ENDPOINT ----------
@app.route("/", methods=["POST"])
def run():
    try:
        image_input = None

        # 1️⃣ FILE UPLOAD
        if "file" in request.files:
            file = request.files["file"]
            image_input = {
                "type": "base64",
                "value": base64.b64encode(file.read()).decode("utf-8")
            }

        # 2️⃣ BASE64 (webcam)
        elif request.json and "base64" in request.json:
            image_input = {
                "type": "base64",
                "value": request.json["base64"].split(",")[-1]
            }

        # 3️⃣ URL
        elif request.json and "url" in request.json:
            image_input = {
                "type": "url",
                "value": request.json["url"]
            }

        else:
            return jsonify({"error": "No image provided"}), 400

        # Send to Roboflow
        response = requests.post(
            WORKFLOW_URL,
            json={
                "api_key": ROBOFLOW_API_KEY,
                "inputs": {
                    "image": image_input
                }
            },
            timeout=30
        )

        return jsonify(response.json())

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ---------- REQUIRED FOR RENDER ----------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
