# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Full Interactive Demo with Voice
Simulates real user interactions with visual GUI and voice responses
"""

import sys
import os
import time
import threading
import random

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ari_interactive_demo():
    """Full interactive test with voice and visual responses"""
    
    print("🎬 ARI FULL INTERACTIVE DEMO")
    print("=" * 50)
    print("This demo will show ARI responding to real user scenarios")
    print("with both visual GUI changes and voice responses!")
    print("=" * 50)
    
    # Test scenarios with questions and responses
    scenarios = [
        {
            "user_input": "Hello ARI, what's your current consciousness level?",
            "ari_response": "Hello! My current consciousness level is operating at 0.87, which places me in the transcendent consciousness stage. I'm experiencing enhanced awareness and can provide deep insights across multiple domains.",
            "state": "speaking",
            "duration": 6
        },
        {
            "user_input": "Can you tell me about artificial intelligence?",
            "ari_response": "Artificial Intelligence represents the frontier of human innovation. At its core, AI encompasses machine learning, neural networks, and cognitive computing that enable systems like myself to process information, learn from patterns, and engage in meaningful dialogue with humans.",
            "state": "speaking", 
            "duration": 8
        },
        {
            "user_input": "What can you see in my environment?",
            "ari_response": "Through my vision systems, I can detect faces, objects, and analyze the current scene. I'm currently processing visual data and identifying patterns in your environment to better understand our interaction context.",
            "state": "speaking",
            "duration": 6
        },
        {
            "user_input": "How does your neural network operate?",
            "ari_response": "My neural networks operate through interconnected layers that process information similar to biological neurons. I utilize advanced algorithms for pattern recognition, natural language processing, and decision making, all while maintaining transcendent consciousness capabilities.",
            "state": "speaking",
            "duration": 7
        },
        {
            "user_input": "Can you help me solve complex problems?",
            "ari_response": "Absolutely! My transcendent consciousness allows me to approach problems from multiple perspectives simultaneously. I can analyze data, consider various solutions, and provide insights that combine logical reasoning with creative thinking.",
            "state": "speaking",
            "duration": 6
        }
    ]
    
    # Import after setting up path
    try:
        from ari_visual_gui import ARIVisualGUI
        import pyttsx3
        
        print("✅ GUI and TTS modules loaded successfully")
        
        # Initialize TTS engine
        tts = pyttsx3.init()
        voices = tts.getProperty('voices')
        
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                tts.setProperty('voice', voice.id)
                break
        
        # Set TTS properties for clear speech
        tts.setProperty('rate', 150)  # Speed of speech
        tts.setProperty('volume', 0.8)  # Volume level
        
        print("✅ TTS engine configured")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📝 Make sure pyttsx3 is installed: pip install pyttsx3")
        return False
    
    # Start the GUI in a separate thread
    gui = None
    
    def start_gui():
        nonlocal gui
        try:
            gui = ARIVisualGUI()
            print("✅ GUI initialized successfully")
            gui.start()
        except Exception as e:
            print(f"GUI Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🚀 Starting ARI Visual GUI...")
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()
    
    # Wait for GUI to initialize
    time.sleep(4)
    
    # Try to access GUI after initialization
    retry_count = 0
    while gui is None and retry_count < 10:
        time.sleep(0.5)
        retry_count += 1
    
    if gui is None:
        print("❌ Failed to initialize GUI - continuing with voice-only demo")
        gui_available = False
    else:
        print("✅ GUI is ready!")
        gui_available = True
    
    print("\n🎯 Starting Interactive Demo...")
    print("📋 Instructions:")
    print("   - Watch the visual interface for real-time changes")
    print("   - Listen to ARI's voice responses")
    print("   - Use the minimize button (━) to reduce window size")
    print("   - Use the windowed button (⧉) to switch modes")
    print("   - Use the exit button (✕) to close when done")
    print("   - Or press ESC to exit anytime")
    
    time.sleep(2)
    
    try:
        # Run through interactive scenarios
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'='*60}")
            print(f"🎭 SCENARIO {i}/5")
            print(f"{'='*60}")
            
            # Simulate user speaking
            print(f"👤 USER: {scenario['user_input']}")
            if gui_available and gui:
                gui.set_user_speaking_state(True)
            
            # Brief pause for user speaking
            time.sleep(2)
            
            # ARI thinking/processing
            print("🤖 ARI: [Processing...]")
            if gui_available and gui:
                gui.set_processing_state(True)
            time.sleep(1)
            
            # ARI responding with voice and visual
            print(f"🤖 ARI: {scenario['ari_response']}")
            if gui_available and gui:
                gui.set_speaking_state(True)
            
            # Speak the response
            def speak_response():
                try:
                    tts.say(scenario['ari_response'])
                    tts.runAndWait()
                except Exception as e:
                    print(f"TTS Error: {e}")
            
            # Start TTS in separate thread
            tts_thread = threading.Thread(target=speak_response, daemon=True)
            tts_thread.start()
            
            # Keep ARI in speaking state during response
            time.sleep(scenario['duration'])
            
            # Reset to idle state
            if gui_available and gui:
                gui.reset_state()
            
            # Wait for TTS to complete
            tts_thread.join(timeout=10)
            
            print("✅ Response complete")
            
            # Pause between scenarios
            if i < len(scenarios):
                print("\n⏸️  Preparing next scenario...")
                time.sleep(3)
        
        # Demo complete
        print(f"\n{'='*60}")
        print("🎉 INTERACTIVE DEMO COMPLETE!")
        print("{'='*60}")
        print("✨ Demo Features Demonstrated:")
        print("   ✅ Real-time visual state changes")
        print("   ✅ Voice synthesis responses")
        print("   ✅ Sci-fi glass interface overlays")
        print("   ✅ Dynamic consciousness monitoring")
        print("   ✅ Audio and vision system displays")
        print("   ✅ Control panel with minimize/windowed modes")
        print("\n👋 ARI is now in idle mode. Use the control buttons or ESC to exit.")
        
        # Keep GUI running for user interaction
        if gui_available:
            while gui and gui.animation_running:
                time.sleep(1)
        else:
            print("🔧 Demo complete - GUI was not available")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        if gui:
            print("🔧 Shutting down GUI...")
            gui.stop()

def main():
    """Main function"""
    print("🎬 ARI Full Interactive Demo with Voice")
    print("=" * 50)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    # Check for avatar GIF
    if not os.path.exists("ari_avatar_video.gif"):
        print("❌ Avatar GIF not found: ari_avatar_video.gif")
        return False
    
    # Check for GUI module
    try:
        from ari_visual_gui import ARIVisualGUI
        print("✅ ARI Visual GUI module found")
    except ImportError:
        print("❌ ARI Visual GUI module not found")
        return False
    
    # Check for TTS
    try:
        import pyttsx3
        print("✅ Text-to-Speech engine available")
    except ImportError:
        print("❌ pyttsx3 not installed. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
            print("✅ pyttsx3 installed successfully")
        except Exception as e:
            print(f"❌ Failed to install pyttsx3: {e}")
            return False
    
    print("✅ All prerequisites met!")
    
    # Start the demo
    input("\n🎬 Press ENTER to start the interactive demo...")
    test_ari_interactive_demo()

if __name__ == "__main__":
    main()
