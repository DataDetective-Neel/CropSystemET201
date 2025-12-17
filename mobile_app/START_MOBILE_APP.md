# 🚀 How to Start the Mobile App

## Windows Users (Quick Method)

### Option 1: Double-click (Easiest)
1. Navigate to `mobile_app` folder
2. Double-click `run_mobile_app.bat`

### Option 2: Command Line
```cmd
python mobile_app\run_mobile_app.py
```

Or from the mobile_app directory:
```cmd
cd mobile_app
python run_mobile_app.py
```

## Mac/Linux Users

```bash
python3 mobile_app/run_mobile_app.py
```

Or make it executable:
```bash
chmod +x mobile_app/run_mobile_app.py
python3 mobile_app/run_mobile_app.py
```

## Alternative: Run Directly

You can also run the API file directly:

```bash
python mobile_app/app_api.py
```

## 📱 Then Access on Your Phone

1. Find your computer's IP address:
   - **Windows**: Open Command Prompt, type `ipconfig`, look for "IPv4 Address"
   - **Mac/Linux**: Open Terminal, type `ifconfig` or `ip addr`

2. On your phone's browser, go to:
   ```
   http://[YOUR_IP]:5001
   ```
   Example: `http://192.168.1.100:5001`

3. Install the app:
   - **iPhone**: Share button → "Add to Home Screen"
   - **Android**: Menu → "Install App"

## ✅ Success!

You should see:
```
==================================================
🌾 AgriAI Crop - Mobile App
==================================================

📱 Mobile App Server Starting...
🔗 Access at: http://127.0.0.1:5001
...
```

The mobile app is now running! 🎉

