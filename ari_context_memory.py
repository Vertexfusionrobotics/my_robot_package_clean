# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Context Memory System - Stage 3A: Conversation Context & Memory
Implements persistent conversation memory and context-aware response generation
"""

import json
import os
import pickle
from datetime import datetime, timedelta
from collections import defaultdict, deque
import uuid

class ARIContextMemory:
    """
    Advanced context memory system for multi-turn conversations
    """
    
    def __init__(self, memory_dir="ari_context_memory", max_context_length=50):
        self.memory_dir = memory_dir
        self.max_context_length = max_context_length
        self.current_session_id = None
        self.conversation_history = deque(maxlen=max_context_length)
        self.user_sessions = {}
        self.conversation_metadata = {}
        
        # Create memory directory
        os.makedirs(memory_dir, exist_ok=True)
        
        # Load existing memory
        self.load_persistent_memory()
        
        print("🧠 ARI Context Memory System initialized")
    
    def start_new_session(self, user_id="default_user"):
        """Start a new conversation session"""
        self.current_session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": self.current_session_id,
            "user_id": user_id,
            "start_time": datetime.now().isoformat(),
            "conversation_count": 0,
            "topics": [],
            "mood_indicators": [],
            "context_keywords": set()
        }
        
        self.user_sessions[self.current_session_id] = session_data
        self.conversation_history.clear()
        
        print(f"🆕 Started new conversation session: {self.current_session_id[:8]}...")
        return self.current_session_id
    
    def add_conversation_turn(self, user_input, ari_response, response_type="unknown", success=True):
        """Add a conversation turn to memory"""
        if not self.current_session_id:
            self.start_new_session()
        
        turn_data = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ari_response": ari_response,
            "response_type": response_type,
            "success": success,
            "context_position": len(self.conversation_history)
        }
        
        # Add to current conversation history
        self.conversation_history.append(turn_data)
        
        # Update session metadata
        session = self.user_sessions[self.current_session_id]
        session["conversation_count"] += 1
        session["last_interaction"] = datetime.now().isoformat()
        
        # Extract context keywords
        keywords = self.extract_context_keywords(user_input)
        session["context_keywords"].update(keywords)
        
        # Detect topics
        topics = self.detect_conversation_topics(user_input, ari_response)
        session["topics"].extend(topics)
        
        # Auto-save periodically
        if session["conversation_count"] % 5 == 0:
            self.save_persistent_memory()
        
        return turn_data
    
    def get_conversation_context(self, context_length=None):
        """Get recent conversation context"""
        if context_length is None:
            context_length = min(10, len(self.conversation_history))
        
        recent_context = list(self.conversation_history)[-context_length:]
        
        context_summary = {
            "total_turns": len(self.conversation_history),
            "recent_turns": recent_context,
            "context_keywords": list(self.user_sessions.get(self.current_session_id, {}).get("context_keywords", [])),
            "current_topics": self.get_current_topics(),
            "session_id": self.current_session_id
        }
        
        return context_summary
    
    def extract_context_keywords(self, text):
        """Extract important keywords for context tracking"""
        # Simple keyword extraction (can be enhanced with NLP)
        import re
        
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        # Extract words
        words = re.findall(r'\\b\\w+\\b', text.lower())
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        
        return set(keywords[:10])  # Top 10 keywords
    
    def detect_conversation_topics(self, user_input, ari_response):
        """Detect conversation topics"""
        topics = []
        
        # Topic patterns
        topic_patterns = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "question": ["what", "how", "why", "when", "where", "who"],
            "learning": ["learn", "teach", "explain", "understand", "know"],
            "emotion": ["feel", "emotion", "happy", "sad", "angry", "excited"],
            "capability": ["can you", "are you able", "do you", "capability"],
            "personal": ["name", "age", "family", "personal", "yourself"],
            "technical": ["computer", "robot", "ai", "technology", "system"],
            "weather": ["weather", "temperature", "rain", "sunny", "cloudy"],
            "time": ["time", "date", "day", "today", "tomorrow", "yesterday"]
        }
        
        text = (user_input + " " + ari_response).lower()
        
        for topic, keywords in topic_patterns.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def get_current_topics(self):
        """Get current conversation topics"""
        if not self.current_session_id or self.current_session_id not in self.user_sessions:
            return []
        
        session = self.user_sessions[self.current_session_id]
        recent_topics = session.get("topics", [])[-10:]  # Last 10 topics
        
        # Count topic frequency
        topic_counts = defaultdict(int)
        for topic in recent_topics:
            topic_counts[topic] += 1
        
        # Return sorted by frequency
        return sorted(topic_counts.keys(), key=lambda x: topic_counts[x], reverse=True)
    
    def get_context_for_response_generation(self):
        """Get formatted context for neural response generation"""
        context = self.get_conversation_context()
        
        # Format for neural networks
        context_features = {
            "conversation_length": context["total_turns"],
            "recent_user_inputs": [turn["user_input"] for turn in context["recent_turns"][-5:]],
            "recent_responses": [turn["ari_response"] for turn in context["recent_turns"][-5:]],
            "current_topics": context["current_topics"][:5],
            "context_keywords": list(context["context_keywords"])[:10],
            "session_duration": self.get_session_duration(),
            "response_success_rate": self.calculate_success_rate()
        }
        
        return context_features
    
    def get_session_duration(self):
        """Get current session duration in minutes"""
        if not self.current_session_id or self.current_session_id not in self.user_sessions:
            return 0
        
        session = self.user_sessions[self.current_session_id]
        start_time = datetime.fromisoformat(session["start_time"])
        duration = (datetime.now() - start_time).total_seconds() / 60
        
        return duration
    
    def calculate_success_rate(self):
        """Calculate conversation success rate"""
        if not self.conversation_history:
            return 0.5
        
        recent_turns = list(self.conversation_history)[-10:]
        successful_turns = sum(1 for turn in recent_turns if turn.get("success", True))
        
        return successful_turns / len(recent_turns) if recent_turns else 0.5
    
    def find_similar_conversations(self, current_input, max_results=5):
        """Find similar past conversations for context"""
        similar_conversations = []
        
        # Load historical conversations
        history_file = os.path.join(self.memory_dir, "conversation_history.json")
        if not os.path.exists(history_file):
            return similar_conversations
        
        try:
            with open(history_file, 'r') as f:
                historical_data = json.load(f)
            
            current_keywords = self.extract_context_keywords(current_input)
            
            for session_id, session_data in historical_data.items():
                if session_id == self.current_session_id:
                    continue
                
                session_keywords = set(session_data.get("context_keywords", []))
                keyword_overlap = len(current_keywords.intersection(session_keywords))
                
                if keyword_overlap > 0:
                    similarity_score = keyword_overlap / len(current_keywords.union(session_keywords))
                    similar_conversations.append({
                        "session_id": session_id,
                        "similarity_score": similarity_score,
                        "topics": session_data.get("topics", []),
                        "conversation_count": session_data.get("conversation_count", 0)
                    })
            
            # Sort by similarity and return top results
            similar_conversations.sort(key=lambda x: x["similarity_score"], reverse=True)
            return similar_conversations[:max_results]
            
        except Exception as e:
            print(f"⚠️ Error finding similar conversations: {e}")
            return similar_conversations
    
    def save_persistent_memory(self):
        """Save conversation memory to disk"""
        try:
            # Save session data
            sessions_file = os.path.join(self.memory_dir, "conversation_history.json")
            
            # Convert sets to lists for JSON serialization
            serializable_sessions = {}
            for session_id, session_data in self.user_sessions.items():
                serializable_data = session_data.copy()
                if "context_keywords" in serializable_data:
                    serializable_data["context_keywords"] = list(serializable_data["context_keywords"])
                serializable_sessions[session_id] = serializable_data
            
            with open(sessions_file, 'w') as f:
                json.dump(serializable_sessions, f, indent=2)
            
            # Save current conversation history
            if self.current_session_id:
                conversation_file = os.path.join(self.memory_dir, f"session_{self.current_session_id}.json")
                with open(conversation_file, 'w') as f:
                    json.dump(list(self.conversation_history), f, indent=2)
            
            print(f"💾 Context memory saved to {self.memory_dir}/")
            
        except Exception as e:
            print(f"⚠️ Error saving context memory: {e}")
    
    def load_persistent_memory(self):
        """Load conversation memory from disk"""
        try:
            sessions_file = os.path.join(self.memory_dir, "conversation_history.json")
            
            if os.path.exists(sessions_file):
                with open(sessions_file, 'r') as f:
                    loaded_sessions = json.load(f)
                
                # Convert lists back to sets
                for session_id, session_data in loaded_sessions.items():
                    if "context_keywords" in session_data:
                        session_data["context_keywords"] = set(session_data["context_keywords"])
                    self.user_sessions[session_id] = session_data
                
                print(f"📚 Loaded {len(self.user_sessions)} previous sessions")
            
        except Exception as e:
            print(f"⚠️ Error loading context memory: {e}")
    
    def get_memory_stats(self):
        """Get memory system statistics"""
        total_conversations = sum(session.get("conversation_count", 0) for session in self.user_sessions.values())
        active_sessions = len([s for s in self.user_sessions.values() 
                              if datetime.now() - datetime.fromisoformat(s.get("last_interaction", s["start_time"])) < timedelta(hours=24)])
        
        stats = {
            "total_sessions": len(self.user_sessions),
            "active_sessions": active_sessions,
            "total_conversations": total_conversations,
            "current_session_length": len(self.conversation_history),
            "memory_directory": self.memory_dir,
            "context_length": self.max_context_length
        }
        
        return stats

# Test the context memory system
if __name__ == "__main__":
    print("🧠 Testing ARI Context Memory System")
    print("=" * 50)
    
    # Create context memory instance
    memory = ARIContextMemory()
    
    # Start a new session
    session_id = memory.start_new_session("test_user")
    
    # Simulate a conversation
    conversations = [
        ("Hello ARI, how are you today?", "Hello! I'm doing well, thank you for asking. How can I help you today?", "greeting"),
        ("What can you do?", "I can help with various tasks including answering questions, having conversations, and learning from our interactions.", "capability"),
        ("Can you learn new things?", "Yes, I have learning capabilities and can improve from our conversations.", "learning"),
        ("That's interesting. What do you know about weather?", "I can discuss weather topics and help with weather-related questions. What would you like to know?", "weather"),
        ("Do you remember what we talked about earlier?", "Yes, we discussed my capabilities, learning abilities, and you asked about weather. I maintain context throughout our conversation.", "memory")
    ]
    
    # Add conversations to memory
    for user_input, ari_response, response_type in conversations:
        memory.add_conversation_turn(user_input, ari_response, response_type, success=True)
        print(f"✅ Added turn: {user_input[:30]}...")
    
    # Test context retrieval
    context = memory.get_conversation_context()
    print(f"\\n📊 Context: {context['total_turns']} turns, Topics: {context['current_topics']}")
    
    # Test similar conversations
    similar = memory.find_similar_conversations("Tell me about your learning abilities")
    print(f"🔍 Found {len(similar)} similar conversations")
    
    # Test context features for neural networks
    features = memory.get_context_for_response_generation()
    print(f"🧠 Context features ready for neural networks")
    
    # Get statistics
    stats = memory.get_memory_stats()
    print(f"📈 Memory stats: {stats}")
    
    # Save memory
    memory.save_persistent_memory()
    
    print("\\n✅ Context memory system test complete!")
