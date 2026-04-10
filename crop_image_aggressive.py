from PIL import Image
import os

path = "/workspace/image/delta_ops/Hackclaw_official.jpg"

try:
    img = Image.open(path)
    width, height = img.size
    
    # Crop a bit more aggressively from the bottom (e.g., 50 pixels) and a bit from the top just in case
    # Since we know there's a white border issue, let's explicitly remove the outer 5% of the bottom edge
    bottom_crop_margin = int(height * 0.05)
    
    # Let's also check if there are any tiny borders left on the sides
    side_crop_margin = int(width * 0.02)
    top_crop_margin = int(height * 0.02)
    
    box = (side_crop_margin, top_crop_margin, width - side_crop_margin, height - bottom_crop_margin)
    
    cropped_img = img.crop(box)
    cropped_img.save(path)
    print(f"Aggressively cropped bottom border. New size: {cropped_img.size}")
except Exception as e:
    print(f"Error: {e}")
