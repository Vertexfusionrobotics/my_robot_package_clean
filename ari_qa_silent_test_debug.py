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

sys.path.append(os.path.dirname(__file__))
from ari_master_brain_final import ARIMasterBrain

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

random.shuffle(questions)

ari = ARIMasterBrain()

start_time = time.time()
end_time = start_time + 300
results = []
q_idx = 0
print(f"[TEST] Starting 5-minute silent Q&A test at {datetime.now()}")
while time.time() < end_time:
    question = questions[q_idx % len(questions)]
    print(f"[DEBUG] Asking: {question}")  # Added debug print before answer
    try:
        response = ari.unified_answer(question)
        print(f"[DEBUG] Got response: {response}")  # Added debug print after answer
    except Exception as e:
        response = f"[ERROR] {e}"
        print(f"[DEBUG] Exception: {e}")
    results.append((question, response))
    q_idx += 1
    time.sleep(0.5)

logfile = f"ari_qa_test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}_debug.txt"
with open(logfile, 'w', encoding='utf-8') as f:
    for q, r in results:
        f.write(f"Q: {q}\nA: {r}\n\n")
print(f"[TEST] Finished. Results saved to {logfile}")
