# 📱 AgriAI Crop - Mobile App

A Progressive Web App (PWA) mobile application for crop recommendation using AI/ML models.

## 🚀 Features

- **Mobile-Optimized UI** - Beautiful, responsive design for smartphones
- **Offline Support** - Works with service worker caching
- **Installable** - Can be installed on iOS and Android devices
- **AI Models** - Uses the same 3-model prediction system:
  - Master Model (99.2% accuracy)
  - Regional Model (Punjab, Haryana, Rajasthan)
  - Seasonal Model (Rabi, Kharif, Zaid)
- **Real-time Predictions** - Get instant crop recommendations

## 📋 Requirements

Same as main project:
- Python 3.11+
- Flask
- scikit-learn
- joblib
- numpy
- pandas

## 🏃 Running the Mobile App

### Option 1: Run Mobile App API (Recommended)
```bash
python mobile_app/run_mobile_app.py
```

### Option 2: Run from main directory
```bash
cd mobile_app
python app_api.py
```

### Option 3: Import and run
```python
from mobile_app.app_api import app
app.run(port=5001, host='0.0.0.0')
```

## 📱 Accessing on Mobile Device

1. **Find your computer's IP address:**
   - Windows: `ipconfig` (look for IPv4 address)
   - Mac/Linux: `ifconfig` or `ip addr`

2. **On your mobile device:**
   - Open browser
   - Go to: `http://[YOUR_IP]:5001`
   - Example: `http://192.168.1.100:5001`

3. **Install as App:**
   - **iOS (Safari)**: Share button → "Add to Home Screen"
   - **Android (Chrome)**: Menu → "Install App" or "Add to Home Screen"

## 🌐 Deploying Mobile App

The mobile app can be deployed alongside the web app or separately.

### Deploy with Main App

The mobile app API uses port 5001 by default. Update the start command:

**For Render.com:**
```yaml
# In render.yaml, add another service:
services:
  - type: web
    name: crop-system-mobile
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: cd mobile_app && python app_api.py
    envVars:
      - key: PORT
        fromService:
          type: web
          property: port
```

**Or use environment variable for PORT:**
```python
# In app_api.py, change:
port = int(os.environ.get('PORT', 5001))
```

### Deploy Separately

1. Push to GitHub
2. Deploy `mobile_app/app_api.py` as a separate service
3. Update API_BASE in `index.html` if needed

## 📁 File Structure

```
mobile_app/
├── __init__.py
├── crop_predictor.py      # AI model logic (extracted)
├── app_api.py             # Flask API backend
├── run_mobile_app.py      # Launcher script
├── static/
│   ├── index.html         # Mobile app UI
│   ├── manifest.json      # PWA manifest
│   ├── service-worker.js  # Offline support
│   ├── icon-192.png       # App icon (192x192)
│   └── icon-512.png       # App icon (512x512)
└── README.md
```

## 🎨 Customization

### Change Port
Edit `mobile_app/app_api.py`:
```python
app.run(debug=True, port=YOUR_PORT, host='0.0.0.0')
```

### Change API URL
Edit `mobile_app/static/index.html`:
```javascript
const API_BASE = 'https://your-api-url.com';
```

### Add Icons
Replace `icon-192.png` and `icon-512.png` in `mobile_app/static/` with your own icons.

## 🔧 API Endpoints

- `GET /` - Serve mobile app UI
- `POST /api/predict` - Get crop predictions
  ```json
  {
    "region": "punjab",
    "season": "kharif",
    "N": 120,
    "P": 60,
    "K": 45,
    "Temperature": 28,
    "Humidity": 65,
    "Rainfall": 150,
    "pH": 7.2
  }
  ```
- `GET /api/health` - Health check

## 📱 Mobile App Features

✅ **Responsive Design** - Works on all screen sizes  
✅ **Touch Optimized** - Large buttons, easy inputs  
✅ **Offline Ready** - Service worker for offline access  
✅ **Installable** - Can be installed on home screen  
✅ **Fast** - Optimized for mobile networks  
✅ **Modern UI** - Beautiful gradient design  

## 🐛 Troubleshooting

**App not loading on mobile?**
- Check firewall allows port 5001
- Ensure mobile device is on same network
- Try accessing from computer's IP address directly

**Install button not showing?**
- Ensure you're using HTTPS (or localhost)
- Check manifest.json is accessible
- Verify service worker is registered

**Predictions not working?**
- Check models are in correct path
- Verify API endpoint is correct
- Check browser console for errors

## 📝 Notes

- The mobile app uses the same AI models as the web app
- Models are loaded from `models/` directory (parent directory)
- The app is a Progressive Web App (PWA) - no app store needed!
- Works on iOS 11.3+ and Android 5+

## 🎉 Enjoy Your Mobile App!

The mobile app is now ready to use. Share the URL with farmers and they can install it on their phones for easy access!

