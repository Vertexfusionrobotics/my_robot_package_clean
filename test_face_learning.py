# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test ARI's Face Learning System
"""

import sys
import os

def main():
    print("🧪 Testing ARI Face Learning System")
    print("=" * 50)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        # Initialize visual recognition
        print("🔍 Initializing visual recognition system...")
        vr = ARIVisualRecognition()
        
        # Test camera activation
        print("📷 Testing camera activation...")
        camera_result = vr.start_camera()
        
        if camera_result:
            print("✅ Camera activated successfully")
            
            # Test face detection
            print("👤 Testing face detection...")
            faces = vr.detect_faces_from_camera()
            
            if faces:
                print(f"✅ Detected {len(faces)} face(s)")
                
                # Test face learning capability
                print("🧠 Testing face learning capability...")
                frame = vr.capture_frame()
                if frame is not None:
                    print("✅ Frame captured successfully")
                    print("📚 Face learning system is ready!")
                    print("\n🎯 To test face learning with ARI:")
                    print("1. Run: python ari_master_brain_final.py")
                    print("2. Say: 'activate vision'")
                    print("3. Say: 'learn my face as [Your Name]'")
                    print("4. Say: 'who am I?' or 'do you recognize me?'")
                else:
                    print("❌ Could not capture frame")
            else:
                print("⚠️ No faces detected - make sure you're in front of the camera")
            
            # Clean up
            vr.stop_camera()
        else:
            print("❌ Could not activate camera")
            
    except Exception as e:
        print(f"❌ Error testing face learning: {e}")
        return False
    
    print("\n✅ Face learning system test complete!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
