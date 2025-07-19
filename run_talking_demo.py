# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import pyttsx3
import time
from test_holo_face import AriFaceGUI
import threading

def speak_with_face(text, face_gui, rate=180):
    engine = pyttsx3.init()
    # Set female voice if available
    voices = engine.getProperty('voices')
    for v in voices:
        if 'female' in v.name.lower() or 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', rate)
    face_gui.show_expression('neutral')

    # --- Start talking animation at a fixed, natural interval ---
    def on_start(name):
        face_gui.start_talking_animation(interval=150)  # ~7 FPS, natural pace
    def on_word(name, location, length):
        pass  # Animation already running, looping through all PNGs
    def on_end(name, completed):
        face_gui.stop_talking_animation('neutral')
    engine.connect('started-utterance', on_start)
    engine.connect('started-word', on_word)
    engine.connect('finished-utterance', on_end)
    engine.say(text)
    engine.runAndWait()
    face_gui.show_expression('smiling')
    face_gui.root.after(1200, lambda: face_gui.show_expression('neutral'))

def main():
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    def run_speech():
        time.sleep(1)
        speak_with_face("Hello! I am ARI. I can talk and move my face while I speak. This is a demo of synchronized talking.", face)
    threading.Thread(target=run_speech, daemon=True).start()
    face.root.mainloop()

if __name__ == "__main__":
    main()
