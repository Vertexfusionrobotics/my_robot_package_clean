# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Voice-Enabled Stage 3: Advanced Neural Intelligence with Voice Input/Output
Full integration of speech recognition, text-to-speech, and Stage 3 neural capabilities.
"""

import sys
import os
import asyncio
import tempfile
import pygame
import time
import json
import random
from datetime import datetime

# Voice modules
try:
    import speech_recognition as sr
    import edge_tts
except ImportError as e:
    print(f"Missing voice dependencies: {e}")
    print("Please install: pip install SpeechRecognition edge-tts pygame")
    sys.exit(1)

# Import Stage 3 neural components
try:
    from ari_master_brain_stage_3 import ARIMasterBrainStage3
    from ari_generative_networks import GenerativeNetworks
except ImportError as e:
    print(f"Stage 3 modules not found: {e}")
    print("Please ensure Stage 3 is properly set up.")
    sys.exit(1)

class ARIVoiceStage3:
    """Voice-enabled ARI with Stage 3 neural capabilities"""
    
    def __init__(self):
        print("🧠 Initializing ARI Voice Stage 3...")
        
        # Initialize neural brain
        self.brain = ARIMasterBrainStage3()
        
        # Voice components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # TTS settings
        self.voice = "en-GB-SoniaNeural"  # Microsoft Sonia
        
        # Audio initialization
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            print("🔊 Audio system initialized")
        except Exception as e:
            print(f"⚠️ Audio initialization warning: {e}")
        
        # Conversation state
        self.conversation_active = False
        self.last_interaction_time = None
        
        print("✅ ARI Voice Stage 3 ready!")
        
    def listen_for_speech(self, timeout=5, phrase_time_limit=10):
        """Listen for speech input with timeout"""
        try:
            with self.microphone as source:
                print("🎙️ Listening... (say something)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: \"{text}\"")
            return text.strip()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand speech")
            return "unclear"
        except sr.RequestError as e:
            print(f"⚠️ Speech service error: {e}")
            return "error"
    
    async def speak_text(self, text):
        """Convert text to speech and play it"""
        if not text or not text.strip():
            return
            
        print(f"🤖 ARI: \"{text}\"")
        
        try:
            # Create temporary file for TTS
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
                tts_path = tf.name
            
            # Generate TTS
            communicate = edge_tts.Communicate(text, voice=self.voice)
            await communicate.save(tts_path)
            
            # Play audio
            if os.path.exists(tts_path) and os.path.getsize(tts_path) > 0:
                try:
                    pygame.mixer.music.load(tts_path)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to complete
                    start_time = time.time()
                    while pygame.mixer.music.get_busy() and time.time() - start_time < 30:
                        await asyncio.sleep(0.1)
                    
                    pygame.mixer.music.unload()
                except Exception as e:
                    print(f"⚠️ Audio playback error: {e}")
            
            # Cleanup
            try:
                os.unlink(tts_path)
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ TTS error: {e}")
    
    def detect_wake_word(self, text):
        """Check if text contains wake words"""
        if not text or text in ["unclear", "error"]:
            return False
            
        wake_words = ["ari", "hey ari", "hello ari", "hi ari"]
        text_lower = text.lower()
        
        for wake_word in wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def detect_goodbye(self, text):
        """Check if text contains goodbye phrases"""
        if not text or text in ["unclear", "error"]:
            return False
            
        goodbye_words = ["goodbye", "bye", "see you later", "talk to you later", 
                        "that's all", "stop listening", "end conversation"]
        text_lower = text.lower()
        
        for goodbye in goodbye_words:
            if goodbye in text_lower:
                return True
        return False
    
    async def start_conversation_loop(self):
        """Main conversation loop with voice interaction"""
        print("\n🎤 ARI Voice Stage 3 is ready!")
        print("💡 Say 'Hey ARI' or 'ARI' to start a conversation")
        print("💡 Say 'goodbye' or 'bye' to end a conversation")
        print("💡 Press Ctrl+C to exit completely\n")
        
        await self.speak_text("Hello! I'm ARI with advanced neural intelligence. Say Hey ARI to start talking with me.")
        
        while True:
            try:
                if not self.conversation_active:
                    # Wait for wake word
                    print("😴 Waiting for wake word...")
                    text = self.listen_for_speech(timeout=10)
                    
                    if text and self.detect_wake_word(text):
                        self.conversation_active = True
                        self.last_interaction_time = datetime.now()
                        
                        # Process the wake phrase (might contain a question)
                        wake_response = await self.process_wake_input(text)
                        await self.speak_text(wake_response)
                        
                        print("🗣️ Conversation started! Ask me anything...")
                        continue
                
                else:
                    # Active conversation
                    text = self.listen_for_speech(timeout=15)
                    
                    if text is None:
                        # Timeout - check if conversation should end
                        time_since_last = (datetime.now() - self.last_interaction_time).seconds
                        if time_since_last > 30:
                            await self.speak_text("I'll go back to waiting mode now. Say Hey ARI when you want to talk again.")
                            self.conversation_active = False
                            continue
                        else:
                            await self.speak_text("I'm still here. What would you like to talk about?")
                            continue
                    
                    if text in ["unclear", "error"]:
                        await self.speak_text("I didn't catch that. Could you try again?")
                        continue
                    
                    if self.detect_goodbye(text):
                        await self.speak_text("Goodbye! Say Hey ARI when you want to talk again.")
                        self.conversation_active = False
                        continue
                    
                    # Process normal conversation
                    self.last_interaction_time = datetime.now()
                    response = await self.process_conversation_input(text)
                    await self.speak_text(response)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down ARI Voice Stage 3...")
                await self.speak_text("Goodbye! It was nice talking with you.")
                break
            except Exception as e:
                print(f"⚠️ Error in conversation loop: {e}")
                await asyncio.sleep(1)
    
    async def process_wake_input(self, text):
        """Process input that contains wake word"""
        # Remove wake word and process remainder
        text_lower = text.lower()
        for wake_word in ["hey ari", "hello ari", "hi ari", "ari"]:
            if wake_word in text_lower:
                remaining = text_lower.replace(wake_word, "").strip()
                if remaining and len(remaining) > 2:
                    # There's a question after the wake word
                    return await self.process_conversation_input(remaining)
                break
        
        # Just a wake word
        greetings = [
            "Hi there! I'm ready to help with my advanced neural capabilities.",
            "Hello! What would you like to explore today?",
            "Hi! I'm ARI with enhanced neural intelligence. What can I help you with?",
            "Hey! Ready to chat. What's on your mind?",
            "Hello! My neural networks are ready to assist you."
        ]
        return random.choice(greetings)
    
    async def process_conversation_input(self, text):
        """Process conversation input using Stage 3 neural capabilities"""
        try:
            # Use the Stage 3 brain to process input
            response = self.brain.process_input(text)
            
            # Ensure we have a good response
            if not response or response.strip() == "":
                response = "I'm processing that. Could you tell me more?"
            
            return response
            
        except Exception as e:
            print(f"⚠️ Error processing input: {e}")
            return "I'm having trouble processing that right now. Could you try rephrasing?"
    
    def get_voice_commands_help(self):
        """Get help text for voice commands"""
        return """Voice Commands Available:
        
🎤 General:
- "Hey ARI" / "ARI" - Start conversation
- "Goodbye" / "Bye" - End conversation
        
🧠 Neural Features:
- "How am I feeling?" - Emotion detection
- "Generate a creative response about [topic]" - Generative AI
- "What do you remember about me?" - Personalization
- "Learn that I like [something]" - Learning
        
💭 Conversation:
- Ask any question or make statements
- ARI will use advanced neural processing to respond
        
⚙️ System:
- "Help" / "What can you do?" - Show capabilities
"""

async def main():
    """Main function to run ARI Voice Stage 3"""
    try:
        ari = ARIVoiceStage3()
        await ari.start_conversation_loop()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting ARI Voice Stage 3: {e}")
        print("Please ensure all dependencies are installed and Stage 3 is set up properly.")

if __name__ == "__main__":
    asyncio.run(main())
