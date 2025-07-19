# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import time
from test_holo_face import AriFaceGUI
import threading
import pyttsx3

def speak_with_face(text, face_gui, rate=180):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        if 'female' in v.name.lower() or 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', rate)
    face_gui.set_subtitle("")
    def on_word(name, location, length):
        face_gui.start_talking_animation(interval=60)
        face_gui.root.after(80, lambda: face_gui.stop_talking_animation('neutral'))
    def on_start(name):
        pass
    def on_end(name, completed):
        face_gui.stop_talking_animation('neutral')
    engine.connect('started-utterance', on_start)
    engine.connect('started-word', on_word)
    engine.connect('finished-utterance', on_end)
    engine.say(text)
    engine.runAndWait()

def long_conversation_demo(face):
    # Simulate a long, two-way conversation using all new expressions
    lines = [
        ("User: Hello ARI", 'listening'),
        ("Hello Mr. Murray. How can I help you today?", 'talking'),
        ("User: What's the weather like today?", 'listening2'),
        ("Let me check the weather for you.", 'thinking'),
        ("The weather today is sunny with a high of 25 degrees.", 'talking'),
        ("User: Tell me a joke.", 'listening3'),
        ("Why did the robot go to the party? Because he had the right bytes!", 'talking'),
        ("User: Are you happy?", 'smiling_listening'),
        ("Of course! I'm always happy to help you.", 'smiling_talking'),
        ("User: What is 2 plus 2?", 'listening1'),
        ("2 plus 2 is 4.", 'talking'),
        ("User: Can you look around?", 'looking_around'),
        ("I'm scanning the room now.", 'talking'),
        ("User: Are you confused?", 'confused'),
        ("Sometimes, but I always try my best!", 'talking'),
        ("User: Surprise me!", 'suprised'),
        ("Boo! Did I surprise you?", 'talking'),
        ("User: Goodbye ARI.", 'listening'),
        ("Goodbye Mr. Murray. Have a great day!", 'talking'),
    ]
    for line, expr in lines:
        if line.startswith("User:"):
            face.set_expression(expr)
            face.set_subtitle(line)
            time.sleep(2)
        else:
            face.set_subtitle("")
            face.set_expression(expr)
            speak_with_face(line, face)
            # Brief smile after greeting or joke
            if "Hello Mr. Murray" in line or "bytes" in line or "great day" in line:
                face.set_expression('smiling')
                time.sleep(1)
            face.set_expression('neutral')
            time.sleep(1)
    face.set_subtitle("Demo complete. You can close the window.")

def main():
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    def run_demo():
        long_conversation_demo(face)
    threading.Thread(target=run_demo, daemon=True).start()
    face.root.mainloop()

if __name__ == "__main__":
    main()
