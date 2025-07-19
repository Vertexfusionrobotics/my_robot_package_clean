# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Convert learned_facts.json to the format expected by learning_module.py
"""

import json

def convert_facts():
    # Load the flat dictionary format
    try:
        with open("learned_facts.json", "r", encoding="utf-8") as f:
            flat_facts = json.load(f)
    except FileNotFoundError:
        print("❌ learned_facts.json not found")
        return

    # Convert to list format expected by learning_module.py
    converted_facts = []
    
    for question, answer in flat_facts.items():
        converted_facts.append({
            "question": [question.strip()],  # Wrap in list for compatibility
            "answer": answer.strip()
        })
    
    # Save as learned_facts_expanded.json
    with open("learned_facts_expanded.json", "w", encoding="utf-8") as f:
        json.dump(converted_facts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(converted_facts)} facts to learned_facts_expanded.json")

if __name__ == "__main__":
    convert_facts()
