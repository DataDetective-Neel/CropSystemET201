
# mobile_app/run_mobile_app.py
# Launcher script for the mobile app
# Run with: python mobile_app/run_mobile_app.py

import os
import sys

# Add parent directory to path to access models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mobile_app.app_api import app

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌾 AgriAI Crop - Mobile App")
    print("="*50)
    print("\n📱 Mobile App Server Starting...")
    print("🔗 Access at: http://127.0.0.1:5001")
    print("📱 Or on your network: http://[YOUR_IP]:5001")
    print("\n💡 To install on mobile:")
    print("   1. Open this URL on your mobile device")
    print("   2. Add to Home Screen (iOS) or Install App (Android)")
    print("\n" + "="*50 + "\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')

