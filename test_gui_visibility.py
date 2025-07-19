# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script to check if GUI window is visible
"""

import time
import tkinter as tk
from ari_visual_gui import ARIVisualGUI

def test_gui_visibility():
    print("Creating GUI...")
    gui = ARIVisualGUI(non_blocking=True)
    
    print("Initializing GUI...")
    gui.initialize()
    
    print("GUI should be visible now!")
    print("Window geometry:", gui.root.geometry())
    print("Window state:", gui.root.state())
    print("Window visible:", gui.root.winfo_viewable())
    
    # Keep the GUI running for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            gui.root.update()
            gui.root.update_idletasks()
            time.sleep(0.1)
        except Exception as e:
            print(f"Error during update: {e}")
            break
    
    print("Stopping GUI...")
    gui.stop()

if __name__ == "__main__":
    test_gui_visibility()
