# train_seasonal_only.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import os

class SeasonalModelTrainer:
    def __init__(self):
        self.seasonal_models = {}
        self.seasonal_encoders = {}
    
    def train_seasonal_model(self, season_name):
        """Train specialized model for each season using your existing data"""
        print(f"🚀 Training SEASONAL model for {season_name}...")
        
        # Load your existing processed data
        df = pd.read_csv("data/processed/general_data.csv")
        season_data = df[df['Season'] == season_name]
        
        if len(season_data) < 10:
            print(f"   ⚠️ Not enough data for {season_name}")
            return None
        
        # Use same features as your regional models for consistency
        features = ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture']
        X = season_data[features].copy()
        y = season_data['Crop']
        
        # Encode target
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        # Train model (similar parameters to your existing models)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ {season_name} seasonal model trained!")
        print(f"   Accuracy: {accuracy:.2%}")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Crops: {list(le.classes_)}")
        
        # Store model
        self.seasonal_models[season_name] = model
        self.seasonal_encoders[season_name] = le
        
        return accuracy
    
    def save_models(self):
        """Save seasonal models"""
        os.makedirs("models/seasonal", exist_ok=True)
        
        for season in self.seasonal_models:
            model_data = {
                'model': self.seasonal_models[season],
                'encoder': self.seasonal_encoders[season],
                'features': ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture']
            }
            joblib.dump(model_data, f"models/seasonal/{season.lower()}_model.pkl")
            print(f"✅ Saved {season} seasonal model")

def main():
    print("🌤 TRAINING SEASONAL MODELS (Model 3)")
    print("=" * 50)
    
    trainer = SeasonalModelTrainer()
    seasons = ['Rabi', 'Kharif', 'Zaid']
    
    # Train only seasonal models
    accuracies = {}
    for season in seasons:
        accuracy = trainer.train_seasonal_model(season)
        if accuracy:
            accuracies[season] = accuracy
    
    # Save models
    trainer.save_models()
    
    print(f"\n📊 SEASONAL MODEL PERFORMANCE:")
    for season, acc in accuracies.items():
        print(f"   {season}: {acc:.2%}")

if __name__ == "__main__":
    main()

    