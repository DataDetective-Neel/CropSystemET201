# 🚀 Free Deployment Guide for Crop Recommendation System

This guide will help you deploy your Flask crop recommendation system for **FREE** on various platforms.

## 🌟 Recommended: Render.com (Easiest & Most Reliable)

### Prerequisites
- GitHub account (free)
- Render account (free at [render.com](https://render.com))

### Step-by-Step Deployment on Render.com

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/crop_system.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com) and sign up/login (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `crop_system` repository
   - Configure the service:
     - **Name**: `crop-system` (or any name you prefer)
     - **Region**: Choose closest to you
     - **Branch**: `main`
     - **Root Directory**: Leave empty (root)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn web_interface:app --bind 0.0.0.0:$PORT`
   - Click "Create Web Service"
   - Render will automatically build and deploy your app!

3. **Wait for deployment** (~5-10 minutes)
   - Render will install dependencies and start your app
   - Your app will be available at: `https://crop-system.onrender.com` (or your custom name)

### Render.com Free Tier Details
- ✅ Free forever
- ✅ 750 hours/month (enough for always-on if you're the only user)
- ⚠️ Spins down after 15 minutes of inactivity (wakes up on first request)
- ✅ Automatic SSL/HTTPS
- ✅ Auto-deploy on git push

---

## 🚂 Alternative: Railway.app

### Deployment Steps

1. **Sign up** at [railway.app](https://railway.app) (free with GitHub)

2. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure service**
   - Railway auto-detects Python
   - Set start command: `gunicorn web_interface:app --bind 0.0.0.0:$PORT`
   - Railway automatically sets PORT environment variable

4. **Deploy**
   - Railway provides a `.railway` domain automatically
   - Deployment happens automatically

### Railway Free Tier
- ✅ $5 free credit monthly (enough for small apps)
- ✅ No credit card required initially
- ✅ Auto-deploy from GitHub

---

## ✈️ Alternative: Fly.io

### Deployment Steps

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Initialize and deploy**
   ```bash
   fly launch
   # Answer prompts (use defaults mostly)
   fly deploy
   ```

### Fly.io Free Tier
- ✅ 3 shared VMs free
- ✅ 160GB outbound data transfer/month
- ✅ Requires credit card (no charge on free tier)

---

## 🐍 Alternative: PythonAnywhere

### Deployment Steps

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload files**
   - Use their file manager or git clone

3. **Configure web app**
   - Go to Web tab
   - Create new web app
   - Set source code path
   - Set WSGI configuration file

4. **Set WSGI config** (in `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   path = '/home/YOUR_USERNAME/crop_system'
   if path not in sys.path:
       sys.path.append(path)
   
   from web_interface import app
   application = app
   ```

### PythonAnywhere Free Tier
- ✅ Free forever
- ✅ 1 web app
- ⚠️ Custom domains require paid tier
- ✅ Auto-reload on file change

---

## 📋 Important Notes

### Model Files
All your `.pkl` model files in the `models/` directory need to be committed to git. They're already in your repo, so deployment will include them automatically.

### Port Configuration
- Render, Railway, Fly.io: Use `$PORT` environment variable (already configured)
- PythonAnywhere: Uses default port, no PORT variable needed

### File Paths
Your code uses relative paths like `models/legacy/...` which work fine on all platforms as long as the directory structure is maintained (which git preserves).

### Testing Locally First
Before deploying, test locally:
```bash
pip install -r requirements.txt
python web_interface.py
# Visit http://127.0.0.1:5000
```

### Environment Variables
If you need to add environment variables (API keys, etc.):
- **Render**: Settings → Environment Variables
- **Railway**: Variables tab
- **Fly.io**: `fly secrets set KEY=value`
- **PythonAnywhere**: Web tab → Static files / WSGI configuration

---

## 🔧 Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Ensure Python version in `runtime.txt` is supported
- Check build logs on platform dashboard

### App Crashes After Deployment
- Check logs on platform dashboard
- Verify model files are committed to git
- Ensure `Procfile` or start command uses correct paths

### Models Not Loading
- Verify all `.pkl` files are in git
- Check file paths in `web_interface.py` match directory structure
- Ensure models directory structure is preserved

### Slow First Request (Render)
- Normal on free tier (app sleeps after 15 min inactivity)
- First request after sleep takes ~30 seconds
- Subsequent requests are fast

---

## 🎯 Quick Start (Recommended: Render.com)

1. Push code to GitHub
2. Sign up at render.com
3. New → Web Service → Connect GitHub → Select repo
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn web_interface:app --bind 0.0.0.0:$PORT`
6. Deploy!

**Your app will be live in ~5 minutes!** 🎉

---

## 📞 Need Help?

- Check platform-specific documentation
- Review error logs in platform dashboard
- Verify all files are committed to git
- Test locally first before deploying

Happy deploying! 🚀

