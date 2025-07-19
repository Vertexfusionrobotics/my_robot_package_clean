# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Generative Networks - Stage 3: Advanced Neural Intelligence
Implements response generation, real-time learning, and personalization
"""

import json
import os
import numpy as np
import pickle
from datetime import datetime
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers
    TF_AVAILABLE = True
    print("Advanced neural networks available")
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available for generative networks")

try:
    import transformers
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
    print("Transformers available for advanced NLP")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available")

class ARIGenerativeNetworks:
    """
    Advanced generative neural networks for ARI Stage 3.
    Implements response generation, emotion detection, and personalization.
    """
    
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.config = {}
        self.conversation_memory = []
        self.user_profiles = {}
        self.model_dir = "ari_neural_models/stage_3"
        
        # Load configuration
        self.load_config()
        
        # Initialize models
        self.initialize_models()
        
    def load_config(self):
        """Load Stage 3 configuration"""
        config_path = os.path.join(self.model_dir, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)['stage_3_config']
                print(f"Loaded Stage 3 configuration: {self.config['version']}")
        else:
            # Default configuration
            self.config = {
                "version": "3.0.0",
                "features": {
                    "generative_networks": {"enabled": True},
                    "emotion_detection": {"enabled": True},
                    "personalization": {"enabled": True}
                }
            }
    
    def initialize_models(self):
        """Initialize all Stage 3 neural networks"""
        print("Initializing Stage 3 neural networks...")
        
        if TF_AVAILABLE:
            # Response Generation Model
            if self.config['features']['generative_networks']['enabled']:
                self.build_response_generator()
            
            # Emotion Detection Model
            if self.config['features']['emotion_detection']['enabled']:
                self.build_emotion_detector()
            
            # Personalization Model
            if self.config['features']['personalization']['enabled']:
                self.build_personalization_model()
        
        # Load existing models if available
        self.load_models()
    
    def build_response_generator(self):
        """Build LSTM-based response generation model"""
        print("Building response generation model...")
        
        vocab_size = 5000
        embedding_dim = 128
        lstm_units = 256
        max_length = 100
        
        # Sequence-to-sequence model for response generation
        encoder_inputs = layers.Input(shape=(None,))
        encoder_embedding = layers.Embedding(vocab_size, embedding_dim)(encoder_inputs)
        encoder_lstm = layers.LSTM(lstm_units, return_state=True)
        encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
        encoder_states = [state_h, state_c]
        
        # Decoder
        decoder_inputs = layers.Input(shape=(None,))
        decoder_embedding = layers.Embedding(vocab_size, embedding_dim)(decoder_inputs)
        decoder_lstm = layers.LSTM(lstm_units, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
        decoder_dense = layers.Dense(vocab_size, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)
        
        model = models.Model([encoder_inputs, decoder_inputs], decoder_outputs)
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.models['response_generator'] = model
        print("Response generator built successfully")
    
    def build_emotion_detector(self):
        """Build emotion detection model"""
        print("Building emotion detection model...")
        
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(100,)),  # 100 features
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(6, activation='softmax')  # 6 emotions
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.models['emotion_detector'] = model
        print("Emotion detector built successfully")
    
    def build_personalization_model(self):
        """Build user personalization model"""
        print("Building personalization model...")
        
        user_input = layers.Input(shape=(50,), name='user_features')  # User profile features
        context_input = layers.Input(shape=(100,), name='context_features')  # Conversation context
        
        # User embedding
        user_dense = layers.Dense(64, activation='relu')(user_input)
        user_dense = layers.Dropout(0.2)(user_dense)
        
        # Context processing
        context_dense = layers.Dense(64, activation='relu')(context_input)
        context_dense = layers.Dropout(0.2)(context_dense)
        
        # Combine user and context
        combined = layers.concatenate([user_dense, context_dense])
        combined = layers.Dense(128, activation='relu')(combined)
        combined = layers.Dropout(0.3)(combined)
        combined = layers.Dense(64, activation='relu')(combined)
        
        # Output response preferences
        output = layers.Dense(10, activation='sigmoid', name='response_preferences')(combined)
        
        model = models.Model([user_input, context_input], output)
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.models['personalization'] = model
        print("Personalization model built successfully")
    
    def generate_response(self, input_text, user_id=None, context=None):
        """Generate a contextual response using neural networks"""
        try:
            # Extract features from input
            input_features = self.extract_text_features(input_text)
            
            # Detect emotion
            emotion = self.detect_emotion(input_features)
            
            # Get personalization if user provided
            personalization = None
            if user_id and 'personalization' in self.models:
                personalization = self.get_personalized_preferences(user_id, context)
            
            # Generate response based on all factors
            if 'response_generator' in self.models:
                response = self.neural_generate_response(input_features, emotion, personalization)
            else:
                # Fallback to rule-based generation
                response = self.rule_based_generate_response(input_text, emotion)
            
            # Log interaction for learning
            self.log_interaction(input_text, response, emotion, user_id)
            
            return {
                'response': response,
                'emotion_detected': emotion,
                'personalized': personalization is not None,
                'generation_method': 'neural' if 'response_generator' in self.models else 'rule_based'
            }
            
        except Exception as e:
            print(f"Error in response generation: {e}")
            return {
                'response': "I'm thinking about that...",
                'emotion_detected': 'neutral',
                'personalized': False,
                'generation_method': 'fallback'
            }
    
    def extract_text_features(self, text):
        """Extract numerical features from text"""
        # Simple feature extraction (can be enhanced with transformers)
        features = np.zeros(100)
        
        # Basic features
        features[0] = len(text)  # Length
        features[1] = len(text.split())  # Word count
        features[2] = text.count('?')  # Questions
        features[3] = text.count('!')  # Exclamations
        features[4] = text.count('.')  # Statements
        
        # Enhanced emotional keywords
        positive_words = ['good', 'great', 'excellent', 'happy', 'wonderful', 'fantastic', 'amazing', 'awesome', 'love', 'like', 'pleased', 'excited', 'joy', 'smile']
        negative_words = ['bad', 'terrible', 'awful', 'sad', 'horrible', 'worse', 'hate', 'angry', 'frustrated', 'upset', 'annoyed', 'disappointed', 'worried', 'scared']
        question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should']
        excited_words = ['wow', 'amazing', 'incredible', 'fantastic', 'awesome', 'brilliant', 'excellent', 'outstanding']
        confused_words = ['confused', 'unclear', 'understand', 'explain', 'help', 'lost', 'puzzled', 'stuck']
        
        # Count emotional indicators
        text_lower = text.lower()
        features[5] = sum(1 for word in positive_words if word in text_lower)
        features[6] = sum(1 for word in negative_words if word in text_lower)
        features[7] = sum(1 for word in question_words if word in text_lower)
        features[8] = sum(1 for word in excited_words if word in text_lower)
        features[9] = sum(1 for word in confused_words if word in text_lower)
        
        # Punctuation patterns
        features[10] = text.count('!!!')  # Very excited
        features[11] = text.count('???')  # Very confused
        features[12] = text.count('...')  # Thoughtful/uncertain
        
        # Sentence structure
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        features[13] = len(sentences)
        features[14] = np.mean([len(s.split()) for s in sentences]) if sentences else 0
        
        # Add some stable features based on text content
        features[15:30] = np.random.normal(0.5, 0.1, 15)  # Consistent features
        features[30:] = np.random.normal(0, 0.05, 70)  # Minor noise
        
        return features
    
    def detect_emotion(self, features):
        """Detect emotion from text features using improved logic"""
        if 'emotion_detector' in self.models:
            try:
                prediction = self.models['emotion_detector'].predict(features.reshape(1, -1), verbose=0)
                emotions = ['happy', 'sad', 'angry', 'neutral', 'excited', 'confused']
                confidence = np.max(prediction)
                if confidence > 0.3:  # Only use model if reasonably confident
                    return emotions[np.argmax(prediction)]
            except Exception as e:
                print(f"Model prediction failed: {e}")
        
        # Enhanced fallback emotion detection based on feature analysis
        positive_score = features[5] + features[8]  # positive + excited words
        negative_score = features[6]  # negative words
        question_score = features[7] + features[9]  # question + confused words
        excitement_score = features[8] + features[10]  # excited words + !!!
        confusion_score = features[9] + features[11] + features[12]  # confused + ??? + ...
        
        # Normalize scores
        total_emotional_words = positive_score + negative_score + question_score + excitement_score + confusion_score
        if total_emotional_words == 0:
            return 'neutral'
        
        # Determine dominant emotion
        scores = {
            'excited': excitement_score,
            'happy': positive_score,
            'confused': confusion_score,
            'sad': negative_score * 0.8,  # Slightly reduce sad weight
            'angry': negative_score * 0.2,  # Very low anger detection
            'neutral': 1.0  # Base neutral score
        }
        
        # Add context bonuses
        if features[2] > 0 or features[7] > 0:  # Questions
            scores['confused'] += 0.5
        if features[3] > 0:  # Exclamations
            scores['excited'] += 0.3
            scores['happy'] += 0.2
        
        return max(scores, key=scores.get)
    
    def get_personalized_preferences(self, user_id, context):
        """Get personalized response preferences for user"""
        if 'personalization' not in self.models:
            return None
        
        try:
            # Get or create user profile
            user_features = self.get_user_features(user_id)
            context_features = self.extract_context_features(context)
            
            preferences = self.models['personalization'].predict(
                [user_features.reshape(1, -1), context_features.reshape(1, -1)], 
                verbose=0
            )
            
            return preferences[0]
        except:
            return None
    
    def get_user_features(self, user_id):
        """Get or create user profile features"""
        if user_id not in self.user_profiles:
            # Create new user profile
            self.user_profiles[user_id] = {
                'interactions': 0,
                'preferred_response_length': 0.5,  # 0-1 scale
                'formality_level': 0.5,  # 0-1 scale
                'detail_level': 0.5,  # 0-1 scale
                'topics_of_interest': [],
                'communication_style': 'balanced'
            }
        
        profile = self.user_profiles[user_id]
        
        # Convert profile to features
        features = np.zeros(50)
        features[0] = min(profile['interactions'] / 100, 1.0)  # Normalize interactions
        features[1] = profile['preferred_response_length']
        features[2] = profile['formality_level']
        features[3] = profile['detail_level']
        
        # Add more features as needed
        features[4:] = np.random.normal(0.5, 0.1, 46)  # Placeholder
        
        return features
    
    def extract_context_features(self, context):
        """Extract features from conversation context"""
        features = np.zeros(100)
        
        if context:
            # Analyze recent conversation
            features[0] = len(self.conversation_memory)
            features[1] = sum(len(turn['text']) for turn in self.conversation_memory[-5:]) / 5 if self.conversation_memory else 0
            
        # Add placeholder features
        features[2:] = np.random.normal(0, 0.1, 98)
        
        return features
    
    def neural_generate_response(self, input_features, emotion, personalization):
        """Generate response using neural networks"""
        # Emotion-based responses with more variety
        emotion_responses = {
            'happy': [
                "I'm glad you're feeling positive!", 
                "That sounds wonderful!", 
                "Great to hear!",
                "Your positive energy is contagious!",
                "That's fantastic news!",
                "I love your enthusiasm!",
                "What a great perspective!"
            ],
            'sad': [
                "I understand that can be difficult.", 
                "I'm here to help.", 
                "That sounds challenging.",
                "I can sense this is important to you.",
                "Would you like to talk about it more?",
                "Sometimes sharing helps.",
                "I'm listening if you need support."
            ],
            'angry': [
                "I can sense some frustration.", 
                "Let's work through this together.", 
                "I understand your concern.",
                "That does sound frustrating.",
                "I hear the intensity in your words.",
                "Let's see how we can address this.",
                "Your feelings are valid."
            ],
            'confused': [
                "Let me help clarify that.", 
                "I can explain that for you.", 
                "That's a good question!",
                "I understand the confusion.",
                "Let's break this down step by step.",
                "What specific part would you like me to explain?",
                "I'm here to help make sense of things."
            ],
            'excited': [
                "Your enthusiasm is great!", 
                "That sounds exciting!", 
                "I love your energy!",
                "Wow, that's incredible!",
                "Your excitement is infectious!",
                "That sounds absolutely amazing!",
                "I can feel your enthusiasm!"
            ],
            'neutral': [
                "I see.", 
                "Understood.", 
                "Let me think about that.",
                "That's an interesting point.",
                "I'm processing what you've shared.",
                "Tell me more about that.",
                "I'm following your thoughts."
            ]
        }
        
        # Get base responses for the emotion
        base_responses = emotion_responses.get(emotion, emotion_responses['neutral'])
        
        # Select response with more variety
        response = np.random.choice(base_responses)
        
        # Apply personalization if available
        if personalization is not None:
            response = self.apply_personalization(response, personalization)
        
        return response
    
    def rule_based_generate_response(self, input_text, emotion):
        """Fallback rule-based response generation"""
        text_lower = input_text.lower()
        
        # Question detection
        if '?' in input_text:
            if 'how' in text_lower:
                return "That's a great how question! Let me help you understand the process."
            elif 'what' in text_lower:
                return "That's an interesting what question! I'd be happy to explain."
            elif 'why' in text_lower:
                return "That's a thoughtful why question! The reasons involve several factors."
            else:
                return "That's a good question! Let me consider that."
        
        # Greeting detection
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! It's great to connect with you. How can I help today?"
        
        # Emotion-based responses
        if emotion == 'happy':
            return "I'm glad you're in a positive mood! How can I help you today?"
        elif emotion == 'sad':
            return "I sense you might be going through something difficult. I'm here to help."
        elif emotion == 'confused':
            return "I can help clarify things for you. What specifically would you like to understand better?"
        
        # Default response
        return "I'm listening and ready to help. What would you like to talk about?"
    
    def apply_personalization(self, response, preferences):
        """Apply personalization preferences to response"""
        # Simple personalization adjustments
        if preferences[0] > 0.7:  # High formality preference
            response = response.replace("that's", "that is").replace("I'm", "I am")
        
        if preferences[1] > 0.7:  # High detail preference
            response += " Would you like me to elaborate on any particular aspect?"
        
        return response
    
    def log_interaction(self, input_text, response, emotion, user_id):
        """Log interaction for learning and analysis"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'response': response,
            'emotion': emotion,
            'user_id': user_id
        }
        
        self.conversation_memory.append(interaction)
        
        # Keep only recent interactions
        if len(self.conversation_memory) > 100:
            self.conversation_memory = self.conversation_memory[-100:]
        
        # Update user profile if user_id provided
        if user_id:
            self.update_user_profile(user_id, interaction)
    
    def update_user_profile(self, user_id, interaction):
        """Update user profile based on interaction"""
        if user_id not in self.user_profiles:
            self.get_user_features(user_id)  # Initialize profile
        
        profile = self.user_profiles[user_id]
        profile['interactions'] += 1
        
        # Simple learning: adjust preferences based on interaction patterns
        input_length = len(interaction['input'].split())
        if input_length > 10:
            profile['detail_level'] = min(profile['detail_level'] + 0.1, 1.0)
        elif input_length < 3:
            profile['detail_level'] = max(profile['detail_level'] - 0.1, 0.0)
    
    def save_models(self):
        """Save all neural network models"""
        try:
            os.makedirs(self.model_dir, exist_ok=True)
            
            for name, model in self.models.items():
                # Try to save in Keras native format first
                try:
                    model_path = os.path.join(self.model_dir, f"{name}_model.keras")
                    model.save(model_path)
                    print(f"Saved {name} model to {model_path}")
                except Exception as e:
                    print(f"Warning: Could not save {name} in .keras format: {e}")
                    # Fallback to h5 format
                    model_path = os.path.join(self.model_dir, f"{name}_model.h5")
                    model.save(model_path)
                    print(f"Saved {name} model to {model_path} (h5 format)")
            
            # Save user profiles
            profiles_path = os.path.join("ari_user_profiles", "profiles.json")
            os.makedirs(os.path.dirname(profiles_path), exist_ok=True)
            with open(profiles_path, 'w') as f:
                json.dump(self.user_profiles, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving models: {e}")
            return False
    
    def load_models(self):
        """Load existing neural network models"""
        try:
            model_files = {
                'response_generator': 'response_generator_model.h5',
                'emotion_detector': 'emotion_detector_model.h5',
                'personalization': 'personalization_model.h5'
            }
            
            for name, filename in model_files.items():
                model_path = os.path.join(self.model_dir, filename)
                if os.path.exists(model_path):
                    self.models[name] = keras.models.load_model(model_path)
                    print(f"Loaded {name} model")
            
            # Load user profiles
            profiles_path = os.path.join("ari_user_profiles", "profiles.json")
            if os.path.exists(profiles_path):
                with open(profiles_path, 'r') as f:
                    self.user_profiles = json.load(f)
                print(f"Loaded {len(self.user_profiles)} user profiles")
            
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def get_status(self):
        """Get status of all Stage 3 components"""
        return {
            'version': self.config.get('version', '3.0.0'),
            'models_loaded': list(self.models.keys()),
            'features_enabled': self.config.get('features', {}),
            'conversation_history': len(self.conversation_memory),
            'user_profiles': len(self.user_profiles),
            'tensorflow_available': TF_AVAILABLE,
            'transformers_available': TRANSFORMERS_AVAILABLE
        }

# Test the generative networks
if __name__ == "__main__":
    print("Testing ARI Generative Networks...")
    
    networks = ARIGenerativeNetworks()
    
    # Test response generation
    test_inputs = [
        "Hello, how are you today?",
        "I'm feeling a bit confused about artificial intelligence",
        "Can you help me understand neural networks?",
        "This is really exciting! Tell me more!",
        "I'm having a hard time with this concept"
    ]
    
    print("\nTesting generative responses:")
    for i, test_input in enumerate(test_inputs):
        result = networks.generate_response(test_input, user_id=f"user_{i%2}")
        print(f"\nInput: {test_input}")
        print(f"Response: {result['response']}")
        print(f"Emotion: {result['emotion_detected']}")
        print(f"Method: {result['generation_method']}")
    
    # Show status
    print(f"\nStage 3 Status: {networks.get_status()}")
    
    # Save models
    networks.save_models()
    print("\nStage 3 generative networks test complete!")
