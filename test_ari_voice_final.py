# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Simple ARI Interactive Test - Confirms Voice Output
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 ARI Interactive Voice Test")
    print("=" * 40)
    print("This will test if ARI speaks her responses correctly.")
    print("Make sure your speakers/headphones are on and volume is up!")
    
    input("\nPress Enter when ready to test ARI's voice...")
    
    try:
        # Import ARI
        from ari_master_brain_final import ARIMasterBrain
        print("✅ Loading ARI...")
        
        # Create ARI (this will take a moment with all the loading)
        ari = ARIMasterBrain()
        print("✅ ARI ready!")
        
        # Test a few interactions
        test_interactions = [
            "Hello ARI",
            "How are you today?",
            "What can you do?"
        ]
        
        print("\n🎙️ Starting voice interaction test...")
        print("You should hear ARI speak each response!")
        
        for i, test_input in enumerate(test_interactions, 1):
            print(f"\n🗣️ Test {i}: {test_input}")
            response = ari.get_response(test_input)
            print(f"📝 ARI: {response}")
            print("🔊 Speaking response...")
            ari.speak(response)
            print("✅ Voice output complete")
            
            if i < len(test_interactions):
                time.sleep(1)  # Brief pause between tests
        
        print("\n🎉 Voice test completed!")
        print("Did you hear ARI speak with the Sonia voice? (y/n): ", end="")
        heard = input().strip().lower()
        
        if heard.startswith('y'):
            print("✅ Great! ARI's voice system is working perfectly!")
            print("💡 You can now run 'python ari_master_brain_final.py' for full interaction")
        else:
            print("❌ Audio issue detected. Check:")
            print("   - Speaker/headphone volume")
            print("   - Windows sound settings")
            print("   - Default audio output device")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
