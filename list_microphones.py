# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
List all microphone devices detected by the system
"""

import speech_recognition as sr

def list_microphones():
    print("Listing all audio input devices detected by speech_recognition:")
    print("-" * 60)
    
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"Total devices found: {len(mic_list)}")
        print()
        
        for i, mic_name in enumerate(mic_list):
            print(f"{i:2d}: {mic_name}")
            
        print()
        print("Note: Many of these are virtual devices, system mixers, or alternative")
        print("interfaces to the same physical microphone. Windows reports all possible")
        print("audio input endpoints, including:")
        print("- Physical microphones")
        print("- Virtual audio cables") 
        print("- System audio mixers")
        print("- Application-specific audio devices")
        print("- Bluetooth audio devices")
        print("- USB audio interfaces")
        print("- HDMI audio inputs")
        print("- And more...")
        
    except Exception as e:
        print(f"Error listing microphones: {e}")

if __name__ == "__main__":
    list_microphones()
