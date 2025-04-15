import os
import re
import requests
import shutil
from git import Repo
from urllib.parse import urlparse
from urllib.parse import quote
from pathlib import Path

def is_dead(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code >= 400
    except:
        return True

def get_archive_url(url):
    print(f"Checking archive.org for: {url}")
    try:
        response = requests.get(f"https://archive.org/wayback/available?url={url}", timeout=10)
        print(f"Raw JSON: {response.text}")
        if response.ok:
            data = response.json()
            snapshot = data.get("archived_snapshots", {}).get("closest")
            if snapshot and snapshot.get("available"):
                archive_url = snapshot.get("url")
                print(f"✅ Found archive: {archive_url}")
                return archive_url
            else:
                # 🔁 fallback to generic search link
                fallback = f"https://web.archive.org/web/*/{quote(url)}"
                print(f"🟠 No snapshot found — using fallback: {fallback}")
                return fallback
    except Exception as e:
        print(f"❌ Archive lookup failed: {e}")

    return None


def find_links(text):
    pattern = r'https?://[^\s)>\]"\']+'
    return re.findall(pattern, text)

def clone_repo(repo_url, dest_folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    return Repo.clone_from(repo_url, dest_folder)

def fix_dead_links_in_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    links = find_links(content)
    modified = False

    for link in links:
        if is_dead(link):
            archive = get_archive_url(link)
            if archive:
                print(f"Replacing {link} with {archive}")
                content = content.replace(link, archive)
                modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    return modified

def fix_repo_links(repo_url):
    repo_name = Path(urlparse(repo_url).path).stem
    dest = f"temp_repos/{repo_name}"
    os.makedirs("temp_repos", exist_ok=True)

    repo = clone_repo(repo_url, dest)

    modified_files = []

    for root, dirs, files in os.walk(dest):
        for file in files:
            if file.endswith((".md", ".txt", ".rst", ".html")):
                path = os.path.join(root, file)
                if fix_dead_links_in_file(path):
                    modified_files.append(path)

    return {
        "modified": modified_files,
        "local_path": dest,
        "repo_name": repo_name,
        "repo_obj": repo
    }
