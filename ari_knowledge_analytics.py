# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Knowledge Statistics and Analytics Module
"""

import json
from collections import defaultdict, Counter
import re
from datetime import datetime

class KnowledgeAnalytics:
    def __init__(self, facts_file="learned_facts_expanded.json"):
        self.facts_file = facts_file
        self.facts = self.load_facts()
        
    def load_facts(self):
        """Load the facts database"""
        with open(self.facts_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_knowledge_stats(self):
        """Get comprehensive statistics about the knowledge base"""
        stats = {}
        
        # Basic counts
        stats['total_facts'] = len(self.facts)
        stats['total_questions'] = sum(len(fact.get("question", [])) for fact in self.facts)
        
        # Question pattern analysis
        question_patterns = Counter()
        question_lengths = []
        
        for fact in self.facts:
            for question in fact.get("question", []):
                # Count patterns
                question_lower = question.lower()
                
                # Extract first 2-3 words as pattern
                words = question_lower.split()[:3]
                pattern = " ".join(words)
                question_patterns[pattern] += 1
                
                # Track length
                question_lengths.append(len(question))
        
        stats['question_patterns'] = dict(question_patterns.most_common(20))
        stats['avg_question_length'] = sum(question_lengths) / len(question_lengths) if question_lengths else 0
        stats['min_question_length'] = min(question_lengths) if question_lengths else 0
        stats['max_question_length'] = max(question_lengths) if question_lengths else 0
        
        # Answer analysis
        answer_lengths = []
        for fact in self.facts:
            answer = fact.get("answer", "")
            if answer:
                answer_lengths.append(len(answer))
        
        stats['avg_answer_length'] = sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0
        stats['min_answer_length'] = min(answer_lengths) if answer_lengths else 0
        stats['max_answer_length'] = max(answer_lengths) if answer_lengths else 0
        
        # Topic categories (rough estimation)
        topics = defaultdict(int)
        for fact in self.facts:
            answer = fact.get("answer", "").lower()
            questions = " ".join(fact.get("question", [])).lower()
            combined_text = answer + " " + questions
            
            # Science topics
            if any(word in combined_text for word in ["physics", "chemistry", "biology", "science", "atom", "molecule"]):
                topics["Science"] += 1
            elif any(word in combined_text for word in ["robot", "ai", "artificial intelligence", "computer", "technology"]):
                topics["Technology/AI"] += 1
            elif any(word in combined_text for word in ["tree", "plant", "animal", "nature", "environment", "climate"]):
                topics["Nature/Environment"] += 1
            elif any(word in combined_text for word in ["space", "planet", "universe", "star", "galaxy", "astronomy"]):
                topics["Space/Astronomy"] += 1
            elif any(word in combined_text for word in ["history", "ancient", "civilization", "war", "historical"]):
                topics["History"] += 1
            elif any(word in combined_text for word in ["music", "art", "movie", "book", "culture"]):
                topics["Arts/Culture"] += 1
            elif any(word in combined_text for word in ["help", "assist", "teach", "learn", "education"]):
                topics["Education/Help"] += 1
            else:
                topics["General/Other"] += 1
        
        stats['topic_distribution'] = dict(topics)
        
        return stats
    
    def find_knowledge_gaps(self):
        """Identify potential gaps in knowledge coverage"""
        gaps = []
        
        # Common topics that might be missing or under-represented
        important_topics = [
            "mathematics", "engineering", "medicine", "psychology", 
            "economics", "politics", "geography", "literature",
            "philosophy", "religion", "sports", "food", "transportation"
        ]
        
        for topic in important_topics:
            count = 0
            for fact in self.facts:
                combined_text = (fact.get("answer", "") + " " + " ".join(fact.get("question", []))).lower()
                if topic in combined_text:
                    count += 1
            
            if count < 5:  # Less than 5 facts about this topic
                gaps.append({"topic": topic, "fact_count": count})
        
        return sorted(gaps, key=lambda x: x["fact_count"])
    
    def get_most_comprehensive_topics(self):
        """Find topics with the most comprehensive coverage"""
        topic_coverage = defaultdict(list)
        
        for i, fact in enumerate(self.facts):
            combined_text = (fact.get("answer", "") + " " + " ".join(fact.get("question", []))).lower()
            
            # Extract key nouns/topics
            words = re.findall(r'\b[a-z]{4,}\b', combined_text)
            for word in set(words):
                if word not in ["what", "this", "that", "them", "they", "with", "from", "about", "would", "could"]:
                    topic_coverage[word].append(i)
        
        # Find topics with most facts
        comprehensive_topics = []
        for topic, fact_indices in topic_coverage.items():
            if len(fact_indices) >= 10:  # Topics covered in 10+ facts
                comprehensive_topics.append({
                    "topic": topic,
                    "fact_count": len(fact_indices),
                    "question_count": sum(len(self.facts[i].get("question", [])) for i in fact_indices)
                })
        
        return sorted(comprehensive_topics, key=lambda x: x["fact_count"], reverse=True)[:15]
    
    def generate_report(self):
        """Generate a comprehensive knowledge base report"""
        stats = self.get_knowledge_stats()
        gaps = self.find_knowledge_gaps()
        comprehensive = self.get_most_comprehensive_topics()
        
        report = f"""
🧠 ARI KNOWLEDGE BASE ANALYTICS REPORT
{'='*60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 BASIC STATISTICS:
{'-'*30}
Total Facts: {stats['total_facts']:,}
Total Questions: {stats['total_questions']:,}
Questions per Fact: {stats['total_questions']/stats['total_facts']:.1f}

📝 QUESTION ANALYSIS:
{'-'*30}
Average Question Length: {stats['avg_question_length']:.1f} characters
Question Length Range: {stats['min_question_length']} - {stats['max_question_length']} characters

Top Question Patterns:
"""
        
        for pattern, count in list(stats['question_patterns'].items())[:10]:
            report += f"  • '{pattern}...': {count:,} questions\n"
        
        report += f"""
💬 ANSWER ANALYSIS:
{'-'*30}
Average Answer Length: {stats['avg_answer_length']:.1f} characters
Answer Length Range: {stats['min_answer_length']} - {stats['max_answer_length']} characters

🏷️ TOPIC DISTRIBUTION:
{'-'*30}
"""
        
        for topic, count in sorted(stats['topic_distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_facts']) * 100
            report += f"  • {topic}: {count} facts ({percentage:.1f}%)\n"
        
        report += f"""
🎯 MOST COMPREHENSIVE TOPICS:
{'-'*30}
"""
        
        for topic_info in comprehensive[:10]:
            report += f"  • {topic_info['topic']}: {topic_info['fact_count']} facts, {topic_info['question_count']} questions\n"
        
        report += f"""
⚠️ KNOWLEDGE GAPS (Topics with <5 facts):
{'-'*30}
"""
        
        for gap in gaps[:10]:
            report += f"  • {gap['topic']}: {gap['fact_count']} facts\n"
        
        report += f"""
✅ RECOMMENDATIONS:
{'-'*30}
1. Consider adding more facts about: {', '.join([g['topic'] for g in gaps[:5]])}
2. Most successful question patterns to use: {', '.join(list(stats['question_patterns'].keys())[:3])}
3. Knowledge base is strongest in: {', '.join([t['topic'] for t in comprehensive[:3]])}
4. Total coverage is excellent with {stats['total_questions']:,} ways to access {stats['total_facts']} facts
"""
        
        return report

def main():
    """Generate and display analytics report"""
    analytics = KnowledgeAnalytics()
    report = analytics.generate_report()
    print(report)
    
    # Save report to file
    with open(f"ari_knowledge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: ari_knowledge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

if __name__ == "__main__":
    main()
