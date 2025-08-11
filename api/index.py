from flask import Flask, request, render_template, send_file
import requests
import io

app = Flask(__name__, template_folder="../templates", static_folder="../static")

BACKGROUND_IMAGE_URL = "https://i.ibb.co/vCd29NJd/1751604135213.jpg"  # Changeable

GRAPH_API_URL = "https://graph.facebook.com/me?fields=id,name,picture&access_token="

@app.route("/", methods=["GET", "POST"])
def index():
    single_result = None
    file_results = {"valid": [], "invalid": []}

    if request.method == "POST":
        # Single token check
        token = request.form.get("single_token", "").strip()
        if token:
            resp = requests.get(GRAPH_API_URL + token)
            if resp.status_code == 200 and "name" in resp.json():
                data = resp.json()
                single_result = {
                    "valid": True,
                    "name": data["name"],
                    "id": data["id"],
                    "picture": data["picture"]["data"]["url"],
                    "token": token
                }
            else:
                single_result = {"valid": False}

        # File token check
        if "token_file" in request.files:
            file = request.files["token_file"]
            if file.filename:
                content = file.read().decode().splitlines()
                for t in content:
                    t = t.strip()
                    if not t:
                        continue
                    r = requests.get(GRAPH_API_URL + t)
                    if r.status_code == 200 and "name" in r.json():
                        d = r.json()
                        file_results["valid"].append({
                            "name": d["name"],
                            "id": d["id"],
                            "picture": d["picture"]["data"]["url"],
                            "token": t
                        })
                    else:
                        file_results["invalid"].append(t)

    return render_template(
        "index.html",
        single_result=single_result,
        file_results=file_results,
        bg_url=BACKGROUND_IMAGE_URL
    )

@app.route("/download_valid_tokens")
def download_valid_tokens():
    tokens = request.args.getlist("token")
    file_content = "\n".join(tokens)
    return send_file(
        io.BytesIO(file_content.encode()),
        mimetype="text/plain",
        as_attachment=True,
        download_name="valid_tokens.txt"
    )

if __name__ == "__main__":
    app.run(debug=True)
