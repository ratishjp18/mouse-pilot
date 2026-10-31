"""
Generate Mouse Pilot icon with mouse symbol inside orbit
"""
from PIL import Image, ImageDraw
import os

def create_mouse_orbit_icon():
    """Create icon with mouse symbol centered in orbit design"""
    
    # Create multiple sizes for .ico file
    sizes = [256, 128, 64, 48, 32, 16]
    images = []
    
    for size in sizes:
        # Create transparent image
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate proportional dimensions
        center = size / 2
        
        # Draw outer circle (dark background)
        outer_radius = size * 0.45
        draw.ellipse(
            [center - outer_radius, center - outer_radius,
             center + outer_radius, center + outer_radius],
            fill=(30, 30, 35, 255),  # Dark gray background
            outline=None
        )
        
        # Draw blue orbit ring (elliptical path)
        orbit_width = size * 0.08
        orbit_radius = size * 0.35
        
        # Create orbit as a thick ellipse outline
        for i in range(int(orbit_width)):
            alpha = int(200 - (i / orbit_width) * 100)  # Gradient effect
            draw.ellipse(
                [center - orbit_radius - i/2, center - orbit_radius - i/2,
                 center + orbit_radius + i/2, center + orbit_radius + i/2],
                outline=(33, 150, 243, alpha),  # Blue color
                width=1
            )
        
        # Draw mouse symbol in center
        mouse_height = size * 0.3
        mouse_width = size * 0.2
        mouse_x = center - mouse_width / 2
        mouse_y = center - mouse_height / 2
        
        # Mouse body (rounded rectangle)
        mouse_radius = size * 0.05
        draw.rounded_rectangle(
            [mouse_x, mouse_y, mouse_x + mouse_width, mouse_y + mouse_height],
            radius=mouse_radius,
            fill=(255, 255, 255, 255),  # White
            outline=(33, 150, 243, 255),  # Blue outline
            width=max(1, int(size * 0.01))
        )
        
        # Left mouse button divider
        divider_x = center
        draw.line(
            [divider_x, mouse_y, divider_x, mouse_y + mouse_height * 0.5],
            fill=(33, 150, 243, 255),
            width=max(1, int(size * 0.01))
        )
        
        # Scroll wheel (small rectangle in top center)
        wheel_width = size * 0.04
        wheel_height = size * 0.08
        wheel_x = center - wheel_width / 2
        wheel_y = mouse_y + mouse_height * 0.15
        
        draw.rounded_rectangle(
            [wheel_x, wheel_y, wheel_x + wheel_width, wheel_y + wheel_height],
            radius=size * 0.01,
            fill=(33, 150, 243, 255),  # Blue scroll wheel
            outline=None
        )
        
        # Add small highlight on mouse for depth
        highlight_size = size * 0.03
        highlight_x = mouse_x + mouse_width * 0.25
        highlight_y = mouse_y + mouse_height * 0.7
        draw.ellipse(
            [highlight_x, highlight_y, 
             highlight_x + highlight_size, highlight_y + highlight_size],
            fill=(200, 220, 240, 150)  # Light blue highlight
        )
        
        # Draw outer border (blue circular border)
        border_width = max(2, int(size * 0.015))
        border_radius = size * 0.48
        for i in range(border_width):
            draw.ellipse(
                [center - border_radius + i, center - border_radius + i,
                 center + border_radius - i, center + border_radius - i],
                outline=(33, 150, 243, 255),  # Blue
                width=1
            )
        
        images.append(img)
    
    # Save as .ico file with multiple sizes
    output_path = os.path.join('assets', 'icon.ico')
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    print(f"✓ Created new icon: {output_path}")
    print(f"  Sizes: {', '.join([f'{s}x{s}' for s in sizes])}")
    print("  Design: Mouse symbol centered in blue orbit")

if __name__ == "__main__":
    create_mouse_orbit_icon()
    print("\n✓ Icon generation complete!")
