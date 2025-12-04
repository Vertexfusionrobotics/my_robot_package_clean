#!/usr/bin/env python3
"""Simple test to see if GUI can be created"""

print("Testing GUI initialization...")

try:
    from ari_visual_gui import ARIVisualGUI
    print("✅ ARIVisualGUI imported successfully")
    
    print("Creating GUI object...")
    gui = ARIVisualGUI()
    print("✅ GUI object created!")
    
    print("Starting mainloop...")
    gui.root.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
