# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import rclpy
from rclpy.node import Node
import os
import json
from datetime import datetime, timedelta
import spacy
import re
from rapidfuzz import fuzz, process
import requests
import math
import wikipedia
from wiktionaryparser import WiktionaryParser
import random

from my_robot_package_clean.rules_engine import ReasoningEngine, ActionRequest, HumanHarm, RobotHarm

# --- Facial expressions integration ---
from send_expression import send_expression, expressions

def set_facial_expression(expression_name):
    """
    Set the robot's facial expression if it exists.
    """
    if expression_name in expressions:
        send_expression(expression_name)
    else:
        print(f"Expression '{expression_name}' not found.")

nlp = spacy.load("en_core_web_sm")

def phrase_in_command(phrases, command, threshold=85):
    for phrase in phrases:
        if re.search(r'\b' + re.escape(phrase) + r'\b', command):
            return True
    best = process.extractOne(command, phrases, scorer=fuzz.token_sort_ratio)
    if best and best[1] >= threshold:
        return True
    return False

def safe_eval(expr):
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "round": round})
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Use of '{name}' not allowed")
    return eval(code, {"__builtins__": {}}, allowed_names)

def clean_name(name):
    name = re.sub(r'\s+([.,])', r'\1', name)
    name = re.sub(r'([.,])\s+', r'\1 ', name)
    return name.title().strip()

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return None

def search_wiktionary(word):
    parser = WiktionaryParser()
    try:
        result = parser.fetch(word)
        if result and result[0]['definitions']:
            return result[0]['definitions'][0]['text'][0]
    except Exception:
        pass
    return None

def ask_llama3(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": prompt}
        )
        data = response.json()
        # Friendlier message for memory errors
        if "error" in data and "memory" in data["error"]:
            return "Sorry, I can't answer that right now because my language model needs more memory than is available on this system."
        return data.get("response", data.get("error", "No response from Phi-3."))
    except Exception as e:
        return "Sorry, I couldn't reach my language model right now."

class VoiceAssistantNode(Node):
    def __init__(self):
        super().__init__('voice_assistant_node')
        self.knowledge_file = "knowledge.json"
        self.user_file = "user_profile.json"
        self.reminders_file = "reminders.json"
        self.knowledge = self.load_knowledge()
        self.user_profile = self.load_user_profile()
        self.reminders = self.load_reminders()
        self.reasoning_engine = ReasoningEngine()
        self.reasoning_engine.reset()
        self.last_subject = None
        self.last_web_query = None

    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_knowledge(self):
        try:
            with open(self.knowledge_file, "w") as f:
                json.dump(self.knowledge, f)
        except Exception:
            pass

    def load_user_profile(self):
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_user_profile(self):
        try:
            with open(self.user_file, "w") as f:
                json.dump(self.user_profile, f)
        except Exception:
            pass

    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_reminders(self):
        try:
            with open(self.reminders_file, "w") as f:
                json.dump(self.reminders, f)
        except Exception:
            pass

    def infer_chain(self, key, depth=0, max_depth=5):
        if depth > max_depth:
            return None
        value = self.knowledge.get(key)
        if value is None:
            return None
        if value in self.knowledge:
            next_value = self.infer_chain(value, depth+1, max_depth)
            if next_value and next_value != value:
                return next_value
        return value

    def parse_command(self, command):
        doc = nlp(command)
        verb = None
        noun = None
        for token in doc:
            if token.pos_ == "VERB" and verb is None:
                verb = token.lemma_
            if token.pos_ in ["NOUN", "PROPN"] and noun is None:
                noun = token.text
        return verb, noun, doc

    def fuzzy_fact_lookup(self, key, threshold=70):
        if key in self.knowledge:
            return key
        best = process.extractOne(key, list(self.knowledge.keys()), scorer=fuzz.token_sort_ratio)
        if best and best[1] >= threshold:
            return best[0]
        return None

    def web_search(self, query):
        # Try Wikipedia first
        wiki = search_wikipedia(query)
        if wiki:
            self.knowledge[query] = wiki
            self.save_knowledge()
            return wiki
        # Try Wiktionary for definitions
        dict_def = search_wiktionary(query)
        if dict_def:
            self.knowledge[query] = dict_def
            self.save_knowledge()
            return dict_def
        # Fallback to DuckDuckGo
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
            if data.get("AbstractText"):
                self.knowledge[query] = data["AbstractText"]
                self.save_knowledge()
                return data["AbstractText"]
            elif data.get("Answer"):
                self.knowledge[query] = data["Answer"]
                self.save_knowledge()
                return data["Answer"]
            elif data.get("RelatedTopics"):
                for topic in data["RelatedTopics"]:
                    if "Text" in topic:
                        self.knowledge[query] = topic["Text"]
                        self.save_knowledge()
                        return topic["Text"]
            return None
        except Exception:
            return None

    def respond(self, text, tone="friendly"):
        if tone == "formal":
            return text
        elif tone == "humorous":
            return text + " 😄"
        else:
            return text

    # ...existing code for reminders, math, and conversation logic...

if __name__ == '__main__':
    rclpy.init()
    node = VoiceAssistantNode()
    print("Type your questions for ARI. Type 'exit', 'quit', or 'stop' to end.")
    while True:
        user_input = input("Ask ARI: ")
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Goodbye!")
            break
        print(node.generate_response(user_input))
