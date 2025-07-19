# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Integration Test - Final Verification
Tests that the GUI launches automatically and responds to all ARI states
"""

import sys
import os
import time

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("🧪 ARI Final Integration Test")
    print("=" * 50)
    print("This test verifies that:")
    print("1. ARI launches with GUI enabled by default")
    print("2. The GUI responds to ARI speaking, listening, and processing")
    print("3. The audio monitor bars reflect the current audio state")
    print("4. The GUI can be safely closed when done")
    print("=" * 50)
    
    # Import the main ARI system
    from ari_master_brain_final import ARIMasterBrain
    
    print("🚀 Creating ARI instance (GUI should be enabled by default)")
    ari = ARIMasterBrain()  # No parameters, should use default True
    
    # Give GUI time to initialize
    time.sleep(3)
    
    # Test speaking state
    print("\n📢 Testing speaking state...")
    ari.speak("This is a test of the ARI speaking state. The GUI should show faster animation and active audio bars.")
    time.sleep(5)
    
    # Test listening state
    print("\n👂 Testing listening state...")
    ari.update_gui_state('is_listening', True)
    print("GUI should now show listening state with medium animation speed.")
    time.sleep(3)
    ari.update_gui_state('is_listening', False)
    
    # Test user speaking state
    print("\n🗣️ Testing user speaking state...")
    ari.update_gui_state('user_speaking', True)
    print("GUI should now show user speaking state with slower animation.")
    time.sleep(3)
    ari.update_gui_state('user_speaking', False)
    
    # Test processing state
    print("\n🧠 Testing processing state...")
    ari.update_gui_state('is_processing', True)
    print("GUI should now show processing state.")
    time.sleep(3)
    ari.update_gui_state('is_processing', False)
    
    print("\n✅ Test complete! Please check that the GUI responded appropriately to each state.")
    print("Press Ctrl+C to exit the test.")
    
    # Keep the script running so the GUI stays open for observation
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Test ended by user.")
    
if __name__ == "__main__":
    main()
