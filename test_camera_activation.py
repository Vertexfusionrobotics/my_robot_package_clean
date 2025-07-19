# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script to verify camera activation and display
"""

import sys
import time
from ari_visual_recognition import ARIVisualRecognition

def test_camera():
    """Test camera activation and display"""
    print("🔍 Testing ARI Camera Activation")
    print("=" * 40)
    
    # Initialize visual recognition
    vision = ARIVisualRecognition()
    
    # Test camera activation
    print("📷 Starting camera...")
    result = vision.start_camera()
    
    if result:
        print("✅ Camera started successfully!")
        
        # Show camera window
        print("📹 Displaying camera window...")
        display_result = vision.show_camera_window()
        
        if display_result:
            print("✅ Camera window displayed!")
            print("👀 You should see a camera window with 'ARI Vision Active' text")
            print("Press any key in the terminal to continue...")
            input()
        else:
            print("❌ Failed to display camera window")
        
        # Test frame capture
        print("📸 Testing frame capture...")
        frame = vision.capture_frame()
        if frame is not None:
            print(f"✅ Frame captured successfully! Size: {frame.shape}")
        else:
            print("❌ Failed to capture frame")
        
        # Stop camera
        vision.stop_camera()
        print("🔄 Camera stopped")
        
    else:
        print("❌ Failed to start camera")
        print("💡 Make sure a camera is connected and not being used by another application")
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    test_camera()
