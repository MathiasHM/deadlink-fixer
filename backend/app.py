from flask import Flask, redirect, request, session, url_for, jsonify
from flask_session import Session
from dotenv import load_dotenv
from flask_cors import CORS

import os

from github_oauth import get_github_auth_url, get_access_token, get_user_info
from dead_link_fixer import fix_repo_links
from github_pr import create_branch_and_pr

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app, supports_credentials=True)

@app.route("/")
def index():
    if "access_token" in session:
        user = get_user_info(session["access_token"])
        return jsonify(user)
    return '<a href="/login">Login with GitHub</a>'

@app.route("/login")
def login():
    return redirect(get_github_auth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token = get_access_token(code)
    if token:
        session["access_token"] = token
        return redirect(url_for("index"))
    return "OAuth failed", 400

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/fix-dead-links", methods=["POST"])
def fix_links():
    if "access_token" not in session:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    repo_url = data.get("repo_url")
    if not repo_url:
        return {"error": "Missing repo_url"}, 400

    try:
        result = fix_repo_links(repo_url)

        if not result["modified"]:
            return {
                "message": "No dead links found.",
                "modified_files": []
            }

        branch_name = "fix/dead-links-001"
        pr_result = create_branch_and_pr(
            repo=result["repo_obj"],
            local_path=result["local_path"],
            branch_name=branch_name,
            modified_files=result["modified"],
            user_token=session["access_token"]
        )

        return {
            "message": pr_result["message"],
            "pull_request_url": pr_result["pull_request_url"],
            "modified_files": result["modified"],
            "existing_pr": pr_result["is_existing_pr"]
        }

    except Exception as e:
        return {"error": str(e)}, 500
