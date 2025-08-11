import os
import requests
from flask import Flask, request, render_template, send_file
from io import BytesIO

app = Flask(__name__)

# ==== SETTINGS ====
BACKGROUND_IMAGE_URL = "https://i.ibb.co/vCd29NJd/1751604135213.jpg"  # Change as needed
GRAPH_API_VERSION = "v20.0"

def check_token(token):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me"
    params = {"fields": "id,name,picture", "access_token": token}
    r = requests.get(url, params=params)
    if r.status_code == 200 and "id" in r.json():
        data = r.json()
        return {
            "valid": True,
            "name": data["name"],
            "id": data["id"],
            "dp": data["picture"]["data"]["url"],
            "token": token
        }
    return {"valid": False, "token": token}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    valid_tokens = []
    invalid_tokens = []

    if request.method == "POST":
        token = request.form.get("token")
        if token:
            result = check_token(token)

        # File upload
        if "token_file" in request.files:
            file = request.files["token_file"]
            if file and file.filename.endswith(".txt"):
                tokens = file.read().decode().splitlines()
                for t in tokens:
                    res = check_token(t.strip())
                    if res["valid"]:
                        valid_tokens.append(res)
                    else:
                        invalid_tokens.append(res["token"])

    return render_template("index.html",
                           result=result,
                           valid_tokens=valid_tokens,
                           invalid_tokens=invalid_tokens,
                           bg_url=BACKGROUND_IMAGE_URL)

@app.route("/download_valid_tokens", methods=["POST"])
def download_valid_tokens():
    tokens = request.form.getlist("tokens[]")
    output = "\n".join(tokens)
    return send_file(BytesIO(output.encode()), as_attachment=True, download_name="valid_tokens.txt")

if __name__ == "__main__":
    app.run(debug=True)
