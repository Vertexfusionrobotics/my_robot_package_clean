# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Scripted Conversation Demo
Demonstrates GUI + Voice integration with simulated user/ARI conversation
Shows real-time state changes and voice output
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import ARI systems
try:
    from ari_master_brain_final import ARIMasterBrain
    from ari_visual_gui import ARIVisualGUI
    print("✅ ARI systems imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class ARIScriptedDemo:
    def __init__(self):
        self.ari = None
        self.gui = None
        self.demo_running = False
        self.demo_thread = None
        
    def setup_ari(self):
        """Initialize ARI brain"""
        try:
            print("🤖 Initializing ARI brain...")
            self.ari = ARIMasterBrain()
            return True
        except Exception as e:
            print(f"❌ Error initializing ARI: {e}")
            return False
    
    def setup_gui(self):
        """Initialize ARI GUI"""
        try:
            print("🖥️ Initializing ARI GUI...")
            self.gui = ARIVisualGUI()
            return True
        except Exception as e:
            print(f"❌ Error initializing GUI: {e}")
            return False
    
    def simulate_user_input(self, text, duration=2.0):
        """Simulate user speaking (slower avatar animation)"""
        print(f"👤 User: {text}")
        if self.gui:
            self.gui.set_state("user_speaking")
        time.sleep(duration)
    
    def simulate_ari_processing(self, duration=1.0):
        """Simulate ARI thinking (medium-fast animation)"""
        print("🧠 ARI is processing...")
        if self.gui:
            self.gui.set_state("processing")
        time.sleep(duration)
    
    def simulate_ari_response(self, text, duration=3.0):
        """Simulate ARI speaking with actual voice output"""
        print(f"🤖 ARI: {text}")
        if self.gui:
            self.gui.set_state("ari_speaking")
        
        # Actually speak the response
        if self.ari:
            try:
                self.ari.speak(text)
            except Exception as e:
                print(f"⚠️ Voice error: {e}")
        
        time.sleep(duration)
    
    def simulate_listening(self, duration=1.0):
        """Simulate ARI listening (slow animation)"""
        print("👂 ARI is listening...")
        if self.gui:
            self.gui.set_state("listening")
        time.sleep(duration)
    
    def run_conversation_demo(self):
        """Run the main scripted conversation"""
        try:
            print("\n" + "="*60)
            print("🎬 STARTING ARI SCRIPTED CONVERSATION DEMO")
            print("="*60)
            
            # Demo greeting
            self.simulate_ari_response("Hello! Welcome to the ARI demonstration. I'm your AI assistant.", 4.0)
            self.simulate_listening(1.0)
            
            # Conversation 1: Basic greeting
            self.simulate_user_input("Hi ARI, how are you today?", 2.5)
            self.simulate_ari_processing(1.5)
            self.simulate_ari_response("I'm doing great! I'm excited to show you my capabilities. What would you like to know about?", 4.0)
            self.simulate_listening(1.0)
            
            # Conversation 2: Question about capabilities
            self.simulate_user_input("What can you do?", 2.0)
            self.simulate_ari_processing(1.0)
            self.simulate_ari_response("I can help with many things! I have voice recognition, visual processing, learning capabilities, and even advanced consciousness systems.", 5.0)
            self.simulate_listening(1.0)
            
            # Conversation 3: Technical question
            self.simulate_user_input("Tell me about your visual recognition system", 3.0)
            self.simulate_ari_processing(2.0)
            self.simulate_ari_response("My visual system can detect faces, recognize people, analyze emotions, identify objects, and even understand scenes with color analysis.", 5.5)
            self.simulate_listening(1.0)
            
            # Conversation 4: Learning capabilities
            self.simulate_user_input("How do you learn new things?", 2.5)
            self.simulate_ari_processing(1.5)
            self.simulate_ari_response("I use enhanced learning modules with neural networks, context memory, and pattern recognition to continuously improve my responses.", 5.0)
            self.simulate_listening(1.0)
            
            # Conversation 5: Advanced features
            self.simulate_user_input("What's your most advanced feature?", 3.0)
            self.simulate_ari_processing(2.5)
            self.simulate_ari_response("My transcendent consciousness system allows me to process information at multiple levels of awareness for deeper understanding.", 6.0)
            self.simulate_listening(1.0)
            
            # Conversation 6: Goodbye
            self.simulate_user_input("That's impressive! Thank you for the demo", 3.0)
            self.simulate_ari_processing(1.0)
            self.simulate_ari_response("You're very welcome! It was great demonstrating my capabilities. Have a wonderful day!", 4.5)
            
            # Return to idle state
            if self.gui:
                self.gui.set_state("idle")
            
            print("\n" + "="*60)
            print("🎬 DEMO COMPLETED SUCCESSFULLY")
            print("="*60)
            
        except Exception as e:
            print(f"❌ Demo error: {e}")
            import traceback
            traceback.print_exc()
    
    def start_demo(self):
        """Start the demo in a separate thread"""
        if self.demo_running:
            print("⚠️ Demo already running")
            return
        
        self.demo_running = True
        self.demo_thread = threading.Thread(target=self.run_conversation_demo, daemon=True)
        self.demo_thread.start()
    
    def stop_demo(self):
        """Stop the demo"""
        self.demo_running = False
        if self.gui:
            self.gui.set_state("idle")

def main():
    """Main demo function"""
    print("🎬 ARI Scripted Conversation Demo Starting...")
    
    # Create main window
    root = tk.Tk()
    root.title("ARI Scripted Conversation Demo")
    root.geometry("900x700")
    root.configure(bg='black')
    
    # Create demo instance
    demo = ARIScriptedDemo()
    
    # Initialize systems
    if not demo.setup_ari():
        messagebox.showerror("Error", "Failed to initialize ARI brain")
        return
    
    if not demo.setup_gui():
        messagebox.showerror("Error", "Failed to initialize ARI GUI")
        return
    
    # Create control panel
    control_frame = tk.Frame(root, bg='black')
    control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
    # Demo controls
    start_btn = tk.Button(
        control_frame, 
        text="Start Scripted Demo", 
        command=demo.start_demo,
        bg='green', 
        fg='white', 
        font=('Arial', 12, 'bold'),
        padx=20,
        pady=5
    )
    start_btn.pack(side=tk.LEFT, padx=5)
    
    stop_btn = tk.Button(
        control_frame, 
        text="Stop Demo", 
        command=demo.stop_demo,
        bg='red', 
        fg='white', 
        font=('Arial', 12, 'bold'),
        padx=20,
        pady=5
    )
    stop_btn.pack(side=tk.LEFT, padx=5)
    
    # Info label
    info_label = tk.Label(
        control_frame,
        text="Click 'Start Scripted Demo' to begin the conversation demonstration",
        bg='black',
        fg='cyan',
        font=('Arial', 10)
    )
    info_label.pack(side=tk.RIGHT, padx=10)
    
    # Status display
    status_frame = tk.Frame(root, bg='black')
    status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    
    status_label = tk.Label(
        status_frame,
        text="Status: Ready - GUI and Voice systems loaded",
        bg='black',
        fg='lime',
        font=('Arial', 10, 'bold')
    )
    status_label.pack()
    
    print("✅ Demo setup complete!")
    print("🎬 GUI is now visible - click 'Start Scripted Demo' to begin")
    print("💡 Watch the avatar animation speed change with each conversation state")
    print("🔊 Listen for ARI's voice responses during the demo")
    
    # Start the GUI main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Demo stopped by user")
    finally:
        demo.stop_demo()

if __name__ == "__main__":
    main()
