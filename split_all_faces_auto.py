# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import os
from PIL import Image

# Folder with your images (can be grids or single faces)
input_folder = r"C:\Users\Tyrell Murray\Pictures\ari facial expressions"
output_folder = r"C:\Users\Tyrell Murray\Pictures\ari_faces_split_final"
os.makedirs(output_folder, exist_ok=True)

# Set grid size for splitting (change if your grids are not 2x6)
grid_rows = 2
grid_cols = 6

def is_grid_image(img):
    # Heuristic: if width is at least 2x height, assume it's a grid
    w, h = img.size
    return w >= grid_cols * (h // grid_rows)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue
    path = os.path.join(input_folder, filename)
    try:
        img = Image.open(path)
        if is_grid_image(img):
            print(f"Splitting grid: {filename}")
            w, h = img.size
            cell_w = w // grid_cols
            cell_h = h // grid_rows
            for row in range(grid_rows):
                for col in range(grid_cols):
                    left = col * cell_w
                    upper = row * cell_h
                    right = left + cell_w
                    lower = upper + cell_h
                    face = img.crop((left, upper, right, lower))
                    out_name = f"{os.path.splitext(filename)[0]}_r{row}_c{col}.png"
                    face.save(os.path.join(output_folder, out_name))
        else:
            # Just copy/resize single face images
            face = img.resize((400, 400), Image.Resampling.LANCZOS)
            out_name = f"{os.path.splitext(filename)[0]}_single.png"
            face.save(os.path.join(output_folder, out_name))
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("Done! All individual faces are in:", output_folder)
