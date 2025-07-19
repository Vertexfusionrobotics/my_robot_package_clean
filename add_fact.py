# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com

#!/usr/bin/env python3
"""
Simple fact adder with automatic question generation
"""

import json

def add_new_fact():
    """Add a new fact with automatic question generation"""
    
    # Load existing facts
    with open("learned_facts_expanded.json", "r", encoding="utf-8") as f:
        facts = json.load(f)
    
    print("🤖 ARI FACT ADDER")
    print("=" * 40)
    print("Let's add a new fact to ARI's knowledge base!")
    
    # Get topic and answer from user
    topic = input("\n📝 What topic do you want to add? (e.g., 'blockchain'): ").strip()
    if not topic:
        print("❌ No topic provided. Exiting.")
        return
    
    answer = input(f"📖 What should ARI say about '{topic}'? ").strip()
    if not answer:
        print("❌ No answer provided. Exiting.")
        return
    
    # Generate basic question variations
    basic_questions = [
        f"what is {topic}",
        f"what is {topic}?",
        f"tell me about {topic}",
        f"explain {topic}",
        f"{topic} definition",
        f"define {topic}",
        f"describe {topic}"
    ]
    
    # Create new fact
    new_fact = {
        "question": basic_questions,
        "answer": answer
    }
    
    # Add to facts list
    facts.append(new_fact)
    
    # Save back to file
    with open("learned_facts_expanded.json", "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Added new fact about '{topic}'!")
    print(f"✅ Generated {len(basic_questions)} basic questions")
    print(f"✅ Total facts in database: {len(facts)}")
    
    # Ask if user wants to enhance with more variations
    enhance = input("\n🚀 Run automatic question enhancement to add 40+ more question variations? (y/n): ").strip().lower()
    if enhance in ['y', 'yes']:
        print("\n🔧 Running question enhancement...")
        import subprocess
        try:
            result = subprocess.run([
                "python", "enhance_questions_advanced.py"
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Question enhancement completed!")
            else:
                print(f"❌ Enhancement failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Could not run enhancement: {e}")
            print("💡 You can run 'enhance_questions_advanced.py' manually later")
    
    print(f"\n🎯 '{topic}' is now ready for ARI to answer!")
    print("🔄 Restart ARI to use the new fact.")

if __name__ == "__main__":
    add_new_fact()
