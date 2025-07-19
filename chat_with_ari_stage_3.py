# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Quick ARI Stage 3 Chat Session
Interactive demonstration of ARI's advanced neural capabilities
"""

import sys
from ari_generative_networks import ARIGenerativeNetworks

def main():
    print("🚀 ARI Stage 3 Neural Chat Session")
    print("=" * 50)
    print("Initializing advanced neural intelligence...")
    
    # Initialize the neural networks
    ari = ARIGenerativeNetworks()
    
    print("✅ ARI Stage 3 ready!")
    print("\nARI: Hello! I'm ARI with advanced neural intelligence.")
    print("     I can detect emotions, personalize responses, and learn from our conversation.")
    print("     Try asking me anything or use commands like:")
    print("     - 'my name is [name]' (I'll remember you)")
    print("     - 'stage 3 status' (system info)")
    print("     - 'quit' to exit")
    print()
    
    conversation_count = 0
    user_name = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nARI: Goodbye! Thanks for chatting with my Stage 3 neural intelligence! 🤖")
                break
            
            if not user_input:
                continue
            
            conversation_count += 1
            
            # Handle special commands
            if user_input.lower().startswith('my name is'):
                user_name = user_input[10:].strip()
                print(f"ARI: Nice to meet you, {user_name}! I'll remember you and adapt to your communication style.")
                continue
            
            if 'stage 3 status' in user_input.lower():
                status = ari.get_status()
                print(f"ARI: Stage 3 Status - Version: {status['version']}")
                print(f"     Models loaded: {len(status['models_loaded'])}")
                print(f"     User profiles: {status['user_profiles']}")
                print(f"     Conversation history: {status['conversation_history']}")
                continue
            
            # Generate response using Stage 3 neural intelligence
            response_data = ari.generate_response(
                user_input, 
                user_id=user_name or f"user_{conversation_count}",
                context=[]
            )
            
            response = response_data['response']
            emotion = response_data['emotion_detected']
            method = response_data['generation_method']
            personalized = response_data['personalized']
            
            # Display the response with neural intelligence info
            print(f"ARI: {response}")
            print(f"     🎭 Emotion detected: {emotion} | 🧬 Method: {method} | 👤 Personalized: {personalized}")
            
        except KeyboardInterrupt:
            print("\n\nARI: Chat session ended. Thanks for testing Stage 3! 🚀")
            break
        except Exception as e:
            print(f"ARI: Sorry, I encountered an error: {e}")
            print("     Let me try to continue...")

if __name__ == "__main__":
    main()
