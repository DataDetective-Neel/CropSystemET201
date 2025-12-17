# train_regional_models.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
import joblib
import os

class RegionalCropTrainer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
    def load_regional_data(self, region_name):
        """Load data for specific region"""
        file_path = f"data/processed/{region_name.lower()}_data.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            print(f"✅ Loaded {region_name} data: {df.shape}")
            return df
        else:
            print(f"❌ No data found for {region_name}")
            return None
    
    def train_region_model(self, region_name):
        """Train model for specific region"""
        print(f"\n🚀 Training model for {region_name}...")
        
        # Load regional data
        df = self.load_regional_data(region_name)
        if df is None:
            return
        
        # Define features and target
        features = ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture', 'Season', 'SoilType', 'Irrigation']
        target = 'Crop'
        
        # Prepare features
        X = df[features].copy()
        y = df[target]
        
        # Encode categorical variables
        label_encoders = {}
        for col in ['Season', 'SoilType', 'Irrigation']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le
        
        # Encode target
        le_crop = LabelEncoder()
        y_encoded = le_crop.fit_transform(y)
        
        # Scale numerical features
        scaler = StandardScaler()
        numerical_cols = ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture']
        X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ {region_name} model trained!")
        print(f"   Accuracy: {accuracy:.2%}")
        print(f"   Crops: {list(le_crop.classes_)}")
        
        # Store components
        self.models[region_name] = model
        self.scalers[region_name] = scaler
        self.encoders[region_name] = {
            'season': label_encoders['Season'],
            'soil': label_encoders['SoilType'], 
            'irrigation': label_encoders['Irrigation'],
            'crop': le_crop
        }
        
        return accuracy
    
    def save_models(self):
        """Save all trained models"""
        print(f"\n💾 Saving models...")
        
        for region in self.models:
            model_data = {
                'model': self.models[region],
                'scaler': self.scalers[region],
                'encoders': self.encoders[region]
            }
            
            file_path = f"models/regional/{region.lower()}_model.pkl"
            joblib.dump(model_data, file_path)
            print(f"✅ Saved {region} model")
    
    def predict_crop(self, region_name, input_features):
        """Predict crop for given region and features"""
        if region_name not in self.models:
            print(f"❌ No model found for {region_name}")
            return None
        
        model = self.models[region_name]
        scaler = self.scalers[region_name]
        encoders = self.encoders[region_name]
        
        # Prepare input
        input_df = pd.DataFrame([input_features])
        
        # Encode categorical features
        for col in ['Season', 'SoilType', 'Irrigation']:
            le = encoders['season' if col == 'Season' else 'soil' if col == 'SoilType' else 'irrigation']
            input_df[col] = le.transform([input_features[col]])[0]
        
        # Scale numerical features
        numerical_cols = ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture']
        input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
        
        # Predict
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        predicted_crop = encoders['crop'].inverse_transform([prediction])[0]
        confidence = np.max(probability)
        
        # Get top 3 recommendations
        top_3_idx = np.argsort(probability)[-3:][::-1]
        top_3_crops = encoders['crop'].inverse_transform(top_3_idx)
        top_3_confidences = probability[top_3_idx]
        
        return {
            'predicted_crop': predicted_crop,
            'confidence': confidence,
            'top_recommendations': list(zip(top_3_crops, top_3_confidences))
        }

def main():
    print("🌾 REGIONAL CROP MODEL TRAINING")
    print("=" * 50)
    
    trainer = RegionalCropTrainer()
    
    regions = ['Punjab', 'Haryana', 'Rajasthan']
    accuracies = {}
    
    # Train models for all regions
    for region in regions:
        accuracy = trainer.train_region_model(region)
        if accuracy:
            accuracies[region] = accuracy
    
    # Save all models
    trainer.save_models()
    
    # Test predictions
    print(f"\n🧪 TESTING PREDICTIONS")
    print("=" * 50)
    
    test_features = {
        'N': 100, 'P': 50, 'K': 40, 'pH': 7.0, 
        'Temperature': 25, 'Humidity': 60, 'Rainfall': 100, 'Moisture': 20,
        'Season': 'Rabi', 'SoilType': 'Clay', 'Irrigation': 'Irrigated'
    }
    
    for region in regions:
        result = trainer.predict_crop(region, test_features)
        if result:
            print(f"\n📍 {region}:")
            print(f"   Predicted: {result['predicted_crop']} ({result['confidence']:.2%})")
            print(f"   Top 3: {result['top_recommendations']}")
    
    print(f"\n🎉 TRAINING COMPLETED!")
    print(f"📊 Regional Model Accuracies:")
    for region, acc in accuracies.items():
        print(f"   {region}: {acc:.2%}")

if __name__ == "__main__":
    main()