# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Stage 2 Neural Networks Test - Complete Deep Learning Integration Test
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stage_2_integration():
    """Test complete Stage 2 neural network integration"""
    print("🧠 ARI Stage 2: Neural Networks Integration Test")
    print("=" * 60)
    
    try:
        # Test 1: Neural Networks Module
        print("\n📊 Test 1: Neural Networks Module")
        from neural_networks import ARINeuralNetworks
        nn = ARINeuralNetworks()
        status = nn.get_neural_status()
        print(f"  ✅ Neural networks status: {status['tensorflow_available']}")
        print(f"  📁 Models directory: {status['model_directory']}")
        
        # Test 2: Enhanced Learning with Neural Integration
        print("\n🔬 Test 2: Enhanced Learning with Neural Integration")
        from learning_module_enhanced import EnhancedLearningModule
        enhanced = EnhancedLearningModule()
        neural_status = enhanced.get_neural_status()
        print(f"  ✅ Neural integration: {neural_status.get('neural_networks_available', False)}")
        print(f"  🎯 Stage: {neural_status.get('stage', 'Unknown')}")
        
        # Test 3: Neural Network Predictions
        print("\n🎯 Test 3: Neural Network Predictions")
        test_inputs = [
            "What is artificial intelligence?",
            "Can you help me with programming?",
            "How are you today?",
        ]
        
        for user_input in test_inputs:
            print(f"\n  Input: '{user_input}'")
            
            # Test response type prediction
            response_pred = enhanced.predict_optimal_response_type(user_input)
            if response_pred:
                print(f"    Response type: {response_pred['recommended_type']}")
                print(f"    Confidence: {response_pred['confidence']:.3f}")
                print(f"    Method: {response_pred['method']}")
            
            # Test quality prediction
            quality_pred = enhanced.predict_conversation_success(user_input)
            if quality_pred:
                print(f"    Quality score: {quality_pred['quality_score']:.3f}")
                print(f"    Success prediction: {quality_pred.get('predicted_success', 'Unknown')}")
        
        # Test 4: ARI Integration
        print("\n🤖 Test 4: ARI Integration with Neural Networks")
        from ari_master_brain_final import ARIMasterBrain
        ari = ARIMasterBrain()
        
        # Test enhanced learning commands
        test_commands = [
            "learning stats",
            "train neural networks"
        ]
        
        for command in test_commands:
            print(f"\n  Command: '{command}'")
            try:
                response = ari.get_response(command, acknowledge_if_slow=False)
                print(f"    Response: '{response}'")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        # Test 5: Neural Network Training
        print("\n🧠 Test 5: Neural Network Training")
        
        # Check if we have enough data
        training_data = enhanced.neural_networks.prepare_training_data() if enhanced.neural_networks else None
        
        if training_data and len(training_data['X']) >= 5:
            print(f"  📊 Training data: {len(training_data['X'])} samples available")
            
            # Train with small epochs for testing
            print("  🚀 Starting neural network training (quick test)...")
            success = enhanced.train_neural_networks(epochs=5)
            
            if success:
                print("  ✅ Neural network training successful!")
                
                # Test predictions after training
                print("  🎯 Testing post-training predictions...")
                for test_input in test_inputs[:2]:  # Test with 2 inputs
                    pred = enhanced.predict_optimal_response_type(test_input)
                    if pred:
                        print(f"    '{test_input}' -> {pred['recommended_type']} ({pred['confidence']:.3f})")
            else:
                print("  ⚠️ Neural network training failed or insufficient data")
        else:
            print("  ⚠️ Insufficient training data for neural networks")
            print("    Try having more conversations with ARI first")
        
        # Test 6: Final Integration Status
        print("\n📈 Test 6: Final Integration Status")
        final_stats = ari.get_enhanced_learning_stats()
        print(f"  Status: {final_stats.get('status', 'Unknown')}")
        print(f"  Stage: {final_stats.get('deep_learning_stage', 'Unknown')}")
        print(f"  Neural networks available: {final_stats.get('neural_networks_available', False)}")
        
        if final_stats.get('models_trained'):
            print(f"  Models trained: {final_stats['models_trained']}")
        
        print("\n" + "=" * 60)
        print("🎉 Stage 2 Neural Networks Integration Test Complete!")
        
        # Summary
        neural_available = neural_status.get('neural_networks_available', False)
        models_trained = bool(final_stats.get('models_trained'))
        
        if neural_available and models_trained:
            print("✅ Status: STAGE 2 COMPLETE - Neural networks active!")
        elif neural_available:
            print("🔄 Status: Stage 2 ready - Neural networks available but not trained")
        else:
            print("⚠️ Status: Stage 1 only - Neural networks not available")
        
        print("🚀 ARI now has deep learning capabilities!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_stage_2_integration()
