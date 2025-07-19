# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Enhanced Learning Module - Stage 2: Neural Network Integration
Extends existing learning capabilities with actual neural networks for deep learning
"""

import json
import os
import time
import numpy as np
from datetime import datetime
from collections import defaultdict, Counter
import re

try:
    from neural_networks import ARINeuralNetworks
    NEURAL_NETWORKS_AVAILABLE = True
except ImportError:
    NEURAL_NETWORKS_AVAILABLE = False
    class ARINeuralNetworks:
        def __init__(self): pass
        def predict_best_response_type(self, *args): return None
        def predict_conversation_quality(self, *args): return None

class EnhancedLearningModule:
    """
    Enhanced learning module with neural network integration.
    Stage 2: Combines pattern analysis with actual deep learning.
    """
    
    def __init__(self):
        self.conversation_history = []
        self.pattern_database = defaultdict(list)
        self.user_behavior_patterns = {}
        self.response_effectiveness = {}
        self.training_data_file = "neural_training_data.json"
        self.patterns_file = "conversation_patterns.json"
        
        # Neural Networks Integration
        if NEURAL_NETWORKS_AVAILABLE:
            self.neural_networks = ARINeuralNetworks()
            print("🧠 Neural networks integrated with enhanced learning")
        else:
            self.neural_networks = None
            print("⚠️ Neural networks not available - using fallback methods")
        
        # Load existing data
        self.load_training_data()
        self.load_patterns()
    
    def analyze_speech_patterns(self, user_input, context=None):
        """
        Analyze patterns in user speech for future neural network training.
        Stage 1: Collect and categorize data.
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'word_count': len(user_input.split()),
            'question_type': self._classify_question_type(user_input),
            'sentiment_indicators': self._extract_sentiment_indicators(user_input),
            'complexity_score': self._calculate_complexity(user_input),
            'context': context or {}
        }
        
        # Store for future neural network training
        self.conversation_history.append(analysis)
        
        # Update pattern database
        q_type = analysis['question_type']
        self.pattern_database[q_type].append({
            'input': user_input,
            'analysis': analysis
        })
        
        return analysis
    
    def collect_training_data(self, user_input, response, response_type=None, success=None, feedback=None, response_time=None):
        """
        Collect conversation data for neural network training.
        This builds the dataset we'll use for deep learning later.
        """
        training_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'system_response': response,
            'response_type': response_type,  # semantic_match, direct_llm, fallback, etc.
            'success': success,  # True/False indicator of response quality
            'feedback': feedback,  # positive, negative, or neutral
            'response_time': response_time,
            'input_features': self._extract_input_features(user_input),
            'response_features': self._extract_response_features(response)
        }
        
        # Add to training dataset
        try:
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            training_data = []
        
        training_data.append(training_entry)
        
        # Keep only last 1000 entries to prevent file from getting too large
        if len(training_data) > 1000:
            training_data = training_data[-1000:]
        
        with open(self.training_data_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2)
        
        return training_entry
    
    def analyze_conversation_effectiveness(self, user_input, response, was_fallback=False, follow_up=None):
        """
        Analyze how effective responses are based on user follow-ups.
        This helps identify what works well for future neural network training.
        """
        effectiveness_score = 0
        
        # Penalize fallback responses
        if was_fallback:
            effectiveness_score -= 1
        
        if follow_up:
            follow_up_lower = follow_up.lower()
            
            # Positive indicators
            positive_indicators = [
                'thank', 'great', 'perfect', 'exactly', 'yes', 'correct', 
                'helpful', 'good', 'right', 'awesome', 'cool'
            ]
            
            # Negative indicators  
            negative_indicators = [
                'no', 'wrong', 'incorrect', 'not what', "that's not", 
                'try again', 'misunderstood', 'different'
            ]
            
            for indicator in positive_indicators:
                if indicator in follow_up_lower:
                    effectiveness_score += 1
            
            for indicator in negative_indicators:
                if indicator in follow_up_lower:
                    effectiveness_score -= 1
        
        # Store effectiveness data
        response_key = self._create_response_key(user_input, response)
        if response_key not in self.response_effectiveness:
            self.response_effectiveness[response_key] = []
        
        self.response_effectiveness[response_key].append({
            'score': effectiveness_score,
            'timestamp': datetime.now().isoformat(),
            'follow_up': follow_up
        })
        
        return effectiveness_score
    
    def predict_response_timing(self, user_input, context=None):
        """
        Predict optimal response timing based on user patterns.
        Stage 1: Rule-based analysis, prepares for neural network implementation.
        """
        # Analyze urgency indicators
        urgency_keywords = ['urgent', 'quickly', 'fast', 'hurry', 'now', 'immediate']
        complexity = self._calculate_complexity(user_input)
        
        urgency_score = 0
        for keyword in urgency_keywords:
            if keyword in user_input.lower():
                urgency_score += 1
        
        # Determine timing category
        if urgency_score > 0:
            timing = 'immediate'  # Respond as fast as possible
        elif complexity > 0.7:
            timing = 'deliberate'  # Take time for complex responses
        else:
            timing = 'normal'  # Standard response timing
        
        return {
            'timing_category': timing,
            'urgency_score': urgency_score,
            'complexity_score': complexity,
            'recommended_delay': self._calculate_response_delay(timing)
        }
    
    def prepare_neural_training_data(self):
        """
        Convert collected conversation data into format suitable for neural network training.
        This prepares the data for Stage 2 implementation.
        """
        try:
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        
        # Convert to neural network training format
        input_vectors = []
        output_vectors = []
        metadata = []
        
        for entry in raw_data:
            # Convert text to numerical features (basic implementation)
            input_vector = self._text_to_vector(entry['user_input'])
            output_vector = self._text_to_vector(entry['system_response'])
            
            input_vectors.append(input_vector)
            output_vectors.append(output_vector)
            metadata.append({
                'timestamp': entry['timestamp'],
                'feedback': entry.get('feedback'),
                'response_time': entry.get('response_time')
            })
        
        neural_data = {
            'input_vectors': input_vectors,
            'output_vectors': output_vectors,
            'metadata': metadata,
            'vector_size': len(input_vectors[0]) if input_vectors else 0,
            'total_samples': len(input_vectors)
        }
        
        # Save prepared data
        with open('neural_ready_data.json', 'w', encoding='utf-8') as f:
            json.dump(neural_data, f, indent=2)
        
        return neural_data
    
    def get_learning_statistics(self):
        """Get statistics about collected learning data."""
        try:
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            training_data = []
        
        stats = {
            'total_conversations': len(training_data),
            'question_types': dict(Counter([
                self._classify_question_type(entry['user_input']) 
                for entry in training_data
            ])),
            'average_response_length': np.mean([
                len(entry['system_response'].split()) 
                for entry in training_data
            ]) if training_data else 0,
            'data_collection_started': min([
                entry['timestamp'] for entry in training_data
            ]) if training_data else None,
            'ready_for_neural_training': len(training_data) >= 50  # Minimum for basic training
        }
        
        return stats
    
    # Helper methods
    def _classify_question_type(self, text):
        """Classify the type of question/input."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['what', 'when', 'where', 'who', 'why', 'how']):
            return 'factual_question'
        elif any(word in text_lower for word in ['can you', 'could you', 'please']):
            return 'request'
        elif any(word in text_lower for word in ['hello', 'hi', 'hey', 'good morning']):
            return 'greeting'
        elif '?' in text:
            return 'general_question'
        else:
            return 'statement'
    
    def _extract_sentiment_indicators(self, text):
        """Extract basic sentiment indicators from text."""
        positive_words = ['good', 'great', 'awesome', 'excellent', 'perfect', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'wrong', 'problem']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'sentiment_score': positive_count - negative_count
        }
    
    def _calculate_complexity(self, text):
        """Calculate complexity score of input text."""
        words = text.split()
        unique_words = set(words)
        
        complexity_factors = [
            len(words) / 20.0,  # Length factor
            len(unique_words) / len(words) if words else 0,  # Vocabulary diversity
            len([w for w in words if len(w) > 6]) / len(words) if words else 0,  # Long words
            text.count('?') * 0.1,  # Question complexity
        ]
        
        return min(1.0, sum(complexity_factors) / len(complexity_factors))
    
    def _extract_input_features(self, text):
        """Extract numerical features from input text."""
        words = text.split()
        return {
            'word_count': len(words),
            'char_count': len(text),
            'question_marks': text.count('?'),
            'exclamation_marks': text.count('!'),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0
        }
    
    def _extract_response_features(self, text):
        """Extract numerical features from response text."""
        return self._extract_input_features(text)  # Same features for now
    
    def _text_to_vector(self, text, max_length=100):
        """Convert text to numerical vector (basic implementation)."""
        # Simple character-based encoding for now
        # In Stage 2, we'll use proper word embeddings
        vector = [0] * max_length
        for i, char in enumerate(text[:max_length]):
            vector[i] = ord(char) / 255.0  # Normalize to 0-1
        return vector
    
    def _create_response_key(self, user_input, response):
        """Create a unique key for response tracking."""
        return f"{hash(user_input)}_{hash(response)}"
    
    def _calculate_response_delay(self, timing_category):
        """Calculate recommended response delay in seconds."""
        delays = {
            'immediate': 0.1,
            'normal': 0.5,
            'deliberate': 1.5
        }
        return delays.get(timing_category, 0.5)
    
    def load_training_data(self):
        """Load existing training data."""
        try:
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversation_history = data[-100:]  # Keep recent history
        except (FileNotFoundError, json.JSONDecodeError):
            self.conversation_history = []
    
    def load_patterns(self):
        """Load existing pattern data."""
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                self.pattern_database = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.pattern_database = defaultdict(list)
    
    def save_patterns(self):
        """Save pattern data to file."""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.pattern_database), f, indent=2)
    
    def predict_optimal_response_type(self, user_input):
        """
        Use neural networks to predict the best response type for user input.
        Stage 2: Real neural network prediction.
        """
        if not self.neural_networks or not NEURAL_NETWORKS_AVAILABLE:
            # Fallback to rule-based prediction
            return self._fallback_response_type_prediction(user_input)
        
        try:
            # Extract features for neural network
            features = self._extract_neural_features(user_input)
            
            # Get neural network prediction
            prediction = self.neural_networks.predict_best_response_type(features)
            
            if prediction:
                return {
                    'recommended_type': prediction['response_type'],
                    'confidence': prediction['confidence'],
                    'method': 'neural_network',
                    'all_predictions': prediction.get('all_predictions', {})
                }
        except Exception as e:
            print(f"⚠️ Neural network prediction failed: {e}")
        
        # Fallback if neural network fails
        return self._fallback_response_type_prediction(user_input)
    
    def predict_conversation_success(self, user_input):
        """
        Use neural networks to predict conversation success probability.
        Stage 2: Real neural network prediction.
        """
        if not self.neural_networks or not NEURAL_NETWORKS_AVAILABLE:
            return {'quality_score': 0.5, 'method': 'fallback'}
        
        try:
            # Extract features for neural network
            features = self._extract_neural_features(user_input)
            
            # Get neural network prediction
            quality = self.neural_networks.predict_conversation_quality(features)
            
            if quality:
                return {
                    'quality_score': quality['quality_score'],
                    'predicted_success': quality['predicted_success'],
                    'method': 'neural_network'
                }
        except Exception as e:
            print(f"⚠️ Neural network quality prediction failed: {e}")
        
        return {'quality_score': 0.5, 'method': 'fallback'}
    
    def _extract_neural_features(self, user_input):
        """
        Extract features in the format expected by neural networks.
        """
        features = []
        
        # Basic text features
        features.extend([
            len(user_input.split()) / 20.0,  # Normalized word count
            len(user_input) / 100.0,  # Normalized character count
            user_input.count('?'),  # Question marks
            user_input.count('!'),  # Exclamation marks
            sum(1 for c in user_input if c.isupper()) / len(user_input) if user_input else 0,  # Uppercase ratio
            np.mean([len(word) for word in user_input.split()]) / 10.0 if user_input.split() else 0,  # Avg word length
        ])
        
        # Question type features
        user_lower = user_input.lower()
        features.extend([
            1.0 if 'what' in user_lower else 0.0,
            1.0 if 'how' in user_lower else 0.0,
            1.0 if 'why' in user_lower else 0.0,
            1.0 if 'when' in user_lower else 0.0,
            1.0 if 'where' in user_lower else 0.0,
            1.0 if 'can you' in user_lower else 0.0,
            1.0 if 'help' in user_lower else 0.0,
            1.0 if 'tell me' in user_lower else 0.0,
        ])
        
        # Pad to 100 features
        while len(features) < 100:
            features.append(0.0)
        
        return features[:100]
    
    def _fallback_response_type_prediction(self, user_input):
        """
        Fallback rule-based prediction when neural networks aren't available.
        """
        user_lower = user_input.lower()
        
        # Simple rule-based logic
        if any(word in user_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return {
                'recommended_type': 'semantic_match',
                'confidence': 0.7,
                'method': 'rule_based'
            }
        elif any(word in user_lower for word in ['can you', 'help', 'please']):
            return {
                'recommended_type': 'direct_llm',
                'confidence': 0.6,
                'method': 'rule_based'
            }
        else:
            return {
                'recommended_type': 'fallback',
                'confidence': 0.5,
                'method': 'rule_based'
            }
    
    def train_neural_networks(self, epochs=20):
        """
        Train the neural networks using collected conversation data.
        Stage 2: Actual neural network training.
        """
        if not self.neural_networks or not NEURAL_NETWORKS_AVAILABLE:
            print("❌ Neural networks not available for training")
            return False
        
        print("🧠 Training neural networks with collected conversation data...")
        
        # Prepare training data
        prepared_data = self.neural_networks.prepare_training_data(self.training_data_file)
        
        if not prepared_data:
            print("❌ Insufficient training data for neural network training")
            return False
        
        # Train both networks
        success_response = self.neural_networks.train_response_predictor(prepared_data, epochs=epochs)
        success_quality = self.neural_networks.train_quality_predictor(prepared_data, epochs=epochs)
        
        if success_response and success_quality:
            print("✅ Neural networks trained successfully!")
            self.neural_networks.save_models()
            return True
        else:
            print("⚠️ Neural network training partially failed")
            return False
    
    def get_neural_status(self):
        """Get status of neural network integration"""
        if not NEURAL_NETWORKS_AVAILABLE:
            return {
                'neural_networks_available': False,
                'status': 'Neural networks module not available'
            }
        
        if not self.neural_networks:
            return {
                'neural_networks_available': True,
                'status': 'Neural networks not initialized'
            }
        
        status = self.neural_networks.get_neural_status()
        status['enhanced_learning_integration'] = True
        status['stage'] = 'Stage 2: Neural Network Integration'
        
        return status
    
    def log_interaction(self, user_input, response, interaction_type="general"):
        """
        Log interaction for backward compatibility with Stage 3
        This method maintains compatibility with existing code that expects log_interaction
        """
        # Create interaction record
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'interaction_type': interaction_type,
            'input_length': len(user_input),
            'response_length': len(response)
        }
        
        # Add to conversation history
        self.conversation_history.append(interaction)
        
        # Collect training data based on interaction type
        feedback = "positive" if interaction_type == "successful" else "neutral"
        self.collect_training_data(user_input, response, feedback)
        
        # Update patterns
        patterns = self.analyze_speech_patterns(user_input)
        self.update_pattern_database(patterns, response)
        
        # Keep history manageable
        if len(self.conversation_history) > 1000:
            self.conversation_history = self.conversation_history[-800:]
        
        return interaction
    
    def update_pattern_database(self, patterns, response):
        """
        Update pattern database for backward compatibility
        This method maintains compatibility with existing pattern tracking code
        """
        try:
            # Store patterns with associated responses
            for pattern_type, pattern_data in patterns.items():
                if pattern_type not in self.pattern_database:
                    self.pattern_database[pattern_type] = []
                
                # Add pattern-response pair
                entry = {
                    'pattern': pattern_data,
                    'response': response,
                    'timestamp': datetime.now().isoformat(),
                    'effectiveness': 1.0  # Default effectiveness
                }
                
                self.pattern_database[pattern_type].append(entry)
                
                # Keep database manageable
                if len(self.pattern_database[pattern_type]) > 100:
                    self.pattern_database[pattern_type] = self.pattern_database[pattern_type][-80:]
            
            # Save patterns periodically
            if len(self.conversation_history) % 10 == 0:
                self.save_patterns()
                
        except Exception as e:
            print(f"Error updating pattern database: {e}")

# Test the enhanced learning module
if __name__ == "__main__":
    enhanced_learning = EnhancedLearningModule()
    
    # Test pattern analysis
    test_input = "What is the weather like today?"
    analysis = enhanced_learning.analyze_speech_patterns(test_input)
    print("Pattern Analysis:", analysis)
    
    # Test training data collection
    training_entry = enhanced_learning.collect_training_data(
        test_input, 
        "I don't have real-time weather data, but you can check a weather app.",
        feedback="neutral"
    )
    print("Training Entry:", training_entry)
    
    # Test timing prediction
    timing = enhanced_learning.predict_response_timing(test_input)
    print("Response Timing:", timing)
    
    # Get statistics
    stats = enhanced_learning.get_learning_statistics()
    print("Learning Statistics:", stats)
