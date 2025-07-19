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
        face_gui.set_subtitle(text)
    def on_end(name, completed):
        face_gui.stop_talking_animation('neutral')
        face_gui.set_subtitle("")
    engine.connect('started-utterance', on_start)
    engine.connect('started-word', on_word)
    engine.connect('finished-utterance', on_end)
    engine.say(text)
    engine.runAndWait()

def conversation_demo(face):
    # Simulate a conversation
    lines = [
        "Hello! I am ARI, your friendly robot companion.",
        "I can talk, listen, and show expressions on my face.",
        "Watch as my mouth moves in sync with my voice, including my new talking image!",
        "I can also look around and tilt my head while I wait.",
        "If you want me to smile, just say the word!",
        "Now, let's pretend we're having a conversation.",
        "How are you today? I hope you're doing well.",
        "Did you know I can help you with many tasks?",
        "Just ask me anything, and I'll do my best to assist you.",
        "Thank you for spending time with me. Goodbye!"
    ]
    for line in lines:
        speak_with_face(line, face)
        time.sleep(0.7)

def main():
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    def run_convo():
        time.sleep(1)
        conversation_demo(face)
        face.set_subtitle("Demo complete. You can close the window.")
    threading.Thread(target=run_convo, daemon=True).start()
    face.root.mainloop()

if __name__ == "__main__":
    main()
