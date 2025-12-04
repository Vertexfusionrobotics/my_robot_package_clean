# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Neural Network Module for ARI - Stage 2: Deep Learning Implementation
Implements actual neural networks for conversation learning and response optimization
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
    print("✅ TensorFlow available for deep learning")
except (ImportError, Exception) as e:
    TF_AVAILABLE = False
    print(f"⚠️ TensorFlow not available - Neural networks disabled (CPU incompatibility)")

try:
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ scikit-learn not available")

class ARINeuralNetworks:
    """
    Neural network system for ARI's deep learning capabilities.
    Implements multiple specialized networks for different conversation aspects.
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.training_history = {}
        self.model_dir = "ari_neural_models"
        self.create_model_directory()
        
        # Load existing models if available
        self.load_models()
        
    def create_model_directory(self):
        """Create directory for storing neural network models"""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            print(f"📁 Created neural models directory: {self.model_dir}")
    
    def build_response_predictor_network(self, input_dim=100, num_response_types=4):
        """
        Build neural network to predict the best response type for a given input.
        This helps ARI choose between semantic matching, LLM generation, etc.
        """
        if not TF_AVAILABLE:
            print("❌ TensorFlow required for neural networks")
            return None
            
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(128, activation='relu', name='hidden_1'),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu', name='hidden_2'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu', name='hidden_3'),
            layers.Dense(num_response_types, activation='softmax', name='output')
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def build_conversation_quality_network(self, input_dim=50):
        """
        Build neural network to predict conversation quality/success probability.
        This helps ARI learn what makes conversations more effective.
        """
        if not TF_AVAILABLE:
            return None
            
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')  # Binary success prediction
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def build_response_optimization_network(self, input_dim=100, output_dim=50):
        """
        Build neural network to optimize response generation.
        This learns patterns for generating better responses.
        """
        if not TF_AVAILABLE:
            return None
            
        # Autoencoder-style network for response optimization
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(output_dim, activation='tanh'),  # Compressed representation
            layers.Dense(32, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(input_dim, activation='linear')  # Reconstruct input
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_training_data(self, training_file="neural_training_data.json"):
        """
        Load and prepare training data from collected conversations.
        Returns prepared datasets for different neural networks.
        """
        if not os.path.exists(training_file):
            print(f"❌ Training data file not found: {training_file}")
            return None
        
        with open(training_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("❌ No training data available")
            return None
        
        print(f"📊 Preparing {len(data)} training samples...")
        
        # Prepare data for response predictor
        input_features = []
        response_types = []
        success_labels = []
        
        for entry in data:
            # Input features (user input characteristics)
            features = []
            input_feat = entry.get('input_features', {})
            
            # Normalize and extract features
            features.extend([
                input_feat.get('word_count', 0) / 20.0,  # Normalize word count
                input_feat.get('char_count', 0) / 100.0,  # Normalize char count
                input_feat.get('question_marks', 0),
                input_feat.get('exclamation_marks', 0),
                input_feat.get('uppercase_ratio', 0),
                input_feat.get('avg_word_length', 0) / 10.0,  # Normalize avg word length
            ])
            
            # Add more sophisticated features
            user_input = entry.get('user_input', '').lower()
            
            # Question type features
            features.extend([
                1.0 if 'what' in user_input else 0.0,
                1.0 if 'how' in user_input else 0.0,
                1.0 if 'why' in user_input else 0.0,
                1.0 if 'when' in user_input else 0.0,
                1.0 if 'where' in user_input else 0.0,
                1.0 if 'can you' in user_input else 0.0,
                1.0 if 'help' in user_input else 0.0,
                1.0 if 'tell me' in user_input else 0.0,
            ])
            
            # Pad to consistent size
            while len(features) < 100:
                features.append(0.0)
            
            input_features.append(features[:100])  # Ensure exactly 100 features
            response_types.append(entry.get('response_type', 'unknown'))
            success_labels.append(1.0 if entry.get('success') else 0.0)
        
        # Convert to numpy arrays
        X = np.array(input_features)
        
        # Encode response types
        response_encoder = LabelEncoder()
        y_response = response_encoder.fit_transform(response_types)
        
        # Convert to categorical
        num_classes = len(response_encoder.classes_)
        y_response_cat = tf.keras.utils.to_categorical(y_response, num_classes)
        
        y_success = np.array(success_labels)
        
        prepared_data = {
            'X': X,
            'y_response': y_response_cat,
            'y_success': y_success,
            'response_encoder': response_encoder,
            'num_response_types': num_classes,
            'feature_names': ['input_features'] * 100
        }
        
        print(f"✅ Prepared data: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"📋 Response types: {list(response_encoder.classes_)}")
        
        return prepared_data
    
    def train_response_predictor(self, prepared_data, epochs=50, validation_split=0.2):
        """
        Train the neural network to predict optimal response types.
        """
        if not TF_AVAILABLE or not prepared_data:
            print("❌ Cannot train response predictor")
            return False
        
        print("🧠 Training Response Predictor Neural Network...")
        
        X = prepared_data['X']
        y = prepared_data['y_response']
        
        # Build model
        model = self.build_response_predictor_network(
            input_dim=X.shape[1], 
            num_response_types=y.shape[1]
        )
        
        if model is None:
            return False
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42
        )
        
        # Train model
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=1
        )
        
        # Evaluate
        val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
        print(f"✅ Response Predictor - Validation Accuracy: {val_accuracy:.3f}")
        
        # Save model
        model_path = os.path.join(self.model_dir, "response_predictor.h5")
        model.save(model_path)
        
        # Save encoder
        encoder_path = os.path.join(self.model_dir, "response_encoder.pkl")
        with open(encoder_path, 'wb') as f:
            pickle.dump(prepared_data['response_encoder'], f)
        
        self.models['response_predictor'] = model
        self.encoders['response_encoder'] = prepared_data['response_encoder']
        self.training_history['response_predictor'] = history.history
        
        return True
    
    def train_quality_predictor(self, prepared_data, epochs=50, validation_split=0.2):
        """
        Train the neural network to predict conversation quality/success.
        """
        if not TF_AVAILABLE or not prepared_data:
            print("❌ Cannot train quality predictor")
            return False
        
        print("🧠 Training Conversation Quality Neural Network...")
        
        X = prepared_data['X']
        y = prepared_data['y_success']
        
        # Build model
        model = self.build_conversation_quality_network(input_dim=50)  # Use subset of features
        
        if model is None:
            return False
        
        # Use subset of features for quality prediction
        X_quality = X[:, :50]  # First 50 features
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X_quality, y, test_size=validation_split, random_state=42
        )
        
        # Train model
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=(X_val, y_val),
            verbose=1
        )
        
        # Evaluate
        val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
        print(f"✅ Quality Predictor - Validation Accuracy: {val_accuracy:.3f}")
        
        # Save model
        model_path = os.path.join(self.model_dir, "quality_predictor.h5")
        model.save(model_path)
        
        self.models['quality_predictor'] = model
        self.training_history['quality_predictor'] = history.history
        
        return True
    
    def predict_best_response_type(self, input_features):
        """
        Use neural network to predict the best response type for given input.
        """
        if 'response_predictor' not in self.models:
            return None
        
        model = self.models['response_predictor']
        encoder = self.encoders.get('response_encoder')
        
        if not encoder:
            return None
        
        # Prepare input
        features = np.array(input_features).reshape(1, -1)
        
        # Predict
        predictions = model.predict(features, verbose=0)[0]
        best_class_idx = np.argmax(predictions)
        confidence = predictions[best_class_idx]
        
        best_response_type = encoder.inverse_transform([best_class_idx])[0]
        
        return {
            'response_type': best_response_type,
            'confidence': float(confidence),
            'all_predictions': {
                encoder.inverse_transform([i])[0]: float(pred) 
                for i, pred in enumerate(predictions)
            }
        }
    
    def predict_conversation_quality(self, input_features):
        """
        Use neural network to predict conversation success probability.
        """
        if 'quality_predictor' not in self.models:
            return None
        
        model = self.models['quality_predictor']
        
        # Prepare input (use first 50 features)
        features = np.array(input_features[:50]).reshape(1, -1)
        
        # Predict
        quality_score = model.predict(features, verbose=0)[0][0]
        
        return {
            'quality_score': float(quality_score),
            'predicted_success': quality_score > 0.5
        }
    
    def save_models(self):
        """Save all trained models and associated data"""
        if not TF_AVAILABLE:
            return
        
        # Save training history
        history_path = os.path.join(self.model_dir, "training_history.json")
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=2)
        
        print(f"💾 Neural models saved to {self.model_dir}/")
    
    def load_models(self):
        """Load existing trained models"""
        if not TF_AVAILABLE:
            return
        
        # Load response predictor
        response_model_path = os.path.join(self.model_dir, "response_predictor.h5")
        if os.path.exists(response_model_path):
            try:
                self.models['response_predictor'] = keras.models.load_model(response_model_path)
                print("✅ Loaded response predictor model")
            except Exception as e:
                print(f"⚠️ Error loading response predictor: {e}")
        
        # Load response encoder
        encoder_path = os.path.join(self.model_dir, "response_encoder.pkl")
        if os.path.exists(encoder_path):
            try:
                with open(encoder_path, 'rb') as f:
                    self.encoders['response_encoder'] = pickle.load(f)
                print("✅ Loaded response encoder")
            except Exception as e:
                print(f"⚠️ Error loading response encoder: {e}")
        
        # Load quality predictor
        quality_model_path = os.path.join(self.model_dir, "quality_predictor.h5")
        if os.path.exists(quality_model_path):
            try:
                self.models['quality_predictor'] = keras.models.load_model(quality_model_path)
                print("✅ Loaded quality predictor model")
            except Exception as e:
                print(f"⚠️ Error loading quality predictor: {e}")
    
    def get_neural_status(self):
        """Get status of neural network training and availability"""
        status = {
            'tensorflow_available': TF_AVAILABLE,
            'sklearn_available': SKLEARN_AVAILABLE,
            'models_trained': list(self.models.keys()),
            'model_directory': self.model_dir
        }
        
        if self.training_history:
            status['training_history'] = {
                model: {
                    'epochs': len(history.get('loss', [])),
                    'final_accuracy': history.get('val_accuracy', [0])[-1] if history.get('val_accuracy') else 0
                }
                for model, history in self.training_history.items()
            }
        
        return status

def install_tensorflow():
    """Install TensorFlow if not available"""
    import subprocess
    import sys
    
    print("🔧 Installing TensorFlow for neural networks...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tensorflow", "scikit-learn"])
        print("✅ TensorFlow and scikit-learn installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install TensorFlow: {e}")
        return False

# Auto-install TensorFlow if not available
if not TF_AVAILABLE:
    print("⚠️ TensorFlow disabled - CPU incompatibility detected. Neural network features will be unavailable.")
