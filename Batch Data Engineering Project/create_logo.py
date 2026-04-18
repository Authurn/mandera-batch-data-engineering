#!/usr/bin/env python3
"""
Script to generate Mandera Analytics Pipeline logo PNG image.
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create a professional logo for Mandera Analytics Pipeline."""

    # Image dimensions
    width, height = 800, 200

    # Create image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Try to use a nice font, fallback to default if not available
    try:
        # Try different font options
        font_paths = [
            '/System/Library/Fonts/Arial.ttf',  # macOS
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
            'arial.ttf',  # Windows
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 48)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Main title
    title = "Mandera Analytics Pipeline"
    draw.text((50, 50), title, fill='navy', font=font)

    # Subtitle
    try:
        small_font = ImageFont.truetype(font_paths[0], 24) if font != ImageFont.load_default() else ImageFont.load_default()
    except:
        small_font = ImageFont.load_default()

    subtitle = "Data Engineering & Analytics Platform"
    draw.text((50, 120), subtitle, fill='gray', font=small_font)

    # Add some decorative elements
    # Blue accent line
    draw.rectangle([50, 110, 750, 115], fill='lightblue')

    # Save the image
    image.save('Mandera Analytics Pipeline.png', 'PNG')
    print("✅ Logo created: Mandera Analytics Pipeline.png")

if __name__ == "__main__":
    create_logo()