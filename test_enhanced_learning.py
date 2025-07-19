# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script for Enhanced Learning Module integration with ARI
This tests Stage 1 functionality: data collection and pattern analysis
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from learning_module_enhanced import EnhancedLearningModule
    print("✅ Enhanced Learning Module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Enhanced Learning Module: {e}")
    sys.exit(1)

def test_enhanced_learning():
    """Test the enhanced learning module functionality"""
    print("\n🧠 Testing Enhanced Learning Module - Stage 1")
    print("=" * 50)
    
    # Initialize the enhanced learning module
    enhanced_learning = EnhancedLearningModule()
    print("✅ Enhanced Learning Module initialized")
    
    # Test 1: Speech pattern analysis
    print("\n📊 Test 1: Speech Pattern Analysis")
    test_inputs = [
        "What is the weather like today?",
        "Tell me about artificial intelligence",
        "How do neural networks work?",
        "Can you help me with programming?",
        "What time is it?"
    ]
    
    for user_input in test_inputs:
        try:
            analysis = enhanced_learning.analyze_speech_patterns(user_input)
            print(f"  Input: '{user_input}'")
            print(f"  Type: {analysis['question_type']}, Complexity: {analysis['complexity_score']:.2f}")
        except Exception as e:
            print(f"  ❌ Error analyzing '{user_input}': {e}")
    
    # Test 2: Training data collection
    print("\n💾 Test 2: Training Data Collection")
    test_conversations = [
        ("What is Python?", "Python is a programming language", "semantic_match", True),
        ("How are you?", "I'm doing well, thank you!", "direct_llm", True),
        ("What is quantum physics?", "I don't have that information yet...", "fallback", False),
    ]
    
    for user_input, response, response_type, success in test_conversations:
        try:
            result = enhanced_learning.collect_training_data(
                user_input=user_input,
                response=response,
                response_type=response_type,
                success=success
            )
            print(f"  ✅ Collected data for: '{user_input}' -> '{response[:30]}...'")
        except Exception as e:
            print(f"  ❌ Error collecting data: {e}")
    
    # Test 3: Conversation effectiveness analysis
    print("\n📈 Test 3: Conversation Effectiveness Analysis")
    test_effectiveness = [
        ("What is AI?", "AI is artificial intelligence", False),
        ("Unknown topic", "I don't have that information yet", True),
    ]
    
    for user_input, response, was_fallback in test_effectiveness:
        try:
            enhanced_learning.analyze_conversation_effectiveness(
                user_input=user_input,
                response=response,
                was_fallback=was_fallback
            )
            print(f"  ✅ Analyzed effectiveness for: '{user_input}' (fallback: {was_fallback})")
        except Exception as e:
            print(f"  ❌ Error analyzing effectiveness: {e}")
    
    # Test 4: Get learning statistics
    print("\n📊 Test 4: Learning Statistics")
    try:
        stats = enhanced_learning.get_learning_statistics()
        print(f"  Total conversations analyzed: {stats.get('total_conversations', 0)}")
        print(f"  Pattern categories identified: {stats.get('pattern_categories', 0)}")
        print(f"  Training samples collected: {stats.get('training_samples', 0)}")
        
        if stats.get('pattern_distribution'):
            print("  Pattern distribution:")
            for pattern, count in stats['pattern_distribution'].items():
                print(f"    {pattern}: {count}")
    except Exception as e:
        print(f"  ❌ Error getting statistics: {e}")
    
    # Test 5: Neural training data preparation
    print("\n🚀 Test 5: Neural Training Data Preparation")
    try:
        prepared_data = enhanced_learning.prepare_neural_training_data()
        if prepared_data:
            print(f"  ✅ Prepared {len(prepared_data.get('training_samples', []))} training samples")
            print(f"  📋 Feature dimensions: {prepared_data.get('feature_dimensions', 'Unknown')}")
            print("  🎯 Ready for Stage 2: Neural Network Implementation")
        else:
            print("  ⚠️ Insufficient data for neural training preparation")
    except Exception as e:
        print(f"  ❌ Error preparing neural training data: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced Learning Module test completed!")
    print("💡 Stage 1 (Data Collection & Pattern Analysis) is working!")
    print("🚀 Ready for Stage 2: Neural Network Implementation")

if __name__ == "__main__":
    test_enhanced_learning()
