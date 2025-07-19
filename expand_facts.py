# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import json

# Load your base learned facts JSON file
with open("learned_facts.json", "r", encoding="utf-8") as f:
    base_facts = json.load(f)

# Paraphrase templates for common question types
paraphrase_templates = {
    "what are you": [
        "who are you",
        "tell me about yourself",
        "can you introduce yourself"
    ],
    "who made you": [
        "who created you",
        "who is your creator",
        "who built you"
    ],
    "what can you do": [
        "what are your capabilities",
        "what can you perform",
        "what functions do you have",
        "tell me your abilities"
    ],
    "how do you work": [
        "how do you operate",
        "how do you function",
        "how do you perform tasks"
    ],
    "are you sentient": [
        "do you have consciousness",
        "are you alive",
        "do you have awareness",
        "do you have a soul"
    ],
    "how do you learn": [
        "how do you get smarter",
        "how do you improve",
        "how do you remember things"
    ],
    "do you have emotions": [
        "can you feel",
        "do you show feelings",
        "do you express emotions"
    ],
    "what is artificial intelligence": [
        "what is ai",
        "explain artificial intelligence",
        "define ai"
    ],
    "can you help me": [
        "can you assist me",
        "can you support me",
        "can you give me help"
    ],
    "how do you feel today": [
        "how are you",
        "what’s your mood",
        "how do you feel"
    ],
    "can you walk": [
        "are you able to walk",
        "can you move around",
        "do you walk"
    ],
    "can you solve math problems": [
        "can you do math",
        "can you help with math",
        "are you good at math"
    ]
    # Add more paraphrase mappings as needed
}

def generate_paraphrased_facts(base_facts, paraphrase_templates):
    expanded_facts = dict(base_facts)  # start with the originals

    for base_key, variants in paraphrase_templates.items():
        if base_key not in base_facts:
            print(f"[SKIPPED] '{base_key}' not in learned_facts.json")
            continue
        base_value = base_facts[base_key]
        for variant in variants:
            if variant not in expanded_facts:
                expanded_facts[variant] = base_value
                print(f"[ADDED] {variant} → {base_key}")

    return expanded_facts

# Generate the new expanded dictionary
expanded_facts = generate_paraphrased_facts(base_facts, paraphrase_templates)

# Save to a new file
with open("learned_facts_expanded.json", "w", encoding="utf-8") as f:
    json.dump(expanded_facts, f, indent=2, ensure_ascii=False)

print("✅ Expanded learned facts saved to learned_facts_expanded.json")

