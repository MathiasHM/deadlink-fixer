# 🧹 Dead Link Fixer

Dead Link Fixer is a web tool that scans GitHub repositories for dead hyperlinks, replaces them with archive.org snapshots, and automatically opens a pull request with the fixes. Based on an idea by Yush G who has listed a bunch of great idea at https://aayushg.com/ideas.

## ✨ Features

- Detects dead links in `.md` and text files
- Replaces dead URLs with working archive.org snapshots
- Authenticates via GitHub OAuth
- Supports public and private repositories
- Fully automated PR creation
- Runs on GitHub Pages + Render backend

---

## 🚀 Deployment

### Frontend (GitHub Pages)
1. Upload contents of `/frontend` to the root of your GitHub repository
2. Go to `Settings → Pages`
3. Set:
   - Source: `main`
   - Folder: `/ (root)`

### Backend (Render)
1. [Create a GitHub OAuth App](https://github.com/settings/developers)
   - Authorization callback: `https://<your-backend>.onrender.com/callback`
   - Homepage URL: `https://<your-username>.github.io/deadlink-fixer/`

2. Deploy your backend folder to Render
   - Build command: `pip install -r requirements.txt`
   - Start command: `flask run --host=0.0.0.0 --port=10000`
   - Start command for production: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - Runtime: Python 3.11+

3. Set the following environment variables in Render:

```env
FLASK_APP=app.py
PORT=10000
SECRET_KEY=your_flask_secret
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_secret
GITHUB_AUTHORIZE_URL=https://github.com/login/oauth/authorize
GITHUB_TOKEN_URL=https://github.com/login/oauth/access_token
GITHUB_API_BASE_URL=https://api.github.com
OAUTH_REDIRECT_URI=https://your-backend.onrender.com/callback
FRONTEND_URL=https://yourusername.github.io/deadlink-fixer/
DEFAULT_BRANCH=main
DEFAULT_PR_TITLE=Fix dead links
DEFAULT_PR_BODY=Fix dead links via DeadLinkFixer
```

### 🔑 Where to Get Environment Variables

| Variable                | Where to Get It                                                                 |
|------------------------|----------------------------------------------------------------------------------|
| `SECRET_KEY`           | Run `python -c "import secrets; print(secrets.token_hex(32))"` to generate one |
| `GITHUB_CLIENT_ID`     | From [GitHub Developer Settings → OAuth Apps](https://github.com/settings/developers) |
| `GITHUB_CLIENT_SECRET` | From the same place as above                                                    |
| `GITHUB_AUTHORIZE_URL` | Usually `https://github.com/login/oauth/authorize`                             |
| `GITHUB_TOKEN_URL`     | Usually `https://github.com/login/oauth/access_token`                          |
| `GITHUB_API_BASE_URL`  | Usually `https://api.github.com`                                               |
| `OAUTH_REDIRECT_URI`   | Matches your Render service: `https://your-backend.onrender.com/callback`     |
| `FRONTEND_URL`         | Your GitHub Pages site: `https://yourusername.github.io/deadlink-fixer/`       |
| `DEFAULT_BRANCH`       | Target PR branch (`main`, `master`, etc.)                                      |
| `DEFAULT_PR_TITLE`     | Text for the PR title                                                          |
| `DEFAULT_PR_BODY`      | Text for the PR body                                                           |

4. (Optional) Add `.nojekyll` to your GitHub Pages root if using raw `index.html`

---

## 🧪 Local Development

Create (do NOT share) a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Then run locally:
```bash
cd backend
python -m flask run
```

---

## 🐳 Docker (Optional)
_Coming soon: deploy the entire backend in one command using Docker._

---

## 🙋 FAQ

- **Does this work for GitHub Enterprise or GitLab?**
  GitHub only, for now. Support for other platforms is in progress.

- **Why doesn't login work on mobile?**
  Mobile browsers may block cross-site cookies. Use desktop Chrome/Firefox for best results, or self-host frontend and backend under one domain.

- **Can I preview changes before PR is created?**
  Not yet — coming soon.

---

## 📄 License

This project is licensed under the GPL-3.0 License.

---

## 👨‍💻 Author
Made by [Mathias Hamza Mirza](https://github.com/MathiasHM). Contributions welcome!

