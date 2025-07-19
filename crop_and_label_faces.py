# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
from PIL import Image, ImageDraw, ImageFont
import os

# === Settings ===
image_path = "A_digital_illustration_displays_a_holographic_depi.png"  # Update this if needed
frame_size = 400  # width and height of each face
cols = 6
rows = 2
output_dir = "ari_faces"

labels = [
    "neutral", "happy", "sad", "angry", "surprised", "confused",
    "neutral_speaking", "happy_speaking", "sad_speaking", "angry_speaking", "surprised_speaking", "confused_speaking"
]

# === Prepare output folder ===
os.makedirs(output_dir, exist_ok=True)

# === Load image ===
img = Image.open(image_path)

# === Load font ===
font = ImageFont.load_default()

# === Crop, label, and save ===
for i, label in enumerate(labels):
    row = i // cols
    col = i % cols
    x = col * frame_size
    y = row * frame_size
    face_crop = img.crop((x, y, x + frame_size, y + frame_size))

    # Create canvas with label space
    canvas = Image.new("RGB", (frame_size, frame_size + 40), "black")
    canvas.paste(face_crop, (0, 0))

    # Draw label
    draw = ImageDraw.Draw(canvas)
    w, h = draw.textsize(label, font=font)
    draw.text(((frame_size - w) // 2, frame_size + 10), label, fill="white", font=font)

    # Save
    output_path = os.path.join(output_dir, f"ari_{label}.png")
    canvas.save(output_path)
    print(f"Saved: {output_path}")

# === Spritesheet Builder ===
spritesheet = Image.new("RGB", (frame_size * cols, frame_size * rows))

for i, label in enumerate(labels):
    row, col = divmod(i, cols)
    x, y = col * frame_size, row * frame_size
    face = Image.open(os.path.join(output_dir, f"ari_{label}.png")).crop((0, 0, frame_size, frame_size))
    spritesheet.paste(face, (x, y))

spritesheet.save("ari_face_spritesheet.png")
print("Saved: ari_face_spritesheet.png")
