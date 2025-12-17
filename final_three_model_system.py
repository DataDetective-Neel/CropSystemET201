# final_three_model_system.py - FIXED VERSION
import joblib
import pandas as pd
import numpy as np
import os

class FinalThreeModelSystem:
    def __init__(self):
        print("🚀 INITIALIZING 3-MODEL CROP SYSTEM")
        print("=" * 50)
        
        self.models_loaded = {
            'model1': False,
            'model2': False, 
            'model3': False
        }
        
        # Load Model 1: Your high-accuracy model
        try:
            self.model1 = joblib.load('models/legacy/crop_classifier_model.pkl')
            self.scaler1 = joblib.load('models/legacy/scaler_clf.pkl')
            self.encoder1 = joblib.load('models/legacy/label_encoder.pkl')
            
            # Check what features Model 1 expects
            try:
                self.model1_features = joblib.load('models/legacy/crop_features.pkl')
                print(f"✅ MODEL 1: Features loaded - {self.model1_features}")
            except:
                print("⚠️ MODEL 1: Using default feature order")
                self.model1_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'moisture', 'region_encoded']
            
            self.models_loaded['model1'] = True
            print("✅ MODEL 1: High-Accuracy (99.2%) - LOADED")
        except Exception as e:
            print(f"❌ MODEL 1: Not available - {e}")
        
        # Load Model 2: Your existing regional models
        self.regional_models = {}
        regions = ['punjab', 'haryana', 'rajasthan']
        for region in regions:
            try:
                # Try improved version first
                model_data = joblib.load(f'models/regional/{region}_improved_model.pkl')
                self.regional_models[region] = model_data
                print(f"✅ MODEL 2: {region.title()} Regional - LOADED")
            except:
                try:
                    # Fallback to regular version
                    model_data = joblib.load(f'models/regional/{region}_model.pkl')
                    self.regional_models[region] = model_data
                    print(f"✅ MODEL 2: {region.title()} Regional - LOADED")
                except Exception as e:
                    print(f"❌ MODEL 2: {region.title()} Regional - Failed")
        
        if self.regional_models:
            self.models_loaded['model2'] = True
        
        # Load Model 3: Seasonal models
        self.seasonal_models = {}
        seasons = ['rabi', 'kharif', 'zaid']
        for season in seasons:
            try:
                model_data = joblib.load(f'models/seasonal/{season}_model.pkl')
                self.seasonal_models[season] = model_data
                print(f"✅ MODEL 3: {season.title()} Seasonal - LOADED")
            except Exception as e:
                print(f"❌ MODEL 3: {season.title()} Seasonal - Not trained yet")
        
        if self.seasonal_models:
            self.models_loaded['model3'] = True
    
    def predict_model1(self, features):
        """Use your high-accuracy model with correct features"""
        if not self.models_loaded['model1']:
            return "Model 1 not available"
        
        try:
            # Create proper feature array for Model 1
            # Based on the error, Model 1 expects 9 features
            feature_mapping = {
                'N': features['N'],
                'P': features['P'], 
                'K': features['K'],
                'temperature': features['Temperature'],
                'humidity': features['Humidity'],
                'ph': features['pH'],
                'rainfall': features['Rainfall'],
                'moisture': features.get('Moisture', 20),  # Default if missing
                'region_encoded': 0  # Default region encoding
            }
            
            # Create feature array in correct order
            feature_array = [[
                feature_mapping['N'],
                feature_mapping['P'], 
                feature_mapping['K'],
                feature_mapping['temperature'],
                feature_mapping['humidity'],
                feature_mapping['ph'],
                feature_mapping['rainfall'],
                feature_mapping['moisture'],
                feature_mapping['region_encoded']
            ]]
            
            features_scaled = self.scaler1.transform(feature_array)
            prediction = self.model1.predict(features_scaled)[0]
            crop_name = self.encoder1.inverse_transform([prediction])[0]
            
            return {
                'crop': crop_name,
                'confidence': '99.2% (trained accuracy)',
                'model_type': 'High-Accuracy General Model',
                'features_used': len(feature_array[0])
            }
        except Exception as e:
            return f"Model 1 error: {e}"
    
    def predict_model2(self, features):
        """Use regional specialized models with correct features"""
        if not self.models_loaded['model2']:
            return "Model 2 not available"
        
        region = features.get('region', 'punjab').lower()
        if region not in self.regional_models:
            return f"No regional model for {region}"
        
        try:
            model_data = self.regional_models[region]
            model = model_data['model']
            
            # For improved models, they expect enhanced features
            if 'improved' in [f for f in os.listdir('models/regional') if region in f and 'improved' in f][0]:
                # Improved model expects 17 features - create enhanced features
                enhanced_features = self.create_enhanced_features(features)
                feature_array = [enhanced_features]
            else:
                # Regular model expects basic features
                feature_array = [[
                    features['N'], features['P'], features['K'], features['pH'],
                    features['Temperature'], features['Humidity'], features['Rainfall'], 
                    features['Moisture']
                ]]
            
            prediction = model.predict(feature_array)[0]
            probability = model.predict_proba(feature_array)[0]
            
            if 'encoder' in model_data:
                crop_name = model_data['encoder'].inverse_transform([prediction])[0]
            else:
                crop_name = f"Crop_{prediction}"
            
            confidence = np.max(probability)
            
            return {
                'crop': crop_name,
                'confidence': f"{confidence:.1%}",
                'model_type': f'{region.title()} Regional Model',
                'features_used': len(feature_array[0])
            }
        except Exception as e:
            return f"Model 2 error: {e}"
    
    def create_enhanced_features(self, features):
        """Create enhanced features for improved models"""
        # Calculate all the enhanced features
        NP_ratio = features['N'] / (features['P'] + 1)
        NK_ratio = features['N'] / (features['K'] + 1)
        PK_ratio = features['P'] / (features['K'] + 1)
        temp_humidity_index = features['Temperature'] * features['Humidity'] / 100
        rainfall_moisture_balance = features['Rainfall'] / (features['Moisture'] + 1)
        soil_suitability = features['pH'] * features['Moisture'] / 10
        
        # Season encoding
        season_strength = {'Rabi': 1, 'Kharif': 2, 'Zaid': 3}
        season_str = season_strength.get(features.get('season', 'Rabi'), 1)
        
        # Soil type encoding (simplified)
        soil_encoding = {'Clay': 0, 'Sandy': 1, 'Loamy': 2}
        soil_encoded = soil_encoding.get(features.get('SoilType', 'Clay'), 0)
        
        # Irrigation encoding
        irrig_encoding = {'Rainfed': 0, 'Irrigated': 1}
        irrig_encoded = irrig_encoding.get(features.get('Irrigation', 'Irrigated'), 1)
        
        # Return all 17 features in correct order
        return [
            features['N'], features['P'], features['K'], features['pH'],
            features['Temperature'], features['Humidity'], features['Rainfall'], 
            features['Moisture'], NP_ratio, NK_ratio, PK_ratio, 
            temp_humidity_index, rainfall_moisture_balance, soil_suitability,
            season_str, soil_encoded, irrig_encoded
        ]
    
    def predict_model3(self, features):
        """Use seasonal specialized models"""
        if not self.models_loaded['model3']:
            return "Model 3 not available"
        
        season = features.get('season', 'rabi').lower()
        if season not in self.seasonal_models:
            return f"No seasonal model for {season}"
        
        try:
            model_data = self.seasonal_models[season]
            model = model_data['model']
            encoder = model_data['encoder']
            
            # Prepare features for seasonal model (8 basic features)
            feature_array = [[
                features['N'], features['P'], features['K'], features['pH'],
                features['Temperature'], features['Humidity'], features['Rainfall'], 
                features['Moisture']
            ]]
            
            prediction = model.predict(feature_array)[0]
            probability = model.predict_proba(feature_array)[0]
            crop_name = encoder.inverse_transform([prediction])[0]
            confidence = np.max(probability)
            
            return {
                'crop': crop_name,
                'confidence': f"{confidence:.1%}",
                'model_type': f'{season.title()} Seasonal Model',
                'features_used': len(feature_array[0])
            }
        except Exception as e:
            return f"Model 3 error: {e}"
    
    def predict_all_models(self, features):
        """Get predictions from all 3 models"""
        print(f"\n🎯 GETTING PREDICTIONS FROM 3 MODELS")
        print("=" * 40)
        
        results = {}
        
        results['model1_general'] = self.predict_model1(features)
        results['model2_regional'] = self.predict_model2(features) 
        results['model3_seasonal'] = self.predict_model3(features)
        
        return results

def main():
    # Initialize the complete system
    system = FinalThreeModelSystem()
    
    print(f"\n📊 SYSTEM SUMMARY:")
    print(f"   Model 1 (General): {'✅ LOADED' if system.models_loaded['model1'] else '❌ MISSING'}")
    print(f"   Model 2 (Regional): {'✅ LOADED' if system.models_loaded['model2'] else '❌ MISSING'}")
    print(f"   Model 3 (Seasonal): {'✅ LOADED' if system.models_loaded['model3'] else '❌ MISSING'}")
    
    # Test the system with complete features
    test_features = {
        'N': 100, 'P': 50, 'K': 40, 'pH': 7.0,
        'Temperature': 25, 'Humidity': 60, 'Rainfall': 100, 'Moisture': 20,
        'region': 'Punjab', 'season': 'Rabi',
        'SoilType': 'Clay', 'Irrigation': 'Irrigated'
    }
    
    results = system.predict_all_models(test_features)
    
    print(f"\n🧪 PREDICTION RESULTS:")
    for model_name, result in results.items():
        print(f"\n   {model_name.upper()}:")
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"      {key}: {value}")
        else:
            print(f"      {result}")

if __name__ == "__main__":
    main()