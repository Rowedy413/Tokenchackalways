from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# === SETTINGS ===
BACKGROUND_IMAGE_URL = "https://i.ibb.co/vCd29NJd/1751604135213.jpg"  # change this to update background

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<title>Facebook Token Checker</title>
<style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: url('{{bg}}') no-repeat center center fixed;
        background-size: cover;
        color: white;
        text-align: center;
        overflow-x: hidden;
    }
    header {
        padding: 10px;
        font-size: 24px;
        font-weight: bold;
        background: rgba(0,0,0,0.5);
    }
    footer {
        padding: 5px;
        font-size: 14px;
        background: rgba(0,0,0,0.5);
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    .container {
        padding: 20px;
        background: rgba(0,0,0,0.5);
        margin: 20px auto;
        max-width: 600px;
        border-radius: 10px;
    }
    textarea, input[type="text"] {
        width: 90%;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border: none;
    }
    button {
        padding: 10px 15px;
        border: none;
        background: #28a745;
        color: white;
        cursor: pointer;
        margin: 5px;
        border-radius: 5px;
    }
    .valid, .invalid {
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
    }
    .valid { background: rgba(0,255,0,0.3); }
    .invalid { background: rgba(255,0,0,0.3); }
    canvas {
        position: fixed;
        top: 0;
        left: 0;
        pointer-events: none;
    }
</style>
</head>
<body>
<canvas id="rain"></canvas>
<header>OWNER ROWEDY KIING</header>
<div class="container">
    <h2>Single Token Check</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="text" name="single_token" placeholder="Enter Facebook Access Token">
        <br><button type="submit">Check Token</button>
    </form>
</div>
<div class="container">
    <h2>Check Tokens from File (.txt)</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt">
        <br><button type="submit">Check File Tokens</button>
    </form>
</div>

{% if results %}
<div class="container">
    <h3>Valid Tokens</h3>
    {% if valid %}
        {% for v in valid %}
        <div class="valid">
            <img src="{{v['dp']}}" width="50" style="border-radius:50%"> 
            {{v['name']}} 
            <button onclick="copyToken('{{v['token']}}')">Copy</button>
        </div>
        {% endfor %}
        <button onclick="downloadAll()">Download All</button>
    {% else %}
        <p>No valid tokens found.</p>
    {% endif %}

    <h3>Invalid Tokens</h3>
    {% if invalid %}
        {% for t in invalid %}
        <div class="invalid">{{t}}</div>
        {% endfor %}
    {% else %}
        <p>No invalid tokens.</p>
    {% endif %}
</div>
{% endif %}

<footer>DEVELOPED BY ROWEDY STYLIYSH</footer>

<script>
function copyToken(token) {
    navigator.clipboard.writeText(token);
    alert("Token copied!");
}
function downloadAll() {
    let tokens = [{% for v in valid %}"{{v['token']}}",{% endfor %}];
    let blob = new Blob([tokens.join("\\n")], { type: "text/plain" });
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "valid_tokens.txt";
    a.click();
}

// Rain effect
const canvas = document.getElementById('rain');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let rainDrops = [];
for (let i = 0; i < 100; i++) {
    rainDrops.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        length: Math.random() * 20 + 10,
        velocity: Math.random() * 4 + 4
    });
}

function drawRain() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'rgba(174,194,224,0.5)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let drop of rainDrops) {
        ctx.moveTo(drop.x, drop.y);
        ctx.lineTo(drop.x, drop.y + drop.length);
    }
    ctx.stroke();
    moveRain();
}

function moveRain() {
    for (let drop of rainDrops) {
        drop.y += drop.velocity;
        if (drop.y > canvas.height) {
            drop.y = 0 - drop.length;
            drop.x = Math.random() * canvas.width;
        }
    }
}

function animateRain() {
    drawRain();
    requestAnimationFrame(animateRain);
}
animateRain();
</script>

</body>
</html>
"""

def check_token(token):
    url = f"https://graph.facebook.com/me?fields=id,name,picture&access_token={token}"
    r = requests.get(url)
    if r.status_code == 200 and "name" in r.json():
        data = r.json()
        return {
            "name": data["name"],
            "dp": data["picture"]["data"]["url"],
            "token": token
        }
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    valid_tokens = []
    invalid_tokens = []
    if request.method == "POST":
        if "single_token" in request.form and request.form["single_token"].strip():
            token = request.form["single_token"].strip()
            res = check_token(token)
            if res:
                valid_tokens.append(res)
            else:
                invalid_tokens.append(token)
        elif "token_file" in request.files:
            file = request.files["token_file"]
            if file:
                tokens = file.read().decode().splitlines()
                for t in tokens:
                    t = t.strip()
                    if not t:
                        continue
                    res = check_token(t)
                    if res:
                        valid_tokens.append(res)
                    else:
                        invalid_tokens.append(t)
    return render_template_string(HTML_TEMPLATE, bg=BACKGROUND_IMAGE_URL, results=True if valid_tokens or invalid_tokens else False, valid=valid_tokens, invalid=invalid_tokens)

if __name__ == "__main__":
    app.run(debug=True)
