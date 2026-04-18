#!/usr/bin/env python3
"""
Create an enhanced Mandera Analytics Pipeline image with project files/components.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_enhanced_logo():
    """Create a comprehensive logo showing pipeline and project components."""

    # Larger dimensions to accommodate all information
    width, height = 1400, 900
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Set up fonts
    try:
        font_paths = [
            '/System/Library/Fonts/Arial.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            'arial.ttf',
        ]
        title_font = None
        subtitle_font = None
        label_font = None
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 48)
                subtitle_font = ImageFont.truetype(font_path, 24)
                label_font = ImageFont.truetype(font_path, 16)
                break
        
        if title_font is None:
            title_font = subtitle_font = label_font = ImageFont.load_default()
    except:
        title_font = subtitle_font = label_font = ImageFont.load_default()

    # Colors
    navy = '#000080'
    dark_blue = '#003366'
    light_blue = '#E6F2FF'
    accent_orange = '#FF8C00'
    text_gray = '#333333'
    light_gray = '#F5F5F5'
    green = '#2E7D32'
    purple = '#6A1B9A'

    # Header section with blue background
    draw.rectangle([0, 0, width, 120], fill=dark_blue)
    
    # Main title
    draw.text((50, 20), "Mandera Analytics Pipeline", fill='white', font=title_font)
    draw.text((50, 75), "Data Engineering & Analytics Platform", fill=light_blue, font=subtitle_font)

    # Divider line
    draw.rectangle([0, 120, width, 130], fill=accent_orange)

    # Left side - Pipeline Architecture
    y_offset = 160
    draw.text((50, y_offset), "📊 DATA PIPELINE FLOW", fill=navy, font=subtitle_font)
    
    pipeline_items = [
        ("1. Generate", "Python + Faker", green),
        ("2. Store", "MongoDB Atlas", dark_blue),
        ("3. Lake", "MinIO (S3)", purple),
        ("4. Land", "PostgreSQL raw", '#D32F2F'),
        ("5. Transform", "PostgreSQL staging", '#FF8C00'),
        ("6. Curate", "PostgreSQL analytics", green),
    ]
    
    y_pos = y_offset + 50
    for idx, (title, desc, color) in enumerate(pipeline_items):
        x_pos = 50 + (idx % 3) * 400
        y_pos_item = y_pos + (idx // 3) * 80
        
        # Draw box
        draw.rectangle([x_pos, y_pos_item, x_pos + 350, y_pos_item + 70], 
                      outline=color, width=2)
        draw.rectangle([x_pos, y_pos_item, x_pos + 350, y_pos_item + 35], 
                      fill=color)
        
        # Draw text
        draw.text((x_pos + 10, y_pos_item + 8), title, fill='white', font=label_font)
        draw.text((x_pos + 10, y_pos_item + 38), desc, fill=text_gray, font=label_font)

    # Right side - Project Components
    draw.text((750, y_offset), "🔧 PROJECT COMPONENTS", fill=navy, font=subtitle_font)
    
    components = [
        ("hello_world.py", "Hello World starter script"),
        ("faker_customers.py", "Generate fake customers"),
        ("faker_products.py", "Generate synthetic products"),
        ("faker_orders.py", "Generate order transactions"),
        ("test_script.ipynb", "Jupyter testing notebook"),
    ]
    
    y_pos = y_offset + 50
    for idx, (filename, desc) in enumerate(components):
        x_pos = 750
        y_pos_item = y_pos + (idx * 65)
        
        # Draw component box
        draw.rectangle([x_pos, y_pos_item, x_pos + 600, y_pos_item + 60],
                      outline=accent_orange, width=2, fill=light_gray)
        
        # Draw filename in bold area
        draw.rectangle([x_pos, y_pos_item, x_pos + 600, y_pos_item + 25],
                      fill=accent_orange)
        draw.text((x_pos + 10, y_pos_item + 5), f"📄 {filename}", 
                 fill='white', font=label_font)
        
        # Draw description
        draw.text((x_pos + 10, y_pos_item + 30), desc,
                 fill=text_gray, font=label_font)

    # Bottom section - Key Features
    bottom_y = 700
    draw.rectangle([0, bottom_y - 10, width, bottom_y], fill=accent_orange)
    
    features = "✓ Real-time Data Ingestion  |  ✓ Multi-stage Transformation  |  ✓ Automated CI/CD Pipeline  |  ✓ Cloud-Native Architecture"
    draw.text((50, bottom_y + 20), features, fill=text_gray, font=label_font)
    
    # Footer
    draw.text((50, bottom_y + 80), "Created: April 2026 | Version: 1.0 | Team: Data Engineering",
             fill=text_gray, font=label_font)

    # Save the image
    image.save('Mandera Analytics Pipeline.png', 'PNG')
    print("✅ Enhanced logo created: Mandera Analytics Pipeline.png (1400x900)")

if __name__ == "__main__":
    create_enhanced_logo()
