# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Knowledge Quality Checker and Validator
"""

import json
import re
from datetime import datetime
from collections import defaultdict

class KnowledgeQualityChecker:
    def __init__(self, facts_file="learned_facts_expanded.json"):
        self.facts_file = facts_file
        self.facts = self.load_facts()
        
    def load_facts(self):
        """Load the facts database"""
        with open(self.facts_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def check_duplicate_questions(self):
        """Find duplicate questions across facts"""
        question_map = defaultdict(list)
        duplicates = []
        
        for i, fact in enumerate(self.facts):
            for question in fact.get("question", []):
                normalized_q = question.lower().strip()
                question_map[normalized_q].append((i, question))
        
        for normalized_q, occurrences in question_map.items():
            if len(occurrences) > 1:
                duplicates.append({
                    "question": normalized_q,
                    "occurrences": occurrences,
                    "count": len(occurrences)
                })
        
        return sorted(duplicates, key=lambda x: x["count"], reverse=True)
    
    def check_empty_or_invalid_entries(self):
        """Find facts with missing or invalid data"""
        issues = []
        
        for i, fact in enumerate(self.facts):
            fact_issues = []
            
            # Check for missing answer
            if not fact.get("answer") or not fact.get("answer").strip():
                fact_issues.append("Missing or empty answer")
            
            # Check for missing questions
            if not fact.get("question") or len(fact.get("question", [])) == 0:
                fact_issues.append("Missing questions")
            
            # Check for very short answers (likely incomplete)
            if fact.get("answer") and len(fact.get("answer").strip()) < 10:
                fact_issues.append(f"Very short answer ({len(fact.get('answer').strip())} chars)")
            
            # Check for questions that are too short
            short_questions = []
            for q in fact.get("question", []):
                if len(q.strip()) < 3:
                    short_questions.append(q)
            if short_questions:
                fact_issues.append(f"Very short questions: {short_questions}")
            
            if fact_issues:
                issues.append({
                    "fact_index": i,
                    "answer_preview": (fact.get("answer", "")[:50] + "...") if fact.get("answer") else "No answer",
                    "question_count": len(fact.get("question", [])),
                    "issues": fact_issues
                })
        
        return issues
    
    def check_answer_quality(self):
        """Analyze answer quality and consistency"""
        quality_issues = []
        
        for i, fact in enumerate(self.facts):
            answer = fact.get("answer", "")
            if not answer:
                continue
                
            issues = []
            
            # Check for very long answers (might be too verbose)
            if len(answer) > 500:
                issues.append(f"Very long answer ({len(answer)} chars)")
            
            # Check for repeated words/phrases
            words = answer.lower().split()
            word_counts = defaultdict(int)
            for word in words:
                if len(word) > 4:  # Only check longer words
                    word_counts[word] += 1
            
            repeated_words = [word for word, count in word_counts.items() if count > 3]
            if repeated_words:
                issues.append(f"Repeated words: {repeated_words[:3]}")
            
            # Check for proper sentence structure
            sentences = re.split(r'[.!?]+', answer)
            if len(sentences) > 1:
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and not sentence[0].isupper():
                        issues.append("Capitalization issues")
                        break
            
            # Check for placeholder text
            placeholders = ["TODO", "TBD", "...", "xxx", "???"]
            for placeholder in placeholders:
                if placeholder.lower() in answer.lower():
                    issues.append(f"Contains placeholder: {placeholder}")
            
            if issues:
                quality_issues.append({
                    "fact_index": i,
                    "answer_preview": answer[:100] + "...",
                    "issues": issues
                })
        
        return quality_issues
    
    def check_question_diversity(self):
        """Analyze question pattern diversity"""
        pattern_counts = defaultdict(int)
        
        for fact in self.facts:
            fact_patterns = set()
            for question in fact.get("question", []):
                # Extract first 2-3 words as pattern
                words = question.lower().split()[:3]
                pattern = " ".join(words)
                fact_patterns.add(pattern)
            
            for pattern in fact_patterns:
                pattern_counts[pattern] += 1
        
        # Find patterns that might be overused
        total_facts = len(self.facts)
        overused_patterns = []
        for pattern, count in pattern_counts.items():
            if count > total_facts * 0.8:  # Used in more than 80% of facts
                overused_patterns.append((pattern, count, count/total_facts*100))
        
        return sorted(overused_patterns, key=lambda x: x[1], reverse=True)
    
    def suggest_improvements(self):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Check duplicates
        duplicates = self.check_duplicate_questions()
        if duplicates:
            suggestions.append({
                "category": "Duplicates",
                "priority": "High",
                "description": f"Found {len(duplicates)} duplicate questions",
                "action": "Remove duplicate questions or merge facts with identical questions"
            })
        
        # Check data quality
        invalid_entries = self.check_empty_or_invalid_entries()
        if invalid_entries:
            suggestions.append({
                "category": "Data Quality",
                "priority": "High",
                "description": f"Found {len(invalid_entries)} facts with data issues",
                "action": "Fix missing answers, empty questions, or very short content"
            })
        
        # Check answer quality
        quality_issues = self.check_answer_quality()
        if quality_issues:
            suggestions.append({
                "category": "Answer Quality",
                "priority": "Medium",
                "description": f"Found {len(quality_issues)} facts with answer quality issues",
                "action": "Review very long answers, fix repeated words, check for placeholders"
            })
        
        # Check diversity
        overused = self.check_question_diversity()
        if overused:
            suggestions.append({
                "category": "Question Diversity",
                "priority": "Low",
                "description": f"Found {len(overused)} overused question patterns",
                "action": "Add more variety to question phrasings"
            })
        
        return suggestions
    
    def generate_quality_report(self):
        """Generate a comprehensive quality report"""
        duplicates = self.check_duplicate_questions()
        invalid_entries = self.check_empty_or_invalid_entries()
        quality_issues = self.check_answer_quality()
        overused_patterns = self.check_question_diversity()
        suggestions = self.suggest_improvements()
        
        total_facts = len(self.facts)
        total_questions = sum(len(fact.get("question", [])) for fact in self.facts)
        
        report = f"""
🔍 ARI KNOWLEDGE QUALITY REPORT
{'='*60}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 OVERVIEW:
{'-'*30}
Total Facts: {total_facts:,}
Total Questions: {total_questions:,}
Average Questions per Fact: {total_questions/total_facts:.1f}

🚨 ISSUES FOUND:
{'-'*30}
Duplicate Questions: {len(duplicates)}
Invalid/Empty Entries: {len(invalid_entries)}
Answer Quality Issues: {len(quality_issues)}
Overused Question Patterns: {len(overused_patterns)}

📋 DETAILED ANALYSIS:
{'-'*30}
"""
        
        if duplicates:
            report += f"\n🔄 TOP DUPLICATE QUESTIONS:\n"
            for dup in duplicates[:5]:
                report += f"  • '{dup['question']}' appears {dup['count']} times\n"
        
        if invalid_entries:
            report += f"\n❌ DATA QUALITY ISSUES:\n"
            for issue in invalid_entries[:5]:
                report += f"  • Fact #{issue['fact_index']}: {', '.join(issue['issues'])}\n"
        
        if quality_issues:
            report += f"\n⚠️ ANSWER QUALITY ISSUES:\n"
            for issue in quality_issues[:5]:
                report += f"  • Fact #{issue['fact_index']}: {', '.join(issue['issues'])}\n"
        
        if overused_patterns:
            report += f"\n🔁 OVERUSED QUESTION PATTERNS:\n"
            for pattern, count, percentage in overused_patterns[:5]:
                report += f"  • '{pattern}...': {count} facts ({percentage:.1f}%)\n"
        
        report += f"\n💡 IMPROVEMENT SUGGESTIONS:\n{'-'*30}\n"
        for suggestion in suggestions:
            report += f"🎯 {suggestion['category']} ({suggestion['priority']} Priority):\n"
            report += f"   {suggestion['description']}\n"
            report += f"   Action: {suggestion['action']}\n\n"
        
        if not suggestions:
            report += "✅ No major issues found! Knowledge base quality is excellent.\n"
        
        report += f"""
📈 QUALITY SCORE:
{'-'*30}
Overall Score: {self.calculate_quality_score():.1f}/100
"""
        
        return report
    
    def calculate_quality_score(self):
        """Calculate an overall quality score"""
        score = 100
        
        # Deduct points for issues
        duplicates = len(self.check_duplicate_questions())
        invalid_entries = len(self.check_empty_or_invalid_entries())
        quality_issues = len(self.check_answer_quality())
        
        total_facts = len(self.facts)
        
        # Deduct points based on percentage of facts with issues
        if total_facts > 0:
            score -= (duplicates / total_facts) * 20  # Up to 20 points for duplicates
            score -= (invalid_entries / total_facts) * 30  # Up to 30 points for invalid entries
            score -= (quality_issues / total_facts) * 15  # Up to 15 points for quality issues
        
        return max(score, 0)

def main():
    """Run the quality checker"""
    checker = KnowledgeQualityChecker()
    report = checker.generate_quality_report()
    print(report)
    
    # Save report to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ari_quality_report_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n📄 Quality report saved to: {filename}")

if __name__ == "__main__":
    main()
