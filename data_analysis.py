# data_analysis.py - UPDATED FOR CSV FILE
import pandas as pd
import os

def analyze_crop_data():
    print("🔍 Analyzing Your Crop Dataset...")
    
    # Check if CSV file exists
    raw_folder = "data/raw/"
    files = os.listdir(raw_folder)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV file found in 'data/raw/'")
        print("Files in raw folder:", os.listdir(raw_folder))
        input("Press Enter to close...")
        return
    
    # Load the CSV file
    csv_file = csv_files[0]
    file_path = os.path.join(raw_folder, csv_file)
    
    print(f"📊 Loading: {csv_file}")
    
    try:
        # Read your CSV file
        df = pd.read_csv(file_path)
        
        # Clean column names (remove extra spaces, special characters)
        df.columns = df.columns.str.strip()
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        input("Press Enter to close...")
        return
    
    # Basic analysis
    print(f"\n✅ Dataset loaded successfully!")
    print(f"📈 Shape: {df.shape} (rows, columns)")
    
    print(f"\n📋 Columns in your dataset:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    # Region analysis
    print(f"\n🌍 REGIONS Analysis:")
    if 'Region' in df.columns:
        regions = df['Region'].unique()
        print(f"   Total regions: {len(regions)}")
        for region in regions:
            region_data = df[df['Region'] == region]
            crops_in_region = region_data['Crop'].unique() if 'Crop' in df.columns else []
            print(f"   📍 {region}: {len(region_data):3d} records, {len(crops_in_region):2d} crops")
    
    # Season analysis
    print(f"\n📅 SEASONS Analysis:")
    if 'Season' in df.columns:
        seasons = df['Season'].unique()
        for season in seasons:
            season_data = df[df['Season'] == season]
            print(f"   🌤 {season}: {len(season_data):3d} records")
    
    # Crop analysis
    print(f"\n🌾 CROPS Analysis:")
    if 'Crop' in df.columns:
        crops = df['Crop'].value_counts()
        print(f"   Total unique crops: {len(crops)}")
        print(f"   Top 10 crops:")
        for crop, count in crops.head(10).items():
            print(f"      {crop}: {count:3d} records")
    
    # Year analysis
    print(f"\n📅 YEARS Analysis:")
    if 'Year' in df.columns:
        years = df['Year'].value_counts().sort_index()
        print(f"   Year range: {df['Year'].min()} - {df['Year'].max()}")
        for year, count in years.items():
            print(f"   {year}: {count:3d} records")
    
    # Soil type analysis
    print(f"\n🌱 SOIL TYPES Analysis:")
    if 'SoilType' in df.columns:
        soil_types = df['SoilType'].value_counts()
        for soil, count in soil_types.items():
            print(f"   {soil}: {count:3d} records")
    
    # Irrigation analysis
    print(f"\n💧 IRRIGATION Analysis:")
    if 'Irrigation' in df.columns:
        irrigation_types = df['Irrigation'].value_counts()
        for irrig, count in irrigation_types.items():
            print(f"   {irrig}: {count:3d} records")
    
    # Crop health analysis
    print(f"\n🏥 CROP HEALTH Analysis:")
    if 'CropHealthLabel' in df.columns:
        health_labels = df['CropHealthLabel'].value_counts()
        for health, count in health_labels.items():
            print(f"   {health}: {count:3d} records")
    
    # Numerical features summary
    print(f"\n📊 NUMERICAL FEATURES Summary:")
    numerical_cols = ['N', 'P', 'K', 'pH', 'Temperature', 'Humidity', 'Rainfall', 'Moisture']
    for col in numerical_cols:
        if col in df.columns:
            print(f"   {col:12s}: Min={df[col].min():6.2f}, Max={df[col].max():6.2f}, Mean={df[col].mean():6.2f}")
    
    # Save processed data
    print(f"\n💾 Saving processed data...")
    df.to_csv("data/processed/general_data.csv", index=False)
    
    # Create regional datasets
    regions_to_save = ['Punjab', 'Haryana', 'Rajasthan']
    for region in regions_to_save:
        if 'Region' in df.columns and region in df['Region'].values:
            region_df = df[df['Region'] == region]
            region_df.to_csv(f"data/processed/{region.lower()}_data.csv", index=False)
            print(f"✅ Saved {region} data: {len(region_df)} records")
    
    print("\n🎉 Analysis completed successfully!")
    print("\n📁 Files created:")
    print("   - data/processed/general_data.csv")
    for region in regions_to_save:
        if 'Region' in df.columns and region in df['Region'].values:
            print(f"   - data/processed/{region.lower()}_data.csv")
    
    input("\nPress Enter to close...")

if __name__ == "__main__":
    analyze_crop_data()