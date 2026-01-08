from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")

@app.route("/infer", methods=["POST"])
def infer():
    image = request.json.get("image")

    url = "https://app.roboflow.com/science-fair-2526/acacia-koa-vs-acacia-confusa/models/acacia-koa-vs-acacia-confusa/2"
    params = {"api_key": ROBOFLOW_API_KEY}

    response = requests.post(
        url,
        params=params,
        json={"image": image}
    )

    return jsonify(response.json())

if __name__ == "__main__":
    app.run()
