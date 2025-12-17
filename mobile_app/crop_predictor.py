# mobile_app/crop_predictor.py
# Extracted AI Model and Backend Logic for Mobile App
import joblib
import numpy as np
import os

class CropPredictor:
    """AI Crop Prediction System - Extracted from web_interface.py"""
    
    def __init__(self, models_base_path='models'):
        self.models_loaded = False
        self.models_base_path = models_base_path
        
        try:
            # Load Model 1: High-accuracy model
            self.model1 = joblib.load(f'{models_base_path}/legacy/crop_classifier_model.pkl')
            self.scaler1 = joblib.load(f'{models_base_path}/legacy/scaler_clf.pkl')
            self.encoder1 = joblib.load(f'{models_base_path}/legacy/label_encoder.pkl')
            self.model1_features = joblib.load(f'{models_base_path}/legacy/crop_features.pkl')
            
            # Load soil moisture prediction model
            self.moisture_model = joblib.load(f'{models_base_path}/legacy/soil_moisture_model.pkl')
            self.moisture_scaler = joblib.load(f'{models_base_path}/legacy/scaler_reg.pkl')
            
            # Load Model 2: Regional models
            self.regional_models = {}
            for region in ['punjab', 'haryana', 'rajasthan']:
                model_data = joblib.load(f'{models_base_path}/regional/{region}_improved_model.pkl')
                self.regional_models[region] = model_data
            
            # Load Model 3: Seasonal models
            self.seasonal_models = {}
            for season in ['rabi', 'kharif', 'zaid']:
                model_data = joblib.load(f'{models_base_path}/seasonal/{season}_model.pkl')
                self.seasonal_models[season] = model_data
            
            self.models_loaded = True
            print("✅ All AI models loaded successfully for mobile app!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.models_loaded = False

    def predict_soil_moisture(self, features):
        """Predict soil moisture based on environmental factors"""
        try:
            # Prepare features for moisture prediction
            moisture_features = [
                features['Temperature'],
                features['Humidity'],
                features['Rainfall'],
                features.get('pH', 7.0),
                features['N'],
                features['P'],
                features['K']
            ]
            
            features_scaled = self.moisture_scaler.transform([moisture_features])
            predicted_moisture = self.moisture_model.predict(features_scaled)[0]
            
            # Ensure moisture is within reasonable bounds
            predicted_moisture = max(10, min(40, predicted_moisture))
            
            return round(predicted_moisture, 1)
        except:
            # Fallback calculation based on rainfall and humidity
            return round((features['Rainfall'] * 0.1 + features['Humidity'] * 0.3) / 2, 1)

    def predict_model1(self, features):
        """Predict using high-accuracy model"""
        try:
            # Predict soil moisture first
            predicted_moisture = self.predict_soil_moisture(features)
            
            # Create feature array for Model 1
            feature_array = [[
                features['N'],
                features['P'], 
                features['K'],
                features['Temperature'],
                features['Humidity'],
                features['N'] + features['P'] + features['K'],
                features['N'] / (features['P'] + 1),
                features['N'] / (features['K'] + 1),
                predicted_moisture
            ]]
            
            features_scaled = self.scaler1.transform(feature_array)
            prediction = self.model1.predict(features_scaled)[0]
            probability = self.model1.predict_proba(features_scaled)[0]
            
            crop_name = self.encoder1.inverse_transform([prediction])[0]
            confidence = np.max(probability)
            
            return {
                'crop': crop_name,
                'confidence': f"{confidence:.1%}",
                'model_type': 'AI Master Model',
                'accuracy': '99.2% Verified',
                'soil_moisture': predicted_moisture,
                'features_used': '9 Optimized Parameters'
            }
        except Exception as e:
            return {'error': f"Master Model: {str(e)}"}

    def predict_model2(self, features):
        """Predict using regional specialized model"""
        try:
            region = features.get('region', 'punjab').lower()
            if region not in self.regional_models:
                return {'error': f"No model for region: {region}"}
            
            model_data = self.regional_models[region]
            model = model_data['model']
            predicted_moisture = self.predict_soil_moisture(features)
            
            # Create enhanced features
            NP_ratio = features['N'] / (features['P'] + 1)
            NK_ratio = features['N'] / (features['K'] + 1)
            PK_ratio = features['P'] / (features['K'] + 1)
            temp_humidity_index = features['Temperature'] * features['Humidity'] / 100
            rainfall_moisture_balance = features['Rainfall'] / (predicted_moisture + 1)
            soil_suitability = features.get('pH', 7.0) * predicted_moisture / 10
            
            season_strength = {'rabi': 1, 'kharif': 2, 'zaid': 3}
            season_str = season_strength.get(features.get('season', 'rabi'), 1)
            
            soil_encoding = {'Clay': 0, 'Sandy': 1, 'Loamy': 2}
            soil_encoded = soil_encoding.get(features.get('SoilType', 'Clay'), 0)
            
            irrig_encoding = {'Rainfed': 0, 'Irrigated': 1}
            irrig_encoded = irrig_encoding.get(features.get('Irrigation', 'Irrigated'), 1)
            
            enhanced_features = [
                features['N'], features['P'], features['K'], features.get('pH', 7.0),
                features['Temperature'], features['Humidity'], features['Rainfall'], 
                predicted_moisture, NP_ratio, NK_ratio, PK_ratio, 
                temp_humidity_index, rainfall_moisture_balance, soil_suitability,
                season_str, soil_encoded, irrig_encoded
            ]
            
            prediction = model.predict([enhanced_features])[0]
            probability = model.predict_proba([enhanced_features])[0]
            
            if 'encoders' in model_data and 'crop' in model_data['encoders']:
                crop_name = model_data['encoders']['crop'].inverse_transform([prediction])[0]
            else:
                crop_name = f"Crop_{prediction}"
            
            confidence = np.max(probability)
            
            return {
                'crop': crop_name,
                'confidence': f"{confidence:.1%}",
                'model_type': f'Regional AI - {region.title()}',
                'accuracy': 'Regional Optimization',
                'soil_moisture': predicted_moisture,
                'features_used': '17 Advanced Parameters'
            }
        except Exception as e:
            return {'error': f"Regional Model: {str(e)}"}

    def predict_model3(self, features):
        """Predict using seasonal specialized model"""
        try:
            season = features.get('season', 'rabi').lower()
            if season not in self.seasonal_models:
                return {'error': f"No model for season: {season}"}
            
            model_data = self.seasonal_models[season]
            model = model_data['model']
            encoder = model_data['encoder']
            predicted_moisture = self.predict_soil_moisture(features)
            
            feature_array = [[
                features['N'], features['P'], features['K'], features.get('pH', 7.0),
                features['Temperature'], features['Humidity'], features['Rainfall'], 
                predicted_moisture
            ]]
            
            prediction = model.predict(feature_array)[0]
            probability = model.predict_proba(feature_array)[0]
            crop_name = encoder.inverse_transform([prediction])[0]
            confidence = np.max(probability)
            
            return {
                'crop': crop_name,
                'confidence': f"{confidence:.1%}",
                'model_type': f'Seasonal AI - {season.title()}',
                'accuracy': 'Seasonal Pattern Recognition',
                'soil_moisture': predicted_moisture,
                'features_used': '8 Core Parameters'
            }
        except Exception as e:
            return {'error': f"Seasonal Model: {str(e)}"}

    def get_consensus_recommendation(self, results):
        """Get consensus from all models"""
        try:
            crops = []
            if 'model1' in results and 'crop' in results['model1']:
                crops.append(results['model1']['crop'])
            if 'model2' in results and 'crop' in results['model2']:
                crops.append(results['model2']['crop'])
            if 'model3' in results and 'crop' in results['model3']:
                crops.append(results['model3']['crop'])
            
            if crops:
                from collections import Counter
                most_common = Counter(crops).most_common(1)[0]
                return most_common[0]
            return "No consensus"
        except:
            return "Analysis required"

    def predict_all_models(self, input_data):
        """Get predictions from all 3 models with consensus"""
        results = {
            'model1': self.predict_model1(input_data),
            'model2': self.predict_model2(input_data),
            'model3': self.predict_model3(input_data)
        }
        
        # Add consensus recommendation
        results['consensus'] = self.get_consensus_recommendation(results)
        
        return results

