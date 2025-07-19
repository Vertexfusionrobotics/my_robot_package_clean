# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Add question variations to improve recognition
"""

import json
import re

def add_question_variations():
    print("🔧 Adding question variations for better recognition...")
    
    # Load current facts
    with open('learned_facts_expanded.json', 'r', encoding='utf-8') as f:
        facts = json.load(f)
    
    enhanced_facts = []
    
    for fact in facts:
        original_questions = fact['question']
        enhanced_questions = list(original_questions)  # Start with originals
        
        for q in original_questions:
            q_lower = q.lower().strip()
            
            # Add variations for "what is X" questions
            if q_lower.startswith('what is '):
                topic = q_lower[8:].rstrip('?')
                
                # Add variations
                variations = [
                    f"tell me about {topic}",
                    f"explain {topic}",
                    f"{topic} definition",
                    f"define {topic}",
                    f"what do you know about {topic}",
                    f"describe {topic}",
                ]
                
                # Add variations for single-word topics
                if len(topic.split()) == 1 and topic not in ['a', 'an', 'the']:
                    variations.extend([
                        f"what is {topic}",
                        f"what is {topic}?",
                        f"{topic} meaning",
                        f"meaning of {topic}",
                    ])
                
                enhanced_questions.extend(variations)
            
            # Add variations for "what are X" questions  
            elif q_lower.startswith('what are '):
                topic = q_lower[9:].rstrip('?')
                variations = [
                    f"tell me about {topic}",
                    f"explain {topic}",
                    f"describe {topic}",
                ]
                enhanced_questions.extend(variations)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_questions = []
        for q in enhanced_questions:
            q_clean = q.lower().strip()
            if q_clean not in seen:
                unique_questions.append(q.strip())
                seen.add(q_clean)
        
        enhanced_facts.append({
            'question': unique_questions,
            'answer': fact['answer']
        })
    
    # Save enhanced facts
    with open('learned_facts_expanded.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_facts, f, indent=2, ensure_ascii=False)
    
    # Count total questions
    total_questions = sum(len(fact['question']) for fact in enhanced_facts)
    original_questions = sum(len(fact['question']) for fact in facts)
    
    print(f"✅ Enhanced knowledge base:")
    print(f"   📊 Facts: {len(enhanced_facts)}")
    print(f"   📝 Questions: {original_questions} → {total_questions}")
    print(f"   ➕ Added: {total_questions - original_questions} variations")

if __name__ == "__main__":
    add_question_variations()
