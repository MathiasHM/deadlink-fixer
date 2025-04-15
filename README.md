# Dead Link Fixer

A web app that scans GitHub repositories for dead links, replaces them with archive.org snapshots, and automatically opens a pull request with the fixes.

- GitHub OAuth login
- Dead link detection and replacement
- Pull request creation via GitHub API
- Clean, browser-based frontend
- Deployable via GitHub Pages + Render

---

## Deployment

### Frontend: GitHub Pages

1. Go to your GitHub repo → **Settings → Pages**
2. Under **Source**, select:
   - Branch: `main`
   - Folder: `/root`
3. Save changes
4. Your frontend will be live at:
```
https://yourusername.github.io/deadlink-fixer/
```

Make sure your `frontend/script.js` points to the deployed backend URL.

---

### Backend: Render

#### 1. Set up environment variables

Create a `.env` file in `backend/` (do NOT commit it) with:

```env
GITHUB_CLIENT_ID=your_github_oauth_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_client_secret
SECRET_KEY=random_flask_secret_key
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 2. Deploy to Render

- Go to [https://render.com](https://render.com)
- Click **"New Web Service"**
- Select your GitHub repo
- Set:

  | Setting            | Value                                 |
  |--------------------|---------------------------------------|
  | Build Command      | `pip install -r backend/requirements.txt` |
  | Start Command      | `flask run --host=0.0.0.0 --port=10000` |
  | Working Directory  | `backend/`                             |

- Add environment variables from your `.env` file as well as
FLASK_APP = app.py
PORT = 10000

#### 3. Set GitHub OAuth Callback

In [https://github.com/settings/developers](https://github.com/settings/developers):

- Set **Authorization callback URL** to:
```
https://your-backend-url.onrender.com/callback
```

---

## Local Development

### Frontend

```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
flask run
# Visit http://localhost:5000
```

---

## License

This project is licensed under the [GNU GPL v3.0](LICENSE).
See the license file for details.
