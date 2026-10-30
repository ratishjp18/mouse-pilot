"""
Create the Mouse Pilot application icon
Generates a modern, professional mouse cursor icon with blue accent
"""

from PIL import Image, ImageDraw


def create_icon():
    """Create application icon at multiple resolutions"""
    
    # Create a 256x256 base image with transparency
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw mouse cursor pointer shape
    # Main cursor body points
    cursor_points = [
        (80, 60),    # Top point
        (80, 200),   # Bottom of main body
        (120, 160),  # Inner bottom corner
        (140, 220),  # Bottom of lower extension
        (160, 210),  # Tip of lower extension
        (140, 150),  # Top of lower extension
        (180, 150),  # Right tip
        (80, 60)     # Back to top
    ]
    
    # Draw black outline/shadow (thicker)
    for offset in range(3):
        shadow_points = [(x + offset, y + offset) for x, y in cursor_points]
        draw.polygon(shadow_points, fill='#2C2C2C', outline='#000000')
    
    # Draw white main cursor body
    cursor_fill = [
        (85, 70),
        (85, 190),
        (120, 155),
        (135, 205),
        (150, 198),
        (135, 150),
        (170, 150),
        (85, 70)
    ]
    draw.polygon(cursor_fill, fill='white', outline='#E0E0E0', width=2)
    
    # Add blue accent circle (Windows 11 style)
    accent_x, accent_y = 165, 100
    accent_radius = 25
    
    # Draw accent shadow
    draw.ellipse(
        [accent_x - accent_radius + 2, accent_y - accent_radius + 2,
         accent_x + accent_radius + 2, accent_y + accent_radius + 2],
        fill='#00000040'
    )
    
    # Draw main accent
    draw.ellipse(
        [accent_x - accent_radius, accent_y - accent_radius,
         accent_x + accent_radius, accent_y + accent_radius],
        fill='#0078D4',
        outline='#005A9E',
        width=2
    )
    
    # Add highlight to accent
    highlight_radius = 8
    draw.ellipse(
        [accent_x - highlight_radius - 5, accent_y - highlight_radius - 5,
         accent_x + highlight_radius - 5, accent_y + highlight_radius - 5],
        fill='#60CDFF80'
    )
    
    # Save as ICO with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('assets/icon.ico', format='ICO', sizes=icon_sizes)
    print(f"✓ Icon created successfully: assets/icon.ico")
    print(f"  Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")


if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("Error: Pillow (PIL) is required to create icons")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"Error creating icon: {e}")
