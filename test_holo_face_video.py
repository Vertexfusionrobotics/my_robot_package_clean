# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
# test_holo_face_video.py
"""
Test GUI for displaying video files in place of PNGs using Tkinter.

Requirements:
    pip install opencv-python Pillow pyttsx3

Place your video files in the 'videos' folder (or update the path as needed).
"""
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import pyttsx3
import threading
import tempfile
import asyncio
import pygame
import edge_tts
import time
import random
import speech_recognition as sr

# List your video filenames here (update as needed)
VIDEO_FOLDER = 'ari_videos'
VIDEO_FILES = [
    f for f in os.listdir(VIDEO_FOLDER)
    if f.lower().endswith(('.mp4', '.avi', '.mov', '.webm'))
]

class VideoPlayer(tk.Tk):
    def __init__(self, video_files):
        super().__init__()
        self.title('Test Holo Face Video GUI')
        self.geometry('640x480')
        self.video_files = video_files
        self.current_video_idx = 0
        self.cap = None
        self.label = tk.Label(self)
        self.label.pack(expand=True)
        self.is_talking = False
        self.is_listening = False
        self.talking_animation_id = None
        self.current_video = self.video_files[0] if self.video_files else None
        if self.current_video:
            self.cap = cv2.VideoCapture(os.path.join(VIDEO_FOLDER, self.current_video))
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((640, 480))
                self.still_img = img
            else:
                self.still_img = Image.new('RGB', (640, 480), color='gray')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            self.still_img = Image.new('RGB', (640, 480), color='gray')
        print("[INFO] GUI window created and first video frame loaded.")
        self.show_still_frame()

    def play_video(self):
        if not self.cap:
            return
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.is_talking = True
        self.show_video_frame()

    def show_video_frame(self):
        if not (self.is_talking or self.is_listening) or not self.cap:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.config(image=imgtk)
            self.talking_animation_id = self.after(10, self.show_video_frame)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.show_video_frame()

    def show_still_frame(self):
        imgtk = ImageTk.PhotoImage(image=self.still_img)
        self.label.imgtk = imgtk
        self.label.config(image=imgtk)

    def start_talking(self):
        self.is_talking = True
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.show_video_frame()

    def stop_talking(self):
        self.is_talking = False
        if self.talking_animation_id:
            self.after_cancel(self.talking_animation_id)
            self.talking_animation_id = None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.show_still_frame()

    def start_listening(self):
        self.is_listening = True
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.show_still_frame()  # Show first frame, do not animate

    def stop_listening(self):
        self.is_listening = False
        if self.talking_animation_id:
            self.after_cancel(self.talking_animation_id)
            self.talking_animation_id = None
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.show_still_frame()

def ensure_pygame_mixer():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[ERROR] Could not initialize pygame mixer: {e}")

if __name__ == '__main__':
    print(f'[DEBUG] VIDEO_FILES found: {VIDEO_FILES}')
    if not VIDEO_FILES:
        print(f'[ERROR] No video files found in {VIDEO_FOLDER}. GUI will not start.')
    else:
        print('[DEBUG] Creating VideoPlayer GUI...')
        app = VideoPlayer(VIDEO_FILES)
        print('[DEBUG] VideoPlayer GUI created.')
        def speak_and_animate(text, asset_idx=None, delay=1000):
            print(f'[DEBUG] speak_and_animate called with text: {text}')
            def tts_and_play():
                async def tts_and_save():
                    voice = "en-GB-SoniaNeural"
                    tts = edge_tts.Communicate(text, voice)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        out_path = fp.name
                    await tts.save(out_path)
                    return out_path
                print('[DEBUG] Starting asyncio event loop for TTS...')
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                out_path = loop.run_until_complete(tts_and_save())
                loop.close()
                print(f'[DEBUG] TTS file created: {out_path}')
                for _ in range(20):
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                        break
                    time.sleep(0.1)
                if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                    print(f"[ERROR] TTS file not created: {out_path}")
                    app.stop_talking()
                    return
                def start_talking_animation():
                    print('[DEBUG] Starting talking animation...')
                    app.start_talking()
                    ensure_pygame_mixer()
                    pygame.mixer.music.load(out_path)
                    pygame.mixer.music.play()
                    def check_music():
                        if pygame.mixer.music.get_busy():
                            app.after(50, check_music)
                        else:
                            print('[DEBUG] TTS finished, stopping talking animation.')
                            app.stop_talking()
                            pygame.mixer.music.unload()
                            os.remove(out_path)
                    app.after(100, check_music)
                app.after(0, start_talking_animation)
            threading.Thread(target=tts_and_play, daemon=True).start()
        def listen_and_respond():
            def listen_thread():
                recognizer = sr.Recognizer()
                mic = sr.Microphone()
                while True:
                    app.start_listening()
                    print("[INFO] Listening for speech...")
                    with mic as source:
                        recognizer.adjust_for_ambient_noise(source)
                        try:
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                            app.stop_listening()
                            print("[INFO] Recognizing...")
                            text = recognizer.recognize_google(audio)
                            print(f"[USER] {text}")
                        except Exception as e:
                            app.stop_listening()
                            print(f"[ERROR] Listening: {e}")
                            text = "Sorry, I didn't catch that. Could you repeat?"
                        app.after(500, lambda t=text: speak_and_animate(t))
                        time.sleep(5)
            threading.Thread(target=listen_thread, daemon=True).start()
        def test_blend_talking_assets():
            talking_assets = [("video", v) for v in VIDEO_FILES]
            random.shuffle(talking_assets)
            def play_next(idx=0):
                if idx >= len(talking_assets):
                    print("[TEST] Finished showing all talking videos.")
                    app.show_still_frame()
                    return
                asset_type, asset = talking_assets[idx]
                label = f"Testing video {os.path.basename(asset)}"
                print(f"[TEST] {label}")
                def tts_and_show():
                    async def tts_and_save():
                        voice = "en-GB-SoniaNeural"
                        tts = edge_tts.Communicate(label, voice)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            out_path = fp.name
                        await tts.save(out_path)
                        return out_path
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    out_path = loop.run_until_complete(tts_and_save())
                    loop.close()
                    for _ in range(20):
                        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                            break
                        time.sleep(0.1)
                    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                        print(f"[ERROR] TTS file not created: {out_path}")
                        app.show_still_frame()
                        app.after(1000, lambda: play_next(idx+1))
                        return
                    def start_asset_and_tts():
                        app.start_talking()
                        ensure_pygame_mixer()
                        pygame.mixer.music.load(out_path)
                        pygame.mixer.music.play()
                        def check_music():
                            if pygame.mixer.music.get_busy():
                                app.after(50, check_music)
                            else:
                                app.stop_talking()  # Always show neutral face after TTS
                                pygame.mixer.music.unload()
                                os.remove(out_path)
                                app.after(400, lambda: play_next(idx+1))
                        app.after(50, check_music)
                    app.after(0, start_asset_and_tts)
                threading.Thread(target=tts_and_show, daemon=True).start()
            play_next()
        def test_conversation_loop():
            phrases = [
                "Hello, I am ARI. How can I help you today?",
                "Let me tell you a fun fact!",
                "Did you know honey never spoils?",
                "Would you like to hear a story or learn something new?",
                "I can answer your questions or have a conversation with you.",
                "Here's something interesting about the Eiffel Tower.",
                "What would you like to talk about next?",
                "Goodbye! Have a great day!",
            ]
            if not VIDEO_FILES:
                print("[TEST] No video files found.")
                return
            def play_next(idx=0):
                if idx >= len(phrases):
                    print("[TEST] Conversation loop finished. Showing neutral face.")
                    app.show_still_frame()
                    return
                phrase = phrases[idx % len(phrases)]
                print(f"[TEST] {phrase}")
                def tts_and_show():
                    async def tts_and_save():
                        voice = "en-GB-SoniaNeural"
                        tts = edge_tts.Communicate(phrase, voice)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            out_path = fp.name
                        await tts.save(out_path)
                        return out_path
                    print('[DEBUG] Starting asyncio event loop for TTS (test)...')
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    out_path = loop.run_until_complete(tts_and_save())
                    loop.close()
                    print(f'[DEBUG] TTS file created: {out_path}')
                    for _ in range(20):
                        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                            break
                        time.sleep(0.1)
                    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                        print(f"[ERROR] TTS file not created: {out_path}")
                        app.show_still_frame()
                        app.after(1000, lambda: play_next(idx+1))
                        return
                    def start_asset_and_tts():
                        print('[DEBUG] Starting talking animation (test)...')
                        app.start_talking()
                        ensure_pygame_mixer()
                        pygame.mixer.music.load(out_path)
                        pygame.mixer.music.play()
                        def check_music():
                            if pygame.mixer.music.get_busy():
                                app.after(50, check_music)
                            else:
                                print('[DEBUG] TTS finished, stopping talking animation (test).')
                                app.stop_talking()
                                pygame.mixer.music.unload()
                                os.remove(out_path)
                                app.after(50, lambda: play_next(idx+1))
                        app.after(50, check_music)
                    app.after(0, start_asset_and_tts)
                threading.Thread(target=tts_and_show, daemon=True).start()
            play_next()
        print('[DEBUG] Starting test_conversation_loop...')
        test_conversation_loop()
        print('[DEBUG] Entering app.mainloop()')
        app.mainloop()
