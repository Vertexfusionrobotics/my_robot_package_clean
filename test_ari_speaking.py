# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Quick test to verify ARI is speaking responses
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ari_speaking():
    """Test that ARI actually speaks her responses"""
    
    print("🧪 Testing ARI Voice Response System")
    print("=" * 40)
    
    try:
        # Import and create ARI instance
        from ari_master_brain_final import ARIMasterBrain
        print("✅ ARI imported successfully")
        
        # Create instance but don't run the full loop
        ari = ARIMasterBrain()
        print("✅ ARI instance created")
        
        # Test the speak method directly
        print("\n🗣️ Testing direct speak method...")
        ari.speak("Hello! This is a test of my voice system.")
        
        # Test getting and speaking a response
        print("\n🤖 Testing response generation and speaking...")
        test_input = "Hello ARI"
        response = ari.get_response(test_input)
        print(f"📝 Generated response: {response}")
        ari.speak(response)
        
        print("\n✅ Voice test completed!")
        print("🎯 If you heard ARI speak, the voice system is working correctly.")
        print("🔧 If you only saw text, there may be an audio output issue.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ari_speaking()
