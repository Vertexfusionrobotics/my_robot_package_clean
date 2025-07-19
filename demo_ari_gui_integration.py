# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI GUI Integration Demo
Shows ARI avatar GUI popping up and responding with voice and visual animation
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 ARI GUI Integration Demo")
    print("=" * 50)
    
    try:
        # Import systems
        print("📦 Loading ARI systems...")
        from ari_visual_gui import ARIVisualGUI
        from ari_voice_robust import ARIVoiceSystem
        
        # Initialize GUI
        print("🎨 Initializing GUI...")
        gui = ARIVisualGUI()
        
        # Initialize voice system
        print("🗣️ Initializing voice system...")
        voice = ARIVoiceSystem()
        
        # Start GUI in main thread (required for tkinter)
        def run_demo():
            print("🎭 Starting animated demo...")
            
            # Wait for GUI to be ready
            time.sleep(2)
            
            # Demo sequence with audio monitoring
            scenarios = [
                {
                    "message": "Hello! I'm ARI, your AI assistant. Watch the audio monitor!",
                    "animation": "speaking",
                    "duration": 4
                },
                {
                    "message": "Notice how the audio bars light up when I speak.",
                    "animation": "speaking", 
                    "duration": 3
                },
                {
                    "message": "The audio monitoring system shows real-time activity levels.",
                    "animation": "speaking",
                    "duration": 4
                },
                {
                    "message": "This demonstrates the integrated GUI, voice, and audio monitoring!",
                    "animation": "speaking",
                    "duration": 5
                }
            ]
            
            for i, scenario in enumerate(scenarios, 1):
                print(f"\n🎬 Demo Step {i}: {scenario['message']}")
                
                # Show processing state briefly
                print("   📊 Setting processing state...")
                gui.set_processing_state(True)
                time.sleep(0.5)
                
                # Set GUI to speaking state (this triggers audio activity)
                print("   🗣️ Setting speaking state...")
                gui.set_speaking_state(True)
                
                # Speak the message
                voice.speak(scenario['message'])
                
                # Keep animation and audio monitoring running for duration
                time.sleep(scenario['duration'])
                
                # Set GUI back to idle
                print("   💤 Resetting to idle state...")
                gui.set_speaking_state(False)
                
                # Brief pause between scenarios
                time.sleep(1.5)
            
            print("\n✅ Demo complete!")
            print("Notice how the audio monitor bars respond to each speaking state.")
            print("The GUI window will stay open. Close it manually when done.")
        
        # Start demo in background thread
        demo_thread = threading.Thread(target=run_demo, daemon=True)
        demo_thread.start()
        
        # Start GUI (this blocks until window is closed)
        print("🎮 Starting GUI (close window to exit)...")
        gui.start()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
