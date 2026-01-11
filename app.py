@app.route("/", methods=["POST"])
def run():
    try:
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

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500
