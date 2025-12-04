# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com

import json
import os

def load_knowledge_files():
    """Load all knowledge files"""
    knowledge_data = {}
    knowledge_files = [
        'knowledge.json',
        'knowledge_improved.json', 
        'knowledge_structured.json',
        'knowledge_expanded.json',
        'learned_facts.json',
        'learned_facts_expanded.json'
    ]
    
    for filename in knowledge_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    knowledge_data[filename] = data
            except Exception as e:
                print(f"[WARNING] Could not load {filename}: {e}")
    
    return knowledge_data

def get_structured_response(user_input, knowledge=None, mode=None, return_q_and_a=False):
    """
    Search all knowledge files for a response to user input.
    Accepts return_q_and_a for compatibility with chatbot_basic.py.
    """
    user_input_lower = user_input.lower().strip()
    
    # Load all knowledge if not provided
    if knowledge is None:
        knowledge = load_knowledge_files()
    
    # Search through all knowledge files
    for filename, data in knowledge.items():
        if isinstance(data, dict):
            # Search in knowledge.json / knowledge_improved.json format
            for key, value in data.items():
                if isinstance(value, dict):
                    # Check if user input matches topic/domain
                    if key.lower() in user_input_lower:
                        # Return casual response if available
                        if 'casual' in value:
                            if return_q_and_a:
                                return {
                                    'chatbot_questions': value.get('chatbot_questions', []),
                                    'chatbot_responses': value.get('chatbot_responses', []),
                                    'formal': value.get('casual', '')
                                }
                            return value['casual']
                        elif 'formal' in value:
                            if return_q_and_a:
                                return {
                                    'chatbot_questions': value.get('chatbot_questions', []),
                                    'chatbot_responses': value.get('chatbot_responses', []),
                                    'formal': value.get('formal', '')
                                }
                            return value['formal']
                        
                        # Check chatbot_questions for matches
                        if 'chatbot_questions' in value and 'chatbot_responses' in value:
                            for q in value['chatbot_questions']:
                                if any(word in user_input_lower for word in q.lower().split()):
                                    if return_q_and_a:
                                        return {
                                            'chatbot_questions': value['chatbot_questions'],
                                            'chatbot_responses': value['chatbot_responses'],
                                            'formal': value.get('casual', value.get('formal', ''))
                                        }
                                    return value['chatbot_responses'][0] if value['chatbot_responses'] else None
                elif isinstance(value, str):
                    # Simple key-value pair
                    if key.lower() in user_input_lower:
                        if return_q_and_a:
                            return {'formal': value}
                        return value
        
        elif isinstance(data, list):
            # Search in learned_facts format
            for fact in data:
                if isinstance(fact, dict):
                    # Check question field
                    questions = fact.get('question', [])
                    if not isinstance(questions, list):
                        questions = [questions]
                    
                    for q in questions:
                        if q and (q.lower() in user_input_lower or user_input_lower in q.lower()):
                            answer = fact.get('answer', fact.get('explanation', ''))
                            if answer:
                                if return_q_and_a:
                                    return {'formal': answer}
                                return answer
                    
                    # Check topic field
                    if 'topic' in fact and fact['topic'].lower() in user_input_lower:
                        answer = fact.get('answer', fact.get('explanation', ''))
                        if answer:
                            if return_q_and_a:
                                return {'formal': answer}
                            return answer
    
    # No match found
    if return_q_and_a:
        return {'formal': "I'm not sure about that topic yet."}
    return "I'm not sure about that topic yet."
