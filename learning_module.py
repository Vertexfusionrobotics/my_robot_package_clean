# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import json
import os
from paraphrase_helper import generate_paraphrases  # Optional helper if you want reworded inputs
import sys
import traceback
import speech_recognition as sr
from rapidfuzz import fuzz, process  # Add this import for fuzzy matching
# Add ChatterBot imports
try:
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    chatterbot_available = True
except ImportError:
    chatterbot_available = False
import requests  # For Ollama API integration

def global_exception_hook(exctype, value, tb):
    print("UNCAUGHT EXCEPTION:", exctype, value)
    traceback.print_tb(tb)
    sys.exit(1)

sys.excepthook = global_exception_hook

class LearningModule:
    def __init__(self, learned_file="learned_facts_expanded.json"):
        self.learned_file = learned_file
        self.facts = self.load_facts()
        self.ollama_available = self.check_ollama_availability()
        
        # Initialize ChatterBot as a fallback
        if chatterbot_available:
            try:
                self.chatbot = ChatBot('ARI', read_only=True)
                self.trainer = ChatterBotCorpusTrainer(self.chatbot)
                # Only train if not already trained
                if not os.path.exists('db.sqlite3'):
                    self.trainer.train('chatterbot.corpus.english')
            except Exception as e:
                print(f"ChatterBot initialization error: {e}")
                self.chatbot = None
        else:
            self.chatbot = None
            
    def check_ollama_availability(self):
        """Check if Ollama is available and running."""
        try:
            # Test connection to Ollama API
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                # Check if phi3 model is available
                models = response.json().get("models", [])
                for model in models:
                    if "phi3" in model.get("name", "").lower():
                        return True
                print("WARNING: Ollama is running but phi3 model is not found. ARI will use fallbacks.")
                return False
            else:
                print("WARNING: Ollama API returned an error. ARI will use fallbacks.")
                return False
        except Exception as e:
            print(f"WARNING: Ollama connection failed ({str(e)}). ARI will use fallbacks.")
            return False

    def load_facts(self):
        if os.path.exists(self.learned_file):
            with open(self.learned_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []

    def save_facts(self):
        with open(self.learned_file, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, indent=2)

    def query_ollama(self, prompt, model="phi3", max_tokens=60, timeout=30):
        """Send a prompt to Ollama and return the full response text, or None on error."""
        # Skip if we already know Ollama is not available
        if not hasattr(self, 'ollama_available') or not self.ollama_available:
            return None
            
        try:
            url = f"http://localhost:11434/api/generate"
            # Optimization: Add system prompt and tune parameters for faster response
            data = {
                "model": model, 
                "prompt": prompt,
                "system": "You are ARI, a helpful AI assistant. Give concise, accurate answers.",
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,  # Lower temperature for more predictable responses
                    "top_k": 40,         # Limit token selection for speed
                    "top_p": 0.9,        # Nucleus sampling for better quality
                    "seed": 42           # Fixed seed for consistent responses
                }
            }
            response = requests.post(url, json=data, timeout=timeout)
            
            if response.status_code == 200:
                # Ollama streams responses, so we need to parse and join all 'response' fields
                lines = response.text.strip().split('\n')
                fragments = []
                import json as _json
                for line in lines:
                    if '"response"' in line:
                        try:
                            fragment = _json.loads(line)["response"]
                            fragments.append(fragment)
                        except Exception as e:
                            pass
                result = ''.join(fragments).strip()
                return result if result else None
            else:
                print(f"[Ollama] Error: {response.status_code}")
                # If model not found, update availability flag
                if response.status_code == 404:
                    print(f"[Ollama] Model {model} not found. Try running 'ollama pull {model}'")
                    self.ollama_available = False
        except Exception as e:
            print(f"[Ollama] Exception: {e}")
            # Update availability flag for connection errors
            self.ollama_available = False
        return None

    def find_match(self, user_input):
        """Find a matching response for user input using various matching strategies.
        Optimized for speed and accuracy."""
        user_input = user_input.strip().lower()
        
        # Quick exact match first (fastest and most accurate)
        for fact in self.facts:
            for q in fact["question"]:
                if user_input == q.lower():
                    return fact["answer"]
        
        # Improved fuzzy matching with better scoring
        best_score = 0
        best_answer = None
        
        for fact in self.facts:
            for q in fact["question"]:
                q_lower = q.lower()
                
                # Multiple scoring methods for better accuracy
                ratio_score = fuzz.ratio(user_input, q_lower)
                token_sort_score = fuzz.token_sort_ratio(user_input, q_lower)
                partial_score = fuzz.partial_ratio(user_input, q_lower)
                
                # Weighted average of different scoring methods
                combined_score = (ratio_score * 0.4) + (token_sort_score * 0.4) + (partial_score * 0.2)
                
                # Bonus for exact word matches
                user_words = set(user_input.split())
                question_words = set(q_lower.split())
                word_overlap = len(user_words.intersection(question_words))
                word_bonus = (word_overlap / max(len(user_words), 1)) * 10
                
                final_score = combined_score + word_bonus
                
                if final_score > best_score:
                    best_score = final_score
                    best_answer = fact["answer"]
                    # Early return for excellent matches
                    if final_score >= 95:
                        return best_answer
        
        # Return if we have a good match
        if best_score >= 80:  # Higher threshold for better accuracy
            return best_answer
        
        # Fallback to Ollama if available (with lower timeout)
        ollama_response = self.query_ollama(user_input, timeout=15)
        if ollama_response:
            return ollama_response
            
        # Fallback to ChatterBot if available
        if self.chatbot:
            try:
                response = self.chatbot.get_response(user_input)
                if response.confidence > 0.2:
                    return str(response)
            except:
                pass
                
        # If we reach here, all fallbacks failed
        return None

    def learn_new_fact(self, user_input, listen_func=None):
        """Learn a new fact from user input. If listen_func is provided, use voice input instead of typed input."""
        print("I don't know how to respond to that yet.")
        
        if listen_func and callable(listen_func):
            # Use voice input
            print("Please tell me what I should say if someone asks that. I'm listening...")
            user_answer = None
            attempts = 0
            while not user_answer and attempts < 3:
                user_answer = listen_func(listen_timeout=10)  # Longer timeout for teaching
                attempts += 1
                if not user_answer and attempts < 3:
                    print("I didn't catch that. Please try again.")
            
            # If still no good response after attempts, try to generate one with LLM
            if not user_answer:
                print("I'll try to find an answer myself.")
                user_answer = self.query_ollama(
                    f"The user asked: '{user_input}'. Please provide a detailed, accurate, and informative response.",
                    model="phi3"
                )
                if user_answer:
                    print(f"I've generated this answer: {user_answer}")
        else:
            # Fall back to typed input if no listen function is provided
            user_answer = input("You: (What should I say if someone asks that?)\n>>> ").strip()
            
        if not user_answer:
            print("Okay, I'll skip learning this one.")
            return None

        # Generate paraphrases to improve future matching
        paraphrases = generate_paraphrases(user_input) if os.path.exists("paraphrase_helper.py") else [user_input]

        new_fact = {
            "question": paraphrases,
            "answer": [user_answer]
        }
        self.facts.append(new_fact)
        self.save_facts()
        print("Got it. I'll remember that for next time!")
        return user_answer

def main():
    """Simple test function for the learning module"""
    learning = LearningModule()
    print("Learning module initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            break
            
        # Try to find a match first
        response = learning.find_match(user_input)
        if response:
            print(f"ARI: {response}")
        else:
            # If no match, learn a new fact
            learning.learn_new_fact(user_input)

if __name__ == "__main__":
    main()
