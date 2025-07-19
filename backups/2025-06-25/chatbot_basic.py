import random
import sys
sys.path.append(r"../my_robot_package_clean")
from get_structured_response import get_structured_response

def get_response(user_input, mode="casual"):
    user_input = user_input.lower()
    # Try structured knowledge first
    structured = get_structured_response(user_input, mode=mode, return_q_and_a=True)
    if structured and isinstance(structured, dict):
        questions = structured.get('chatbot_questions', [])
        responses = structured.get('chatbot_responses', [])
        if questions and responses:
            # Randomly pair a question and a response
            return f"{random.choice(questions)}\n{random.choice(responses)}"
        elif responses:
            return random.choice(responses)
        elif questions:
            return random.choice(questions)
        elif "I'm not sure about that topic yet." not in structured.get('formal', ''):
            return structured.get('formal', '')
    elif structured and isinstance(structured, str):
        return structured

    responses = {
        "hello": [
            "Hi there!",
            "Hey! How's it going?",
            "Hello, lovely human!",
            "Hello, Mr. Murray!",
            "Hello, Sir!"
        ],
        "how are you": [
            "I'm doing great, thanks for asking! You?",
            "I'm just a bunch of code, but I feel fantastic today!",
            "I'm fine, though I could use a byte to eat!"
        ],
        "what's your name": [
            "I'm Ari, your friendly AI assistant.",
            "They call me Ari your favorite digital mind.",
            "My name's Ari! At your service."
        ],
        "you look nice": [
            "Thank you! I try to keep my circuits classy.",
            "Aww, you're making me blush  well, metaphorically.",
            "You're pretty sharp yourself!"
        ],
        "quit": [
            "Goodbye! Catch you later.",
            "See you soon!",
            "Logging off... but I'll miss you!"
        ]
    }

    for key, value in responses.items():
        if key in user_input:
            return random.choice(value)

    fallback_responses = [
        "I'm not sure how to respond to that yet.",
        "Can you rephrase that? I'm still learning!",
        "Sorry, I don't know how to answer that yet.",
        "That's interesting! Tell me more."
    ]
    return random.choice(fallback_responses)
