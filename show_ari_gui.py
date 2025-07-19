# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Simple ARI GUI Test - Just show the visual interface
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def show_ari_gui():
    """Show just the ARI GUI"""
    
    print("🎨 Opening ARI Visual Interface...")
    print("=" * 40)
    
    try:
        from ari_visual_gui import ARIVisualGUI
        
        print("✅ Creating ARI visual interface...")
        gui = ARIVisualGUI()
        
        print("✅ GUI created successfully!")
        print("📺 You should see a window with:")
        print("   • Animated ARI avatar in the center")
        print("   • Futuristic overlays around the edges")
        print("   • System monitoring displays")
        print("   • Control panel at the top")
        print("")
        print("💡 Controls:")
        print("   • F11: Toggle fullscreen")
        print("   • ESC: Exit")
        print("   • Minimize button: Minimize to taskbar")
        print("   • Standard Windows controls available")
        print("")
        print("🚀 Starting GUI...")
        
        # Start the GUI (this will block until window is closed)
        gui.start()
        
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_ari_gui()
