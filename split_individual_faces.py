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
input_dir = r"C:\Users\Tyrell Murray\Pictures\ari facial expressions"
output_dir = 'ari_faces_split'
os.makedirs(output_dir, exist_ok=True)

# Get all PNG/JPG files in the folder
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

for file in image_files:
    try:
        img = Image.open(os.path.join(input_dir, file))
        # Optionally, resize to 400x400 if needed
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        out_path = os.path.join(output_dir, file)
        img.save(out_path)
        print(f"Saved: {out_path}")
    except Exception as e:
        print(f"Could not process {file}: {e}")
