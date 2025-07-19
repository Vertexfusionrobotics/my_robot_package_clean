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

def demo_scenario(face):
    # 1. Start with looking_around
    face.set_expression('looking_around')
    face.set_subtitle("")
    time.sleep(2)
    # 2. User says "Hello ARI" (simulate speech detection)
    face.set_expression('listening')
    face.set_subtitle("User: Hello ARI")
    time.sleep(1.5)
    # 3. ARI responds with greeting
    face.set_subtitle("")
    speak_with_face("Hello Mr. Murray. How can I help you today?", face)
    # 4. Briefly flash smiling after greeting
    face.set_expression('smiling')
    time.sleep(1)
    # 5. Back to listening for user input
    face.set_expression('listening')
    face.set_subtitle("Listening...")
    time.sleep(2.5)
    # 6. User asks a question (simulate speech)
    face.set_subtitle("User: What's the capital of France?")
    time.sleep(2)
    # 7. ARI doesn't know, goes to looking_around while searching
    face.set_expression('looking_around')
    face.set_subtitle("Searching for answer...")
    time.sleep(2)
    # 8. ARI finds answer, responds
    face.set_subtitle("")
    speak_with_face("The capital of France is Paris.", face)
    # 9. Back to listening
    face.set_expression('listening')
    face.set_subtitle("Listening...")
    time.sleep(2.5)
    # 10. No user input, back to looking_around
    face.set_expression('looking_around')
    face.set_subtitle("")
    time.sleep(2)
    face.set_subtitle("Demo complete. You can close the window.")

def main():
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    def run_demo():
        demo_scenario(face)
    threading.Thread(target=run_demo, daemon=True).start()
    face.root.mainloop()

if __name__ == "__main__":
    main()
