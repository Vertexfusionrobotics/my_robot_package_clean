# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Live test of ARI Enhanced Learning - monitors data collection in real-time
"""

import sys
import os
import json
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def monitor_learning_data():
    """Monitor the neural training data file for new entries"""
    print("🧠 ARI Enhanced Learning Data Monitor")
    print("=" * 50)
    
    training_file = "neural_training_data.json"
    
    try:
        # Check initial state
        if os.path.exists(training_file):
            with open(training_file, 'r', encoding='utf-8') as f:
                initial_data = json.load(f)
            print(f"📊 Initial training samples: {len(initial_data)}")
        else:
            initial_data = []
            print("📊 No training data file found yet")
        
        print("\n🎯 Test the enhanced learning by:")
        print("1. Run: python ari_master_brain_final.py")
        print("2. Have a conversation with ARI")
        print("3. Try commands: 'learning stats', 'prepare neural training'")
        print("4. This monitor will show data collection in real-time")
        print("\n⏰ Monitoring for data changes...")
        
        last_count = len(initial_data)
        
        while True:
            time.sleep(2)  # Check every 2 seconds
            
            if os.path.exists(training_file):
                try:
                    with open(training_file, 'r', encoding='utf-8') as f:
                        current_data = json.load(f)
                    
                    current_count = len(current_data)
                    
                    if current_count > last_count:
                        new_entries = current_count - last_count
                        print(f"\n✨ NEW DATA! {new_entries} new training sample(s) collected")
                        print(f"📈 Total samples: {current_count}")
                        
                        # Show details of the latest entry
                        if current_data:
                            latest = current_data[-1]
                            print(f"🎙️ Latest input: '{latest.get('user_input', 'Unknown')}'")
                            print(f"🤖 Response type: {latest.get('response_type', 'Unknown')}")
                            print(f"✅ Success: {latest.get('success', 'Unknown')}")
                        
                        last_count = current_count
                
                except json.JSONDecodeError:
                    pass  # File might be being written to
            
    except KeyboardInterrupt:
        print("\n\n🔄 Monitor stopped by user")
        
        # Final stats
        if os.path.exists(training_file):
            try:
                with open(training_file, 'r', encoding='utf-8') as f:
                    final_data = json.load(f)
                print(f"📊 Final training samples collected: {len(final_data)}")
                
                # Show response type distribution
                response_types = {}
                for entry in final_data:
                    resp_type = entry.get('response_type', 'unknown')
                    response_types[resp_type] = response_types.get(resp_type, 0) + 1
                
                if response_types:
                    print("\n📋 Response Type Distribution:")
                    for resp_type, count in response_types.items():
                        print(f"  {resp_type}: {count}")
            except:
                pass

def test_specific_enhanced_features():
    """Test specific enhanced learning features"""
    print("\n🔬 Testing Specific Enhanced Learning Features")
    print("=" * 50)
    
    try:
        from learning_module_enhanced import EnhancedLearningModule
        enhanced = EnhancedLearningModule()
        
        # Test with more diverse inputs
        test_inputs = [
            "Hello ARI, how are you today?",
            "What is machine learning and how does it work?",
            "Can you help me understand quantum computing?",
            "I'm feeling confused about neural networks",
            "Goodbye for now",
        ]
        
        print("📊 Analyzing diverse conversation patterns:")
        for i, user_input in enumerate(test_inputs, 1):
            analysis = enhanced.analyze_speech_patterns(user_input)
            print(f"{i}. '{user_input}'")
            print(f"   Type: {analysis['question_type']}")
            print(f"   Complexity: {analysis['complexity_score']:.3f}")
            print(f"   Word count: {analysis['word_count']}")
            print()
        
        # Test data collection with different scenarios
        print("💾 Testing data collection scenarios:")
        scenarios = [
            ("What's the weather?", "It's sunny today!", "semantic_match", True),
            ("Tell me a joke", "I don't know any jokes yet", "fallback", False),
            ("How do robots work?", "Robots use sensors and actuators...", "direct_llm", True),
        ]
        
        for user_input, response, resp_type, success in scenarios:
            enhanced.collect_training_data(
                user_input=user_input,
                response=response,
                response_type=resp_type,
                success=success
            )
            print(f"✅ Collected: {resp_type} ({'successful' if success else 'needs improvement'})")
        
        # Get updated statistics
        stats = enhanced.get_learning_statistics()
        print(f"\n📈 Updated Statistics:")
        print(f"   Total conversations: {stats.get('total_conversations', 0)}")
        print(f"   Training samples: {stats.get('training_samples', 0)}")
        
        print("\n🎉 Enhanced learning features are working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing enhanced features: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_learning_data()
    elif len(sys.argv) > 1 and sys.argv[1] == "--features":
        test_specific_enhanced_features()
    else:
        print("🧠 ARI Enhanced Learning Test Suite")
        print("=" * 40)
        print()
        print("Options:")
        print("  python test_enhanced_full.py --monitor")
        print("    Monitor real-time data collection during ARI conversations")
        print()
        print("  python test_enhanced_full.py --features") 
        print("    Test specific enhanced learning features")
        print()
        print("  python test_enhanced_full.py")
        print("    Show this help")
