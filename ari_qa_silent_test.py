# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import time
import random
import sys
import os
from datetime import datetime

# Import ARI master brain (assume class is named ARIMasterBrain or similar)
sys.path.append(os.path.dirname(__file__))
from ari_master_brain_final import ARIMasterBrain

# Load knowledge.json for question generation
import json
with open(os.path.join(os.path.dirname(__file__), '../my_robot_package_clean/knowledge.json'), 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

def collect_questions(knowledge):
    questions = []
    def recurse(d, path=None):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == 'chatbot_questions' and isinstance(v, list):
                    questions.extend(v)
                else:
                    recurse(v, path+[k] if path else [k])
        elif isinstance(d, list):
            for item in d:
                recurse(item, path)
    recurse(knowledge)
    return questions

questions = collect_questions(knowledge)
if not questions:
    print('No chatbot_questions found in knowledge.json!')
    sys.exit(1)

# Add some fallback/general questions
questions += [
    'What is science?',
    'Tell me about black holes.',
    'Do you like music?',
    'What is psychology?',
    'What is a robot?',
    'What is the first law of robotics?',
    'What is your purpose?',
    'What is a cat?',
    'What is a banana?',
    'What is the Sahara Desert?',
    'What is programming?',
    'What is art?',
    'What is nutrition?',
    'What is Mars?',
    'What is chemistry?',
    'What is philosophy?',
    'What is sociology?',
    'What is astronomy?',
    'What is mental health?',
    'What is renewable energy?'
]

# Shuffle questions for variety
random.shuffle(questions)

# Initialize ARI master brain
ari = ARIMasterBrain()

# Run test for 5 minutes
start_time = time.time()
end_time = start_time + 300  # 5 minutes
results = []
q_idx = 0
print(f"[TEST] Starting 5-minute silent Q&A test at {datetime.now()}")
while time.time() < end_time:
    question = questions[q_idx % len(questions)]
    try:
        response = ari.unified_answer(question)
    except Exception as e:
        response = f"[ERROR] {e}"
    results.append((question, response))
    q_idx += 1
    # Wait a bit to simulate real Q&A, but not too slow
    time.sleep(0.5)

# Save results to log
logfile = f"ari_qa_test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(logfile, 'w', encoding='utf-8') as f:
    for q, r in results:
        f.write(f"Q: {q}\nA: {r}\n\n")
print(f"[TEST] Finished. Results saved to {logfile}")
