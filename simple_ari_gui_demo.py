# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Simple ARI GUI Demo
Launch ARI with GUI in main thread to avoid threading issues
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Simple ARI GUI Demo")
    print("=" * 40)
    
    try:
        # Import GUI
        from ari_visual_gui import ARIVisualGUI
        
        # Initialize GUI
        print("🎨 Initializing ARI GUI...")
        gui = ARIVisualGUI()
        
        # Simple demo function to run in background
        def demo_sequence():
            print("🎭 Starting demo sequence...")
            time.sleep(2)  # Wait for GUI to initialize
            
            try:
                from ari_voice_robust import ARIVoiceSystem
                voice = ARIVoiceSystem()
                
                # Demo messages
                messages = [
                    "Hello! Welcome to ARI!",
                    "This is the ARI visual interface working with voice!",
                    "Watch the avatar animations!",
                    "Demo complete!"
                ]
                
                for i, message in enumerate(messages, 1):
                    print(f"\n🎬 Demo step {i}: {message}")
                    
                    # Set speaking state
                    gui.set_speaking_state(True)
                    
                    # Speak
                    voice.speak(message)
                    
                    # Wait a bit
                    time.sleep(2)
                    
                    # Reset speaking state
                    gui.set_speaking_state(False)
                    time.sleep(1)
                
                print("\n✅ Demo complete! Close the GUI window to exit.")
                
            except Exception as e:
                print(f"❌ Demo error: {e}")
        
        # Start demo in background thread
        demo_thread = threading.Thread(target=demo_sequence, daemon=True)
        demo_thread.start()
        
        # Start GUI in main thread (this is important for tkinter)
        print("🎮 Starting GUI (main thread)...")
        gui.start()
        
    except Exception as e:
        print(f"❌ Failed to start demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
