# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import random
import os
import threading
import queue

class AriFaceGUI:
    def __init__(self, faces_folder, img_size=(800, 800)):
        self.faces_folder = faces_folder
        self.img_size = img_size
        self.root = tk.Tk()
        self.root.title("ARI Holographic Face")
        self.root.configure(bg="black")
        self.root.state('zoomed')  # Start maximized/fullscreen
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True, fill=tk.BOTH)
        # Subtitle label
        self.subtitle = tk.Label(self.root, text="", font=("Arial", 16), fg="#00ffff", bg="black")
        self.subtitle.pack(side=tk.BOTTOM, pady=5)
        # Map expressions to filenames (add more if you have them)
        self.expressions = {
            'neutral': 'ari_neutral(1).png',
            'neutral_alt': 'ari_neutral.png(1).png',
            'smiling': 'ari_smiling.png',
            'smiling_listening': 'ari_smiling_ listening.png',
            'smiling_talking': 'ari_smiling_talking.png',
            'listening': 'ari_ listening .png.png',
            'listening1': 'ari_listening.png',
            'listening2': 'ari_listening 2.png',
            'listening3': 'ari_listening(1).png',
            'talking': 'ari_talking.png',
            'talking_base': 'ari talking.png',
            'talking_dash': 'ari-talking.png',
            'talking1': 'ari_talking(1).png',
            'talking2': 'ari_talking(2).png',
            'talking3': 'ari_talking(3).png',
            'talking4': 'ari_talking(4).png',
            'talking5': 'ari_talking(5).png',
            'talking6': 'ari_talking(6).png',
            'talking7': 'ari_talking(7).png',
            'talking8': 'ari_talking(8).png',
            'talking9': 'ari_talking(9).png',
            'talking10': 'ari_talking(10).png',
            'talking11': 'ari_talking(11).png',
            'talking12': 'ari_talking(12).png',
            'talking13': 'ari_talking(13).png',
            'talking14': 'ari_talking(14).png',
            'talking15': 'ari_talking(15).png',
            'talking16': 'ari_talking(16).png',
            'talking17': 'ari_talking(17).png',
            'talking18': 'ari_talking(18).png',
            'talking19': 'ari_talking(19).png',
            'talking20': 'ari_talking(20).png',
            'talking21': 'ari_talking(21).png',
            'talking22': 'ari_talking(22).png',
            'talking23': 'ari_talking(23).png',
            'talking24': 'ari_talking(24).png',
            'talking25': 'ari_talking(25).png',
            'talking26': 'ari_talking(26).png',
            'talking27': 'ari_talking(27).png',
            'talking28': 'ari_talking(28).png',
            'talking29': 'ari_talking(29).png',
            'talking30': 'ari_talking(30).png',
            'talking31': 'ari_talking(31).png',
            'confused': 'ari_confused.png.png',
            'looking_around': 'ari_looking_ around.png.png',
            'thinking': 'ari_thinking.png',
            'suprised': 'ari_suprised.png',
        }
        self.base_imgs = {k: self.load_img(v) for k, v in self.expressions.items()}
        print('Loaded base face images:')
        for k, v in self.base_imgs.items():
            print(f'  {k}:', 'OK' if v else 'NOT FOUND')
        self.current_expression = 'neutral'
        self.mouth_moving = False
        self.blink_state = False
        self.running = True
        self.eye_pos = (0, 0)  # (x, y) offset for eye movement
        self.idle_timer = None
        self._talking = False
        self._talking_idx = 0
        self._talking_keys = ['talking', 'talking1', 'talking2']
        self.anim_speed = 200
        self.command_queue = queue.Queue()
        self.root.bind('<Configure>', self.on_resize)
        self.update_face()
        self.root.after(random.randint(1200, 2500), self.blink)
        self.root.after(3000, self.idle_animation)
        self.root.after(50, self.process_queue)

    def load_img(self, name):
        path = os.path.join(self.faces_folder, name)
        if os.path.exists(path):
            return Image.open(path).convert("RGBA")
        return None

    def show_expression(self, expr):
        if expr in self.base_imgs and self.base_imgs[expr]:
            self.current_expression = expr
            self.update_face()

    def process_queue(self):
        while not self.command_queue.empty():
            cmd, args = self.command_queue.get()
            if cmd == 'set_expression':
                self.show_expression(*args)
            elif cmd == 'set_subtitle':
                self.subtitle.config(text=args[0])
            elif cmd == 'start_talking_animation':
                self._start_talking_animation_main(*args)
            elif cmd == 'stop_talking_animation':
                self._stop_talking_animation_main(*args)
        self.root.after(50, self.process_queue)

    def set_expression(self, expr):
        self.command_queue.put(('set_expression', (expr,)))

    def set_subtitle(self, text):
        self.command_queue.put(('set_subtitle', (text,)))

    def animate_talking(self, interval=None):
        self.mouth_moving = True
        self.update_face()
        self.root.after(interval or self.anim_speed//2, self.stop_talking)

    def stop_talking(self):
        self.mouth_moving = False
        self.update_face()

    def blink(self):
        if not self.running:
            return
        self.blink_state = not self.blink_state
        self.update_face()
        self.root.after(random.randint(1200, 2500), self.blink)

    def move_eyes(self, x, y):
        self.eye_pos = (x, y)
        self.update_face()

    def idle_animation(self):
        if not self.running or self._talking:
            return
        # Use all available idle/listening/other expressions
        action = random.choice([
            'look', 'neutral', 'tilt', 'listening', 'listening1', 'listening2', 'listening3',
            'smiling_listening', 'confused', 'looking_around', 'thinking', 'suprised'
        ])
        if action == 'look':
            ex = random.randint(-10, 10)
            ey = random.randint(-10, 10)
            self.move_eyes(ex, ey)
            self.root.after(800, lambda: self.move_eyes(0, 0))
        elif action == 'tilt':
            self.update_face(jitter=True)
            self.root.after(600, lambda: self.update_face(jitter=False))
        else:
            self.show_expression(action)
            self.root.after(1200, lambda: self.show_expression('neutral'))
        self.idle_timer = self.root.after(random.randint(2500, 5000), self.idle_animation)

    def update_face(self, jitter=False):
        # Dynamically get current window size
        width = self.label.winfo_width() or self.img_size[0]
        height = self.label.winfo_height() or self.img_size[1]
        base = self.base_imgs.get(self.current_expression, self.base_imgs.get('neutral'))
        if not base:
            return
        # Resize to fit window
        img = base.resize((width, height), Image.Resampling.LANCZOS)
        brightness = random.uniform(0.85, 1.15)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        glow_intensity = random.randint(30, 80)
        glow = Image.new("RGBA", img.size, (0, 180, 255, glow_intensity))
        img_with_glow = Image.alpha_composite(img, glow)
        draw = ImageDraw.Draw(img_with_glow)
        for y in range(0, height, 4):
            line_alpha = random.randint(10, 30)
            draw.line([(0, y), (width, y)], fill=(0, 255, 255, line_alpha), width=1)
        ex, ey = self.eye_pos
        ex = int(ex * 1.2)
        ey = int(ey * 1.2)
        jitter_x = random.randint(-2, 2) + (5 if jitter else 0) + ex
        jitter_y = random.randint(-2, 2) + (5 if jitter else 0) + ey
        final_img = Image.new("RGBA", (width, height), (0,0,0,255))
        final_img.paste(img_with_glow, (jitter_x, jitter_y), img_with_glow)
        photo = ImageTk.PhotoImage(final_img)
        self.label.config(image=photo)
        self.label.image = photo

    def on_resize(self, event):
        self.img_size = (event.width, event.height)
        self.update_face()

    def close(self):
        self.running = False
        if self.idle_timer:
            self.root.after_cancel(self.idle_timer)
        self.root.quit()

    def _start_talking_animation_main(self, interval=None):
        self._talking = True
        self._talking_idx = 0
        keys = []
        for k in ['talking', 'talking_base', 'talking_dash']:
            if k in self.base_imgs and self.base_imgs[k]:
                keys.append(k)
        for i in range(1, 32):
            k = f'talking{i}'
            if k in self.base_imgs and self.base_imgs[k]:
                keys.append(k)
        if not keys:
            keys = ['neutral']
        self._talking_keys = keys
        def animate():
            if not self._talking:
                return
            expr = self._talking_keys[self._talking_idx % len(self._talking_keys)]
            self.show_expression(expr)
            self._talking_idx += 1
            self.root.after(interval or self.anim_speed, animate)
        animate()
        # Cancel idle while talking
        if self.idle_timer:
            self.root.after_cancel(self.idle_timer)
            self.idle_timer = None

    def _stop_talking_animation_main(self, after_expr='neutral'):
        self._talking = False
        self.show_expression(after_expr)
        # Resume idle after talking
        if not self.idle_timer:
            self.idle_timer = self.root.after(random.randint(2500, 5000), self.idle_animation)

    # API for robot logic
    def speak(self, text):
        def do_speak():
            self.command_queue.put(('start_talking_animation', (150,)))
            from pyttsx3 import init
            engine = init()
            # Print all available voices for debug
            voices = engine.getProperty('voices')
            print("Available voices:")
            for v in voices:
                gender = getattr(v, 'gender', None)
                gender_str = gender if isinstance(gender, str) else 'unknown'
                print(f"  id: {v.id}\n    name: {v.name}\n    gender: {gender_str}\n    languages: {getattr(v, 'languages', 'unknown')}")
            # Try to select a female voice by name (Hazel, Zira, etc.)
            selected_voice = None
            for v in voices:
                name = v.name.lower() if hasattr(v, 'name') and v.name else ''
                if any(female in name for female in ['zira', 'hazel', 'jenny', 'eva', 'susan', 'helen', 'linda', 'mary']):
                    selected_voice = v
                    break
            if selected_voice:
                engine.setProperty('voice', selected_voice.id)
                print(f"Selected female voice: {selected_voice.name} (id: {selected_voice.id})")
            else:
                print("No female voice found, using default.")
            engine.say(text)
            engine.runAndWait()
            self.command_queue.put(('stop_talking_animation', ('neutral',)))
            self.command_queue.put(('set_expression', ('smiling',)))
            self.root.after(1200, lambda: self.set_expression('neutral'))
        threading.Thread(target=do_speak, daemon=True).start()

# Minimal automated demo: just show the face and run idle/auto behaviors
if __name__ == "__main__":
    face = AriFaceGUI(r"C:\Users\Tyrell Murray\Documents\my_robot_package_clean\ari_faces_split")
    face.set_subtitle("Voice demo: ARI is always voice-activated. Say something!")
    # Speak a sample phrase with synchronized talking animation
    face.speak("Hello! I am ARI. I am always listening for your voice. This is a synchronized talking demo.")
    face.root.mainloop()
