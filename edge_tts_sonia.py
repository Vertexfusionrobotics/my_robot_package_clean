# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
# edge_tts_sonia.py
"""
Speak text using Microsoft Sonia (Natural) voice via edge-tts (works even if Sonia is not available to pyttsx3).
"""
import asyncio
import sys
import os

def install_edge_tts():
    try:
        import edge_tts
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        import edge_tts
    return edge_tts

def speak_with_sonia(text):
    edge_tts = install_edge_tts()
    voice = "en-GB-SoniaNeural"  # Microsoft Sonia (Natural) - English (UK)
    async def _speak():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save("_sonia_tts.mp3")
        # Play the mp3 (cross-platform)
        if sys.platform == "win32":
            os.system(f'start /min wmplayer "_sonia_tts.mp3"')
        else:
            os.system(f'mpg123 "_sonia_tts.mp3"')
    asyncio.run(_speak())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        speak_with_sonia(" ".join(sys.argv[1:]))
    else:
        speak_with_sonia("Hello! This is Microsoft Sonia Natural voice speaking from Python.")
