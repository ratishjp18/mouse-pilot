"""
Convert the provided PNG icon to .ico format with multiple sizes
"""
from PIL import Image
import os

def convert_png_to_ico():
    """Convert PNG to ICO with multiple sizes"""
    
    # Note: The image was provided in the chat. For now, we'll use the existing
    # icon.ico path. If you have the PNG file, save it as 'new_icon.png' first.
    
    # If you have a new PNG file, uncomment and use this:
    png_path = 'new_icon.png'
    
    if not os.path.exists(png_path):
        print("❌ PNG file not found. Please save your icon as 'new_icon.png' in this folder.")
        print("   Then run this script again.")
        return
    
    # Open the PNG image
    img = Image.open(png_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create multiple sizes for ICO
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # Save as ICO with multiple sizes
    output_path = os.path.join('assets', 'icon.ico')
    img.save(output_path, format='ICO', sizes=sizes)
    
    print(f"✅ Successfully converted to: {output_path}")
    print(f"   Sizes: {', '.join([f'{w}x{h}' for w, h in sizes])}")

if __name__ == "__main__":
    convert_png_to_ico()
