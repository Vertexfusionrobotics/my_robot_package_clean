# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script to verify fuzzy matching logic for learned facts
"""

import json

def test_fuzzy_match(user_input, known_question):
    """Test the fuzzy matching algorithm"""
    user_input_lc = user_input.lower()
    
    # Calculate similarity using word overlap
    user_words = set(user_input_lc.split())
    question_words = set(known_question.lower().split())
    
    # Calculate Jaccard similarity (intersection over union)
    if len(user_words) > 0 and len(question_words) > 0:
        intersection = len(user_words.intersection(question_words))
        union = len(user_words.union(question_words))
        similarity = intersection / union
        
        # Also check if most user words are in the question
        user_coverage = intersection / len(user_words)
        
        # Use a combination of similarity and coverage
        score = (similarity * 0.6) + (user_coverage * 0.4)
        
        print(f"User input: '{user_input}'")
        print(f"Known question: '{known_question}'")
        print(f"User words: {user_words}")
        print(f"Question words: {question_words}")
        print(f"Intersection: {user_words.intersection(question_words)}")
        print(f"Similarity: {similarity:.3f}")
        print(f"User coverage: {user_coverage:.3f}")
        print(f"Final score: {score:.3f}")
        print(f"Would match (>0.4): {score > 0.4}")
        print("-" * 50)
        
        return score
    return 0

# Test cases
test_cases = [
    ("why would you want to learn new things", "why would you want to learn new things"),  # Exact match
    ("why would you learn new things", "why would you want to learn new things"),  # Missing "want to"
    ("why learn new things", "why would you want to learn new things"),  # Missing "would you want to"
    ("why do you learn", "why would you want to learn new things"),  # Partial match
    ("learn new things why", "why would you want to learn new things"),  # Different order
    ("what are you", "why would you want to learn new things"),  # No match
]

print("Testing fuzzy matching logic:")
print("=" * 50)

for user_input, known_question in test_cases:
    test_fuzzy_match(user_input, known_question)
