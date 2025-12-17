# 📜 Scripts Directory

## keep_alive.py

Keeps your Render.com app awake by pinging it every 10 minutes.

### Usage:

1. **Edit the script** - Change `APP_URL` to your Render app URL:
   ```python
   APP_URL = "https://your-app-name.onrender.com/api/health"
   ```

2. **Install requests** (if not already installed):
   ```bash
   pip install requests
   ```

3. **Run the script**:
   ```bash
   python scripts/keep_alive.py
   ```

4. **Keep it running** - Leave this script running on:
   - Your computer (when it's on)
   - A server
   - Or use a free service like UptimeRobot

### Alternative: Use UptimeRobot (Easier!)

1. Go to https://uptimerobot.com (free account)
2. Add a new monitor
3. Type: HTTP(s)
4. URL: `https://your-app.onrender.com/api/health`
5. Interval: Every 5 minutes
6. Done! No script needed!

This is easier than running the script yourself.

