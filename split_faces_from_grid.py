# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
from PIL import Image
import os

# === Settings ===
image_path = "ari_faces_grid.png"  # <-- Change this to your actual grid image filename if different
frame_size = 400  # width and height of each face
cols = 6
rows = 2
output_dir = "ari_faces_split_from_grid"
os.makedirs(output_dir, exist_ok=True)

# === Load image ===
img = Image.open(image_path)

# === Crop and save ===
for i in range(rows * cols):
    row = i // cols
    col = i % cols
    x = col * frame_size
    y = row * frame_size
    face_crop = img.crop((x, y, x + frame_size, y + frame_size))
    output_path = os.path.join(output_dir, f"face_{row}_{col}.png")
    face_crop.save(output_path)
    print(f"Saved: {output_path}")
