# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com


#!/usr/bin/env python3
"""
ARI Advanced Neural Response Generator - Stage 3B: Context-Aware Response Generation
Implements LSTM-based sequence models with attention mechanisms for dynamic response synthesis
"""

import json
import os
import numpy as np
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("⚠️ TensorFlow not available for advanced response generation")

try:
    from ari_context_memory import ARIContextMemory
    CONTEXT_MEMORY_AVAILABLE = True
except ImportError:
    CONTEXT_MEMORY_AVAILABLE = False
    print("⚠️ Context memory not available")

class ARIAdvancedResponseGenerator:
    """
    Advanced neural response generator with LSTM, attention, and context awareness
    """
    
    def __init__(self, model_dir="ari_neural_models/generative"):
        self.model_dir = model_dir
        self.models = {}
        self.tokenizers = {}
        self.max_sequence_length = 50
        self.vocab_size = 5000
        self.embedding_dim = 128
        self.lstm_units = 256
        
        # Initialize context memory if available
        self.context_memory = None
        if CONTEXT_MEMORY_AVAILABLE:
            self.context_memory = ARIContextMemory()
        
        # Create model directory
        os.makedirs(model_dir, exist_ok=True)
        
        # Try to load existing models
        self.load_models()
        
        print("🧠 ARI Advanced Response Generator initialized")
    
    def build_lstm_response_generator(self, vocab_size=None, embedding_dim=None, lstm_units=None):
        """Build LSTM-based response generation model"""
        if not TF_AVAILABLE:
            return None
        
        if vocab_size is None:
            vocab_size = self.vocab_size
        if embedding_dim is None:
            embedding_dim = self.embedding_dim
        if lstm_units is None:
            lstm_units = self.lstm_units
        
        # Input for user message
        input_sequence = layers.Input(shape=(self.max_sequence_length,))
        
        # Input for conversation context
        context_input = layers.Input(shape=(10,))  # Context features
        
        # Embedding layer
        embedding = layers.Embedding(vocab_size, embedding_dim, mask_zero=True)(input_sequence)
        
        # LSTM with return sequences for attention
        lstm_out = layers.LSTM(lstm_units, return_sequences=True, dropout=0.3)(embedding)
        
        # Attention mechanism
        attention = layers.MultiHeadAttention(num_heads=8, key_dim=lstm_units//8)(lstm_out, lstm_out)
        attention = layers.Dropout(0.3)(attention)
        
        # Global attention pooling
        attention_pooled = layers.GlobalAveragePooling1D()(attention)
        
        # Combine with context
        context_dense = layers.Dense(64, activation='relu')(context_input)
        combined = layers.Concatenate()([attention_pooled, context_dense])
        
        # Response generation layers
        dense1 = layers.Dense(512, activation='relu')(combined)
        dense1 = layers.Dropout(0.4)(dense1)
        
        dense2 = layers.Dense(256, activation='relu')(dense1)
        dense2 = layers.Dropout(0.3)(dense2)
        
        # Output layer for response generation
        output = layers.Dense(vocab_size, activation='softmax')(dense2)
        
        # Create model
        model = models.Model(inputs=[input_sequence, context_input], outputs=output)
        
        # Compile with appropriate loss for text generation
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("🏗️ Built LSTM response generator with attention mechanism")
        return model
    
    def build_context_encoder(self):
        """Build context encoding model"""
        if not TF_AVAILABLE:
            return None
        
        # Conversation history input
        history_input = layers.Input(shape=(None, self.max_sequence_length))
        
        # Context metadata input
        metadata_input = layers.Input(shape=(20,))  # Various context features
        
        # Process conversation history
        history_lstm = layers.LSTM(128, return_sequences=False)(history_input)
        
        # Combine with metadata
        combined_context = layers.Concatenate()([history_lstm, metadata_input])
        
        # Context encoding
        context_encoded = layers.Dense(64, activation='relu')(combined_context)
        context_encoded = layers.Dense(32, activation='tanh')(context_encoded)
        
        model = models.Model(inputs=[history_input, metadata_input], outputs=context_encoded)
        model.compile(optimizer='adam', loss='mse')
        
        print("🧩 Built context encoder model")
        return model
    
    def prepare_training_data_from_context(self):
        """Prepare training data using context memory"""
        if not self.context_memory:
            print("⚠️ Context memory not available for training data preparation")
            return None
        
        training_sequences = []
        target_sequences = []
        context_features = []
        
        # Load conversation history
        memory_stats = self.context_memory.get_memory_stats()
        
        if memory_stats["total_conversations"] < 5:
            print("⚠️ Not enough conversation data for training")
            return None
        
        try:
            # Get all sessions
            for session_id, session_data in self.context_memory.user_sessions.items():
                # Load session conversation file
                session_file = os.path.join(self.context_memory.memory_dir, f"session_{session_id}.json")
                
                if os.path.exists(session_file):
                    with open(session_file, 'r') as f:
                        conversations = json.load(f)
                    
                    # Create training pairs
                    for i in range(len(conversations) - 1):
                        current_turn = conversations[i]
                        next_turn = conversations[i + 1]
                        
                        # Input: current user input + context
                        input_sequence = current_turn["user_input"]
                        target_sequence = current_turn["ari_response"]
                        
                        # Context features
                        context_feat = [
                            len(conversations),  # Conversation length
                            i / len(conversations),  # Position in conversation
                            1.0 if current_turn.get("success", True) else 0.0,  # Success indicator
                            len(current_turn["user_input"].split()),  # Input length
                            len(target_sequence.split()),  # Response length
                            len(session_data.get("topics", [])),  # Topic count
                            session_data.get("conversation_count", 0) / 50.0,  # Normalized conversation count
                            len(session_data.get("context_keywords", [])) / 20.0,  # Normalized keyword count
                            1.0,  # Placeholder for user satisfaction
                            0.5   # Placeholder for difficulty
                        ]
                        
                        training_sequences.append(input_sequence)
                        target_sequences.append(target_sequence)
                        context_features.append(context_feat)
            
            print(f"📊 Prepared {len(training_sequences)} training sequences from context memory")
            
            return {
                "input_sequences": training_sequences,
                "target_sequences": target_sequences,
                "context_features": context_features
            }
            
        except Exception as e:
            print(f"❌ Error preparing training data: {e}")
            return None
    
    def create_tokenizer(self, texts):
        """Create and fit tokenizer on texts"""
        tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
        tokenizer.fit_on_texts(texts)
        
        return tokenizer
    
    def preprocess_sequences(self, input_texts, target_texts, context_features):
        """Preprocess text sequences for training"""
        if not TF_AVAILABLE:
            return None
        
        # Create tokenizers
        all_texts = input_texts + target_texts
        tokenizer = self.create_tokenizer(all_texts)
        self.tokenizers['main'] = tokenizer
        
        # Convert texts to sequences
        input_sequences = tokenizer.texts_to_sequences(input_texts)
        target_sequences = tokenizer.texts_to_sequences(target_texts)
        
        # Pad sequences
        input_padded = pad_sequences(input_sequences, maxlen=self.max_sequence_length, padding='post')
        target_padded = pad_sequences(target_sequences, maxlen=self.max_sequence_length, padding='post')
        
        # Prepare target for sequence classification (simplified approach)
        # Use first meaningful token from each target sequence
        target_output = []
        for seq in target_padded:
            # Find first non-zero token as target class
            first_token = next((token for token in seq if token != 0), 1)
            target_output.append(first_token)
        
        # Ensure targets are within vocab range
        target_output = [min(token, self.vocab_size - 1) for token in target_output]
        
        # Pad context features to match input length
        context_array = np.array(context_features)
        
        return {
            "input_sequences": input_padded,
            "target_sequences": np.array(target_output),
            "context_features": context_array,
            "tokenizer": tokenizer
        }
    
    def train_lstm_generator(self, epochs=50, validation_split=0.2):
        """Train the LSTM response generator"""
        if not TF_AVAILABLE:
            print("❌ TensorFlow not available for training")
            return False
        
        # Prepare training data
        training_data = self.prepare_training_data_from_context()
        if not training_data:
            print("❌ No training data available")
            return False
        
        print("🔄 Preprocessing training data...")
        processed_data = self.preprocess_sequences(
            training_data["input_sequences"],
            training_data["target_sequences"],
            training_data["context_features"]
        )
        
        if not processed_data:
            print("❌ Failed to preprocess training data")
            return False
        
        # Build model if not exists
        if 'lstm_generator' not in self.models:
            self.models['lstm_generator'] = self.build_lstm_response_generator()
        
        model = self.models['lstm_generator']
        if not model:
            print("❌ Failed to build LSTM generator model")
            return False
        
        # Prepare training inputs
        X_input = processed_data["input_sequences"]
        X_context = processed_data["context_features"]
        y = processed_data["target_sequences"]
        
        print(f"🏋️ Training LSTM generator on {len(X_input)} samples...")
        
        try:
            # Training callbacks
            callbacks = [
                keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                keras.callbacks.ReduceLROnPlateau(factor=0.8, patience=5)
            ]
            
            # Train model
            history = model.fit(
                [X_input, X_context],
                y,
                epochs=epochs,
                validation_split=validation_split,
                batch_size=32,
                callbacks=callbacks,
                verbose=1
            )
            
            print("✅ LSTM generator training completed")
            
            # Save model and tokenizer
            self.save_models()
            
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def generate_context_aware_response(self, user_input, max_length=50):
        """Generate context-aware response using LSTM"""
        if not TF_AVAILABLE or 'lstm_generator' not in self.models:
            return self.fallback_response_generation(user_input)
        
        try:
            # Get context features
            context_features = self.get_context_features_for_generation()
            
            # Tokenize input
            tokenizer = self.tokenizers.get('main')
            if not tokenizer:
                return self.fallback_response_generation(user_input)
            
            # Prepare input sequence
            input_seq = tokenizer.texts_to_sequences([user_input])
            input_padded = pad_sequences(input_seq, maxlen=self.max_sequence_length, padding='post')
            
            # Prepare context
            context_array = np.array([context_features])
            
            # Generate response
            model = self.models['lstm_generator']
            prediction = model.predict([input_padded, context_array], verbose=0)
            
            # Convert prediction to text
            predicted_tokens = np.argmax(prediction[0], axis=-1)
            
            # Convert tokens back to text
            response = self.tokens_to_text(predicted_tokens, tokenizer)
            
            if response and len(response.strip()) > 0:
                return response.strip()
            else:
                return self.fallback_response_generation(user_input)
                
        except Exception as e:
            print(f"⚠️ Neural response generation failed: {e}")
            return self.fallback_response_generation(user_input)
    
    def get_context_features_for_generation(self):
        """Get context features for response generation"""
        if self.context_memory:
            context_data = self.context_memory.get_context_for_response_generation()
            
            features = [
                context_data.get("conversation_length", 0) / 20.0,
                len(context_data.get("recent_user_inputs", [])) / 5.0,
                len(context_data.get("current_topics", [])) / 10.0,
                context_data.get("session_duration", 0) / 60.0,
                context_data.get("response_success_rate", 0.5),
                len(context_data.get("context_keywords", [])) / 15.0,
                0.5,  # Time of day (placeholder)
                0.5,  # User mood (placeholder)
                0.5,  # Conversation complexity (placeholder)
                0.5   # Response urgency (placeholder)
            ]
        else:
            # Default context features
            features = [0.1, 0.1, 0.1, 0.1, 0.5, 0.1, 0.5, 0.5, 0.5, 0.5]
        
        return features
    
    def tokens_to_text(self, tokens, tokenizer):
        """Convert token sequence back to text"""
        try:
            # Get reverse word index
            reverse_word_index = {v: k for k, v in tokenizer.word_index.items()}
            
            # Convert tokens to words
            words = []
            for token in tokens:
                if token > 0 and token in reverse_word_index:
                    word = reverse_word_index[token]
                    if word != "<OOV>":
                        words.append(word)
            
            return " ".join(words)
            
        except Exception as e:
            print(f"⚠️ Token to text conversion failed: {e}")
            return ""
    
    def fallback_response_generation(self, user_input):
        """Fallback response generation when neural models fail"""
        fallback_responses = [
            "I understand what you're saying. Let me think about that.",
            "That's an interesting point. Can you tell me more?",
            "I'm processing your message. How can I help you with that?",
            "Thank you for sharing that. What would you like to know?",
            "I see. Let me provide you with a thoughtful response.",
            "That's a good question. Let me help you with that.",
            "I appreciate you asking. Here's what I think about that."
        ]
        
        # Simple selection based on input characteristics
        if "?" in user_input:
            return "That's a great question! Let me help you find the answer."
        elif "hello" in user_input.lower() or "hi" in user_input.lower():
            return "Hello! It's nice to talk with you. How can I help you today?"
        elif "thank" in user_input.lower():
            return "You're very welcome! I'm glad I could help."
        else:
            import random
            return random.choice(fallback_responses)
    
    def save_models(self):
        """Save all models and tokenizers"""
        if not TF_AVAILABLE:
            return
        
        try:
            # Save models
            for model_name, model in self.models.items():
                model_path = os.path.join(self.model_dir, f"{model_name}.h5")
                model.save(model_path)
                print(f"💾 Saved {model_name} model")
            
            # Save tokenizers
            tokenizer_path = os.path.join(self.model_dir, "tokenizers.pkl")
            with open(tokenizer_path, 'wb') as f:
                pickle.dump(self.tokenizers, f)
            print("💾 Saved tokenizers")
            
        except Exception as e:
            print(f"⚠️ Error saving models: {e}")
    
    def load_models(self):
        """Load existing models and tokenizers"""
        if not TF_AVAILABLE:
            return
        
        try:
            # Load tokenizers
            tokenizer_path = os.path.join(self.model_dir, "tokenizers.pkl")
            if os.path.exists(tokenizer_path):
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizers = pickle.load(f)
                print("📚 Loaded tokenizers")
            
            # Load models
            model_files = [f for f in os.listdir(self.model_dir) if f.endswith('.h5')]
            for model_file in model_files:
                model_name = model_file.replace('.h5', '')
                model_path = os.path.join(self.model_dir, model_file)
                
                try:
                    self.models[model_name] = keras.models.load_model(model_path)
                    print(f"📚 Loaded {model_name} model")
                except Exception as e:
                    print(f"⚠️ Failed to load {model_name}: {e}")
            
        except Exception as e:
            print(f"⚠️ Error loading models: {e}")
    
    def get_generator_status(self):
        """Get status of the response generator"""
        status = {
            "tensorflow_available": TF_AVAILABLE,
            "context_memory_available": CONTEXT_MEMORY_AVAILABLE,
            "models_loaded": list(self.models.keys()),
            "tokenizers_loaded": list(self.tokenizers.keys()),
            "model_directory": self.model_dir,
            "max_sequence_length": self.max_sequence_length,
            "vocab_size": self.vocab_size
        }
        
        if self.context_memory:
            memory_stats = self.context_memory.get_memory_stats()
            status["memory_stats"] = memory_stats
        
        return status
    
    def process_user_feedback(self, user_input, ari_response, feedback_type):
        """Process user feedback for real-time learning"""
        try:
            # Map feedback to scores
            feedback_scores = {
                "good response": 1.0,
                "great response": 1.0,
                "excellent": 1.0,
                "perfect": 1.0,
                "good": 0.8,
                "okay": 0.6,
                "try again": 0.2,
                "bad response": 0.1,
                "terrible": 0.0,
                "improve that": 0.3,
                "not helpful": 0.2
            }
            
            score = feedback_scores.get(feedback_type.lower(), 0.5)
            
            # Store feedback for training
            feedback_data = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "ari_response": ari_response,
                "feedback_type": feedback_type,
                "feedback_score": score,
                "context_features": self.get_context_features_for_generation()
            }
            
            # Save to feedback file
            feedback_file = os.path.join(self.model_dir, "user_feedback.json")
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    feedbacks = json.load(f)
            else:
                feedbacks = []
            
            feedbacks.append(feedback_data)
            
            with open(feedback_file, 'w') as f:
                json.dump(feedbacks, f, indent=2)
            
            print(f"📝 Recorded feedback: {feedback_type} (score: {score})")
            
            # Trigger incremental learning if enough feedback collected
            if len(feedbacks) % 10 == 0:  # Every 10 feedback items
                self.incremental_learning_update()
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error processing feedback: {e}")
            return False
    
    def incremental_learning_update(self):
        """Update models based on recent user feedback"""
        try:
            feedback_file = os.path.join(self.model_dir, "user_feedback.json")
            if not os.path.exists(feedback_file):
                return False
            
            with open(feedback_file, 'r') as f:
                feedbacks = json.load(f)
            
            # Get recent feedback (last 20 items)
            recent_feedback = feedbacks[-20:] if len(feedbacks) > 20 else feedbacks
            
            # Prepare training data from feedback
            positive_examples = [f for f in recent_feedback if f["feedback_score"] > 0.7]
            negative_examples = [f for f in recent_feedback if f["feedback_score"] < 0.4]
            
            if len(positive_examples) > 3 and len(negative_examples) > 1:
                print("🔄 Performing incremental learning update...")
                
                # Create mini-batch training data
                input_texts = [f["user_input"] for f in positive_examples]
                target_texts = [f["ari_response"] for f in positive_examples]
                context_features = [f["context_features"] for f in positive_examples]
                
                # Quick mini-batch training
                processed_data = self.preprocess_sequences(input_texts, target_texts, context_features)
                
                if processed_data and 'lstm_generator' in self.models:
                    model = self.models['lstm_generator']
                    
                    # Small learning update
                    X_input = processed_data["input_sequences"]
                    X_context = processed_data["context_features"]
                    y = processed_data["target_sequences"]
                    
                    # Single epoch update with lower learning rate
                    model.compile(
                        optimizer=optimizers.Adam(learning_rate=0.0001),
                        loss='sparse_categorical_crossentropy',
                        metrics=['accuracy']
                    )
                    
                    model.fit([X_input, X_context], y, epochs=1, verbose=0)
                    print("✅ Incremental learning update completed")
                    
                    # Save updated model
                    self.save_models()
                    
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Incremental learning failed: {e}")
            return False
        
    def calculate_conversation_quality_metrics(self):
        """Calculate comprehensive conversation quality metrics"""
        try:
            metrics = {
                "response_coherence": 0.0,
                "user_satisfaction": 0.0,
                "context_awareness": 0.0,
                "response_diversity": 0.0,
                "learning_progress": 0.0,
                "overall_quality": 0.0
            }
            
            # Get feedback data
            feedback_file = os.path.join(self.model_dir, "user_feedback.json")
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    feedbacks = json.load(f)
                
                if feedbacks:
                    # User satisfaction from feedback
                    recent_scores = [f["feedback_score"] for f in feedbacks[-20:]]
                    metrics["user_satisfaction"] = np.mean(recent_scores)
                    
                    # Learning progress (improvement over time)
                    if len(feedbacks) > 10:
                        early_scores = [f["feedback_score"] for f in feedbacks[:10]]
                        late_scores = [f["feedback_score"] for f in feedbacks[-10:]]
                        improvement = np.mean(late_scores) - np.mean(early_scores)
                        metrics["learning_progress"] = max(0.0, min(1.0, 0.5 + improvement))
            
            # Get conversation context quality
            if self.context_memory:
                context_data = self.context_memory.get_context_for_response_generation()
                
                # Context awareness based on conversation length and topics
                conv_length = context_data.get("conversation_length", 0)
                topics_count = len(context_data.get("current_topics", []))
                
                metrics["context_awareness"] = min(1.0, (conv_length * 0.1 + topics_count * 0.2) / 2.0)
                
                # Response success rate
                success_rate = context_data.get("response_success_rate", 0.5)
                metrics["response_coherence"] = success_rate
            
            # Response diversity (estimate based on vocab usage)
            if 'main' in self.tokenizers:
                vocab_size_used = len(self.tokenizers['main'].word_index)
                metrics["response_diversity"] = min(1.0, vocab_size_used / 1000.0)
            
            # Overall quality (weighted average)
            weights = {
                "response_coherence": 0.3,
                "user_satisfaction": 0.3,
                "context_awareness": 0.2,
                "response_diversity": 0.1,
                "learning_progress": 0.1
            }
            
            metrics["overall_quality"] = sum(
                metrics[key] * weights[key] for key in weights.keys()
            )
            
            return metrics
            
        except Exception as e:
            print(f"⚠️ Error calculating quality metrics: {e}")
            return {"overall_quality": 0.5}
    
    def get_learning_recommendations(self):
        """Get recommendations for improving the neural network"""
        try:
            metrics = self.calculate_conversation_quality_metrics()
            recommendations = []
            
            if metrics["user_satisfaction"] < 0.6:
                recommendations.append("Collect more user feedback to improve response quality")
            
            if metrics["context_awareness"] < 0.5:
                recommendations.append("Need more conversation data for better context understanding")
            
            if metrics["response_diversity"] < 0.4:
                recommendations.append("Expand vocabulary and response patterns")
            
            if metrics["learning_progress"] < 0.3:
                recommendations.append("Implement more aggressive learning from feedback")
            
            if not recommendations:
                recommendations.append("System is performing well - continue current approach")
            
            return {
                "metrics": metrics,
                "recommendations": recommendations,
                "priority_areas": [k for k, v in metrics.items() if v < 0.5 and k != "overall_quality"]
            }
            
        except Exception as e:
            print(f"⚠️ Error generating recommendations: {e}")
            return {"recommendations": ["System analysis failed"]}
    
    def get_training_readiness_assessment(self):
        """Assess if the system is ready for advanced training"""
        try:
            assessment = {
                "ready_for_lstm_training": False,
                "ready_for_attention_training": False,
                "ready_for_transformer_training": False,
                "data_quality_score": 0.0,
                "recommendations": []
            }
            
            # Check data availability
            if self.context_memory:
                stats = self.context_memory.get_memory_stats()
                total_conversations = stats.get("total_conversations", 0)
                
                if total_conversations >= 20:
                    assessment["ready_for_lstm_training"] = True
                    assessment["data_quality_score"] += 0.3
                
                if total_conversations >= 50:
                    assessment["ready_for_attention_training"] = True
                    assessment["data_quality_score"] += 0.3
                
                if total_conversations >= 100:
                    assessment["ready_for_transformer_training"] = True
                    assessment["data_quality_score"] += 0.4
            
            # Check feedback availability
            feedback_file = os.path.join(self.model_dir, "user_feedback.json")
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    feedbacks = json.load(f)
                
                if len(feedbacks) >= 10:
                    assessment["data_quality_score"] += 0.2
                if len(feedbacks) >= 30:
                    assessment["data_quality_score"] += 0.3
            
            # Generate recommendations
            if not assessment["ready_for_lstm_training"]:
                assessment["recommendations"].append("Need more conversation data (minimum 20 conversations)")
            
            if assessment["data_quality_score"] < 0.5:
                assessment["recommendations"].append("Collect more user feedback for better training")
            
            if assessment["ready_for_transformer_training"]:
                assessment["recommendations"].append("Ready for advanced transformer training!")
            
            return assessment
            
        except Exception as e:
            print(f"⚠️ Error assessing training readiness: {e}")
            return {"ready_for_lstm_training": False}

# Test the advanced response generator
if __name__ == "__main__":
    print("🧠 Testing ARI Advanced Response Generator")
    print("=" * 55)
    
    # Create generator instance
    generator = ARIAdvancedResponseGenerator()
    
    # Get status
    status = generator.get_generator_status()
    print(f"📊 Status: {status}")
    
    # Test fallback response generation
    test_inputs = [
        "Hello, how are you?",
        "What can you do?",
        "Can you help me learn something?",
        "Thank you for your help",
        "This is a complex technical question about neural networks"
    ]
    
    print("\\n🔄 Testing response generation:")
    for user_input in test_inputs:
        response = generator.generate_context_aware_response(user_input)
        print(f"User: {user_input}")
        print(f"ARI: {response}")
        print()
    
    # Try to train if enough data is available
    print("🏋️ Attempting to train LSTM generator...")
    training_success = generator.train_lstm_generator(epochs=5)
    
    if training_success:
        print("✅ Training completed successfully!")
    else:
        print("⚠️ Training skipped - not enough data or missing dependencies")
    
    print("\\n✅ Advanced response generator test complete!")
