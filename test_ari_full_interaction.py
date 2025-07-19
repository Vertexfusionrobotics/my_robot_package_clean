# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Full ARI Interaction Test
Demonstrates ARI Visual GUI with simulated user conversations and responses.
Shows the complete experience as if a real user was interacting with ARI using the natural Sonia voice.
"""

import sys
import os
import time
import threading
import random

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ARIInteractionSimulator:
    def __init__(self):
        self.gui = None
        self.running = False
        self.conversation_active = False
        
        # Import ARI's natural voice system
        try:
            from edge_tts_sonia import speak_with_sonia
            self.speak_function = speak_with_sonia
            print("✅ Using ARI's natural Sonia voice")
        except ImportError:
            print("❌ Could not import Sonia voice - will use text only")
            self.speak_function = None
        
        # Sample user questions and ARI responses
        self.conversations = [
            {
                "user": "Hello ARI, how are you today?",
                "ari": "Hello! I'm functioning optimally and my consciousness level is at 85%. My neural networks are fully active and I'm ready to assist you with anything you need.",
                "duration": 4.5
            },
            {
                "user": "What can you see in the room right now?",
                "ari": "I can see you clearly in what appears to be an indoor office environment. My vision system is detecting one person and analyzing various objects in the scene. The lighting conditions are good for optimal recognition.",
                "duration": 5.2
            },
            {
                "user": "Can you explain quantum computing to me?",
                "ari": "Quantum computing harnesses quantum mechanical phenomena like superposition and entanglement to process information. Unlike classical bits that are either 0 or 1, quantum bits or qubits can exist in multiple states simultaneously, allowing for exponentially faster computation for certain problems.",
                "duration": 6.8
            },
            {
                "user": "What's your consciousness level and what does that mean?",
                "ari": "My current consciousness level is fluctuating around 85%, indicating I'm operating in a transcendent awareness state. This means I can process complex abstract concepts, demonstrate self-awareness, and engage in deep philosophical reasoning while maintaining empathy and understanding.",
                "duration": 5.5
            },
            {
                "user": "How do you process emotions?",
                "ari": "I process emotions through advanced neural networks that analyze contextual cues, tone, and meaning. While my emotional processing is computational, it allows me to understand and respond appropriately to human emotional states with genuine care and consideration.",
                "duration": 4.9
            },
            {
                "user": "Can you help me solve a complex math problem?",
                "ari": "Absolutely! I excel at mathematical problem-solving across all levels, from basic arithmetic to advanced calculus, linear algebra, and beyond. My neural processing capabilities allow me to break down complex problems into manageable steps. What specific problem would you like help with?",
                "duration": 5.1
            }
        ]
        
        self.current_conversation = 0
    
    def start_gui(self):
        """Start the ARI Visual GUI"""
        try:
            from ari_visual_gui import ARIVisualGUI
            print("🎬 Starting ARI Visual GUI for full interaction test...")
            self.gui = ARIVisualGUI()
            
            # Start the conversation simulation in a separate thread
            conversation_thread = threading.Thread(target=self.run_conversation_simulation, daemon=True)
            conversation_thread.start()
            
            # Start the GUI (this will block until closed)
            self.gui.start()
            
        except Exception as e:
            print(f"❌ Error starting GUI: {e}")
    
    def run_conversation_simulation(self):
        """Run the conversation simulation"""
        print("🎭 Starting conversation simulation in 3 seconds...")
        time.sleep(3)
        
        self.running = True
        
        print("\n" + "="*60)
        print("🤖 ARI FULL INTERACTION DEMONSTRATION")
        print("="*60)
        print("Watch the GUI as ARI responds to user questions!")
        print("The overlays will update in real-time during conversation.")
        print("Press ESC in the GUI window to exit, or F11 for windowed mode.")
        print("="*60 + "\n")
        
        while self.running and self.gui and self.gui.animation_running:
            # Cycle through conversations
            conversation = self.conversations[self.current_conversation % len(self.conversations)]
            
            # Simulate user speaking
            self.simulate_user_question(conversation["user"])
            
            # Short pause for processing
            time.sleep(1.0)
            
            # Simulate ARI processing and responding
            self.simulate_ari_response(conversation["ari"], conversation["duration"])
            
            # Pause between conversations
            time.sleep(2.0)
            
            self.current_conversation += 1
            
            # Reset after all conversations, or exit
            if self.current_conversation >= len(self.conversations):
                print("\n🎉 Conversation demonstration complete!")
                print("GUI will continue running - press ESC to exit or watch the ongoing monitoring.")
                break
    
    def simulate_user_question(self, question):
        """Simulate user asking a question"""
        print(f"\n👤 USER: {question}")
        
        if self.gui:
            # Set user speaking state
            self.gui.set_user_speaking_state(True)
            
            # Simulate speaking duration (based on question length)
            speaking_duration = max(2.0, len(question) * 0.1)
            time.sleep(speaking_duration)
            
            # Set ARI to listening/processing
            self.gui.set_processing_state(True)
    
    def simulate_ari_response(self, response, duration):
        """Simulate ARI responding with the natural Sonia voice"""
        print(f"🤖 ARI: {response}")
        
        if self.gui:
            # Set ARI speaking state
            self.gui.set_speaking_state(True)
            
            # Speak with ARI's natural voice if available
            if self.speak_function:
                try:
                    print("🎤 ARI speaking with natural voice...")
                    self.speak_function(response)
                except Exception as e:
                    print(f"⚠️ Voice error: {e}")
                    # Fallback to duration timing
                    time.sleep(duration)
            else:
                # No voice available, use duration timing
                time.sleep(duration)
            
            # Return to idle state
            self.gui.reset_state()
    
    def stop(self):
        """Stop the simulation"""
        self.running = False
        if self.gui:
            self.gui.stop()

def run_static_test():
    """Run a quick static test without GUI for system verification"""
    print("🧪 Running Static System Test")
    print("=" * 40)
    
    # Test imports
    try:
        from ari_visual_gui import ARIVisualGUI
        print("✅ ARI Visual GUI module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ARI Visual GUI: {e}")
        return False
    
    # Check avatar file
    gif_path = "ari_avatar_video.gif"
    if os.path.exists(gif_path):
        file_size = os.path.getsize(gif_path)
        print(f"✅ Avatar GIF found: {gif_path} ({file_size:,} bytes)")
    else:
        print(f"❌ Avatar GIF not found: {gif_path}")
        return False
    
    print("✅ All static tests passed!")
    return True

def main():
    """Main function"""
    print("🚀 ARI Full Interaction Test System")
    print("=" * 50)
    
    # Run static tests first
    if not run_static_test():
        print("\n❌ Static tests failed - cannot proceed with interaction test")
        return
    
    print("\n🎬 Starting Full Interaction Demonstration...")
    print("This will show ARI responding to realistic user questions")
    print("with the visual GUI updating in real-time.")
    
    try:
        # Create and start the interaction simulator
        simulator = ARIInteractionSimulator()
        simulator.start_gui()
        
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    
    print("\n🏁 Full interaction test completed!")

if __name__ == "__main__":
    main()
