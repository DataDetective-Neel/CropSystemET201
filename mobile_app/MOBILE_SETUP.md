# 📱 Quick Setup Guide for Mobile App

## 🚀 Running the Mobile App

### Step 1: Run the Mobile App Server

```bash
python mobile_app/run_mobile_app.py
```

The server will start on `http://127.0.0.1:5001`

### Step 2: Access on Your Phone

1. **Find your computer's IP address:**
   ```bash
   # Windows
   ipconfig
   # Look for "IPv4 Address" - something like 192.168.1.100
   
   # Mac/Linux
   ifconfig
   # Look for inet address under your network interface
   ```

2. **On your mobile device:**
   - Make sure your phone is on the same WiFi network
   - Open browser (Safari on iOS, Chrome on Android)
   - Go to: `http://[YOUR_IP]:5001`
   - Example: `http://192.168.1.100:5001`

3. **Install the App:**
   - **iPhone (Safari)**: 
     - Tap Share button (square with arrow)
     - Select "Add to Home Screen"
     - Tap "Add"
   
   - **Android (Chrome)**:
     - Tap menu (3 dots)
     - Select "Install app" or "Add to Home screen"
     - Tap "Install"

## 🎨 Create App Icons (Optional)

If you want to create placeholder icons:

```bash
pip install Pillow
python mobile_app/create_icons.py
```

Or replace `mobile_app/static/icon-192.png` and `icon-512.png` with your own 192x192 and 512x512 images.

## 📋 What You Get

✅ **Mobile-optimized interface**  
✅ **Same AI models** as the web app  
✅ **Offline support** (cached)  
✅ **Installable** on iOS and Android  
✅ **Beautiful UI** designed for touch  

## 🔧 Troubleshooting

**Can't access from phone?**
- Check firewall allows port 5001
- Ensure phone and computer are on same WiFi
- Try disabling firewall temporarily

**Install button not showing?**
- Use HTTPS if deploying (or localhost)
- Check browser supports PWA (Chrome, Safari)

**Icons not showing?**
- Run `create_icons.py` to generate placeholder icons
- Or add your own icons to `mobile_app/static/`

## 📱 Usage

Once installed:
1. Open the app from your home screen
2. Fill in soil parameters
3. Select region and season
4. Tap "Analyze Crop"
5. Get AI-powered recommendations!

Enjoy your mobile crop recommendation app! 🌾

