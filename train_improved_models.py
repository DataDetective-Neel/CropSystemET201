# train_improved_models.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class ImprovedCropTrainer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
    def load_regional_data(self, region_name):
        """Load and enhance regional data"""
        file_path = f"data/processed/{region_name.lower()}_data.csv"
        df = pd.read_csv(file_path)
        
        # Create better features
        df = self.create_better_features(df)
        return df
    
    def create_better_features(self, df):
        """Create enhanced features for better prediction"""
        # Nutrient ratios
        df['NP_ratio'] = df['N'] / (df['P'] + 1)  # +1 to avoid division by zero
        df['NK_ratio'] = df['N'] / (df['K'] + 1)
        df['PK_ratio'] = df['P'] / (df['K'] + 1)
        
        # Climate indices
        df['temp_humidity_index'] = df['Temperature'] * df['Humidity'] / 100
        df['rainfall_moisture_balance'] = df['Rainfall'] / (df['Moisture'] + 1)
        
        # Soil suitability score
        df['soil_suitability'] = df['pH'] * df['Moisture'] / 10
        
        # Season encoding (more meaningful)
        season_strength = {'Rabi': 1, 'Kharif': 2, 'Zaid': 3}
        df['season_strength'] = df['Season'].map(season_strength)
        
        return df
    
    def train_region_model(self, region_name):
        """Train improved model for specific region"""
        print(f"\n🚀 Training IMPROVED model for {region_name}...")
        
        # Load enhanced data
        df = self.load_regional_data(region_name)
        print(f"   Data shape after feature engineering: {df.shape}")
        
        # Enhanced feature set
        features = [
            'N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture',
            'NP_ratio', 'NK_ratio', 'PK_ratio', 'temp_humidity_index', 
            'rainfall_moisture_balance', 'soil_suitability', 'season_strength',
            'SoilType', 'Irrigation'
        ]
        
        target = 'Crop'
        
        # Prepare features
        X = df[features].copy()
        y = df[target]
        
        # Encode categorical variables
        label_encoders = {}
        for col in ['SoilType', 'Irrigation']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le
        
        # Encode target
        le_crop = LabelEncoder()
        y_encoded = le_crop.fit_transform(y)
        
        # Scale features
        scaler = StandardScaler()
        numerical_features = [f for f in features if f not in ['SoilType', 'Irrigation']]
        X[numerical_features] = scaler.fit_transform(X[numerical_features])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train IMPROVED model with better parameters
        model = RandomForestClassifier(
            n_estimators=200,           # More trees
            max_depth=15,               # Deeper trees
            min_samples_split=5,        # Better generalization
            min_samples_leaf=2,
            max_features='sqrt',        # Better feature selection
            random_state=42,
            class_weight='balanced'     # Handle any class imbalance
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation for better accuracy estimate
        cv_scores = cross_val_score(model, X, y_encoded, cv=5)
        
        print(f"✅ {region_name} IMPROVED model trained!")
        print(f"   Accuracy: {accuracy:.2%}")
        print(f"   Cross-validation: {cv_scores.mean():.2%} (+/- {cv_scores.std() * 2:.2%})")
        print(f"   Features used: {len(features)}")
        print(f"   Crops: {list(le_crop.classes_)}")
        
        # Store components
        self.models[region_name] = model
        self.scalers[region_name] = scaler
        self.encoders[region_name] = {
            'soil': label_encoders['SoilType'],
            'irrigation': label_encoders['Irrigation'],
            'crop': le_crop
        }
        
        return accuracy, cv_scores.mean()
    
    def save_models(self):
        """Save all improved models"""
        print(f"\n💾 Saving IMPROVED models...")
        
        for region in self.models:
            model_data = {
                'model': self.models[region],
                'scaler': self.scalers[region],
                'encoders': self.encoders[region],
                'feature_names': self.get_feature_names()
            }
            
            file_path = f"models/regional/{region.lower()}_improved_model.pkl"
            joblib.dump(model_data, file_path)
            print(f"✅ Saved {region} improved model")
    
    def get_feature_names(self):
        """Return the enhanced feature names"""
        return [
            'N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture',
            'NP_ratio', 'NK_ratio', 'PK_ratio', 'temp_humidity_index', 
            'rainfall_moisture_balance', 'soil_suitability', 'season_strength',
            'SoilType', 'Irrigation'
        ]
    
    def predict_crop(self, region_name, input_features):
        """Predict crop with improved model"""
        if region_name not in self.models:
            print(f"❌ No model found for {region_name}")
            return None
        
        model = self.models[region_name]
        scaler = self.scalers[region_name]
        encoders = self.encoders[region_name]
        
        # Prepare input with enhanced features
        input_df = self.create_input_features(input_features)
        
        # Encode categorical features
        for col in ['SoilType', 'Irrigation']:
            le = encoders['soil' if col == 'SoilType' else 'irrigation']
            input_df[col] = le.transform([input_features[col]])[0]
        
        # Scale features
        numerical_features = [f for f in self.get_feature_names() if f not in ['SoilType', 'Irrigation']]
        input_df[numerical_features] = scaler.transform(input_df[numerical_features])
        
        # Predict
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        predicted_crop = encoders['crop'].inverse_transform([prediction])[0]
        confidence = np.max(probability)
        
        # Get top 3 recommendations with better formatting
        top_3_idx = np.argsort(probability)[-3:][::-1]
        top_3_crops = encoders['crop'].inverse_transform(top_3_idx)
        top_3_confidences = [f"{prob:.1%}" for prob in probability[top_3_idx]]
        
        recommendations = list(zip(top_3_crops, top_3_confidences))
        
        return {
            'predicted_crop': predicted_crop,
            'confidence': f"{confidence:.1%}",
            'top_recommendations': recommendations,
            'all_probabilities': {
                crop: f"{prob:.1%}" 
                for crop, prob in zip(encoders['crop'].classes_, probability)
            }
        }
    
    def create_input_features(self, input_features):
        """Create enhanced features for prediction input"""
        base = input_features.copy()
        
        # Calculate enhanced features
        base['NP_ratio'] = base['N'] / (base['P'] + 1)
        base['NK_ratio'] = base['N'] / (base['K'] + 1)
        base['PK_ratio'] = base['P'] / (base['K'] + 1)
        base['temp_humidity_index'] = base['Temperature'] * base['Humidity'] / 100
        base['rainfall_moisture_balance'] = base['Rainfall'] / (base['Moisture'] + 1)
        base['soil_suitability'] = base['pH'] * base['Moisture'] / 10
        
        # Season encoding
        season_strength = {'Rabi': 1, 'Kharif': 2, 'Zaid': 3}
        base['season_strength'] = season_strength[base['Season']]
        
        # Create DataFrame with all features
        feature_names = self.get_feature_names()
        input_df = pd.DataFrame({feature: [base[feature]] for feature in feature_names})
        
        return input_df

def main():
    print("🌾 IMPROVED REGIONAL CROP MODEL TRAINING")
    print("=" * 60)
    
    trainer = ImprovedCropTrainer()
    
    regions = ['Punjab', 'Haryana', 'Rajasthan']
    results = {}
    
    # Train improved models for all regions
    for region in regions:
        accuracy, cv_score = trainer.train_region_model(region)
        results[region] = {'accuracy': accuracy, 'cv_score': cv_score}
    
    # Save all improved models
    trainer.save_models()
    
    # Test predictions with realistic data
    print(f"\n🧪 TESTING IMPROVED PREDICTIONS")
    print("=" * 60)
    
    # Realistic test cases for different seasons
    test_cases = [
        {
            'name': 'Rabi Season (Winter)',
            'features': {
                'N': 120, 'P': 45, 'K': 35, 'pH': 7.2, 
                'Temperature': 18, 'Humidity': 65, 'Rainfall': 50, 'Moisture': 22,
                'Season': 'Rabi', 'SoilType': 'Clay', 'Irrigation': 'Irrigated'
            }
        },
        {
            'name': 'Kharif Season (Monsoon)',
            'features': {
                'N': 110, 'P': 55, 'K': 45, 'pH': 6.8, 
                'Temperature': 30, 'Humidity': 80, 'Rainfall': 200, 'Moisture': 35,
                'Season': 'Kharif', 'SoilType': 'Loamy', 'Irrigation': 'Rainfed'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🌤 {test_case['name']}:")
        for region in regions:
            result = trainer.predict_crop(region, test_case['features'])
            if result:
                print(f"   📍 {region}: {result['predicted_crop']} ({result['confidence']})")
                print(f"      Top 3: {result['top_recommendations']}")
    
    print(f"\n🎉 IMPROVED TRAINING COMPLETED!")
    print(f"📊 Regional Model Performance:")
    for region, scores in results.items():
        print(f"   {region}:")
        print(f"      Test Accuracy: {scores['accuracy']:.2%}")
        print(f"      CV Accuracy:   {scores['cv_score']:.2%}")

if __name__ == "__main__":
    main()