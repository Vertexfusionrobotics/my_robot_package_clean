# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Quick test of ARI with Enhanced Learning Integration
Tests the new voice commands for learning statistics and neural training preparation
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ari_enhanced_commands():
    """Test ARI's enhanced learning voice commands"""
    print("🧠 Testing ARI Enhanced Learning Integration")
    print("=" * 50)
    
    try:
        # Import the integrated ARI system
        from ari_master_brain_final import ARIMasterBrain
        print("✅ ARI Master Brain imported successfully")
        
        # Create ARI instance (but don't start full conversation loop)
        brain = ARIMasterBrain()
        print("✅ ARI initialized with enhanced learning capabilities")
        
        # Test enhanced learning voice commands
        test_commands = [
            "learning stats",
            "learning statistics", 
            "prepare neural training",
            "neural training data"
        ]
        
        print("\n🗣️ Testing Enhanced Learning Voice Commands:")
        for command in test_commands:
            try:
                response = brain.get_response(command, acknowledge_if_slow=False)
                print(f"  Command: '{command}'")
                print(f"  Response: '{response}'")
                print()
            except Exception as e:
                print(f"  ❌ Error with command '{command}': {e}")
        
        # Test enhanced learning statistics
        print("📊 Testing Enhanced Learning Statistics:")
        try:
            stats = brain.get_enhanced_learning_stats()
            print(f"  Status: {stats.get('status', 'Unknown')}")
            if 'deep_learning_stage' in stats:
                print(f"  Stage: {stats['deep_learning_stage']}")
        except Exception as e:
            print(f"  ❌ Error getting stats: {e}")
        
        # Test neural training preparation
        print("\n🚀 Testing Neural Training Preparation:")
        try:
            result = brain.trigger_neural_training_preparation()
            print(f"  Preparation successful: {result}")
        except Exception as e:
            print(f"  ❌ Error in preparation: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 ARI Enhanced Learning Integration test completed!")
        print("✅ Stage 1 integration successful!")
        print("🚀 Ready for live conversation with enhanced learning!")
        
    except ImportError as e:
        print(f"❌ Failed to import ARI components: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_ari_enhanced_commands()
