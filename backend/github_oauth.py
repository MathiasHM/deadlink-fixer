import os
import requests

CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "https://deadlink-fixer.onrender.com/callback"


def get_github_auth_url():
    return (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={CLIENT_ID}&scope=repo&redirect_uri={REDIRECT_URI}"
    )


def get_access_token(code):
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
    )
    if response.ok:
        return response.json().get("access_token")
    return None


def get_user_info(token):
    response = requests.get(
        "https://api.github.com/user", headers={"Authorization": f"token {token}"}
    )
    if response.ok:
        return response.json()
    return None
