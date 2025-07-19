# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Fixed ARI GUI + Voice Demo - GUI runs in main thread
Shows the complete ARI experience with animated avatar and voice responses
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_ari_gui_voice():
    """Demo ARI with GUI in main thread and voice responses"""
    
    print("🚀 ARI Visual + Voice Demo")
    print("=" * 40)
    print("This will open the GUI with animated ARI avatar")
    print("and demonstrate voice responses with visual feedback.")
    print("=" * 40)
    
    try:
        # Import the GUI system
        from ari_visual_gui import ARIVisualGUI
        print("✅ GUI system imported")
        
        # Create the GUI (this will open the window)
        gui = ARIVisualGUI()
        print("✅ GUI created - window should be visible")
        print("💡 The GUI starts in windowed mode so you can minimize it")
        print("💡 Use F11 for fullscreen, ESC to exit")
        
        # Import ARI brain system
        print("\n🧠 Loading ARI brain system...")
        from ari_master_brain_final import ARIMasterBrain
        ari = ARIMasterBrain()
        print("✅ ARI brain ready")
        
        # Demo function that shows different GUI states
        def demo_interaction(user_text, description):
            print(f"\n🎭 Demo: {description}")
            print(f"👤 Simulated user: {user_text}")
            
            # Show user speaking state
            gui.set_user_speaking_state(True)
            gui.root.update()  # Force GUI update
            time.sleep(1.5)
            
            # Show processing state
            gui.set_processing_state(True)
            gui.root.update()
            time.sleep(0.5)
            
            # Get ARI's response
            response = ari.get_response(user_text)
            print(f"🤖 ARI: {response}")
            
            # Show ARI speaking state
            gui.set_speaking_state(True)
            gui.root.update()
            
            # Speak the response
            ari.speak(response)
            
            # Reset to idle state
            gui.reset_state()
            gui.root.update()
            time.sleep(1)
        
        # Start the demo scenarios
        print("\n🎬 Starting interactive demo...")
        print("Watch the ARI avatar change animation speed based on states!")
        
        # Demo scenarios
        scenarios = [
            ("Hello ARI", "Basic greeting"),
            ("How are you today?", "Casual conversation"),
            ("What can you see?", "Vision system demo"),
            ("Tell me about consciousness", "Advanced AI demo"),
            ("Can you analyze emotions?", "Emotion detection demo")
        ]
        
        # Run scenarios with GUI updates
        for user_input, description in scenarios:
            demo_interaction(user_input, description)
            
            # Update GUI between scenarios
            for _ in range(20):  # Update GUI for 2 seconds
                gui.root.update()
                time.sleep(0.1)
        
        print("\n🎉 Demo completed!")
        print("=" * 40)
        print("GUI Features demonstrated:")
        print("• Avatar animation changes based on speaking states")
        print("• Real-time system monitoring overlays")
        print("• Futuristic sci-fi interface design")
        print("• Voice output with natural Sonia voice")
        print("=" * 40)
        print("\nThe GUI will stay open. You can:")
        print("• Press F11 to toggle fullscreen")
        print("• Use minimize button to minimize to taskbar")
        print("• Press ESC to exit")
        print("\nPress Enter to keep GUI open or close the window to exit...")
        
        # Keep GUI running
        input()
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_ari_gui_voice()
