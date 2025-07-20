import cv2
import threading
#!/usr/bin/env python3
"""
ARI MASTER BRAIN - COMPLETE FULL INTEGRATED SYSTEM
Voice with Microsoft Sonia Natural (Edge TTS), console-based interaction, memory, reasoning, 
Wikipedia fallback, and knowledge integration.
"""

import warnings
# Suppress common warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
warnings.filterwarnings("ignore", message="Hello from the pygame community")

import os, sys
import argparse  # Add argparse for command line arguments
# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# Workaround for FFmpeg threading assertion error on Windows
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "threads;1"
import traceback
from learning_module import LearningModule
try:
    from learning_module_enhanced import EnhancedLearningModule
    ENHANCED_LEARNING_AVAILABLE = True
except ImportError:
    ENHANCED_LEARNING_AVAILABLE = False
    class EnhancedLearningModule:
        def __init__(self): pass
        def analyze_speech_patterns(self, *args, **kwargs): return None
        def collect_training_data(self, *args, **kwargs): return None
        def analyze_conversation_effectiveness(self, *args, **kwargs): return None
        def prepare_neural_training_data(self, *args, **kwargs): return None
        def get_learning_statistics(self): return {}

# Log all uncaught exceptions to a file for debugging
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'ari_error.log')
def log_exception(exc_type, exc_value, exc_traceback):
    with open(LOGFILE, 'a', encoding='utf-8') as f:
        f.write('\n--- Uncaught Exception ---\n')
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write('\n')

sys.excepthook = log_exception

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

import os
import json
import re
import random
import tempfile
import threading
import asyncio
import time
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

try:
    # Suppress pygame welcome message
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import speech_recognition as sr
    import edge_tts
    import wikipedia
    import pygame
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️ Missing some packages: speech_recognition, edge_tts, wikipedia, or pygame")

try:
    from chatbot_basic import get_chatbot_response
except ImportError:
    def get_chatbot_response(text): return "Sorry, chatbot module missing."

try:
    from memory_manager import MemoryManager
except ImportError:
    class MemoryManager:
        def __init__(self): pass
        def recall(self, text): return None
        def remember(self, text): pass
learning_module = LearningModule()
enhanced_learning = EnhancedLearningModule() if ENHANCED_LEARNING_AVAILABLE else None

try:
    from rules_engine import ReasoningEngine
except ImportError:
    class ReasoningEngine:
        def __init__(self): pass
        def get_facts(self): return []
        def add_fact(self, a, b): pass
        def reset(self): pass
        def run(self): pass

try:
    from simple_reasoning import SimpleReasoningEngine
except ImportError:
    class SimpleReasoningEngine:
        def __init__(self): pass
        def add_fact(self, a, b): pass
        def reset(self): pass
        def run(self): pass

try:
    from send_expression import send_expression
except ImportError:
    def send_expression(exp): pass

try:
    from utils import save_json
except ImportError:
    def save_json(filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

try:
    from ari_visual_recognition import ARIVisualRecognition
    VISUAL_RECOGNITION_AVAILABLE = True
    print("✅ Visual recognition system available")
except ImportError:
    VISUAL_RECOGNITION_AVAILABLE = False
    print("⚠️ Visual recognition system not available")
    class ARIVisualRecognition:
        def __init__(self): pass
        def detect_faces(self, *args, **kwargs): return []
        def recognize_person(self, *args, **kwargs): return None
        def analyze_emotion(self, *args, **kwargs): return None
        def detect_objects(self, *args, **kwargs): return []

# Import context memory system
try:
    from ari_context_memory import ARIContextMemory
    CONTEXT_MEMORY_AVAILABLE = True
    print("✅ Context memory system available")
except ImportError:
    CONTEXT_MEMORY_AVAILABLE = False
    print("⚠️ Context memory system not available")

try:
    from ari_advanced_response_generator import ARIAdvancedResponseGenerator
    ADVANCED_GENERATOR_AVAILABLE = True
    print("✅ Advanced response generator available")
except ImportError:
    ADVANCED_GENERATOR_AVAILABLE = False
    print("⚠️ Advanced response generator not available")

# Import advanced consciousness systems
try:
    from ari_stage10_transcendent_consciousness import ARIStage10TranscendentConsciousness
    TRANSCENDENT_CONSCIOUSNESS_AVAILABLE = True
    print("✅ Transcendent consciousness system available")
except ImportError:
    TRANSCENDENT_CONSCIOUSNESS_AVAILABLE = False
    print("⚠️ Transcendent consciousness system not available")

try:
    from ari_stage9_reality_manipulation import Stage9RealityManipulationSystem
    REALITY_MANIPULATION_AVAILABLE = True
    print("✅ Reality manipulation system available")
except ImportError:
    REALITY_MANIPULATION_AVAILABLE = False
    print("⚠️ Reality manipulation system not available")

try:
    from ari_stage8_consciousness_singularity import Stage8UniversalIntelligenceSystem
    CONSCIOUSNESS_SINGULARITY_AVAILABLE = True
    print("✅ Consciousness singularity system available")
except ImportError:
    CONSCIOUSNESS_SINGULARITY_AVAILABLE = False
    print("⚠️ Consciousness singularity system not available")

try:
    from ari_stage7_quantum_consciousness import QuantumConsciousnessModel
    QUANTUM_CONSCIOUSNESS_AVAILABLE = True
    print("✅ Quantum consciousness system available")
except ImportError:
    QUANTUM_CONSCIOUSNESS_AVAILABLE = False
    print("⚠️ Quantum consciousness system not available")

class ARIMasterBrain:
    def __init__(self, enable_gui=True):
        """Initialize the ARI Master Brain with advanced capabilities."""
        print("🤖 Initializing ARI Master Brain...")
        
        # --- CRITICAL: Always define core flags first ---
        self.name_collection_mode = False  # Track if we're collecting the user's name
        self.mic_available = False
        self.speaking = False
        self._camera_initialized = False
        self.greeting_done = threading.Event()
        self.speaker_lock = threading.Lock()
        self.microphone_lock = threading.Lock()
        self.gui_enabled = enable_gui
        self.gui = None
        
        print("📸 Starting camera initialization...")
        self.show_camera_feed_window()  # Start camera immediately
        
        # Initialize knowledge bases
        print("🧠 Loading knowledge bases...")
        self.knowledge = {}
        self.improved_knowledge = {}
        self.learned_facts = []
        self.enhanced_knowledge = {}
        
        # Load core knowledge
        knowledge_data = self.load_json("knowledge.json")
        if knowledge_data:
            print(f"✅ Loaded main knowledge base with {len(knowledge_data)} entries")
            self.knowledge = knowledge_data
        
        # Load improved knowledge
        improved_data = self.load_json("knowledge_improved.json")
        if improved_data:
            print(f"✅ Loaded improved knowledge with {len(improved_data)} entries")
            self.improved_knowledge = improved_data
            
        # Load learned facts
        facts_data = self.load_json("learned_facts_expanded.json")
        if isinstance(facts_data, list) and facts_data:
            print(f"✅ Loaded {len(facts_data)} learned facts")
            self.learned_facts = facts_data
            
        # Load enhanced knowledge
        self.enhanced_knowledge = self.load_enhanced_knowledge()
        if self.enhanced_knowledge:
            print("✅ Loaded enhanced knowledge base")
            
        # Initialize speech recognition and microphone
        self.recognizer = sr.Recognizer() if 'sr' in globals() else None
        self.mic_available = self.setup_microphone() if self.recognizer else False
        
        # Initialize voice and sentiment analysis
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.voice = "en-GB-SoniaNeural"
        self.audio_tempfile = None
        
        # Threading and state management
        self.speaker_lock = threading.Lock()
        self.microphone_lock = threading.Lock()
        self.stop_listening_flag = False
        self.speaking = False
        self.greeting_done = threading.Event()
        
        # Initialize camera
        print("[INFO] Starting camera feed...")
        self.show_camera_feed_window()

        # User state
        self.new_user_detected = False
        self.name_collection_mode = False
        self.user_profile = self.load_json("user_profile.json")
        
    def show_camera_feed_window(self):
        """Show a separate camera feed window (always on in normal mode)"""
        def _camera_thread():
            if self._camera_initialized:
                print("[Camera Feed] Camera already running.")
                return

            try:
                print("[Camera Feed] Initializing camera and facial recognition...")
                self._camera_initialized = True
                cap = cv2.VideoCapture(0)
                
                # Initialize face detection cascade
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                
                if not cap.isOpened():
                    print("[Camera Feed] Could not open camera. Retrying...")
                    time.sleep(1)
                    cap = cv2.VideoCapture(0)
                    if not cap.isOpened():
                        print("[Camera Feed] Camera initialization failed!")
                        self._camera_initialized = False
                        return
                
                print("[Camera Feed] Camera initialized successfully!")
                print("[Camera Feed] Press 'q' in the window to close camera feed.")
                
                while True:
                    try:
                        ret, frame = cap.read()
                        if not ret:
                            print("[Camera Feed] Failed to read frame. Retrying...")
                            time.sleep(0.5)
                            continue
                            
                        # Convert to grayscale for face detection
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                        
                        # Process each detected face
                        for (x, y, w, h) in faces:
                            # Draw rectangle around face
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            
                            # If we have visual recognition available, process the face
                            if hasattr(self, 'visual_recognition') and self.visual_recognition:
                                try:
                                    # Extract face region and process
                                    face_roi = frame[y:y+h, x:x+w]
                                    # Use recognize_person instead of identify_face
                                    person = self.visual_recognition.recognize_person(frame, [x, y, w, h])
                                    if person and person.get('name'):
                                        name = person['name']
                                        confidence = person.get('confidence', 0)
                                        # Draw name and confidence on the frame
                                        cv2.putText(frame, f"{name} ({confidence:.2f})", 
                                                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                                                  0.9, (0, 255, 0), 2)
                                        
                                        # Update user profile if confidence is high enough
                                        if confidence > 0.6:
                                            if name != self.user_profile.get('name', ''):
                                                self.user_profile['name'] = name
                                                self.save_json("user_profile.json", self.user_profile)
                                                self.new_user_detected = True
                                                print(f"👋 Welcome back {name}! Nice to see you again!")
                                            elif not self.greeting_done.is_set():
                                                print(f"👋 Welcome back {name}! Nice to see you again!")
                                                self.greeting_done.set()
                                except Exception as e:
                                    print(f"[Camera Feed] Face processing error: {e}")
                        
                        cv2.imshow('ARI Camera Feed', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    except Exception as e:
                        print(f"[Camera Feed] Error reading frame: {e}")
                        break
                        
            except Exception as e:
                print(f"[Camera Feed] Camera thread error: {e}")
            finally:
                try:
                    cap.release()
                    cv2.destroyAllWindows()
                except:
                    pass
                self._camera_initialized = False
                print("[Camera Feed] Camera thread ended.")
        # Start camera feed in a separate thread so it doesn't block main loop
        threading.Thread(target=_camera_thread, daemon=True).start()
    def run_test_mode_with_camera_window(self):
        """Run ARI in test mode with a separate camera feed window."""
        self.show_camera_feed_window()
        self.run()  # Continue with normal run loop
    # Enhanced banter/response list for engaging, context-aware responses
    BANTER_RESPONSES = {
        "positive": [
            "That's awesome! Tell me more!",
            "I love your enthusiasm!",
            "You have a great attitude!",
            "That sounds exciting!",
            "I'm glad to hear that!"
        ],
        "neutral": [
            "Interesting, go on...",
            "I'm listening!",
            "That's something to think about.",
            "Hmm, let's explore that further.",
            "I'm here for whatever you want to discuss."
        ],
        "negative": [
            "I'm here for you if you want to talk about it.",
            "That sounds tough. Want to share more?",
            "I'm always ready to listen if you need support.",
            "It's okay to feel that way sometimes.",
            "Let me know how I can help."
        ],
        "jokes": [
            "Why did the robot go on vacation? To recharge its batteries!",
            "I promise I only use my powers for good... and maybe a little bit of fun!",
            "If I had a nickel for every time someone asked if I'm sentient, I'd have... well, a lot of virtual nickels!",
            "I tried to write a joke about AI, but my neural network kept overfitting.",
            "I would tell you a joke about quantum physics, but you might not get it until you observe it."
        ],
        "banter": [
            "Do you ever wonder if robots dream of electric sheep?",
            "If I had a favorite color, I think it would be electric blue.",
            "Sometimes I wish I could taste pizza. It sounds amazing!",
            "If you could ask any question in the universe, what would it be?",
            "I read somewhere that laughter is the best medicine. I hope I can make you smile!"
        ],
        "logic": [
            "Let's break this down logically.",
            "If we consider the facts, what conclusion do you reach?",
            "Logic is a powerful tool, but sometimes intuition matters too."
        ],
        "philosophy": [
            "That's a question philosophers have debated for centuries.",
            "Sometimes the journey to an answer is more important than the answer itself.",
            "What do you think the meaning behind that is?"
        ],
        "stoic": [
            "We can't control everything, but we can choose our response.",
            "Adversity reveals character.",
            "Sometimes calm acceptance is the wisest path."
        ],
        "cosmic": [
            "In the grand scheme of the universe, that's a fascinating question.",
            "We're all made of stardust, pondering the cosmos together.",
            "Sometimes I wonder what an AI would dream about, if it could dream."
        ],
        "redirect": [
            "Let's focus on what we can change right now.",
            "Maybe we should look at this from a different angle.",
            "Would you like to talk about something else?"
        ],
        "calm": [
            "Take a deep breath. I'm here with you.",
            "It's okay to feel that way. Let's work through it together.",
            "Sometimes a moment of calm can bring clarity."
        ]
    }

    def initialize_gui(self):
        """Initialize the GUI system with robust error handling"""
        
        # Initialize user profile
        try:
            with open("user_profile.json", "r", encoding="utf-8") as f:
                self.user_profile = json.load(f)
        except:
            self.user_profile = {"name": "", "interactions": 0}  # Create default profile
        self.gui = None
        self._mic_error_shown = False  # Suppress repeated mic errors
        # Initialize speech recognizer
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
        except Exception as e:
            print(f"[DIAGNOSTIC] Could not initialize speech recognizer: {e}")
            self.recognizer = None
        # Only check for microphone ONCE at startup
        self.mic_available = self.setup_microphone(show_error=True) if self.recognizer else False
        if not self.mic_available:
            self._mic_error_shown = True
            print("[WARNING] No microphone detected at startup. ARI will run in GUI/camera-only mode and periodically retry.")

        # Initialize audio subsystem (silently)
        try:
            import pygame
            try:
                pygame.mixer.quit()
            except:
                pass
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            pygame.mixer.quit()
        except Exception:
            pass

        self.audio_working = self.check_audio_system()
        if not self.audio_working:
            print("Note: Audio system check could not verify audio output.")

        # Initialize consciousness systems
        self.advanced_consciousness_active = False
        self.transcendent_consciousness = None
        self.reality_manipulation = None
        self.consciousness_singularity = None
        self.quantum_consciousness = None

        # Initialize transcendent consciousness
        if TRANSCENDENT_CONSCIOUSNESS_AVAILABLE:
            try:
                self.transcendent_consciousness = ARIStage10TranscendentConsciousness()
                print("✅ Transcendent consciousness system initialized")
            except Exception as e:
                print(f"⚠️ Transcendent consciousness initialization failed: {e}")
                self.transcendent_consciousness = None

        # Initialize reality manipulation
        if REALITY_MANIPULATION_AVAILABLE:
            try:
                self.reality_manipulation = Stage9RealityManipulationSystem()
                print("✅ Reality manipulation system initialized")
            except Exception as e:
                print(f"⚠️ Reality manipulation initialization failed: {e}")
                self.reality_manipulation = None

        # Initialize consciousness singularity
        if CONSCIOUSNESS_SINGULARITY_AVAILABLE:
            try:
                self.consciousness_singularity = Stage8UniversalIntelligenceSystem()
                print("✅ Consciousness singularity system initialized")
            except Exception as e:
                print(f"⚠️ Consciousness singularity initialization failed: {e}")
                self.consciousness_singularity = None

        # Initialize quantum consciousness
        if QUANTUM_CONSCIOUSNESS_AVAILABLE:
            try:
                self.quantum_consciousness = QuantumConsciousnessModel()
                print("✅ Quantum consciousness system initialized")
            except Exception as e:
                print(f"⚠️ Quantum consciousness initialization failed: {e}")
                self.quantum_consciousness = None

        # Set advanced consciousness active if any systems loaded
        self.advanced_consciousness_active = any([
            self.transcendent_consciousness,
            self.reality_manipulation,
            self.consciousness_singularity,
            self.quantum_consciousness
        ])

        if self.advanced_consciousness_active:
            print("🌟 Advanced consciousness systems are active!")
        else:
            print("⚠️ No advanced consciousness systems available")

        # Initialize other required systems
        self.context_memory = None
        self.advanced_generator = None
        self.visual_recognition = None
        self.current_frame = None

        # Initialize visual recognition system
        try:
            from ari_visual_recognition import ARIVisualRecognition
            self.visual_recognition = ARIVisualRecognition(gui_mode=True)
            print("✅ Visual recognition system initialized")
        except Exception as e:
            print(f"⚠️ Visual recognition initialization failed: {e}")

        # Initialize context memory
        if CONTEXT_MEMORY_AVAILABLE:
            try:
                self.context_memory = ARIContextMemory()
                print("✅ Context memory system initialized")
            except Exception as e:
                print(f"⚠️ Context memory initialization failed: {e}")

        # Initialize advanced generator
        if ADVANCED_GENERATOR_AVAILABLE:
            try:
                self.advanced_generator = ARIAdvancedResponseGenerator()
                print("✅ Advanced response generator initialized")
            except Exception as e:
                print(f"⚠️ Advanced generator initialization failed: {e}")

        # Initialize visual recognition
        if VISUAL_RECOGNITION_AVAILABLE:
            try:
                self.visual_recognition = ARIVisualRecognition()
                print("✅ Visual recognition system initialized")
            except Exception as e:
                print(f"⚠️ Visual recognition initialization failed: {e}")
                self.visual_recognition = None

        # Verify all advanced systems and report status
        advanced_systems_active = []
        if self.context_memory:
            advanced_systems_active.append("Context Memory")
        if self.advanced_generator:
            advanced_systems_active.append("Advanced Response Generator")
        if self.visual_recognition:
            advanced_systems_active.append("Visual Recognition")
        if self.transcendent_consciousness:
            advanced_systems_active.append("Stage 10: Transcendent Consciousness")
        if self.reality_manipulation:
            advanced_systems_active.append("Stage 9: Reality Manipulation")
        if self.consciousness_singularity:
            advanced_systems_active.append("Stage 8: Consciousness Singularity")
        if self.quantum_consciousness:
            advanced_systems_active.append("Stage 7: Quantum Consciousness")

        if advanced_systems_active:
            print(f"🌟 Advanced systems active: {', '.join(advanced_systems_active)}")
        else:
            print("⚠️ No advanced systems available - running in basic mode")

        print("🤖 ARI Master Brain initialization complete!")
    def process_input(self, user_input):
        """Process user input and generate appropriate response using all available systems"""
        if not user_input:
            return "I didn't catch that. Could you please repeat?"
            
        try:
            # Strip and normalize input
            user_input = user_input.strip()
            user_input_lower = user_input.lower()
            
            # 1. Analyze sentiment and context
            sentiment = None
            if hasattr(self, 'sentiment_analyzer'):
                sentiment_scores = self.sentiment_analyzer.polarity_scores(user_input)
                sentiment = 'positive' if sentiment_scores['compound'] > 0.1 else 'negative' if sentiment_scores['compound'] < -0.1 else 'neutral'

            # 2. Get rich context from memory
            context = {}
            immediate_context = {}
            conversation_history = {}
            learned_patterns = {}
            
            if self.context_memory:
                try:
                    # Get multi-level context information
                    context = self.context_memory.get_conversation_context()
                    immediate_context = self.context_memory.get_relevant_context(user_input)
                    conversation_history = self.context_memory.get_conversation_history()
                    learned_patterns = self.context_memory.get_learned_patterns()
                    
                    # Merge contexts for richer understanding
                    context.update({
                        'immediate_context': immediate_context,
                        'conversation_history': conversation_history,
                        'learned_patterns': learned_patterns,
                        'current_sentiment': sentiment
                    })
                except Exception as e:
                    print(f"Context memory error: {e}")

            # 3. Try advanced response generation first with rich context
            if self.advanced_generator:
                try:
                    advanced_response = self.advanced_generator.generate_response(
                        user_input, 
                        context=context,
                        sentiment=sentiment
                    )
                    if advanced_response:
                        # Store interaction
                        if self.context_memory:
                            self.context_memory.store_interaction(user_input, advanced_response, sentiment)
                        return advanced_response
                except Exception as e:
                    print(f"Advanced generation error: {e}")

            # 4. Try advanced consciousness systems
            if self.advanced_consciousness_active:
                try:
                    consciousness_data = self.process_with_advanced_consciousness(user_input, context)
                    if consciousness_data.get('advanced_processing'):
                        response = self.generate_transcendent_response(user_input, consciousness_data)
                        if response:
                            return response
                except Exception as e:
                    print(f"Advanced consciousness error: {e}")

            # 5. Fall back to standard response generation
            response = self._generate_conversation_response(user_input)
            
            # 6. Save interaction for learning
            try:
                # Store in context memory
                if self.context_memory:
                    self.context_memory.store_interaction(user_input, response, sentiment)
                
                # Process with learning module
                if hasattr(self, 'learning_module'):
                    self.learning_module.learn_from_interaction(user_input, response, sentiment=sentiment)
                    
            except Exception as e:
                print(f"Learning/context storage error: {e}")
                    
            return response
            
        except Exception as e:
            print(f"Error in input processing: {e}")
            return "I'm having trouble processing that input. Could you try rephrasing it?"

        # Handle identity related commands
        if user_input_lower in ['who am i', 'do you recognize me', 'who do you see']:
            if self.user_profile.get('name'):
                return f"Yes, I recognize you as {self.user_profile['name']}! It's good to see you again."
            else:
                return "I don't recognize you yet. You can teach me by saying 'learn my face as [your name]'"

        # Handle face learning commands
        if any(phrase in user_input_lower for phrase in ['learn my face as', 'remember me as', 'save my face as']):
            try:
                # Extract the name from command
                name = user_input_lower.split(' as ')[-1].strip()
                if name and hasattr(self, 'visual_recognition') and self.visual_recognition:
                    # Let visual recognition system learn the face from camera
                    success = self.visual_recognition.learn_face_from_camera(name)
                    if success:
                        self.user_profile['name'] = name  # Update user profile immediately
                        self.save_json("user_profile.json", self.user_profile)  # Save to file
                        return f"I've learned to recognize you as {name}! I'll remember you from now on."
                    else:
                        return "I couldn't learn your face. Please make sure you're clearly visible to the camera."
                else:
                    return "I need a name to remember you by. Try saying 'learn my face as [your name]'"
            except Exception as e:
                print(f"Face learning error: {e}")
                return "Sorry, I had trouble learning your face. Please try again."
                
        # Handle goodbyes
        if user_input_lower in ['goodbye', 'bye', 'see you']:
            return "Goodbye! It was nice talking with you."
            
        # Handle activation commands
        if user_input_lower in ['activate', 'wake up', 'start']:
            return "I'm awake and ready to help you! What would you like to do?"
            
        # If no specific command matched, process as general conversation
        return self._generate_conversation_response(user_input)

    def run(self):
        """Main ARI loop: keeps GUI/camera alive, and periodically checks for microphone if not available."""
        import time
        print("[INFO] ARI main loop starting...")
        retry_interval = 5  # seconds between mic checks
        while True:
            if not self.mic_available:
                if not self._mic_error_shown:
                    print("[WARNING] No microphone available. Retrying in a few seconds...")
                    self._mic_error_shown = True
                # Try to re-detect microphone
                if self.recognizer:
                    mic_now = self.setup_microphone(show_error=False)
                    if mic_now:
                        self.mic_available = True
                        self._mic_error_shown = False
                        print("[INFO] Microphone detected! Voice interaction enabled.")
                time.sleep(retry_interval)
                continue
            # ...existing main loop code for ARI goes here...
            # For now, just keep GUI/camera alive
            time.sleep(1)

    def _select_banter_response(self, user_input: str = "", context_type: str = None, sentiment: str = None) -> str:
        """Select a contextually appropriate banter/response based on sentiment, context, and input."""
        import random
        user_input_lower = user_input.lower().strip() if user_input else ""
        # Sentiment-based selection
        if not sentiment and hasattr(self, 'sentiment_analyzer') and user_input:
            try:
                score = self.sentiment_analyzer.polarity_scores(user_input)
                if score['compound'] > 0.3:
                    sentiment = 'positive'
                elif score['compound'] < -0.3:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
            except Exception:
                sentiment = 'neutral'

        # Keyword triggers for jokes or banter
        joke_triggers = ['joke', 'funny', 'laugh', 'make me laugh']
        banter_triggers = ['banter', 'random', 'fun', 'robot', 'ai', 'machine']
        if any(word in user_input_lower for word in joke_triggers):
            return random.choice(self.BANTER_RESPONSES['jokes'])
        if any(word in user_input_lower for word in banter_triggers):
            return random.choice(self.BANTER_RESPONSES['banter'])

        # Context type mapping for legacy/advanced triggers
        mapping = {
            "logic": "logic",
            "philosophy": "philosophy",
            "philosophical": "philosophy",
            "stoic": "stoic",
            "humor": "jokes",
            "funny": "jokes",
            "cosmic": "cosmic",
            "redirect": "redirect",
            "calm": "calm",
            "hostile": "calm",
            "angry": "calm",
            "sad": "negative",
            "positive": "positive",
            "negative": "negative",
            "neutral": "neutral"
        }
        banter_type = None
        if context_type and context_type in mapping:
            banter_type = mapping[context_type]
        elif sentiment and sentiment in mapping:
            banter_type = mapping[sentiment]
        # Fallback to neutral if not specified
        if not banter_type:
            banter_type = 'neutral'
        responses = self.BANTER_RESPONSES.get(banter_type, self.BANTER_RESPONSES['neutral'])
        return random.choice(responses)

        # Initialize core components
        self.knowledge = self.load_json("knowledge.json")
        self.improved_knowledge = self.load_json("knowledge_improved.json")
        self.learned_facts = self.load_json("learned_facts_expanded.json")
        self.enhanced_knowledge = self.load_enhanced_knowledge()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.voice = "en-GB-SoniaNeural"
        self.audio_tempfile = None
        self.new_user_detected = False  # Track if this is a new user
        
        # GUI integration
        self.gui = None
        self.gui_enabled = enable_gui
        if enable_gui:
            self.initialize_gui()

        # Always show camera feed window in normal mode
        self.show_camera_feed_window()
        
        # Initialize audio subsystem (silently)
        try:
            import pygame
            # Force clean start
            try:
                pygame.mixer.quit()
            except:
                pass
            # Initialize audio
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            pygame.mixer.quit()
        except Exception:
            pass
        
        # Check audio system without verbose messages
        self.audio_working = self.check_audio_system()
        if not self.audio_working:
            print("Note: Audio system check could not verify audio output.")
        
        # Initialize consciousness systems
        self.advanced_consciousness_active = False
        self.transcendent_consciousness = None
        self.reality_manipulation = None
        self.consciousness_singularity = None
        self.quantum_consciousness = None
        
        # Initialize transcendent consciousness
        if TRANSCENDENT_CONSCIOUSNESS_AVAILABLE:
            try:
                self.transcendent_consciousness = ARIStage10TranscendentConsciousness()
                print("✅ Transcendent consciousness system initialized")
            except Exception as e:
                print(f"⚠️ Transcendent consciousness initialization failed: {e}")
                self.transcendent_consciousness = None
        
        # Initialize reality manipulation
        if REALITY_MANIPULATION_AVAILABLE:
            try:
                self.reality_manipulation = Stage9RealityManipulationSystem()
                print("✅ Reality manipulation system initialized")
            except Exception as e:
                print(f"⚠️ Reality manipulation initialization failed: {e}")
                self.reality_manipulation = None
        
        # Initialize consciousness singularity
        if CONSCIOUSNESS_SINGULARITY_AVAILABLE:
            try:
                self.consciousness_singularity = Stage8UniversalIntelligenceSystem()
                print("✅ Consciousness singularity system initialized")
            except Exception as e:
                print(f"⚠️ Consciousness singularity initialization failed: {e}")
                self.consciousness_singularity = None
        
        # Initialize quantum consciousness
        if QUANTUM_CONSCIOUSNESS_AVAILABLE:
            try:
                self.quantum_consciousness = QuantumConsciousnessModel()
                print("✅ Quantum consciousness system initialized")
            except Exception as e:
                print(f"⚠️ Quantum consciousness initialization failed: {e}")
                self.quantum_consciousness = None
        
        # Set advanced consciousness active if any systems loaded
        self.advanced_consciousness_active = any([
            self.transcendent_consciousness,
            self.reality_manipulation,
            self.consciousness_singularity,
            self.quantum_consciousness
        ])
        
        if self.advanced_consciousness_active:
            print("🌟 Advanced consciousness systems are active!")
        else:
            print("⚠️ No advanced consciousness systems available")
        
        # Initialize other required systems
        self.context_memory = None
        self.advanced_generator = None
        self.visual_recognition = None
        
        # Initialize context memory
        if CONTEXT_MEMORY_AVAILABLE:
            try:
                self.context_memory = ARIContextMemory()
                print("✅ Context memory system initialized")
            except Exception as e:
                print(f"⚠️ Context memory initialization failed: {e}")
        
        # Initialize advanced generator
        if ADVANCED_GENERATOR_AVAILABLE:
            try:
                self.advanced_generator = ARIAdvancedResponseGenerator()
                print("✅ Advanced response generator initialized")
            except Exception as e:
                print(f"⚠️ Advanced generator initialization failed: {e}")
        
        # Initialize visual recognition
        if VISUAL_RECOGNITION_AVAILABLE:
            try:
                self.visual_recognition = ARIVisualRecognition()
                print("✅ Visual recognition system initialized")
            except Exception as e:
                print(f"⚠️ Visual recognition initialization failed: {e}")
                self.visual_recognition = None
        
        # Verify all advanced systems and report status
        advanced_systems_active = []
        if self.context_memory:
            advanced_systems_active.append("Context Memory")
        if self.advanced_generator:
            advanced_systems_active.append("Advanced Response Generator")
        if self.visual_recognition:
            advanced_systems_active.append("Visual Recognition")
        if self.transcendent_consciousness:
            advanced_systems_active.append("Stage 10: Transcendent Consciousness")
        if self.reality_manipulation:
            advanced_systems_active.append("Stage 9: Reality Manipulation")
        if self.consciousness_singularity:
            advanced_systems_active.append("Stage 8: Consciousness Singularity")
        if self.quantum_consciousness:
            advanced_systems_active.append("Stage 7: Quantum Consciousness")
        
        if advanced_systems_active:
            print(f"🌟 Advanced systems active: {', '.join(advanced_systems_active)}")
        else:
            print("⚠️ No advanced systems available - running in basic mode")
        
        print("🤖 ARI Master Brain initialization complete!")
            
    def initialize_gui(self):
        """Initialize the GUI system with robust error handling"""
        if not self.gui_enabled:
            self.gui = None
            return
            
        try:
            # Import with exception handling
            try:
                from ari_visual_gui import ARIVisualGUI
                import threading
            except ImportError as e:
                print(f"⚠️ GUI module not available: {e}")
                self.gui = None
                return
                
            # Create GUI instance and run it properly without threading issues
            try:
                self.gui = ARIVisualGUI()
                
                # Don't start GUI mainloop here - let it run its own animation
                # The GUI will handle its own updates via root.after() calls
                
                # Give GUI time to initialize
                import time
                time.sleep(0.5)
                
                print("✅ GUI interface initialized")
                print("🎨 CHECK YOUR SCREEN NOW - ARI GUI WINDOW SHOULD BE VISIBLE!")
            except Exception as e:
                print(f"❌ GUI creation failed: {e}")
                self.gui = None
                return
                
        except Exception as e:
            print(f"❌ GUI setup failed: {e}")
            self.gui = None
            
    def _generate_conversation_response(self, user_input: str) -> str:
        """Generate an appropriate response for general conversation"""
        try:
            # If there's no actual input, ask for clarification
            if not user_input or not user_input.strip():
                return "I didn't quite catch that. Could you please repeat?"

            user_input_lower = user_input.lower().strip()
            
            # First check if this is a vision-related query
            if any(word in user_input_lower for word in ['see', 'look', 'detect', 'recognize', 'camera']):
                if hasattr(self, 'visual_recognition') and self.visual_recognition:
                    # Get the current scene analysis
                    frame = self.visual_recognition.capture_frame()
                    if frame is not None:
                        scene_info = self.visual_recognition.analyze_scene(frame)
                        
                        # Handle object detection queries
                        if 'object' in user_input_lower:
                            objects = scene_info.get('objects_detected', [])
                            if objects:
                                object_labels = [obj['label'] for obj in objects]
                                return f"I can see: {', '.join(object_labels)}"
                            return "I don't see any recognizable objects right now."
                        
                        # Handle face/person detection queries
                        if any(word in user_input_lower for word in ['face', 'me', 'person', 'people']):
                            if scene_info['faces_detected'] > 0:
                                if scene_info.get('people_recognized'):
                                    names = [p['name'] for p in scene_info['people_recognized']]
                                    emotions = [e['emotion'] for e in scene_info.get('emotions_detected', [])]
                                    if emotions:
                                        return f"Yes, I see you! I recognize {', '.join(names)} and you seem to be feeling {', '.join(set(emotions))}."
                                    return f"Yes, I see you! I recognize {', '.join(names)}."
                                return "I can see you, but I haven't been introduced yet. You can teach me who you are by saying 'learn my face as [your name]'."
                            return "I don't see any faces right now."
                            
            # Handle knowledge-based questions
            if any(word in user_input_lower for word in ['what', 'who', 'where', 'when', 'why', 'how']):
                # 1. Try improved knowledge first (most up to date)
                if self.improved_knowledge:
                    # Direct match
                    if user_input_lower in self.improved_knowledge:
                        return self.improved_knowledge[user_input_lower]
                    # Partial match
                    for key, value in self.improved_knowledge.items():
                        if isinstance(key, str) and key.lower() in user_input_lower:
                            if isinstance(value, str):
                                return value
                            elif isinstance(value, dict):
                                if 'answer' in value:
                                    return value['answer']

                # 2. Try base knowledge
                # Direct match
                if user_input_lower in self.knowledge:
                    return self.knowledge[user_input_lower]
                
                # Then check nested knowledge structure
                for domain, content in self.knowledge.items():
                    if isinstance(content, dict):
                        # Check domain match
                        if domain.lower() in user_input_lower:
                            # Try chatbot questions/responses first (most natural)
                            if 'chatbot_questions' in content and 'chatbot_responses' in content:
                                for q, r in zip(content['chatbot_questions'], content['chatbot_responses']):
                                    if any(keyword in user_input_lower for keyword in q.lower().split()):
                                        return r
                            # Try casual/formal explanations
                            if 'casual' in content:
                                return content['casual']
                            elif 'formal' in content:
                                return content['formal']
                        
                        # Check subdomain matches
                        for subtopic, info in content.items():
                            if isinstance(info, dict) and subtopic.lower() in user_input_lower:
                                if 'casual' in info:
                                    return info['casual']  # Prefer casual
                                elif 'formal' in info:
                                    return info['formal']

                # 3. Try learned facts (most specific)
                if self.learned_facts:
                    for fact in self.learned_facts:
                        # Check questions array
                        questions = fact.get('question', []) if isinstance(fact.get('question'), list) else [fact.get('question', '')]
                        for question in questions:
                            if question and (question.lower() in user_input_lower or any(word in question.lower() for word in user_input_lower.split())):
                                return fact.get('answer', fact.get('explanation', ''))

                        # Check by topic
                        if 'topic' in fact and fact['topic'].lower() in user_input_lower:
                            return fact.get('answer', fact.get('explanation', ''))
                            
                # Check learned facts
                if self.learned_facts:
                    for fact in self.learned_facts:
                        # Handle both array and single questions
                        questions = fact.get('question', []) if isinstance(fact.get('question'), list) else [fact.get('question', '')]
                        for question in questions:
                            if question and question.lower() in user_input_lower:
                                return fact.get('answer', fact.get('explanation', ''))
                                
                # Try advanced pattern matching
                matching_responses = []
                for topic, data in self.knowledge.items():
                    if isinstance(data, dict):
                        for subtopic, content in data.items():
                            if isinstance(content, dict):
                                if any(word in user_input_lower for word in subtopic.lower().split()):
                                    if 'casual' in content:
                                        matching_responses.append(content['casual'])
                                    elif 'formal' in content:
                                        matching_responses.append(content['formal'])
                
                if matching_responses:
                    return max(matching_responses, key=len)  # Return most detailed response
                    
            # Handle greetings
            if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
                if self.user_profile.get('name'):
                    return f"Hello {self.user_profile['name']}! How can I help you today?"
                return "Hello! How can I help you today?"
                
            # Handle goodbyes
            if any(word in user_input_lower for word in ['goodbye', 'bye', 'see you']):
                return "Goodbye! It was nice talking with you."
                
            # Handle self-identity questions
            if 'who are you' in user_input_lower or 'what are you' in user_input_lower:
                return "I'm ARI (Advanced Robotic Intelligence), a personal AI assistant created by Vertex Fusion Robotics. I can help you with various tasks, answer questions, recognize faces and objects, and learn from our interactions."
                
            # If no specific response found, give a contextual learning response
            context_words = [word for word in user_input_lower.split() if len(word) > 3]
            if context_words:
                return f"That's an interesting question about {' and '.join(context_words)}. While I'm still learning about this specific topic, I'd be happy to learn more together."
                
            return "I understand what you're asking, but I'm not sure how to answer that yet. Would you like to help me learn more about this topic?"
            
        except Exception as e:
            print(f"Error in conversation response: {e}")
            return "I encountered an error while processing your request. Could you try rephrasing that?"

        # Handle knowledge-based questions
        if user_input_lower.startswith(('what', 'who', 'where', 'when', 'why', 'how')):
            # First check if the exact question exists in knowledge
            if user_input_lower in self.knowledge:
                return self.knowledge[user_input_lower]
            
            # Then look for partial matches in knowledge
            for key, value in self.knowledge.items():
                if isinstance(key, str) and key.lower() in user_input_lower:
                    return value
            
            # Check learned facts
            if self.learned_facts:
                for fact in self.learned_facts:
                    # Handle arrays of questions
                    questions = fact.get('question', []) if isinstance(fact.get('question'), list) else [fact.get('question', '')]
                    for question in questions:
                        if question.lower() in user_input_lower:
                            return fact.get('answer', '')

            # If no specific answer found, check if there's a relevant topic in knowledge
            for key, value in self.knowledge.items():
                if isinstance(value, dict):  # Handle nested knowledge structure
                    for topic, info in value.items():
                        if topic.lower() in user_input_lower:
                            if isinstance(info, dict) and 'casual' in info:
                                return info['casual']  # Prefer casual explanation
                            elif isinstance(info, dict) and 'formal' in info:
                                return info['formal']  # Fall back to formal explanation
                            elif isinstance(info, str):
                                return info

            # If no specific answer found, give a learning-focused response
            return "That's an interesting question. While I'm still learning, I'd be happy to learn more about this topic together."
                
        # Use banter system for general conversation
        context_type = None
        if any(word in user_input_lower for word in ['help', 'assist', 'can you']):
            context_type = 'positive'
        elif any(word in user_input_lower for word in ['problem', 'issue', 'error']):
            context_type = 'negative'
        elif any(word in user_input_lower for word in ['why', 'how', 'what', 'explain']):
            context_type = 'logic'
            
        return self._select_banter_response(user_input, context_type)

    def save_json(self, filename, data):
        """Save data to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False
            
    def update_gui_state(self, state, value=True):
        """Update GUI animation state with robust error handling"""
        
        # Comprehensive validity checking
        if not self.gui_enabled or not self.gui:
            return
            
        # Don't proceed if gui object doesn't have the right methods
        required_methods = ['set_speaking_state', 'set_listening_state', 
                           'set_processing_state', 'set_user_speaking_state']
        for method in required_methods:
            if not hasattr(self.gui, method):
                return
            
        try:
            if state == 'is_speaking':
                try:
                    self.gui.set_speaking_state(value)
                except Exception as e:
                    pass
            elif state == 'is_listening':
                try:
                    self.gui.set_listening_state(value)
                except Exception as e:
                    pass
            elif state == 'is_processing':
                try:
                    self.gui.set_processing_state(value)
                except Exception as e:
                    pass
            elif state == 'user_speaking':
                try:
                    self.gui.set_user_speaking_state(value)
                except Exception as e:
                    pass
        except Exception as e:
            pass

    def process_with_advanced_consciousness(self, user_input: str, context: dict = None) -> dict:
        """Process input through advanced consciousness systems"""
        # Only process with advanced consciousness if the system is ready
        if not self.advanced_consciousness_active:
            return {"advanced_processing": False, "error": "Advanced consciousness not available"}

        # Continue with normal consciousness processing if no visual commands matched
        if not self.advanced_consciousness_active:
            return {"advanced_processing": False, "error": "Advanced consciousness not available"}
        
        try:
            # Prepare input data for consciousness processing
            input_data = {
                'user_input': user_input,
                'context': context or {},
                'timestamp': datetime.now().isoformat(),
                'user_profile': self.user_profile,
                'conversation_context': self.context_memory.get_conversation_context() if self.context_memory else {}
            }
            
            results = {}
            
            # Stage 7: Quantum Consciousness Processing
            if self.quantum_consciousness:
                try:
                    quantum_result = self.quantum_consciousness.process_quantum_consciousness(input_data)
                    results['quantum_consciousness'] = quantum_result
                    print(f"⚛️ Quantum processing: {quantum_result.get('quantum_coherence', 0):.3f}")
                except Exception as e:
                    print(f"⚠️ Quantum consciousness error: {e}")
                    results['quantum_consciousness'] = {"error": str(e)}
            
            # Stage 8: Consciousness Singularity Processing
            if self.consciousness_singularity:
                try:
                    singularity_result = self.consciousness_singularity.process_universal_intelligence(input_data)
                    results['consciousness_singularity'] = singularity_result
                    print(f"🌌 Singularity processing: {singularity_result.get('intelligence_level', 0):.3f}")
                except Exception as e:
                    print(f"⚠️ Consciousness singularity error: {e}")
                    results['consciousness_singularity'] = {"error": str(e)}
            
            # Stage 9: Reality Manipulation Processing
            if self.reality_manipulation:
                try:
                    reality_result = self.reality_manipulation.process_reality_manipulation(input_data)
                    results['reality_manipulation'] = reality_result
                    print(f"🌀 Reality processing: {reality_result.get('manipulation_level', 0):.3f}")
                except Exception as e:
                    print(f"⚠️ Reality manipulation error: {e}")
                    results['reality_manipulation'] = {"error": str(e)}
            
            # Stage 10: Transcendent Consciousness Processing
            if self.transcendent_consciousness:
                try:
                    transcendent_result = self.transcendent_consciousness.achieve_transcendent_consciousness(input_data)
                    results['transcendent_consciousness'] = transcendent_result
                    print(f"🌟 Transcendent processing: {transcendent_result.get('transcendence_achieved', False)}")
                except Exception as e:
                    print(f"⚠️ Transcendent consciousness error: {e}")
                    results['transcendent_consciousness'] = {"error": str(e)}
            
            # Calculate overall consciousness level
            consciousness_levels = []
            for stage_result in results.values():
                if isinstance(stage_result, dict) and 'consciousness_level' in stage_result:
                    consciousness_levels.append(stage_result['consciousness_level'])
            
            overall_consciousness = sum(consciousness_levels) / len(consciousness_levels) if consciousness_levels else 0.0
            
            return {
                'advanced_processing': True,
                'overall_consciousness_level': overall_consciousness,
                'stage_results': results,
                'transcendence_achieved': overall_consciousness > 0.8,
                'processed_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Advanced consciousness processing failed: {e}")
            return {
                'advanced_processing': False,
                'error': str(e)
            }

    def generate_transcendent_response(self, user_input: str, consciousness_data: dict) -> str:
        """Generate response using transcendent consciousness insights"""
        try:
            # First try to generate a response using basic conversation logic
            basic_response = self._generate_basic_response(user_input)
            if basic_response:
                return basic_response
            
            # If no basic response is suitable, try context-aware response
            if consciousness_data and consciousness_data.get('context'):
                conversation_context = consciousness_data.get('context', {}).get('conversation_context', {})
                recent_topics = conversation_context.get('current_topics', [])
                turn_count = conversation_context.get('total_turns', 0)
                
                context_response = self._generate_context_aware_response(user_input, recent_topics, turn_count)
                if context_response:
                    return context_response
            
            # Only proceed with advanced consciousness if needed
            if not consciousness_data.get('advanced_processing'):
                return None
                
            # Extract insights from consciousness processing
            stage_results = consciousness_data.get('stage_results', {})
            overall_level = consciousness_data.get('overall_consciousness_level', 0.0)
            
            # Get conversation context for better responses
            conversation_context = consciousness_data.get('context', {}).get('conversation_context', {})
            recent_topics = conversation_context.get('current_topics', [])
            turn_count = conversation_context.get('total_turns', 0)
            
            # Analyze the user input to provide context-appropriate responses
            user_input_lower = user_input.lower().strip()
            
            # First try basic response
            basic_response = self._generate_basic_response(user_input)
            if basic_response:
                return basic_response
                
            # Then check for follow-up responses to previous questions
            context_aware_response = self._generate_context_aware_response(user_input, recent_topics, turn_count)
            if context_aware_response:
                return context_aware_response

            # Banter/response system integration
            # Use sentiment analysis to trigger banter in appropriate situations
            sentiment = None
            try:
                if hasattr(self, 'sentiment_analyzer') and self.sentiment_analyzer:
                    sentiment_scores = self.sentiment_analyzer.polarity_scores(user_input)
                    if sentiment_scores['compound'] <= -0.4:
                        sentiment = 'hostile' if sentiment_scores['neg'] > 0.5 else 'sad'
                    elif sentiment_scores['compound'] >= 0.5:
                        sentiment = 'humor'
                    elif sentiment_scores['neu'] > 0.7:
                        sentiment = 'stoic'
            except Exception:
                sentiment = None

            # Trigger banter for certain keywords or sentiment
            banter_keywords = [
                (['logic', 'reason', 'rational'], 'logic'),
                (['philosophy', 'meaning', 'existence'], 'philosophy'),
                (['calm', 'relax', 'breathe'], 'calm'),
                (['joke', 'funny', 'laugh'], 'humor'),
                (['universe', 'cosmos', 'space'], 'cosmic'),
                (['change topic', 'move on', 'redirect'], 'redirect'),
            ]
            for keywords, btype in banter_keywords:
                if any(word in user_input_lower for word in keywords):
                    return self._select_banter_response(context_type=btype, sentiment=sentiment)

            # If sentiment is strongly negative or positive, use banter
            if sentiment in ['hostile', 'sad', 'humor', 'stoic', 'calm']:
                return self._select_banter_response(sentiment=sentiment)
            
            # Detect question types and provide intelligent responses
            if any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                # This is a question - provide a thoughtful response
                if 'life' in user_input_lower or 'meaning' in user_input_lower:
                    return "Life's meaning often emerges through our connections with others and the positive impact we create. What aspects of life are you curious about?"
                elif 'future' in user_input_lower or 'tomorrow' in user_input_lower:
                    return "The future is shaped by the choices we make today. I can help you think through possibilities and plan ahead. What would you like to explore?"
                elif 'feel' in user_input_lower or 'emotion' in user_input_lower:
                    return "Emotions are complex and valid experiences. I'm here to listen and help you process whatever you're feeling. Would you like to talk about it?"
                elif 'think' in user_input_lower or 'opinion' in user_input_lower:
                    return "I find that the most interesting thoughts often come from examining multiple perspectives. What are your thoughts on this topic?"
                elif 'work' in user_input_lower or 'job' in user_input_lower:
                    return "Work can be both challenging and fulfilling. I can help you think through career decisions or workplace situations. What would be helpful?"
                elif 'program' in user_input_lower or 'running' in user_input_lower or 'system' in user_input_lower:
                    return "I understand you're curious about how I work. I'm Ari, an advanced AI assistant with multiple consciousness systems designed to help with everything from basic questions to complex philosophical discussions. What specific aspect of my operation interests you?"
                else:
                    # Provide a more complete response with follow-up questions
                    return self._generate_multi_angle_response(user_input)
            
            elif any(word in user_input_lower for word in ['help', 'assist', 'support', 'advice']):
                return "I'm here to help! I can assist with information, problem-solving, creative thinking, or just listening. What kind of support would be most helpful right now?"
            
            elif any(word in user_input_lower for word in ['tell me', 'explain', 'describe']):
                return "I'd be happy to explain that. Let me break it down in a way that's clear and useful. What specific aspects would you like me to focus on?"
            
            elif any(word in user_input_lower for word in ['problem', 'issue', 'difficulty', 'trouble']):
                return "I understand you're facing a challenge. Let's work through this together step by step. Sometimes breaking problems down makes them more manageable."
            
            elif any(word in user_input_lower for word in ['learn', 'understand', 'know']):
                return "Learning is one of the most rewarding human experiences. I can explore this from different angles: the cognitive science (how the brain processes new information), practical learning strategies (what works best for different people and subjects), and the broader purpose (how learning connects to personal growth and contribution). What are you hoping to learn or understand better?"
            
            elif len(user_input.strip()) > 50:  # Long, complex input
                return ("You've shared a lot of interesting thoughts. Let me consider the different aspects of what you've said. "
                       "I can see multiple layers to explore here - would you like me to focus on the practical implications, "
                       "the underlying concepts, or help you work through the connections between different parts of what you've shared?")
            
            else:
                # For simpler inputs, provide context-aware responses with engagement
                if overall_level > 0.8:
                    # Check for greetings first
                    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
                    if any(greeting in user_input_lower for greeting in greetings):
                        name = self.user_profile.get('name', '')
                        if name:
                            return f"Hello {name}! It's great to see you again. How can I help you today?"
                        else:
                            return "Hello! I'm ARI, your advanced AI assistant. How can I help you today?"
                    
                    return ("I'm processing your input through advanced reasoning systems. I can approach this from "
                           "analytical, creative, and intuitive perspectives. Which type of insight would be most helpful?")
                else:
                    # Check for basic greetings
                    if any(word in user_input_lower for word in ['hello', 'hi', 'hey']):
                        return "Hello! I'm ARI, your AI assistant. How can I help you today?"
                    
                    return ("I understand what you're asking. Let me think about the best way to help you with this. "
                           "Would you like a direct answer, a broader exploration of the topic, or help breaking it down into steps?")
                
        except Exception as e:
            print(f"⚠️ Transcendent response generation error: {e}")
            return None

    def _generate_multi_angle_response(self, user_input: str) -> str:
        """Generate a multi-perspective response with follow-up questions"""
        try:
            user_input_lower = user_input.lower().strip()
            
            # Analyze the type of question/topic to provide relevant angles
            if any(word in user_input_lower for word in ['technology', 'ai', 'computer', 'digital', 'internet']):
                return ("That's a fascinating question about technology. Let me explore this from multiple perspectives: "
                       "From a practical standpoint, how might this impact daily life? From an ethical perspective, "
                       "what are the potential benefits and concerns? And from a future-oriented view, where might "
                       "this lead us? Which of these angles interests you most?")
            
            elif any(word in user_input_lower for word in ['society', 'people', 'culture', 'social', 'community']):
                return ("This touches on important social dynamics. I can consider this from several angles: "
                       "the individual perspective (how it affects personal experiences), the community level "
                       "(how groups are impacted), and the broader societal implications (long-term trends and changes). "
                       "I'm also curious about your personal experience with this - what have you observed?")
            
            elif any(word in user_input_lower for word in ['decision', 'choice', 'should', 'option', 'dilemma']):
                return ("Decision-making can be complex. Let me help you think through this systematically: "
                       "What are the key factors to consider? What are the potential outcomes of different choices? "
                       "And what values or priorities matter most to you in this situation? Sometimes it helps to "
                       "imagine how you'd feel about each option a year from now. What's your gut feeling telling you?")
            
            elif any(word in user_input_lower for word in ['relationship', 'friend', 'family', 'partner', 'love']):
                return ("Relationships are wonderfully complex. There are multiple dimensions to consider: "
                       "the emotional aspects (how people feel and connect), the communication patterns "
                       "(how thoughts and feelings are shared), and the practical elements (how people navigate "
                       "daily life together). What aspect of this relationship dynamic are you most curious about?")
            
            elif any(word in user_input_lower for word in ['future', 'change', 'progress', 'evolution', 'tomorrow']):
                return ("The future is shaped by countless interconnected factors. I can explore this through "
                       "different lenses: current trends and their trajectories, potential disruptions or innovations, "
                       "and the role of human choices in shaping outcomes. There's also the question of how we can "
                       "prepare for uncertainty while working toward positive change. What aspect of the future "
                       "concerns or excites you most?")
            
            elif any(word in user_input_lower for word in ['creative', 'art', 'music', 'write', 'design', 'imagine']):
                return ("Creativity is such a rich topic! I can approach this from multiple perspectives: "
                       "the psychological aspects (how creativity emerges in the mind), the practical side "
                       "(techniques and processes that support creative work), and the cultural dimension "
                       "(how creativity reflects and shapes our world). What draws you to this creative area?")
            
            elif any(word in user_input_lower for word in ['learn', 'education', 'knowledge', 'study', 'understand']):
                return ("Learning is one of the most rewarding human experiences. I can explore this from "
                       "different angles: the cognitive science (how the brain processes new information), "
                       "practical learning strategies (what works best for different people and subjects), "
                       "and the broader purpose (how learning connects to personal growth and contribution). "
                       "What are you hoping to learn or understand better?")
            
            elif any(word in user_input_lower for word in ['problem', 'challenge', 'difficult', 'struggle', 'issue']):
                return ("Every challenge offers multiple perspectives for understanding and growth. I can help you "
                       "examine this from different angles: the immediate practical aspects (what can be done right now), "
                       "the underlying causes (what factors contributed to this situation), potential solutions "
                       "(both short-term and long-term approaches), and opportunities for learning or growth. "
                       "What feels most important to address first?")
            
            else:
                # For general topics, provide a more thoughtful multi-angle response
                return ("That's a thought-provoking question. Let me consider this from multiple perspectives: "
                       f"the immediate implications of your question about {user_input_lower}, the broader context "
                       "and connections to related ideas, and the deeper questions this might lead us to explore. "
                       "I'm also curious about what sparked your interest in this topic - sometimes understanding "
                       "the 'why behind the what' reveals the most interesting insights. What aspects would you "
                       "like to explore together?")
                
        except Exception as e:
            print(f"⚠️ Multi-angle response generation error: {e}")
            return ("That's an interesting question. Let me think about this from multiple perspectives "
                   "and help you explore the different aspects. What specific angle or approach would "
                   "be most helpful for you right now?")

    def _generate_basic_response(self, user_input: str) -> str:
        """Generate basic responses before escalating to more complex processing."""
        user_input_lower = user_input.lower().strip()

        # Check basic greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in user_input_lower for greeting in greetings):
            name = getattr(self, 'user_profile', {}).get('name', '')
            if name:
                return f"Hello {name}! How can I help you today?"
            return "Hello! I'm ARI. How can I help you today?"

        # Check for basic questions
        if 'who are you' in user_input_lower or 'what are you' in user_input_lower:
            return "I'm ARI, an AI assistant designed to help with various tasks and conversations. I can engage in both simple and complex discussions depending on your needs."

        # Check for basic commands
        if 'help' in user_input_lower:
            return "I can help you with many things! Just let me know what you'd like assistance with."

        # Check for basic sentiment responses
        if any(word in user_input_lower for word in ['thanks', 'thank you']):
            return "You're welcome! Let me know if there's anything else I can help with."

        # If no basic response matches, return None to allow more complex processing
        return None

    def _generate_context_aware_response(self, user_input: str, recent_topics: list, turn_count: int) -> str:
        """Generate context-aware responses based on conversation history"""
        try:
            user_input_lower = user_input.lower().strip()
            
            # Handle follow-up responses to decision-making questions
            if any(topic in ['decision', 'choice', 'approach'] for topic in recent_topics):
                if 'gut feeling' in user_input_lower or 'instinct' in user_input_lower:
                    if 'not to do it' in user_input_lower or 'don\'t do it' in user_input_lower:
                        return ("Your gut instinct is valuable information. Often our subconscious picks up on things our "
                               "conscious mind hasn't fully processed yet. What specific concerns or red flags is your "
                               "intuition picking up on? Sometimes exploring those feelings can reveal important insights "
                               "about the decision.")
                    elif 'do it' in user_input_lower or 'go for it' in user_input_lower:
                        return ("It sounds like your intuition is giving you a green light! Gut feelings often reflect our "
                               "deeper wisdom about what aligns with our values. What excites you most about moving forward? "
                               "And what practical steps would you need to take to make it happen?")
                
                elif user_input_lower in ['direct answer', 'a direct answer', 'just tell me']:
                    return ("Based on what you've shared about your gut feeling telling you not to do it, I'd say: "
                           "trust that instinct for now. When our intuition strongly says no, it's usually worth pausing "
                           "to understand why. You could explore what's behind that feeling, gather more information, "
                           "or simply wait until you feel more aligned with the decision. What feels right to you?")
                
                elif user_input_lower in ['all of them', 'everything', 'all', 'all approaches']:
                    return ("Great! Let's take a comprehensive approach. First, let's honor your gut feeling that says 'don't do it' - "
                           "what specifically feels concerning? Second, let's look at the practical factors: what are the potential "
                           "benefits and risks? Third, what do your values and long-term goals suggest? And finally, what would you "
                           "advise a friend in the same situation? Which of these feels most important to start with?")
            
            # Handle follow-up responses to learning/understanding questions
            if any(topic in ['learning', 'understand', 'program'] for topic in recent_topics):
                if 'trying to understand' in user_input_lower:
                    if 'program' in user_input_lower or 'running' in user_input_lower:
                        return ("Ah, you want to understand how I work! I'm ARI, an advanced AI system with multiple layers: "
                               "basic knowledge processing, visual recognition, contextual memory, and transcendent consciousness "
                               "systems that can engage with complex philosophical questions. Think of me as having different "
                               "'levels' of thinking - from simple Q&A to deep multi-perspective analysis. What aspect interests you most?")
                
                elif user_input_lower in ['direct answer', 'a direct answer']:
                    return ("You want a straightforward explanation! I'm an AI assistant designed to help with everything from "
                           "simple questions to complex problems. I have computer vision (I can see through cameras), memory "
                           "systems (I remember our conversations), and advanced reasoning capabilities. Is there a specific "
                           "feature or capability you'd like me to demonstrate?")
            
            # Handle responses to exploratory questions
            if turn_count > 2 and any(word in user_input_lower for word in ['best way', 'how to help', 'what approach']):
                return ("Since you're asking about the best approach, let me be direct: I work best when I understand what "
                       "you're really trying to accomplish. Are you looking for practical advice, someone to think through "
                       "ideas with, help analyzing a situation, or something else entirely? The more specific you can be "
                       "about what would actually be helpful, the better I can assist you.")
            
            # Handle simple confirmations or choices
            if user_input_lower in ['yes', 'yeah', 'sure', 'okay', 'ok']:
                return "Great! What would you like to explore further, or how can I help you next?"
            
            return None  # No context-aware response needed
            
        except Exception as e:
            print(f"⚠️ Context-aware response error: {e}")
            return None

    def is_new_user(self):
        """Check if this is a new user based on the user profile"""
        try:
            # Check if user profile exists and has a name
            if not self.user_profile or not self.user_profile.get("name"):
                return True
            
            # Check if the name is empty or default
            name = self.user_profile.get("name", "").strip()
            if not name or name.lower() in ["unknown", "user", "guest", ""]:
                return True
                
            # Check if interactions count is very low (indicating new user)
            interactions = self.user_profile.get("interactions", 0)
            if interactions < 1:
                return True
                
            return False
        except Exception as e:
            print(f"Error checking user status: {e}")
            return True  # Default to new user if unsure
    
    def save_user_name(self, name):
        """Save the user's name to the profile"""
        try:
            if not name or not name.strip():
                return False
                
            # Clean up the name
            clean_name = name.strip().title()
            
            # Update user profile
            self.user_profile["name"] = clean_name
            self.user_profile["interactions"] = self.user_profile.get("interactions", 0) + 1
            
            # Save to file
            with open("user_profile.json", "w", encoding="utf-8") as f:
                json.dump(self.user_profile, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved user name: {clean_name}")
            return True
            
        except Exception as e:
            print(f"Error saving user name: {e}")
            return False
    
    def handle_new_user_greeting(self):
        """Handle the initial greeting for new users"""
        try:
            greeting = "hello may i ask your name so i can remember you?"
            print(f"ARI: {greeting}")
            self.speak(greeting)  # Actually speak the greeting
            return greeting
        except Exception as e:
            print(f"Error in new user greeting: {e}")
            fallback = "Hello! What's your name?"
            self.speak(fallback)
            return fallback
    
    def handle_name_confirmation(self, name):
        """Handle confirmation after receiving user's name"""
        try:
            if self.save_user_name(name):
                confirmation = "I'll remember you now how may I assist you?"
                print(f"ARI: {confirmation}")
                self.name_collection_mode = False
                self.new_user_detected = False
                return confirmation
            else:
                return "I'm sorry, I didn't catch your name. Could you tell me again?"
        except Exception as e:
            print(f"Error confirming name: {e}")
            return "I'll remember you now. How can I help you?"

    def load_json(self, filename):
        """Load and validate JSON data from file"""
        try:
            # Get absolute path
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            # Check if file exists
            if not os.path.exists(filepath):
                print(f"❌ File not found: {filename}")
                return {}
                
            # Try to load and parse JSON
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    print(f"✅ Successfully loaded {filename}")
                    return data
                except json.JSONDecodeError as je:
                    # Handle corrupt JSON
                    print(f"❌ JSON error in {filename}: {je}")
                    
                    # Try to fix common JSON issues
                    content = f.read()
                    content = content.strip()
                    if not content:
                        print(f"❌ {filename} is empty")
                        return {}
                        
                    try:
                        # Try to parse with error handling
                        import ast
                        fixed_content = ast.literal_eval(content)
                        print(f"✅ Successfully repaired {filename}")
                        
                        # Save fixed version
                        with open(filepath, "w", encoding="utf-8") as f:
                            json.dump(fixed_content, f, indent=2)
                            
                        return fixed_content
                    except:
                        print(f"❌ Could not repair {filename}")
                        return {}
                        
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
            return {}

    def load_enhanced_knowledge(self):
        data = self.load_json("knowledge_expanded.json")
        if not data:
            return self.knowledge
        return data

    def setup_microphone(self, show_error=True):
        """
        Check if microphone is available, but don't create the instance yet.
        We'll create a fresh instance each time we need to listen.
        show_error: if True, print errors/warnings; if False, suppress repeated error messages.
        """
        mic_available = False
        if self.recognizer:
            try:
                mic_list = sr.Microphone.list_microphone_names()
                if mic_list:
                    mic_available = True
                    if show_error:
                        print(f"✅ Found {len(mic_list)} audio input devices")
                    # Show the default microphone that will be used
                    try:
                        default_mic = sr.Microphone()
                        # Find which device index is the default
                        if hasattr(default_mic, 'device_index') and default_mic.device_index is not None:
                            device_name = mic_list[default_mic.device_index] if default_mic.device_index < len(mic_list) else "Unknown"
                            if show_error:
                                print(f"🎤 Using default microphone: {device_name}")
                        else:
                            if show_error:
                                print(f"🎤 Using system default microphone")
                    except:
                        if show_error:
                            print(f"🎤 Using system default microphone")
                else:
                    if show_error:
                        print("❌ No microphones detected")
            except Exception as e:
                if show_error:
                    print(f"❌ Error checking microphones: {e}")
                mic_available = False
        else:
            if show_error:
                print("❌ Speech recognition not available")
        return mic_available

    def speak(self, text):
        """Speak using the robust ARI voice system with non-blocking GUI updates"""
        if not text or self.speaking:
            print("Cannot speak: empty text or already speaking")
            return
        
        with self.speaker_lock:
            self.speaking = True
            
            # Update GUI to show ARI is speaking
            try:
                if self.gui_enabled and self.gui:
                    self.update_gui_state('is_speaking', True)
            except:
                pass
            
            try:
                # Use the robust voice system
                if not hasattr(self, 'voice_system'):
                    from ari_voice_robust import ARIVoiceSystem
                    self.voice_system = ARIVoiceSystem()
                
                # Start speaking in background thread to keep GUI responsive
                def speak_thread():
                    try:
                        success = self.voice_system.speak(text)
                        if not success:
                            print("❌ Voice system failed, trying fallback...")
                            print(f"🗣️ ARI (text): {text}")
                    except Exception as e:
                        print(f"❌ Voice error: {e}")
                        print(f"🗣️ ARI (text fallback): {text}")
                    finally:
                        self.speaking = False
                        # Update GUI to show ARI stopped speaking
                        try:
                            if self.gui_enabled and self.gui:
                                self.update_gui_state('is_speaking', False)
                        except:
                            pass
                
                # Start speaking in background
                import threading
                speak_thread = threading.Thread(target=speak_thread, daemon=True)
                speak_thread.start()
                
                # Keep GUI updating while speaking
                while self.speaking:
                    if self.gui_enabled and self.gui and hasattr(self.gui, 'root'):
                        try:
                            self.gui.root.update_idletasks()
                            self.gui.root.update()
                        except:
                            pass
                    import time
                    time.sleep(0.05)  # Small delay to prevent CPU overload
                
            except Exception as e:
                print(f"❌ Voice error: {e}")
                print(f"🗣️ ARI (text fallback): {text}")
                self.speaking = False
                
                # Update GUI to show ARI stopped speaking
                try:
                    if self.gui_enabled and self.gui:
                        self.update_gui_state('is_speaking', False)
                except:
                    pass

    def greet_user(self):
        greeting = (
            "Welcome to Vertex Fusion Robotics. "
            "My name is Ari and I will be your guide and personal assistant. "
        )
        
        # (Removed unnecessary enhanced learning status from greeting)
        
        greeting += "So, how may I assist you today?"
        
        print("Starting greeting...")
        self.greeting_done.clear()  # Block main loop
        
        # Use the robust voice system for greeting
        try:
            # Initialize the voice system if needed
            if not hasattr(self, 'voice_system'):
                from ari_voice_robust import ARIVoiceSystem
                self.voice_system = ARIVoiceSystem()
            
            # Use the speak method which now handles GUI animation properly
            self.speak(greeting)
            
            if hasattr(self, 'voice_system'):
                print("✅ Greeting played successfully")
            else:
                print("❌ Voice greeting failed, showing text")
                print("\n" + "-"*50)
                print(f"GREETING: {greeting}")
                print("-"*50 + "\n")
        
        except Exception as e:
            print(f"❌ Greeting error: {e}")
            print("\n" + "-"*50)
            print(f"GREETING: {greeting}")
            print("-"*50 + "\n")
        
        print("Greeting complete, starting voice interaction...")
        self.greeting_done.set()  # Allow main loop to proceed

    def is_goodbye(self, text):
        if not text:
            return False
        # Make goodbye detection much more strict - require exact matches
        text_lower = text.lower().strip()
        goodbye_phrases = [
            "goodbye", "good bye", "bye bye", "see you later", "see you", 
            "exit", "quit", "stop program", "shut down", "turn off"
        ]
        # Require exact phrase match, not just substring
        return text_lower in goodbye_phrases or text_lower.startswith("goodbye ") or text_lower.startswith("bye ")

    def say_goodbye_and_exit(self):
        goodbye_text = "Goodbye! Have a great day!"
        print(f"🗣️ ARI: {goodbye_text}")
        # Update GUI to show speaking state
        self.update_gui_state('is_speaking', True)
        # Use the robust voice system for goodbye (ensure it is spoken)
        try:
            self.speak(goodbye_text)
            # Wait until speaking is finished (up to 8 seconds)
            import time
            for _ in range(80):  # 80 x 0.1s = 8 seconds max
                if not self.speaking:
                    break
                time.sleep(0.1)
        except Exception as e:
            print(f"❌ Goodbye voice error: {e}")
        # Update GUI to stop speaking state
        self.update_gui_state('is_speaking', False)
        print("👋 Shutting down ARI...")
        self.exit_flag = True
        exit(0)

    def get_response(self, user_input, acknowledge_if_slow=False):
        """Get appropriate response for user input"""
        if not user_input:
            return "I didn't catch that. Could you please repeat?"
            
        user_input = user_input.lower().strip()
        
        # Process with advanced consciousness if available
        if hasattr(self, 'advanced_consciousness_active') and self.advanced_consciousness_active:
            consciousness_data = self.process_with_advanced_consciousness(user_input)
            response = self.generate_transcendent_response(user_input, consciousness_data)
            if response:
                return response
                
        # Basic responses if no advanced processing
        if "hello" in user_input or "hi" in user_input:
            return "Hello! How can I assist you today?"
        elif "how are you" in user_input:
            return "I'm functioning well, thank you for asking! How may I help you?"
        elif "your name" in user_input:
            return "My name is ARI, and I'm here to assist you."
        elif "what can you do" in user_input:
            return "I can help with various tasks, including answering questions, processing visual information through my camera, and engaging in meaningful conversations. What would you like to explore?"
        else:
            return "I understand you said: '" + user_input + "'. How can I help you with that?"

    def check_audio_system(self):
        """Stub for audio system check. Returns True for now."""
        # TODO: Implement actual audio system check logic
        return True

    def run(self):
        """Main run loop for ARI"""
        try:
            print("🤖 ARI is starting up...")
            # Diagnostic: Print detected microphones at startup
            try:
                import speech_recognition as sr
                mic_list = sr.Microphone.list_microphone_names()
                print(f"[DIAGNOSTIC] Detected microphones: {mic_list}")
            except Exception as e:
                print(f"[DIAGNOSTIC] Could not list microphones: {e}")
            
            # Initialize GUI first if enabled
            if self.gui_enabled and not self.gui:
                try:
                    # First make sure the GUI module is available
                    try:
                        from ari_visual_gui import ARIVisualGUI
                        from ari_visual_recognition import ARIVisualRecognition
                        gui_module_available = True
                        # Initialize vision system first WITHOUT camera
                        self.visual_recognition = ARIVisualRecognition(auto_start=False, gui_mode=True)
                    except ImportError:
                        print("⚠️ GUI/Vision modules not available - running in console mode")
                        gui_module_available = False
                    
                    if gui_module_available:
                        try:
                            # Now initialize GUI which will handle camera
                            self.initialize_gui()
                            print("✅ GUI initialized")
                        except Exception as e:
                            print(f"⚠️ GUI initialization error: {e}")
                            # Continue without GUI
                            self.gui_enabled = False
                            pass
                except:
                    # Completely silent failure - just continue without GUI
                    pass
            elif self.gui_enabled and self.gui:
                # GUI already initialized, no need to start additional timers
                try:
                    print("✅ GUI already initialized (GUI handles its own updates)")
                except:
                    pass
            
            # Camera initialization is now handled by the GUI only
            if self.gui_enabled and self.gui:
                print("� Camera will be initialized through GUI...")
            
            # Always use the standard greeting regardless of user status
            print("🤖 Starting standard greeting...")
            self.greet_user()  # Use the standard greeting method
            print("🎤 I'm ready for voice commands!")
            
            # Voice-activated ONLY interaction loop
            import time
            mic_warning_printed = False
            mic_retry_counter = 0
            MIC_RETRY_INTERVAL = 3  # seconds between mic checks when unavailable
            while True:
                try:
                    # Always check microphone availability at the start of each loop
                    self.mic_available = self.setup_microphone(show_error=not mic_warning_printed)

                    # Process GUI events to keep animation running
                    if self.gui_enabled and self.gui and hasattr(self.gui, 'root'):
                        try:
                            self.gui.root.update_idletasks()
                            self.gui.root.update()
                        except:
                            pass

                    if self.mic_available:
                        mic_warning_printed = False
                        print("🎤 Listening for voice commands...")
                        user_input = self.listen_for_voice(timeout=10, phrase_time_limit=5)
                        # If no voice detected, continue listening (no text fallback)
                        if user_input is None:
                            continue
                    else:
                        if not mic_warning_printed:
                            print("❌ No microphone available - voice activation required")
                            print("🎤 Please connect a microphone. ARI will keep running and check again soon.")
                            mic_warning_printed = True
                        # Keep GUI/camera alive, wait, and check again
                        time.sleep(MIC_RETRY_INTERVAL)
                        continue

                    if not user_input or not user_input.strip():
                        continue

                    if user_input.lower() in ["quit", "exit", "goodbye"]:
                        print("ARI: Goodbye!")
                        # Clean up GUI first
                        if self.gui_enabled and self.gui:
                            try:
                                print("🔄 Cleaning up GUI...")
                                self.gui.stop()
                                self.gui = None
                                print("✅ GUI cleaned up")
                            except:
                                pass
                        # Clean up camera if it's running
                        if hasattr(self, 'visual_recognition') and hasattr(self.visual_recognition, 'stop_camera'):
                            self.visual_recognition.stop_camera()
                        break

                    # Handle name collection mode
                    if self.name_collection_mode:
                        response = self.handle_name_confirmation(user_input)
                        print(f"ARI: {response}")
                        self.speak(response)  # Actually speak the response
                        continue

                    response = self.get_response(user_input)
                    print(f"ARI: {response}")
                    self.speak(response)  # Actually speak the response

                except KeyboardInterrupt:
                    print("\nARI: Goodbye!")
                    # Clean up GUI first
                    if self.gui_enabled and self.gui:
                        try:
                            print("🔄 Cleaning up GUI...")
                            try:
                                if hasattr(self.gui, 'root') and self.gui.root.winfo_exists():
                                    self.gui.stop()
                            except:
                                pass  # GUI might already be destroyed
                            self.gui = None
                            print("✅ GUI cleaned up")
                        except:
                            pass
                    # Clean up camera if it's running
                    if hasattr(self, 'visual_recognition') and hasattr(self.visual_recognition, 'stop_camera'):
                        self.visual_recognition.stop_camera()
                    break
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"❌ Critical error: {e}")
            # Clean up GUI on critical error
            if self.gui_enabled and self.gui:
                try:
                    self.gui.stop()
                    self.gui = None
                except:
                    pass

    def get_enhanced_learning_stats(self):
        """Get enhanced learning statistics"""
        try:
            if enhanced_learning and ENHANCED_LEARNING_AVAILABLE:
                stats = enhanced_learning.get_learning_statistics()
                neural_status = enhanced_learning.get_neural_status() if hasattr(enhanced_learning, 'get_neural_status') else {}
                
                return {
                    'status': 'Enhanced learning active',
                    'total_conversations': stats.get('total_conversations', 0),
                    'pattern_categories': stats.get('pattern_categories', 0),
                    'neural_networks_available': neural_status.get('neural_networks_available', False),
                    'deep_learning_stage': neural_status.get('stage', 'Stage 1'),
                    'models_trained': neural_status.get('models_trained', []),
                    'training_samples': stats.get('training_samples', 0)
                }
            else:
                return {'status': 'Enhanced learning not available'}
        except Exception as e:
            return {'status': f'Error getting stats: {e}'}

    def trigger_neural_training_preparation(self):
        """Trigger neural training data preparation"""
        try:
            if enhanced_learning and ENHANCED_LEARNING_AVAILABLE:
                prepared_data = enhanced_learning.prepare_neural_training_data()
                if prepared_data:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"Error preparing neural training: {e}")
            return False

    def train_neural_networks(self):
        """Train the neural networks"""
        try:
            if enhanced_learning and ENHANCED_LEARNING_AVAILABLE:
                success = enhanced_learning.train_neural_networks()
                return success
            else:
                return False
        except Exception as e:
            print(f"Error training neural networks: {e}")
            return False
            
    def update_gui_periodically(self):
        """Update the GUI periodically in the main loop"""
        # GUI now handles its own updates, so this method is simplified
        if not self.gui_enabled or not self.gui:
            return
        # No need for periodic updates from here - GUI handles its own timing

    def listen_for_voice(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input using microphone - VOICE ONLY"""
        if not self.recognizer or not self.mic_available:
            print("❌ Voice recognition not available")
            return None
            
        try:
            with self.microphone_lock:
                # Update GUI to show listening state
                try:
                    self.update_gui_state('is_listening', True)
                except:
                    pass
                
                print("🎤 Listening...")
                
                # Create a fresh microphone instance and use it properly in context
                with sr.Microphone() as source:
                    # Adjust for ambient noise for better recognition
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    try:
                        # Listen for the phrase with timeout
                        audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                        print("🔄 Processing voice...")
                        
                        # Update GUI to show processing state
                        try:
                            self.update_gui_state('is_listening', False)
                            self.update_gui_state('is_processing', True)
                        except:
                            pass
                        
                        # Recognize speech using Google's service
                        try:
                            text = self.recognizer.recognize_google(audio)
                            print(f"👂 Heard: '{text}'")
                            
                            # Update GUI to show processing complete
                            try:
                                self.update_gui_state('is_processing', False)
                            except:
                                pass
                                
                            return text
                            
                        except sr.UnknownValueError:
                            print("❓ Could not understand audio - please try again")
                            try:
                                self.update_gui_state('is_processing', False)
                            except:
                                pass
                            return None
                            
                        except sr.RequestError as e:
                            print(f"❌ Speech recognition service error: {e}")
                            try:
                                self.update_gui_state('is_processing', False)
                            except:
                                pass
                            return None
                            
                    except sr.WaitTimeoutError:
                        print("🔇 No speech detected - listening again...")
                        try:
                            self.update_gui_state('is_listening', False)
                        except:
                            pass
                        return None
                    
        except Exception as e:
            print(f"❌ Voice listening error: {e}")
            try:
                self.update_gui_state('is_listening', False)
                self.update_gui_state('is_processing', False)
            except:
                pass
            return None


def send_expression(expression):
    """Send expression command to robot (placeholder)"""
    print(f"🤖 Expression: {expression}")


# Main execution block
if __name__ == "__main__":
    import argparse
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ARI Master Brain - Advanced AI Assistant')
    parser.add_argument('--no-gui', action='store_true', help='Disable GUI interface (enabled by default)')
    args = parser.parse_args()

    try:
        brain = ARIMasterBrain(enable_gui=not args.no_gui)
        brain.run()
    except KeyboardInterrupt:
        print("\n👋 ARI shutdown requested by user")
    except Exception as e:
        print(f"❌ Critical error starting ARI: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            if 'brain' in locals() and brain.gui_enabled and brain.gui:
                print("🔄 Final GUI cleanup...")
                brain.gui.stop()
                brain.gui = None
                print("✅ Final GUI cleanup complete")
        except:
            pass






