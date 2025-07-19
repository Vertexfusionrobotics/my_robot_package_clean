# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Interactive Question Suggestion System
"""

import json
import random
from rapidfuzz import fuzz
from collections import defaultdict

class QuestionSuggester:
    def __init__(self, facts_file="learned_facts_expanded.json"):
        self.facts_file = facts_file
        self.facts = self.load_facts()
        self.topic_index = self.build_topic_index()
        
    def load_facts(self):
        """Load the facts database"""
        with open(self.facts_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def build_topic_index(self):
        """Build an index of topics to facts"""
        topic_index = defaultdict(list)
        
        for i, fact in enumerate(self.facts):
            # Extract keywords from questions and answers
            combined_text = fact.get("answer", "") + " " + " ".join(fact.get("question", []))
            words = combined_text.lower().split()
            
            # Filter meaningful words
            meaningful_words = []
            for word in words:
                word = word.strip(".,!?;:()")
                if len(word) > 3 and word not in [
                    "what", "that", "this", "they", "them", "with", "from", "about", 
                    "would", "could", "should", "might", "will", "can", "are", "the",
                    "and", "but", "for", "you", "your", "have", "has", "been"
                ]:
                    meaningful_words.append(word)
            
            # Add to topic index
            for word in set(meaningful_words):
                topic_index[word].append(i)
        
        return topic_index
    
    def suggest_questions_by_topic(self, topic, max_suggestions=10):
        """Suggest questions related to a specific topic"""
        topic_lower = topic.lower()
        related_facts = []
        
        # Find facts related to the topic
        for word, fact_indices in self.topic_index.items():
            if topic_lower in word or fuzz.ratio(topic_lower, word) > 80:
                for idx in fact_indices:
                    if idx not in [f[0] for f in related_facts]:
                        related_facts.append((idx, word))
        
        if not related_facts:
            return []
        
        # Sample questions from related facts
        suggestions = []
        for fact_idx, matching_word in related_facts[:max_suggestions]:
            fact = self.facts[fact_idx]
            if fact.get("question"):
                # Pick a diverse question format
                question = random.choice(fact["question"])
                suggestions.append({
                    "question": question,
                    "topic": matching_word,
                    "answer_preview": fact.get("answer", "")[:100] + "..."
                })
        
        return suggestions[:max_suggestions]
    
    def suggest_random_questions(self, count=5):
        """Suggest random interesting questions"""
        random_facts = random.sample(self.facts, min(count, len(self.facts)))
        suggestions = []
        
        for fact in random_facts:
            if fact.get("question"):
                question = random.choice(fact["question"])
                suggestions.append({
                    "question": question,
                    "answer_preview": fact.get("answer", "")[:100] + "..."
                })
        
        return suggestions
    
    def suggest_follow_up_questions(self, previous_answer, max_suggestions=5):
        """Suggest follow-up questions based on a previous answer"""
        if not previous_answer:
            return self.suggest_random_questions(max_suggestions)
        
        # Extract keywords from the previous answer
        words = previous_answer.lower().split()
        keywords = []
        for word in words:
            word = word.strip(".,!?;:()")
            if len(word) > 4:
                keywords.append(word)
        
        # Find related questions
        suggestions = []
        for keyword in keywords[:3]:  # Use top 3 keywords
            topic_suggestions = self.suggest_questions_by_topic(keyword, 2)
            suggestions.extend(topic_suggestions)
        
        # Remove duplicates and return
        unique_suggestions = []
        seen_questions = set()
        for suggestion in suggestions:
            if suggestion["question"] not in seen_questions:
                seen_questions.add(suggestion["question"])
                unique_suggestions.append(suggestion)
        
        return unique_suggestions[:max_suggestions]
    
    def get_popular_topics(self, top_n=10):
        """Get the most popular topics in the knowledge base"""
        topic_counts = {topic: len(indices) for topic, indices in self.topic_index.items()}
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_topics[:top_n]
    
    def interactive_session(self):
        """Run an interactive question suggestion session"""
        print("🤖 ARI QUESTION SUGGESTION SYSTEM")
        print("=" * 50)
        print("I can suggest questions for you to ask ARI!")
        print("Commands:")
        print("  'topic <name>' - Get questions about a topic")
        print("  'random' - Get random questions")
        print("  'popular' - See popular topics")
        print("  'help' - Show this help")
        print("  'quit' - Exit")
        print("=" * 50)
        
        last_answer = None
        
        while True:
            try:
                user_input = input("\n💭 What kind of questions would you like? ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Happy questioning!")
                    break
                
                elif user_input.lower() == 'help':
                    print("\nCommands:")
                    print("  'topic <name>' - Get questions about a specific topic")
                    print("  'random' - Get 5 random questions")
                    print("  'popular' - See the most popular topics")
                    print("  'follow' - Get follow-up questions (if you've seen an answer)")
                    print("  'quit' - Exit")
                
                elif user_input.lower() == 'random':
                    suggestions = self.suggest_random_questions(5)
                    print("\n🎲 Here are 5 random questions to ask ARI:")
                    for i, suggestion in enumerate(suggestions, 1):
                        print(f"{i}. {suggestion['question']}")
                        print(f"   Preview: {suggestion['answer_preview']}")
                
                elif user_input.lower() == 'popular':
                    popular = self.get_popular_topics(10)
                    print("\n🔥 Most popular topics in ARI's knowledge base:")
                    for i, (topic, count) in enumerate(popular, 1):
                        print(f"{i:2d}. {topic} ({count} facts)")
                    print("\nTry: 'topic <name>' to get questions about any topic!")
                
                elif user_input.lower().startswith('topic '):
                    topic = user_input[6:].strip()
                    if topic:
                        suggestions = self.suggest_questions_by_topic(topic, 8)
                        if suggestions:
                            print(f"\n🎯 Questions about '{topic}':")
                            for i, suggestion in enumerate(suggestions, 1):
                                print(f"{i}. {suggestion['question']}")
                                print(f"   Preview: {suggestion['answer_preview']}")
                        else:
                            print(f"\n❌ No questions found about '{topic}'. Try a different topic or 'popular' to see available topics.")
                    else:
                        print("\n❌ Please specify a topic. Example: 'topic physics'")
                
                elif user_input.lower() == 'follow':
                    if last_answer:
                        suggestions = self.suggest_follow_up_questions(last_answer, 5)
                        print("\n🔗 Follow-up questions based on the last answer:")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"{i}. {suggestion['question']}")
                    else:
                        print("\n❌ No previous answer to base follow-ups on. Try asking ARI a question first!")
                
                else:
                    # Treat as a topic search
                    suggestions = self.suggest_questions_by_topic(user_input, 5)
                    if suggestions:
                        print(f"\n🔍 Questions related to '{user_input}':")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"{i}. {suggestion['question']}")
                            print(f"   Preview: {suggestion['answer_preview']}")
                    else:
                        print(f"\n❓ I didn't understand '{user_input}'. Type 'help' for commands or try 'random' for inspiration!")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Happy questioning!")
                break

def main():
    """Run the question suggester"""
    suggester = QuestionSuggester()
    suggester.interactive_session()

if __name__ == "__main__":
    main()
