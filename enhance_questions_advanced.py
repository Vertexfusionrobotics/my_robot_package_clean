# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Advanced question enhancement - Add even more natural language variations
"""

import json
import re
from collections import defaultdict

def load_facts():
    """Load the current facts database"""
    with open("learned_facts_expanded.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_base_topic(questions):
    """Extract the core topic from a list of questions"""
    # Look for "what is X" patterns first
    for q in questions:
        match = re.search(r"what is (?:a |an |the )?(.+?)[\?]?$", q.lower())
        if match:
            return match.group(1).strip()
    
    # Fallback: use the first question and try to extract topic
    first_q = questions[0].lower()
    # Remove common question prefixes
    for prefix in ["tell me about", "explain", "describe", "define"]:
        if first_q.startswith(prefix):
            return first_q.replace(prefix, "").strip()
    
    return first_q

def generate_advanced_variations(topic):
    """Generate even more natural question variations"""
    topic = topic.strip()
    
    # Remove articles and question marks
    clean_topic = re.sub(r"^(a |an |the )", "", topic)
    clean_topic = re.sub(r"[\?\!\.]+$", "", clean_topic)
    
    variations = []
    
    # Conversational questions
    variations.extend([
        f"tell me something about {clean_topic}",
        f"what can you tell me about {clean_topic}",
        f"what should I know about {clean_topic}",
        f"give me information about {clean_topic}",
        f"share what you know about {clean_topic}",
        f"help me understand {clean_topic}",
        f"can you teach me about {clean_topic}",
        f"I want to learn about {clean_topic}",
        f"I need to know about {clean_topic}",
        f"could you explain {clean_topic} to me",
        f"would you explain {clean_topic}",
        f"please explain {clean_topic}",
        f"please tell me about {clean_topic}",
    ])
    
    # Informal/casual questions
    variations.extend([
        f"what's {clean_topic}",
        f"what's a {clean_topic}",
        f"what's the deal with {clean_topic}",
        f"so what is {clean_topic}",
        f"tell me - what is {clean_topic}",
        f"okay what is {clean_topic}",
        f"um what is {clean_topic}",
        f"uh what is {clean_topic}",
    ])
    
    # Question variations with different structures
    variations.extend([
        f"how would you describe {clean_topic}",
        f"how do you define {clean_topic}",
        f"what exactly is {clean_topic}",
        f"what precisely is {clean_topic}",
        f"what specifically is {clean_topic}",
        f"can you define {clean_topic} for me",
        f"could you define {clean_topic}",
        f"would you define {clean_topic}",
        f"how about {clean_topic}",
        f"what about {clean_topic}",
    ])
    
    # Academic/formal variations
    variations.extend([
        f"provide a definition of {clean_topic}",
        f"give a definition of {clean_topic}",
        f"what is the definition of {clean_topic}",
        f"what is the meaning of {clean_topic}",
        f"what does {clean_topic} refer to",
        f"what does {clean_topic} mean",
        f"explain the concept of {clean_topic}",
        f"describe the concept of {clean_topic}",
        f"what is the concept of {clean_topic}",
    ])
    
    # If it's a single word, add variations with articles
    if " " not in clean_topic:
        variations.extend([
            f"what is a {clean_topic}",
            f"what is an {clean_topic}",
            f"tell me about a {clean_topic}",
            f"explain a {clean_topic}",
            f"describe a {clean_topic}",
            f"define a {clean_topic}",
        ])
    
    # Remove duplicates and normalize
    unique_variations = []
    seen = set()
    for var in variations:
        normalized = var.lower().strip()
        if normalized not in seen and len(normalized) > 0:
            seen.add(normalized)
            unique_variations.append(var)
    
    return unique_variations

def enhance_facts_advanced():
    """Add advanced question variations to all facts"""
    facts = load_facts()
    enhanced_count = 0
    total_new_questions = 0
    
    print("🚀 ADVANCED QUESTION ENHANCEMENT")
    print("=" * 50)
    
    for fact in facts:
        if "question" not in fact or not fact["question"]:
            continue
            
        original_count = len(fact["question"])
        topic = get_base_topic(fact["question"])
        
        if not topic:
            continue
            
        # Generate new variations
        new_variations = generate_advanced_variations(topic)
        
        # Add variations that don't already exist
        existing_questions = [q.lower().strip() for q in fact["question"]]
        added_count = 0
        
        for variation in new_variations:
            if variation.lower().strip() not in existing_questions:
                fact["question"].append(variation)
                existing_questions.append(variation.lower().strip())
                added_count += 1
        
        if added_count > 0:
            enhanced_count += 1
            total_new_questions += added_count
            new_count = len(fact["question"])
            print(f"📝 Enhanced '{topic}': {original_count} → {new_count} questions (+{added_count})")
    
    # Save enhanced facts
    with open("learned_facts_expanded.json", "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"✅ Enhanced {enhanced_count} fact entries")
    print(f"✅ Added {total_new_questions} new question variations")
    print(f"✅ Total facts in database: {len(facts)}")
    
    # Count total questions
    total_questions = sum(len(fact.get("question", [])) for fact in facts)
    print(f"✅ Total questions now: {total_questions}")
    
    return facts

if __name__ == "__main__":
    enhance_facts_advanced()
