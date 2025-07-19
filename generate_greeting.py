# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import asyncio
import edge_tts

async def generate_greeting():
    greeting = "Welcome to Vertex Fusion Robotics. My name is ARI and I will be your guide and personal assistant. So, how may I assist you today?"
    communicate = edge_tts.Communicate(greeting, voice="en-GB-SoniaNeural")
    await communicate.save("_sonia_greeting.mp3")
    print("Greeting file generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_greeting())
