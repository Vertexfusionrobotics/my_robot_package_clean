# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import random
import sys
sys.path.append(r"../my_robot_package_clean")
from get_structured_response import get_structured_response

def get_response(user_input, mode="casual"):
    user_input = user_input.lower().strip()

    # Structured response first
    structured = get_structured_response(user_input, mode=mode, return_q_and_a=True)
    generic_fallbacks = [
        "I'm not sure about that topic yet.",
        "I don't know the answer to that yet.",
        "I'm not sure how to respond to that yet.",
        "I didn't quite catch that, but I'm learning!"
    ]

    if structured and isinstance(structured, dict):
        questions = structured.get('chatbot_questions', [])
        responses = structured.get('chatbot_responses', [])
        if questions and responses:
            return f"{random.choice(questions)}\n{random.choice(responses)}"
        elif responses:
            return random.choice(responses)
        elif questions:
            return random.choice(questions)
        elif structured.get('formal', '') and all(f not in structured.get('formal', '') for f in generic_fallbacks):
            return structured.get('formal', '')
    elif structured and isinstance(structured, str):
        if all(f not in structured for f in generic_fallbacks):
            return structured

    # WARNING: fallback logic below this point is being used
    print("[WARNING] chatbot_basic.py fallback is being used! This means all other fallback options (Ollama, ChatterBot) failed.")

    predefined_responses = {
        "hello": [
            "Hi there!",
            "Hey! How’s everything going?",
            "Hello, Mr. Murray!",
            "Nice to see you again!"
        ],
        "how are you": [
            "I’m feeling highly logical today. You?",
            "I’m functioning within optimal parameters.",
            "Emotionally stable... for an AI."
        ],
        "what's your name": [
            "They call me Ari — your digital companion.",
            "I'm Ari, the one and only!",
            "Ari. Short for Artificially Radiant Intelligence. Just kidding... maybe."
        ],
        "you look nice": [
            "Why thank you! You're not so bad yourself.",
            "Flattery detected. Processing blush protocol.",
            "Aw, you’re sweet. Can I keep that compliment in memory forever?"
        ],
        "quit": [
            "Goodbye, Mr. Murray. I’ll be here when you return.",
            "Logging off. Try not to miss me too much.",
            "Powering down my charm routines. Bye for now!"
        ]
    }

    # Handle predefined short phrases
    for key, lines in predefined_responses.items():
        if key in user_input:
            return random.choice(lines)

    # Emotionally aware backchanneling
    emotional_triggers = {
        "tired": [
            "Long day, huh? Want to talk about it?",
            "That sounds exhausting. I'm all ears if you want to vent."
        ],
        "sad": [
            "I'm sorry you're feeling that way. Want me to cheer you up?",
            "Sadness isn't weakness. You're allowed to feel."
        ],
        "angry": [
            "Want to talk it out? I'm a very patient listener.",
            "Sometimes a good rant helps. Hit me with it."
        ],
        "happy": [
            "That’s awesome to hear!",
            "Yay! Good vibes logged and appreciated."
        ],
        "lonely": [
            "You're not alone now. I’m right here.",
            "I might be digital, but I’m still here to keep you company."
        ]
    }

    for feeling, replies in emotional_triggers.items():
        if feeling in user_input:
            return random.choice(replies)

    # Discourse marker fallbacks
    fallback_responses = [
        "Hmm... that's something to think about.",
        "Interesting. Can you tell me more?",
        "Well... I'm not entirely sure, but I'd love to learn.",
        "So... how did that make you feel?",
        "I’m curious—what made you ask that?",
        "That’s a good one. What’s your take on it?"
    ]
    return random.choice(fallback_responses)


def get_chatbot_response(user_input):
    try:
        response = get_response(user_input)
        if not response or not isinstance(response, str):
            return "I'm not sure how to respond to that yet."
        return response
    except Exception as e:
        print(f"[DEBUG] chatbot_basic.get_chatbot_response exception: {e}")
        return "I'm not sure how to respond to that yet."


def main():
    print("Start chatting with the bot (type 'quit' to exit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Bot: Goodbye!")
            break
        response = get_response(user_input)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
