@app.route("/callback")
def callback():
    try:
        code = request.args.get("code")

        CLIENT_ID = "1488084101066920116"
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        REDIRECT_URI = "https://royal-verification.onrender.com/callback"

        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        token = requests.post(
            "https://discord.com/api/oauth2/token",
            data=data,
            headers=headers
        ).json()

        access_token = token.get("access_token")

        if not access_token:
            return f"❌ Token Error: {token}"

        user = requests.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        return "✅ Verified Successfully!"

    except Exception as e:
        return f"Error: {e}"
