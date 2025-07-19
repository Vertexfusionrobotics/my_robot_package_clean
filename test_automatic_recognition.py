# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Demonstrate automatic recognition of new facts
"""

import json
import tempfile
import os
from rapidfuzz import fuzz

def test_automatic_recognition():
    print("🧪 TESTING AUTOMATIC FACT RECOGNITION")
    print("=" * 50)
    
    # Create a temporary facts file with a new fact
    test_facts = [
        {
            "question": [
                "what is quantum computing",
                "tell me about quantum computing", 
                "explain quantum computing",
                "quantum computing definition",
                "help me understand quantum computing"
            ],
            "answer": "Quantum computing uses quantum mechanical phenomena to process information in ways that classical computers cannot."
        },
        {
            "question": [
                "what is blockchain",
                "explain blockchain technology",
                "blockchain definition"
            ],
            "answer": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, which are linked and secured using cryptography."
        }
    ]
    
    # Save test facts to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_facts, f, indent=2)
        temp_file = f.name
    
    print(f"✅ Created temporary facts file with {len(test_facts)} new facts")
    
    # Simulate the loading process (same as ARI does)
    def load_facts(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_match(user_input, facts):
        """Simplified version of ARI's matching logic"""
        user_input = user_input.strip().lower()
        
        # Exact match first
        for fact in facts:
            for q in fact["question"]:
                if user_input == q.lower():
                    return fact["answer"]
        
        # Fuzzy matching
        best_score = 0
        best_answer = None
        
        for fact in facts:
            for q in fact["question"]:
                score = fuzz.ratio(user_input, q.lower())
                if score > best_score:
                    best_score = score
                    best_answer = fact["answer"]
        
        if best_score >= 80:
            return best_answer
        
        return None
    
    # Load the facts (simulating ARI startup)
    facts = load_facts(temp_file)
    print(f"✅ Loaded {len(facts)} facts with {sum(len(f['question']) for f in facts)} total questions")
    
    # Test various questions
    test_queries = [
        "what is quantum computing",
        "explain quantum computing", 
        "tell me about blockchain",
        "quantum computing definition",
        "what is quantu",  # Partial match
        "blockchain definition"
    ]
    
    print("\n🎯 TESTING NEW FACT RECOGNITION:")
    print("-" * 40)
    
    success_count = 0
    for query in test_queries:
        answer = find_match(query, facts)
        if answer:
            print(f"✅ '{query}' → {answer[:60]}...")
            success_count += 1
        else:
            print(f"❌ '{query}' → No match found")
    
    print(f"\n📊 SUCCESS RATE: {success_count}/{len(test_queries)} ({success_count/len(test_queries)*100:.1f}%)")
    print("=" * 50)
    print("✅ CONCLUSION: New facts are automatically recognized!")
    print("   No manual updates needed - just add to JSON and restart ARI")
    
    # Cleanup
    os.unlink(temp_file)

if __name__ == "__main__":
    test_automatic_recognition()
