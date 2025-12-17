# ⚡ Render.com Performance Guide

## Why Render Takes Time to Load

### The Free Tier "Spin Down" Issue

**What's happening:**
- Render's **free tier** spins down your app after **15 minutes of inactivity**
- When someone visits your app after it's "asleep", it needs to "wake up"
- This "cold start" takes **30-60 seconds** (sometimes up to 2 minutes)

**The logs you see:**
```
SERVICE WAKING UP ...
ALLOCATING COMPUTE RESOURCES ...
PREPARING INSTANCE ...
STARTING THE INSTANCE ...
```
These are normal startup steps that take time.

### Why This Happens

1. **Free Tier Limitation** - Render offers free hosting but saves resources by spinning down inactive apps
2. **Cold Start** - Your Flask app needs to:
   - Allocate server resources
   - Load Python environment
   - Load all your AI models (`.pkl` files) - this can be slow!
   - Start the web server
3. **Model Loading** - Your crop models are large files that need to be loaded into memory

## ⏱️ Loading Time Breakdown

- **First visit after 15 min**: 30-60 seconds
- **Subsequent visits** (within 15 min): Instant (< 1 second)
- **After spin-down**: Another 30-60 seconds

## 🚀 Solutions to Improve Performance

### Option 1: Keep App Awake (Free Tier)

Create a simple script that pings your app every 10 minutes to keep it alive:

**Create `keep_alive.py`:**
```python
import requests
import time
import schedule

def ping_app():
    try:
        response = requests.get('https://your-app.onrender.com/api/health')
        print(f"✅ Pinged app: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Ping every 10 minutes
schedule.every(10).minutes.do(ping_app)

while True:
    schedule.run_pending()
    time.sleep(1)
```

Run this on your computer or use a free service like:
- **UptimeRobot** (free) - https://uptimerobot.com
- **Cron-Job.org** (free) - https://cron-job.org

### Option 2: Optimize Model Loading

Your models load every time the app starts. Consider:

1. **Lazy Loading** - Only load models when first prediction is requested
2. **Model Optimization** - Use smaller model files if possible
3. **Caching** - Cache predictions if appropriate

### Option 3: Upgrade to Paid Tier

Render's paid tier ($7/month) keeps your app always running - no spin-down!

### Option 4: Use Faster Free Alternatives

**Railway.app** (Free $5 credit/month):
- Faster cold starts
- More reliable free tier
- Auto-deploy from GitHub

**Fly.io** (Free tier):
- Very fast cold starts
- Better for apps with large files

## 📊 Expected Performance

### Free Tier (Current):
- ✅ First request after spin-down: **30-60 seconds**
- ✅ Subsequent requests: **Instant** (< 1 second)
- ✅ Free forever
- ❌ Spins down after 15 min inactivity

### Paid Tier ($7/month):
- ✅ All requests: **Instant** (< 1 second)
- ✅ Always running
- ✅ No spin-down delay
- ❌ Costs money

## 💡 Best Practices

### 1. Add a Loading Page
Show users that the app is waking up:
```html
<!-- Add to your HTML -->
<div id="loading-screen">
  <h2>🌾 Waking up AI models...</h2>
  <p>Please wait 30-60 seconds</p>
  <div class="spinner"></div>
</div>
```

### 2. Optimize Startup
- Reduce model file sizes if possible
- Use lazy loading for non-critical models
- Add startup health check endpoint

### 3. Use Health Endpoint
Create `/api/health` endpoint (you already have this) to check if app is ready:
```javascript
// Check if app is ready before showing main UI
async function waitForApp() {
    while (true) {
        try {
            const response = await fetch('/api/health');
            if (response.ok) {
                return true; // App is ready!
            }
        } catch (e) {
            // Still loading...
        }
        await new Promise(r => setTimeout(r, 2000)); // Wait 2 seconds
    }
}
```

## 🔧 Quick Fix: Keep App Alive Script

**Add to your project: `scripts/keep_alive.py`:**

```python
import requests
import time
from datetime import datetime

APP_URL = "https://your-app-name.onrender.com/api/health"

def ping():
    try:
        r = requests.get(APP_URL, timeout=10)
        print(f"[{datetime.now()}] ✅ App is alive! Status: {r.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {e}")

if __name__ == "__main__":
    print("🔄 Starting keep-alive script...")
    print(f"📡 Pinging: {APP_URL}")
    print("⏰ Will ping every 10 minutes\n")
    
    while True:
        ping()
        time.sleep(600)  # 10 minutes
```

**Run this 24/7 on:**
- Your computer (when it's on)
- A Raspberry Pi
- A free cloud service (Google Cloud Run, AWS Lambda with scheduler)
- UptimeRobot or similar service

## 📝 Summary

**Why it's slow:**
- Free tier spins down after 15 min
- Cold start takes 30-60 seconds
- Models need to load each time

**How to fix:**
- Use keep-alive service (free)
- Optimize model loading
- Upgrade to paid tier ($7/month)
- Switch to faster platform

**For now:**
- First visit: Wait 30-60 seconds (normal!)
- Next visits: Instant (if within 15 min)
- Set up keep-alive to prevent spin-down

Your app is working correctly - this is just how Render's free tier behaves! 🎉

