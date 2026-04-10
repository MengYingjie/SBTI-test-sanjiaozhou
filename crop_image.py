from PIL import Image, ImageChops
import os

path = "/workspace/image/delta_ops/Hackclaw_official.jpg"

try:
    img = Image.open(path)
    
    # Create a white background image of the same size
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    
    # Calculate the difference between the image and the background
    diff = ImageChops.difference(img, bg)
    
    # Find the bounding box of the non-background area
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    
    if bbox:
        # Crop the image to the bounding box
        cropped_img = img.crop(bbox)
        cropped_img.save(path)
        print(f"Successfully cropped auto-detected border. New size: {cropped_img.size}")
    else:
        print("Could not detect border.")
        
except Exception as e:
    print(f"Error: {e}")
