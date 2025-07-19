# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Stage 2 Demo - Neural Networks in Action!
Demonstrates the complete deep learning integration with ARI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_stage_2():
    """Demonstrate ARI's Stage 2 neural network capabilities"""
    print("🤖 ARI Stage 2: Neural Networks Demo")
    print("=" * 50)
    
    try:
        from ari_master_brain_final import ARIMasterBrain
        
        # Initialize ARI with neural networks
        print("🚀 Initializing ARI with neural networks...")
        ari = ARIMasterBrain()
        
        # Demo conversation scenarios
        demo_inputs = [
            "learning stats",  # Check current learning status
            "what is artificial intelligence",  # Test AI question
            "can you help me with programming",  # Test request
            "train neural networks",  # Train the networks
            "learning stats",  # Check status after training
            "how are you feeling today",  # Test after neural training
        ]
        
        print("\n🎯 Demo Conversation with Neural Network Guidance:")
        print("-" * 50)
        
        for i, user_input in enumerate(demo_inputs, 1):
            print(f"\n{i}. User: '{user_input}'")
            
            try:
                response = ari.get_response(user_input, acknowledge_if_slow=False)
                print(f"   ARI: '{response}'")
                
                # Special handling for training command
                if "train neural networks" in user_input.lower():
                    print("   🧠 Neural network training initiated!")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Show final neural network status
        print(f"\n📊 Final Neural Network Status:")
        stats = ari.get_enhanced_learning_stats()
        print(f"   Status: {stats.get('status', 'Unknown')}")
        print(f"   Stage: {stats.get('deep_learning_stage', 'Unknown')}")
        
        if stats.get('models_trained'):
            print(f"   Models trained: {', '.join(stats['models_trained'])}")
        
        print(f"\n🎉 Demo Complete!")
        print(f"✅ ARI now uses neural networks to:")
        print(f"   • Predict optimal response types")
        print(f"   • Assess conversation quality")
        print(f"   • Learn from conversation patterns")
        print(f"   • Continuously improve responses")
        
        # Test neural network predictions directly
        print(f"\n🧠 Direct Neural Network Predictions:")
        
        if hasattr(ari, '_enhanced_learning') or 'enhanced_learning' in globals():
            from learning_module_enhanced import EnhancedLearningModule
            enhanced = EnhancedLearningModule()
            
            test_phrases = [
                "What is machine learning?",
                "Help me understand robotics",
                "Tell me a joke"
            ]
            
            for phrase in test_phrases:
                pred = enhanced.predict_optimal_response_type(phrase)
                quality = enhanced.predict_conversation_success(phrase)
                
                if pred and quality:
                    print(f"   '{phrase}':")
                    print(f"     -> Response type: {pred['recommended_type']}")
                    print(f"     -> Confidence: {pred['confidence']:.3f}")
                    print(f"     -> Quality score: {quality['quality_score']:.3f}")
        
        print(f"\n🚀 Stage 2 Complete: ARI is now a neural network-powered AI!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_stage_2()
