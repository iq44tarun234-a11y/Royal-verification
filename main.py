@app.route("/callback")
def callback():
    try:
        code = request.args.get("code")

        import os

CLIENT_SECRET = os.getenv("CLIENT_SECRET")

data = {
    "client_id": "1488084101066920116",
    "client_secret": CLIENT_SECRET,
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "https://royal-verification.onrender.com/callback"
}

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

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

        user_id = user.get("id")

        if not user_id:
            return f"❌ User Error: {user}"

        # 🔥 JOIN SERVER
        requests.put(
            f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}",
            json={"access_token": access_token},
            headers={"Authorization": f"Bot {BOT_TOKEN}"}
        )

        # 🔥 GIVE ROLE (YOUR ROLE ID ADDED)
        requests.put(
            f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}/roles/1488138522773688360",
            headers={"Authorization": f"Bot {BOT_TOKEN}"}
        )

        # ✅ SUCCESS PAGE
        return """
        <html>
        <body style="background:#0f0f0f;color:white;text-align:center;margin-top:20%;">
            <h1>✅ Verification Done</h1>
            <p>Thanks for verifying! You can now return to Discord.</p>
        </body>
        </html>
        """

    except Exception as e:
        return f"❌ Error: {str(e)}"
