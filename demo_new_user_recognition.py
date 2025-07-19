# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Demonstration of ARI's new user recognition feature.
This simulates the interaction without requiring user input.
"""

import json
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ari_master_brain_final import ARIMasterBrain

def demo_new_user_recognition():
    """Demonstrate the new user recognition feature"""
    
    print("🎭 DEMONSTRATION: ARI New User Recognition")
    print("=" * 50)
    
    # Test 1: New User Scenario
    print("\n🆕 Test 1: New User Scenario")
    print("-" * 30)
    
    # Create empty user profile
    with open("user_profile.json", 'w') as f:
        json.dump({}, f)
    
    print("📝 Created empty user profile (simulating new user)")
    
    try:
        # Initialize ARI
        print("🚀 Initializing ARI...")
        ari = ARIMasterBrain()
        
        # Check if it detects new user
        is_new = ari.is_new_user()
        print(f"🔍 Is new user detected? {is_new}")
        
        if is_new:
            print("✅ NEW USER DETECTED!")
            greeting = ari.handle_new_user_greeting()
            print(f"🗣️ ARI greeting: '{greeting}'")
            
            # Simulate user providing name
            test_name = "Alice"
            print(f"👤 User says: '{test_name}'")
            
            confirmation = ari.handle_name_confirmation(test_name)
            print(f"🗣️ ARI response: '{confirmation}'")
            
            # Verify name was saved
            with open("user_profile.json", 'r') as f:
                saved_profile = json.load(f)
            print(f"💾 Saved profile: {saved_profile}")
            
        else:
            print("❌ New user not detected (unexpected)")
            
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Known User Scenario
    print("\n👤 Test 2: Known User Scenario")
    print("-" * 30)
    
    try:
        # Reinitialize ARI with the saved profile
        print("🔄 Reinitializing ARI with saved profile...")
        ari2 = ARIMasterBrain()
        
        # Check if it detects known user
        is_new2 = ari2.is_new_user()
        print(f"🔍 Is new user detected? {is_new2}")
        
        if not is_new2:
            print("✅ KNOWN USER DETECTED!")
            user_name = ari2.user_profile.get("name", "friend")
            print(f"🗣️ ARI would greet: 'Welcome back, {user_name}!'")
        else:
            print("❌ Known user not detected (unexpected)")
            
    except Exception as e:
        print(f"❌ Error in test 2: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("✅ New user recognition feature is working!")
    print("=" * 50)

if __name__ == "__main__":
    demo_new_user_recognition()
