# scripts/keep_alive.py
# Keeps Render.com app awake by pinging it every 10 minutes
# Run this script to prevent your app from spinning down

import requests
import time
from datetime import datetime

# CHANGE THIS to your Render app URL
APP_URL = "https://crop-system-1.onrender.com/api/health"

def ping_app():
    """Ping the app to keep it awake"""
    try:
        response = requests.get(APP_URL, timeout=10)
        status = response.status_code
        if status == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ App is alive! Status: {status}")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ App responded with status: {status}")
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏰ Request timed out (app might be waking up)")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔄 Render.com Keep-Alive Script")
    print("="*60)
    print(f"📡 App URL: {APP_URL}")
    print("⏰ Ping interval: Every 10 minutes")
    print("💡 This will prevent your app from spinning down")
    print("⚠️  Keep this script running to maintain app availability")
    print("="*60 + "\n")
    
    # Ping immediately
    ping_app()
    
    # Then ping every 10 minutes (600 seconds)
    while True:
        time.sleep(600)  # Wait 10 minutes
        ping_app()

