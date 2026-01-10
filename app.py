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
    @app.route("/", methods=["POST"])
def run():
    ...

