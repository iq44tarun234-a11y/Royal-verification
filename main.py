from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

# ===== CONFIG ===== #
CLIENT_ID = "1488084101066920116"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GUILD_ID = "1477632935149441044"
ROLE_ID = "1485905236009816154"

REDIRECT_URI = "https://royal-verification.onrender.com"
# ================== #

@app.route("/")
def home():
    return """
    <html>
    <body style="background:#0f0f0f;color:white;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="text-align:center;">
            <h1>Royal Verification</h1>
            <a href="/login">
                <button style="padding:12px 30px;background:#5865F2;color:white;border:none;border-radius:10px;">
                Verify
                </button>
            </a>
        </div>
    </body>
    </html>
    """

@app.route("/login")
def login():
    return redirect(
        f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify guilds.join"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    ).json()

    access_token = token.get("access_token")

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user_id = user["id"]

    # JOIN SERVER
    requests.put(
        f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}",
        json={"access_token": access_token},
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )

    # GIVE ROLE
    requests.put(
        f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )

    return "<h1 style='color:lime;text-align:center;margin-top:20%;'>✅ Verified! You can close this.</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
