# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Simple TTS test to debug audio issues
"""

import asyncio
import edge_tts
import pygame
import tempfile
import time
import os

def test_tts():
    text = "This is a simple TTS test"
    voice = "en-GB-SoniaNeural"
    
    print("Creating TTS audio...")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
        tts_path = tf.name
    
    async def generate_tts():
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save(tts_path)
    
    asyncio.run(generate_tts())
    
    if os.path.exists(tts_path):
        file_size = os.path.getsize(tts_path)
        print(f"TTS file created: {tts_path} ({file_size} bytes)")
        
        if file_size > 0:
            print("Initializing pygame...")
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
                print("Loading audio file...")
                pygame.mixer.music.load(tts_path)
                print("Playing audio...")
                pygame.mixer.music.play()
                
                # Wait for playback
                start_time = time.time()
                while pygame.mixer.music.get_busy() and time.time() - start_time < 10:
                    time.sleep(0.1)
                
                print("Playback completed")
                pygame.mixer.music.unload()
                pygame.mixer.quit()
                
            except Exception as e:
                print(f"Pygame error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("TTS file is empty!")
        
        # Clean up
        try:
            time.sleep(0.2)
            os.remove(tts_path)
            print("Temp file cleaned up")
        except Exception as e:
            print(f"Cleanup error: {e}")
    else:
        print("TTS file was not created!")

if __name__ == "__main__":
    test_tts()
