# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test Neural Networks Module
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_neural_networks():
    print("🧠 Testing Neural Networks Module")
    print("=" * 40)
    
    try:
        from neural_networks import ARINeuralNetworks
        print("✅ Neural Networks module imported successfully")
        
        # Initialize neural networks
        nn = ARINeuralNetworks()
        print("✅ Neural Networks initialized")
        
        # Get status
        status = nn.get_neural_status()
        print(f"📊 Status: {status}")
        
        # Test with existing training data
        prepared_data = nn.prepare_training_data()
        if prepared_data:
            print(f"✅ Training data prepared: {prepared_data['X'].shape[0]} samples")
            
            # Try training a small model
            print("🧠 Starting neural network training...")
            
            # Train response predictor
            success1 = nn.train_response_predictor(prepared_data, epochs=10)
            if success1:
                print("✅ Response predictor trained successfully!")
            
            # Train quality predictor  
            success2 = nn.train_quality_predictor(prepared_data, epochs=10)
            if success2:
                print("✅ Quality predictor trained successfully!")
            
            # Test predictions
            if success1:
                sample_features = prepared_data['X'][0]
                prediction = nn.predict_best_response_type(sample_features)
                if prediction:
                    print(f"🎯 Response prediction: {prediction['response_type']} (confidence: {prediction['confidence']:.3f})")
            
            if success2:
                sample_features = prepared_data['X'][0]
                quality = nn.predict_conversation_quality(sample_features)
                if quality:
                    print(f"📈 Quality prediction: {quality['quality_score']:.3f} ({'success' if quality['predicted_success'] else 'needs improvement'})")
            
            # Save models
            nn.save_models()
            print("💾 Models saved")
            
        else:
            print("⚠️ No training data available")
        
        print("\n🎉 Neural Networks test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neural_networks()
