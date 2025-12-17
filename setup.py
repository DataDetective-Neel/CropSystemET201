# setup.py - RUN THIS FIRST
import os
import shutil

def create_structure():
    """Create the complete folder structure"""
    folders = [
        'data/raw',
        'data/processed', 
        'data/backups',
        'models/general',
        'models/regional',
        'models/legacy',
        'src',
        'scripts'
    ]
    
    print("🚀 Creating project structure...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created: {folder}")
    
    # Create empty files
    open('src/__init__.py', 'w').close()
    
    print("\n🎉 Folder structure created successfully!")
    print("\n📁 Next steps:")
    print("1. Copy your Excel file to 'data/raw/'")
    print("2. Copy your previous model files to 'models/legacy/'")
    print("3. Run data_analysis.py")

if __name__ == "__main__":
    create_structure()