# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
from test_holo_face import AriFaceGUI
import time
import threading

def robot_logic(face):
    sequence = [
        ("happy", 2),
        ("smiling", 2),
        ("thinking", 2),
        ("concerned", 2),
        ("angry", 2),
        ("sad", 2),
        ("upset", 2),
        ("neutral", 2),
    ]
    for expr, duration in sequence:
        face.show_expression(expr)
        for _ in range(duration * 5):
            face.animate_talking()
            time.sleep(0.2)
    # Keep the GUI running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    # Start robot logic in a background thread
    t = threading.Thread(target=robot_logic, args=(face,), daemon=True)
    t.start()
    face.root.mainloop()
