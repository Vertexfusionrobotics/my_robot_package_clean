# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script for ARI Visual GUI
Tests the visual interface with the avatar GIF
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ari_visual_gui():
    """Test the ARI Visual GUI system"""
    
    print("🧪 Testing ARI Visual GUI System")
    print("=" * 40)
    
    # Check if the avatar GIF exists
    gif_path = "ari_avatar_video.gif"
    if os.path.exists(gif_path):
        file_size = os.path.getsize(gif_path)
        print(f"✅ Avatar GIF found: {gif_path}")
        print(f"   File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    else:
        print(f"❌ Avatar GIF not found: {gif_path}")
        return False
    
    # Test importing the GUI
    try:
        from ari_visual_gui import ARIVisualGUI
        print("✅ ARI Visual GUI module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ARI Visual GUI: {e}")
        return False
    
    # Test creating the GUI (but don't start it yet)
    try:
        print("🎨 Creating ARI Visual GUI instance...")
        gui = ARIVisualGUI()
        print("✅ GUI created successfully")
        
        # Test the state methods
        print("🔧 Testing state control methods...")
        
        # Test frames loaded
        frame_count = len(gui.avatar_frames)
        print(f"   📹 Loaded {frame_count} animation frames")
        
        if frame_count > 0:
            print("✅ Avatar animation ready")
        else:
            print("❌ No animation frames loaded")
            return False
        
        # Don't actually start the GUI in test mode
        gui.stop()
        print("✅ GUI test completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating GUI: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_visual_gui_demo():
    """Run a live demo of the visual GUI"""
    print("\n🚀 Starting ARI Visual GUI Demo...")
    print("=" * 40)
    print("📝 Instructions:")
    print("   - A window will open showing your animated GIF")
    print("   - Use the test buttons to see different states")
    print("   - Close the window when done testing")
    print("\n🎬 Starting GUI in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        from ari_visual_gui import ARIVisualGUI
        gui = ARIVisualGUI()
        gui.start()  # This will open the window
    except Exception as e:
        print(f"❌ Error running GUI demo: {e}")

if __name__ == "__main__":
    # Run the test first
    success = test_ari_visual_gui()
    
    if success:
        print("\n" + "=" * 40)
        print("🎉 GUI Test Passed!")
        print("=" * 40)
        
        # Ask if user wants to see the live demo
        try:
            response = input("\n🎬 Would you like to see the live GUI demo? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                run_visual_gui_demo()
            else:
                print("👍 Test completed. Run 'python ari_visual_gui.py' when ready to see the GUI!")
        except KeyboardInterrupt:
            print("\n👋 Test completed!")
    else:
        print("\n❌ GUI Test Failed - Please check the errors above")
