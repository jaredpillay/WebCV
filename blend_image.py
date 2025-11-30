from PIL import Image
import numpy as np
import os

os.chdir('c:\\Users\\Admin\\source\\repos\\WebCV-1')

# Load images
jared = Image.open('images/Jared.png')
banner = Image.open('images/banner.png')

print(f'Jared image size: {jared.size}')
print(f'Jared image mode: {jared.mode}')
print(f'Banner image size: {banner.size}')

# Convert Jared to RGBA if needed
if jared.mode != 'RGBA':
    jared = jared.convert('RGBA')
    print('Converted Jared to RGBA')

# Simple background removal using color threshold (white background)
# This is a basic approach - removes white/light backgrounds
data = jared.getdata()
new_data = []

for item in data:
    # If pixel is mostly white (R, G, B > 200), make it transparent
    if item[0] > 200 and item[1] > 200 and item[2] > 200:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

jared.putdata(new_data)

# Resize Jared to fit nicely on banner (about 40% of banner width)
banner_width = banner.size[0]
new_width = int(banner_width * 0.35)
ratio = new_width / jared.size[0]
new_height = int(jared.size[1] * ratio)
jared_resized = jared.resize((new_width, new_height), Image.Resampling.LANCZOS)

print(f'Resized Jared to: {jared_resized.size}')

# Create a copy of banner to blend on
blended = banner.convert('RGBA').copy()

# Position Jared on right side of banner, vertically centered
x_pos = banner.size[0] - new_width - 40  # 40px from right edge
y_pos = (banner.size[1] - new_height) // 2  # centered vertically

# Paste with alpha blending
blended.paste(jared_resized, (x_pos, y_pos), jared_resized)

# Convert back to RGB and save
result = Image.new('RGB', blended.size, (255, 255, 255))
result.paste(blended, mask=blended.split()[3])

# Save as banner_with_jared.png
result.save('images/banner_with_jared.png')
print('Saved blended image as banner_with_jared.png')
