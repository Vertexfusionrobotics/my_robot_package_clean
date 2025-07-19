# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Enhanced debug test with new question variations
"""

import json
from rapidfuzz import fuzz
import random

# Load facts
with open("learned_facts_expanded.json", "r", encoding="utf-8") as f:
    facts = json.load(f)

# Test a variety of natural questions
test_queries = [
    # Original format
    "what is climate",
    "what is physics", 
    
    # New conversational formats
    "tell me something about climate",
    "help me understand physics",
    "what can you tell me about the atmosphere",
    "what's the deal with robotics",
    "how would you describe weather",
    "give me information about a volcano",
    "I want to learn about earthquakes",
    "could you explain storms to me",
    "what's a tree",
    "so what is an ocean",
    
    # Casual formats
    "um what is lightning",
    "okay what is thunder",
    "please explain mountains",
    
    # Incomplete/partial
    "what is clim",
    "tell me about phys",
    "explain weath"
]

print("🧪 ENHANCED QUESTION RECOGNITION TEST")
print("=" * 60)
print(f"✅ Loaded {len(facts)} facts from knowledge base")

total_questions = sum(len(fact.get("question", [])) for fact in facts)
print(f"✅ Total questions in database: {total_questions:,}")
print("=" * 60)

success_count = 0
for i, query in enumerate(test_queries, 1):
    print(f"{i:2d}. Testing: '{query}'")
    
    # Test exact match first
    found_exact = False
    for fact in facts:
        for q in fact["question"]:
            if query.lower() == q.lower():
                print(f"    ✅ EXACT MATCH: '{q}'")
                print(f"    📝 Answer: {fact['answer'][:60]}...")
                found_exact = True
                success_count += 1
                break
        if found_exact:
            break
    
    if not found_exact:
        # Test fuzzy matching
        best_score = 0
        best_match = None
        best_answer = None
        
        for fact in facts:
            for q in fact["question"]:
                score = fuzz.ratio(query.lower(), q.lower())
                if score > best_score:
                    best_score = score
                    best_match = q
                    best_answer = fact["answer"]
        
        print(f"    🔍 Best fuzzy: '{best_match}' (score: {best_score:.1f})")
        if best_score >= 80:
            print(f"    ✅ FUZZY MATCH: {best_answer[:60]}...")
            success_count += 1
        else:
            print(f"    ❌ No good match found")
    print()

print("=" * 60)
print(f"📊 SUCCESS RATE: {success_count}/{len(test_queries)} ({success_count/len(test_queries)*100:.1f}%)")

# Sample some random questions to show variety
print("\n🎯 SAMPLE QUESTION VARIATIONS:")
print("-" * 40)
physics_fact = next((f for f in facts if any("physics" in q.lower() for q in f.get("question", []))), None)
if physics_fact:
    sample_questions = random.sample(physics_fact["question"], min(8, len(physics_fact["question"])))
    for q in sample_questions:
        print(f"  • {q}")
