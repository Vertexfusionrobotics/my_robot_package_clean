# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
from PIL import Image, ImageDraw

# Create a transparent mouth overlay (simple red oval for demo)
img_size = (400, 400)
mouth_overlay = Image.new("RGBA", img_size, (0,0,0,0))
draw = ImageDraw.Draw(mouth_overlay)
draw.ellipse([(150, 270), (250, 320)], fill=(200,0,0,180), outline=(255,0,0,255), width=4)
mouth_overlay.save("ari_faces_split/mouth_talking.png")

# Create a transparent eyes overlay (simple blue ovals for demo)
eyes_overlay = Image.new("RGBA", img_size, (0,0,0,0))
draw = ImageDraw.Draw(eyes_overlay)
draw.ellipse([(120, 140), (170, 180)], fill=(0,100,255,180), outline=(0,0,255,255), width=3)
draw.ellipse([(230, 140), (280, 180)], fill=(0,100,255,180), outline=(0,0,255,255), width=3)
eyes_overlay.save("ari_faces_split/eyes_blink.png")

print("Sample overlays created: mouth_talking.png and eyes_blink.png in ari_faces_split/")
