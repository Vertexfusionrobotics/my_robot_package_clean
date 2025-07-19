# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Quick conversation test with ARI to verify enhanced learning integration
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_ari_test():
    """Quick test of ARI with enhanced learning - text-based simulation"""
    print("🤖 Quick ARI Enhanced Learning Test")
    print("=" * 40)
    
    try:
        from ari_master_brain_final import ARIMasterBrain
        
        # Create ARI instance
        ari = ARIMasterBrain()
        print("✅ ARI initialized with enhanced learning")
        
        # Test various inputs without voice
        test_inputs = [
            "hello",
            "learning stats", 
            "what is artificial intelligence",
            "prepare neural training",
            "how are you doing",
            "learning statistics"
        ]
        
        print("\n🗣️ Testing conversation with enhanced learning:")
        
        for i, user_input in enumerate(test_inputs, 1):
            print(f"\n{i}. User: '{user_input}'")
            try:
                response = ari.get_response(user_input, acknowledge_if_slow=False)
                print(f"   ARI: '{response}'")
                
                # Check if this was an enhanced learning command
                if "learning" in user_input.lower():
                    print("   📊 Enhanced learning command detected!")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Get final enhanced learning stats
        print(f"\n📈 Final Enhanced Learning Status:")
        try:
            stats = ari.get_enhanced_learning_stats()
            print(f"   Status: {stats.get('status', 'Unknown')}")
            print(f"   Stage: {stats.get('deep_learning_stage', 'Unknown')}")
            if 'total_conversations' in stats:
                print(f"   Conversations analyzed: {stats['total_conversations']}")
        except Exception as e:
            print(f"   ❌ Error getting stats: {e}")
        
        print("\n🎉 Quick test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_ari_test()
