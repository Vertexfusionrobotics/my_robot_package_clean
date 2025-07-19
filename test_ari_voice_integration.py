# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test ARI Voice Integration
Quick test to ensure the robust voice system works with ARI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ari_voice_integration():
    """Test ARI with the new robust voice system"""
    
    print("🧪 Testing ARI Voice Integration")
    print("=" * 40)
    
    try:
        # Test the voice system directly first
        print("🎵 Testing voice system directly...")
        from ari_voice_robust import ARIVoiceSystem
        voice_system = ARIVoiceSystem()
        
        # Quick voice test
        test_success = voice_system.speak("ARI voice system test. Can you hear me?")
        if not test_success:
            print("❌ Direct voice test failed")
            return False
        
        print("✅ Direct voice test passed")
        
        # Now test importing the main ARI system
        print("\n🤖 Testing ARI main system import...")
        
        # Import the main ARI system
        from ari_master_brain_final import ARIMasterBrain
        print("✅ ARI system imported successfully")
        
        # Create ARI instance (but don't start the full interactive session)
        print("🔧 Creating ARI instance...")
        ari = ARIMasterBrain()
        print("✅ ARI instance created")
        
        # Test the speak method
        print("\n🗣️ Testing ARI speak method...")
        ari.speak("Hello! This is ARI speaking with my new robust voice system.")
        print("✅ ARI speak test completed")
        
        print("\n🎉 All tests passed! ARI voice integration is working.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ari_voice_integration()
    if success:
        print("\n✅ Ready to run ARI with improved voice system!")
        print("📝 Use: python ari_master_brain_final.py")
    else:
        print("\n❌ Voice integration needs fixing before running ARI")
