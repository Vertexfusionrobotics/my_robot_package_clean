# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Full ARI Demo - GUI + Voice + Interaction
Shows the complete ARI experience with animated avatar and voice responses
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_ari_with_gui():
    """Run ARI with both GUI and voice interaction"""
    
    print("🚀 Starting Full ARI Experience")
    print("=" * 50)
    print("This will open:")
    print("   🎨 Visual GUI with animated ARI avatar")
    print("   🗣️ Voice interaction system")
    print("   🤖 Full AI conversation capabilities")
    print("=" * 50)
    
    try:
        # Import systems
        from ari_visual_gui import ARIVisualGUI
        from ari_master_brain_final import ARIMasterBrain
        
        print("✅ Systems imported successfully")
        
        # Create GUI in a separate thread
        gui = ARIVisualGUI()
        print("✅ GUI created - starts in windowed mode")
        
        def run_gui():
            """Run the GUI in a separate thread"""
            try:
                gui.start()
            except Exception as e:
                print(f"GUI error: {e}")
        
        # Start GUI thread
        gui_thread = threading.Thread(target=run_gui, daemon=True)
        gui_thread.start()
        print("✅ GUI thread started")
        
        # Give GUI time to initialize
        time.sleep(2)
        
        # Create ARI brain
        print("🧠 Initializing ARI brain system...")
        ari = ARIMasterBrain()
        print("✅ ARI brain ready")
        
        # Demo conversation scenarios
        demo_scenarios = [
            {
                "user_input": "Hello ARI",
                "description": "Basic greeting",
                "gui_state": "listening"
            },
            {
                "user_input": "How are you today?",
                "description": "Casual question",
                "gui_state": "processing"
            },
            {
                "user_input": "What can you see with your vision system?",
                "description": "Vision capabilities",
                "gui_state": "processing"
            },
            {
                "user_input": "Tell me about your consciousness levels",
                "description": "Advanced consciousness demo",
                "gui_state": "processing"
            },
            {
                "user_input": "Can you detect my emotions?",
                "description": "Emotion analysis",
                "gui_state": "processing"
            }
        ]
        
        print("\n🎬 Starting Interactive Demo")
        print("=" * 50)
        print("Watch the GUI window - you'll see:")
        print("   • ARI avatar animating differently based on states")
        print("   • Futuristic overlays updating in real-time")
        print("   • System status and consciousness indicators")
        print("   • Audio/vision monitoring displays")
        print("=" * 50)
        
        for i, scenario in enumerate(demo_scenarios, 1):
            print(f"\n🎭 Demo Scenario {i}: {scenario['description']}")
            print(f"👤 User: {scenario['user_input']}")
            
            # Set GUI state to show user is speaking
            if hasattr(gui, 'set_user_speaking_state'):
                gui.set_user_speaking_state(True)
                time.sleep(1)  # Show user speaking animation
                gui.set_user_speaking_state(False)
            
            # Set GUI to processing state
            if hasattr(gui, 'set_processing_state'):
                gui.set_processing_state(True)
            
            # Get ARI's response
            response = ari.get_response(scenario['user_input'])
            print(f"🤖 ARI: {response}")
            
            # Set GUI to speaking state
            if hasattr(gui, 'set_speaking_state'):
                gui.set_speaking_state(True)
            
            # Speak the response
            ari.speak(response)
            
            # Reset GUI state
            if hasattr(gui, 'reset_state'):
                gui.reset_state()
            
            # Pause between scenarios
            if i < len(demo_scenarios):
                print("   ⏳ Next scenario in 3 seconds...")
                time.sleep(3)
        
        print("\n🎉 Demo completed!")
        print("=" * 50)
        print("The GUI will remain open so you can:")
        print("   • See the real-time monitoring overlays")
        print("   • Use F11 to toggle fullscreen")
        print("   • Use standard Windows controls to minimize")
        print("   • Press ESC in the GUI to exit")
        print("=" * 50)
        
        # Keep the demo running
        input("\nPress Enter to end the demo...")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("👋 Demo ending...")
        # GUI will close when main thread ends

if __name__ == "__main__":
    run_ari_with_gui()
