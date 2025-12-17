# mobile_app/create_icons.py
# Script to create placeholder app icons
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple icon with crop symbol"""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#00F5FF')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple crop/seedling symbol
    # Center circle
    center = size // 2
    radius = size // 3
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill='#9D4EDD',
        outline='white',
        width=3
    )
    
    # Try to add text if possible
    try:
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
        text = "🌾"
        # For emoji, we'll just draw a simple shape instead
        # Draw a leaf shape
        leaf_points = [
            (center, center - radius // 2),
            (center - radius // 3, center),
            (center, center + radius // 2),
            (center + radius // 3, center)
        ]
        draw.polygon(leaf_points, fill='#38B000')
    except:
        pass
    
    img.save(output_path)
    print(f"✅ Created icon: {output_path} ({size}x{size})")

if __name__ == '__main__':
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    
    # Create icons
    create_icon(192, os.path.join(static_dir, 'icon-192.png'))
    create_icon(512, os.path.join(static_dir, 'icon-512.png'))
    
    print("\n✅ Icons created successfully!")
    print("💡 You can replace these with custom icons if desired.")

