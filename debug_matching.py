# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Comprehensive test to diagnose question recognition issues
"""

import json
from rapidfuzz import fuzz

def test_question_recognition():
    print("🔍 COMPREHENSIVE QUESTION RECOGNITION TEST")
    print("=" * 60)
    
    # Load facts
    try:
        with open("learned_facts_expanded.json", "r", encoding="utf-8") as f:
            facts = json.load(f)
        print(f"✅ Loaded {len(facts)} facts from knowledge base")
    except Exception as e:
        print(f"❌ Error loading facts: {e}")
        return
    
    # Test various question formats
    test_queries = [
        # Questions that should work
        "what is climate",
        "what is physics", 
        "what is the atmosphere",
        "what is an ocean",
        "what is a volcano",
        "what is robotics",
        
        # Questions that might have issues
        "what is phys",  # Incomplete
        "tell me about climate",  # Different format
        "explain physics",  # Different format
        "climate definition",  # Different format
        "physics meaning",  # Different format
    ]
    
    print(f"\n🧪 Testing {len(test_queries)} different question formats:")
    print("-" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        # Test exact match
        found_exact = False
        exact_match = None
        exact_answer = None
        
        for fact in facts:
            for q in fact["question"]:
                if query.lower().strip() == q.lower().strip():
                    exact_match = q
                    exact_answer = fact["answer"]
                    found_exact = True
                    break
            if found_exact:
                break
        
        if found_exact:
            print(f"   ✅ EXACT MATCH: '{exact_match}'")
            print(f"   📝 Answer: {exact_answer[:80]}...")
        else:
            print("   ❌ No exact match")
            
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
            
            print(f"   🔍 Best fuzzy: '{best_match}' (score: {best_score:.1f})")
            if best_score >= 80:
                print(f"   ✅ FUZZY MATCH: {best_answer[:80]}...")
            else:
                print("   ❌ No good match found")
    
    # Check for common question patterns in knowledge base
    print(f"\n📊 KNOWLEDGE BASE ANALYSIS:")
    print("-" * 40)
    
    question_patterns = {}
    for fact in facts:
        for q in fact["question"]:
            first_words = " ".join(q.lower().split()[:3])
            if first_words not in question_patterns:
                question_patterns[first_words] = 0
            question_patterns[first_words] += 1
    
    print("Most common question patterns:")
    sorted_patterns = sorted(question_patterns.items(), key=lambda x: x[1], reverse=True)
    for pattern, count in sorted_patterns[:10]:
        print(f"   '{pattern}': {count} questions")
    
    # Check specific problematic questions
    print(f"\n🎯 SPECIFIC ISSUE ANALYSIS:")
    print("-" * 40)
    
    problematic = ["physics", "climate", "robotics"]
    for topic in problematic:
        matching_facts = []
        for fact in facts:
            for q in fact["question"]:
                if topic in q.lower():
                    matching_facts.append(q)
        
        if matching_facts:
            print(f"✅ Found {len(matching_facts)} questions about '{topic}':")
            for q in matching_facts[:3]:  # Show first 3
                print(f"   - '{q}'")
            if len(matching_facts) > 3:
                print(f"   ... and {len(matching_facts) - 3} more")
        else:
            print(f"❌ No questions found about '{topic}'")

if __name__ == "__main__":
    test_question_recognition()
