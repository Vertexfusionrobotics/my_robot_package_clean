# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Master Brain - Enhanced with Stage 3: Advanced Neural Intelligence
Integrates generative networks, emotion detection, and personalization
"""

import speech_recognition as sr
import threading
import time
import json
import os
from datetime import datetime

# Import existing ARI components
try:
    from ari_speak import ARISpeak
    from ari_listen import ARIListen
    from chatbot_basic import ChatbotBasic
    from learning_module_enhanced import EnhancedLearningModule
    from neural_networks import ARINeuralNetworks
    from ari_generative_networks import ARIGenerativeNetworks
    ARI_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"Some ARI components not available: {e}")
    ARI_COMPONENTS_AVAILABLE = False

class ARIMasterBrainStage3:
    """
    Enhanced ARI Master Brain with Stage 3 capabilities:
    - Generative response networks
    - Real-time emotion detection  
    - User personalization
    - Advanced conversation memory
    """
    
    def __init__(self):
        print("🚀 Initializing ARI Master Brain - Stage 3: Advanced Neural Intelligence")
        
        # Initialize components
        self.speaker = None
        self.listener = None
        self.chatbot = None
        self.enhanced_learning = None
        self.neural_networks = None
        self.generative_networks = None
        
        # Stage 3 specific attributes
        self.stage = "Stage 3: Advanced Neural Intelligence"
        self.current_user = None
        self.conversation_context = []
        self.emotion_history = []
        self.personalization_active = True
        
        # Initialize all components
        self.initialize_components()
        
        # Configuration
        self.active = True
        self.listening = False
        
        print(f"✅ ARI Master Brain {self.stage} initialized successfully!")
    
    def initialize_components(self):
        """Initialize all ARI components including Stage 3 networks"""
        try:
            if ARI_COMPONENTS_AVAILABLE:
                # Core components
                self.speaker = ARISpeak()
                self.listener = ARIListen()
                self.chatbot = ChatbotBasic()
                
                # Enhanced learning (Stage 2)
                self.enhanced_learning = EnhancedLearningModule()
                self.neural_networks = ARINeuralNetworks()
                
                # Stage 3: Generative networks
                self.generative_networks = ARIGenerativeNetworks()
                
                print("✅ All ARI components initialized")
            else:
                print("⚠️ Running in limited mode - some components unavailable")
                
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
    
    def get_response(self, user_input, user_id=None):
        """
        Enhanced response generation with Stage 3 capabilities:
        - Generative neural networks
        - Emotion detection and response
        - User personalization
        - Context awareness
        """
        print(f"🧠 Processing with Stage 3 neural intelligence: '{user_input}'")
        
        try:
            # Stage 3: Use generative networks for advanced response
            if self.generative_networks:
                generation_result = self.generative_networks.generate_response(
                    user_input, 
                    user_id=user_id or self.current_user,
                    context=self.conversation_context
                )
                
                print(f"🎭 Emotion detected: {generation_result['emotion_detected']}")
                print(f"🧬 Generation method: {generation_result['generation_method']}")
                print(f"👤 Personalized: {generation_result['personalized']}")
                
                # Update emotion history
                self.emotion_history.append({
                    'timestamp': datetime.now(),
                    'emotion': generation_result['emotion_detected'],
                    'user_input': user_input
                })
                
                # Keep recent emotion history
                if len(self.emotion_history) > 20:
                    self.emotion_history = self.emotion_history[-20:]
                
                # If generative networks provided a good response, use it
                if generation_result['generation_method'] in ['neural', 'rule_based']:
                    response = generation_result['response']
                    
                    # Check if response is too generic - if so, try knowledge base
                    generic_responses = [
                        "I can explain that for you.",
                        "That's a good question!",
                        "Let me help clarify that.",
                        "I'm still learning how to respond to that."
                    ]
                    
                    if response in generic_responses:
                        # Try to get a better response from chatbot/knowledge base
                        if self.chatbot:
                            knowledge_response = self.chatbot.get_response(user_input)
                            # If knowledge base has a substantial response, use it
                            if knowledge_response and len(knowledge_response) > 30 and not any(generic in knowledge_response for generic in generic_responses):
                                response = knowledge_response
                                print(f"🧠 Enhanced response with knowledge base")
                    
                    # Enhance with Stage 2 neural network guidance if available
                    if self.neural_networks:
                        try:
                            input_features = self.enhanced_learning.extract_features(user_input, response)
                            nn_guidance = self.neural_networks.predict_best_response_type(input_features)
                            print(f"🧠 Stage 2 neural guidance: {nn_guidance}")
                        except:
                            pass
                    
                    # Update conversation context
                    self.update_conversation_context(user_input, response, generation_result)
                    
                    return response
            
            # Fallback to Stage 2 neural networks if Stage 3 not available
            if self.neural_networks and self.enhanced_learning:
                # Get Stage 2 response with neural network guidance
                chatbot_response = self.chatbot.get_response(user_input) if self.chatbot else "I'm thinking..."
                
                input_features = self.enhanced_learning.extract_features(user_input, chatbot_response)
                nn_guidance = self.neural_networks.predict_best_response_type(input_features)
                quality_score = self.neural_networks.predict_conversation_quality(input_features)
                
                print(f"🧠 Neural guidance: {nn_guidance} (quality: {quality_score:.3f})")
                
                # Apply neural network guidance to response selection
                if nn_guidance['predicted_type'] == 'direct_llm' and nn_guidance['confidence'] > 0.4:
                    response = chatbot_response
                elif nn_guidance['predicted_type'] == 'semantic_match':
                    response = self.enhanced_learning.get_semantic_response(user_input)
                else:
                    response = chatbot_response
                
                return response
            
            # Final fallback to basic chatbot
            if self.chatbot:
                return self.chatbot.get_response(user_input)
            else:
                return "I'm still learning how to respond to that."
                
        except Exception as e:
            print(f"❌ Error in get_response: {e}")
            return "I'm having trouble processing that right now."
    
    def update_conversation_context(self, user_input, response, generation_result):
        """Update conversation context for better continuity"""
        context_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'emotion': generation_result.get('emotion_detected', 'neutral'),
            'personalized': generation_result.get('personalized', False),
            'method': generation_result.get('generation_method', 'unknown')
        }
        
        self.conversation_context.append(context_entry)
        
        # Keep recent context (last 10 exchanges)
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]
    
    def handle_voice_command(self, user_input):
        """Handle special voice commands including Stage 3 features"""
        user_input_lower = user_input.lower()
        
        # Stage 3 specific commands
        if any(phrase in user_input_lower for phrase in ['set user', 'i am', 'my name is']):
            return self.handle_user_identification(user_input)
        
        elif any(phrase in user_input_lower for phrase in ['emotion history', 'how am i feeling', 'my emotions']):
            return self.get_emotion_summary()
        
        elif any(phrase in user_input_lower for phrase in ['conversation summary', 'what have we discussed']):
            return self.get_conversation_summary()
        
        elif any(phrase in user_input_lower for phrase in ['personalization', 'personalize', 'adapt to me']):
            return self.toggle_personalization()
        
        elif any(phrase in user_input_lower for phrase in ['stage 3 status', 'neural status']):
            return self.get_stage_3_status()
        
        # Stage 2 commands (from previous implementation)
        elif any(phrase in user_input_lower for phrase in ['train neural networks', 'train networks']):
            return self.train_neural_networks()
        
        elif any(phrase in user_input_lower for phrase in ['learning stats', 'learning statistics']):
            return self.get_enhanced_learning_stats()
        
        # Basic commands
        elif any(phrase in user_input_lower for phrase in ['stop listening', 'stop', 'quit', 'exit']):
            return self.stop_listening()
        
        elif any(phrase in user_input_lower for phrase in ['start listening', 'listen', 'wake up']):
            return self.start_listening()
        
        else:
            # Not a command, process as regular conversation
            return None
    
    def handle_user_identification(self, user_input):
        """Handle user identification for personalization"""
        try:
            # Extract user name/id from input
            words = user_input.lower().split()
            if 'i am' in user_input.lower():
                name_start = words.index('am') + 1
            elif 'my name is' in user_input.lower():
                name_start = words.index('is') + 1
            elif 'set user' in user_input.lower():
                name_start = words.index('user') + 1
            else:
                return "I didn't understand how to identify you. Try saying 'I am [your name]'."
            
            if name_start < len(words):
                self.current_user = ' '.join(words[name_start:]).strip()
                return f"Hello {self.current_user}! I'll personalize our conversation for you. How can I help you today?"
            else:
                return "I didn't catch your name. Could you tell me again?"
                
        except Exception as e:
            print(f"Error in user identification: {e}")
            return "I had trouble understanding your name. Could you try again?"
    
    def get_emotion_summary(self):
        """Get summary of detected emotions in conversation"""
        if not self.emotion_history:
            return "I haven't detected any emotions in our conversation yet."
        
        # Count emotions
        emotions = [entry['emotion'] for entry in self.emotion_history]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get most recent emotion
        latest_emotion = self.emotion_history[-1]['emotion']
        
        # Create summary
        most_common = max(emotion_counts.items(), key=lambda x: x[1])
        
        summary = f"In our conversation, I've detected {len(self.emotion_history)} emotional expressions. "
        summary += f"Your most common emotion has been '{most_common[0]}' ({most_common[1]} times). "
        summary += f"Right now, you seem to be feeling '{latest_emotion}'."
        
        return summary
    
    def get_conversation_summary(self):
        """Get summary of conversation context"""
        if not self.conversation_context:
            return "We haven't had much conversation yet."
        
        total_exchanges = len(self.conversation_context)
        recent_topics = [entry['user_input'][:50] + "..." if len(entry['user_input']) > 50 
                        else entry['user_input'] for entry in self.conversation_context[-3:]]
        
        summary = f"We've had {total_exchanges} exchanges in this conversation. "
        summary += f"Recent topics include: {', '.join(recent_topics)}. "
        
        if self.current_user:
            summary += f"I'm personalizing responses for {self.current_user}."
        
        return summary
    
    def toggle_personalization(self):
        """Toggle personalization on/off"""
        self.personalization_active = not self.personalization_active
        status = "enabled" if self.personalization_active else "disabled"
        return f"Personalization has been {status}. {'I will adapt my responses to your preferences.' if self.personalization_active else 'I will use standard responses.'}"
    
    def get_stage_3_status(self):
        """Get comprehensive Stage 3 status"""
        if not self.generative_networks:
            return "Stage 3 generative networks are not available."
        
        status = self.generative_networks.get_status()
        
        response = f"ARI Stage 3 Status:\\n"
        response += f"Version: {status['version']}\\n"
        response += f"Models loaded: {len(status['models_loaded'])} ({', '.join(status['models_loaded'])})\\n"
        response += f"Conversation history: {status['conversation_history']} interactions\\n"
        response += f"User profiles: {status['user_profiles']} users\\n"
        response += f"Current user: {self.current_user or 'Unknown'}\\n"
        response += f"Emotion tracking: {len(self.emotion_history)} emotions detected\\n"
        response += f"Personalization: {'Active' if self.personalization_active else 'Inactive'}"
        
        return response
    
    def train_neural_networks(self):
        """Train Stage 2 neural networks"""
        if not self.neural_networks or not self.enhanced_learning:
            return "Neural network training is not available."
        
        try:
            print("🧠 Starting neural network training...")
            prepared_data = self.enhanced_learning.prepare_neural_training_data()
            
            if prepared_data['sample_count'] < 5:
                return "Not enough training data yet. Need at least 5 conversation samples."
            
            # Train networks
            success = self.neural_networks.train_all_networks(prepared_data)
            
            if success:
                return "Neural networks have been trained successfully! I can now use deep learning to improve my responses."
            else:
                return "There was an issue training the neural networks. Please try again later."
                
        except Exception as e:
            print(f"Error training neural networks: {e}")
            return "I encountered an error while training. Please try again."
    
    def get_enhanced_learning_stats(self):
        """Get enhanced learning statistics"""
        if not self.enhanced_learning:
            return "Enhanced learning is not available."
        
        try:
            stats = self.enhanced_learning.get_learning_statistics()
            neural_status = "Neural Networks Active" if self.neural_networks else "Neural Networks Inactive"
            
            response = f"Enhanced Learning Statistics:\\n"
            response += f"Stage: {self.stage}\\n"
            response += f"Status: {neural_status}\\n"
            response += f"Conversations analyzed: {stats['conversations_analyzed']}\\n"
            response += f"Patterns identified: {stats['patterns_identified']}\\n"
            response += f"Response types: {', '.join(stats['response_types'])}\\n"
            response += f"Average response quality: {stats['avg_response_quality']:.2f}"
            
            return response
            
        except Exception as e:
            print(f"Error getting learning stats: {e}")
            return "I couldn't retrieve learning statistics right now."
    
    def start_listening(self):
        """Start listening for voice input"""
        if not self.listener:
            return "Voice recognition is not available."
        
        self.listening = True
        return "I'm now listening for your voice input."
    
    def stop_listening(self):
        """Stop listening and shutdown"""
        self.listening = False
        self.active = False
        return "Goodbye! I'm shutting down now."
    
    def speak_response(self, response):
        """Speak the response if speaker is available"""
        if self.speaker:
            try:
                self.speaker.speak(response)
            except Exception as e:
                print(f"Error speaking response: {e}")
    
    def run_conversation_loop(self):
        """Main conversation loop with Stage 3 capabilities"""
        print(f"🚀 Starting ARI conversation with {self.stage}")
        
        # Welcome message
        welcome_msg = "Hello! I'm ARI with advanced neural intelligence. I can now generate personalized responses, detect emotions, and adapt to your communication style. How can I help you today?"
        print(f"ARI: {welcome_msg}")
        self.speak_response(welcome_msg)
        
        while self.active:
            try:
                if self.listening and self.listener:
                    # Voice input
                    user_input = self.listener.listen()
                    if user_input:
                        print(f"User: {user_input}")
                        self.process_input(user_input)
                else:
                    # Text input
                    user_input = input("You: ").strip()
                    if user_input:
                        self.process_input(user_input)
                    
            except KeyboardInterrupt:
                print("\\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error in conversation loop: {e}")
                time.sleep(1)
    
    def process_input(self, user_input):
        """Process user input with Stage 3 capabilities"""
        if not user_input.strip():
            return
        
        # Check for voice commands first
        command_response = self.handle_voice_command(user_input)
        if command_response:
            print(f"ARI: {command_response}")
            self.speak_response(command_response)
            return
        
        # Get regular response with Stage 3 enhancements
        response = self.get_response(user_input, self.current_user)
        print(f"ARI: {response}")
        self.speak_response(response)
        
        # Log interaction for enhanced learning
        if self.enhanced_learning:
            try:
                self.enhanced_learning.log_interaction(user_input, response, "successful")
            except Exception as e:
                print(f"Error logging interaction: {e}")

def main():
    """Main function to run ARI Stage 3"""
    try:
        ari = ARIMasterBrainStage3()
        ari.run_conversation_loop()
    except Exception as e:
        print(f"Error running ARI Stage 3: {e}")

if __name__ == "__main__":
    main()
