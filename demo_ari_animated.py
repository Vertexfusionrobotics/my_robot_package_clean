# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Enhanced ARI Demo - GUI with Responsive Animation Speeds
Shows ARI avatar animating at different speeds based on speaking states
"""

import sys
import os
import threading
import time
import tkinter as tk

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ARIAnimatedDemo:
    def __init__(self):
        self.gui = None
        self.ari = None
        self.demo_running = False
        
    def initialize_systems(self):
        """Initialize ARI systems"""
        print("🚀 Initializing ARI Systems")
        print("=" * 50)
        
        try:
            # Import and create GUI
            from ari_visual_gui import ARIVisualGUI
            self.gui = ARIVisualGUI()
            print("✅ GUI system ready")
            
            # Import and create ARI brain
            from ari_master_brain_final import ARIMasterBrain
            self.ari = ARIMasterBrain()
            print("✅ ARI brain system ready")
            
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def demonstrate_animation_states(self):
        """Demonstrate different animation speeds"""
        
        scenarios = [
            {
                "description": "🤖 ARI Speaking (Fast Animation)",
                "user_input": "Hello ARI, how are you today?",
                "state": "ari_speaking",
                "duration": 3
            },
            {
                "description": "👤 User Speaking (Attentive Animation)",
                "user_input": "Can you tell me about your capabilities?",
                "state": "user_speaking", 
                "duration": 2
            },
            {
                "description": "🧠 ARI Processing (Medium Animation)",
                "user_input": "What can you see with your vision system?",
                "state": "processing",
                "duration": 2
            },
            {
                "description": "👂 ARI Listening (Slow Animation)",
                "user_input": "",
                "state": "listening",
                "duration": 3
            },
            {
                "description": "😴 ARI Idle (Normal Animation)",
                "user_input": "",
                "state": "idle",
                "duration": 3
            }
        ]
        
        print("\n🎬 Animation State Demonstration")
        print("=" * 50)
        print("Watch the ARI avatar - you'll see different animation speeds:")
        print("   • FAST when ARI is speaking")
        print("   • MEDIUM when processing") 
        print("   • SLOW when user is speaking (attentive)")
        print("   • SLOWER when listening")
        print("   • NORMAL when idle")
        print("=" * 50)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎭 Demo {i}/5: {scenario['description']}")
            
            # Set the appropriate GUI state
            if scenario['state'] == 'ari_speaking':
                self.gui.set_speaking_state(True)
                if scenario['user_input']:
                    # Get ARI's response and speak it
                    response = self.ari.get_response(scenario['user_input'])
                    print(f"🗣️ ARI: {response}")
                    # Speak in a separate thread so we can see the animation
                    threading.Thread(target=self.ari.speak, args=(response,), daemon=True).start()
                
            elif scenario['state'] == 'user_speaking':
                print(f"👤 User: {scenario['user_input']}")
                self.gui.set_user_speaking_state(True)
                
            elif scenario['state'] == 'processing':
                print(f"👤 User: {scenario['user_input']}")
                self.gui.set_processing_state(True)
                # Actually get a response while processing
                response = self.ari.get_response(scenario['user_input'])
                print(f"💭 Processing: {response[:50]}...")
                
            elif scenario['state'] == 'listening':
                print("👂 ARI waiting for user input...")
                self.gui.set_listening_state(True)
                
            elif scenario['state'] == 'idle':
                print("😴 ARI in idle state...")
                self.gui.reset_state()
            
            # Let the animation run for the specified duration
            print(f"   ⏱️ Animation running for {scenario['duration']} seconds...")
            time.sleep(scenario['duration'])
            
            # Reset state between demos
            self.gui.reset_state()
            
            if i < len(scenarios):
                print("   ⏳ Next demo in 1 second...")
                time.sleep(1)
        
        print("\n🎉 Animation demonstration completed!")
        
    def run_interactive_demo(self):
        """Run interactive demo with voice and animation"""
        
        print("\n🎤 Interactive Demo Mode")
        print("=" * 50)
        print("Type messages to see ARI respond with voice + animation!")
        print("Watch how the avatar animation changes speed based on state:")
        print("   • Fast when ARI speaks")
        print("   • Slow when you 'speak' (type)")
        print("   • Medium when processing")
        print("Type 'quit' to end the demo")
        print("=" * 50)
        
        while self.demo_running:
            try:
                # Show user typing state
                self.gui.set_user_speaking_state(True)
                user_input = input("\n👤 You: ")
                self.gui.set_user_speaking_state(False)
                
                if not user_input.strip():
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    print("🛑 Ending demo...")
                    break
                
                # Show processing state
                self.gui.set_processing_state(True)
                print("🧠 ARI is thinking...")
                time.sleep(0.5)  # Brief processing animation
                
                # Get response
                response = self.ari.get_response(user_input)
                
                # Show speaking state
                self.gui.set_speaking_state(True)
                print(f"🤖 ARI: {response}")
                
                # Speak the response
                self.ari.speak(response)
                
                # Reset to idle
                self.gui.reset_state()
                
            except KeyboardInterrupt:
                print("\n🛑 Demo interrupted")
                break
            except Exception as e:
                print(f"❌ Demo error: {e}")
                self.gui.reset_state()
    
    def run_demo(self):
        """Run the complete demo"""
        
        print("🎬 ARI Animated Demo Starting!")
        print("=" * 50)
        
        # Initialize systems
        if not self.initialize_systems():
            return
        
        # Start GUI in separate thread
        def run_gui():
            try:
                self.gui.start()
            except Exception as e:
                print(f"GUI error: {e}")
        
        gui_thread = threading.Thread(target=run_gui, daemon=True)
        gui_thread.start()
        
        # Wait for GUI to initialize
        print("⏳ Waiting for GUI to initialize...")
        time.sleep(3)
        
        try:
            self.demo_running = True
            
            # First run animation state demo
            self.demonstrate_animation_states()
            
            # Then run interactive demo
            self.run_interactive_demo()
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
        finally:
            self.demo_running = False
            print("👋 Demo ended - GUI will remain open")
            print("Press ESC in the GUI window to close it")

def main():
    """Main demo function"""
    demo = ARIAnimatedDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
