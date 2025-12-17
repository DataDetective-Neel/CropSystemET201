# mobile_app/app_api.py
# Flask API Backend for Mobile App
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
from datetime import datetime
from mobile_app.crop_predictor import CropPredictor

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)  # Enable CORS for mobile app

# Initialize the AI predictor
crop_predictor = CropPredictor(models_base_path='models')

@app.route('/')
def index():
    """Serve mobile app"""
    return send_file(os.path.join(STATIC_DIR, 'index.html'))

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(STATIC_DIR, filename)

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for crop prediction"""
    try:
        data = request.json
        
        # Add default values
        defaults = {
            'pH': 7.0,
            'SoilType': 'Clay', 
            'Irrigation': 'Irrigated'
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        # Make predictions using AI models
        results = crop_predictor.predict_all_models(data)
        
        return jsonify({
            'success': True,
            'predictions': results,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'analysis_id': f"ANA{datetime.now().strftime('%Y%m%d%H%M%S')}"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': crop_predictor.models_loaded
    })

if __name__ == '__main__':
    os.makedirs('mobile_app/static', exist_ok=True)
    print("🚀 Mobile App API Server Starting...")
    print("📱 Mobile app will be available at: http://127.0.0.1:5001")
    app.run(debug=True, port=5001, host='0.0.0.0')

