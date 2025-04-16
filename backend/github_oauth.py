import os
import requests

CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")
AUTH_URL = os.environ.get("GITHUB_AUTHORIZE_URL", "https://github.com/login/oauth/authorize")
TOKEN_URL = os.environ.get("GITHUB_TOKEN_URL", "https://github.com/login/oauth/access_token")
API_URL = os.environ.get("GITHUB_API_BASE_URL", "https://api.github.com")


def get_github_auth_url():
    return f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"


def get_access_token(code):
    response = requests.post(
        TOKEN_URL,
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
        f"{API_URL}/user", headers={"Authorization": f"token {token}"}
    )
    if response.ok:
        return response.json()
    return None
