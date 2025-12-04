#!/usr/bin/env python3
"""
ARI Grass GUI - Animated grass visualization with real grass image background
"""
import tkinter as tk
import math
import random
from PIL import Image, ImageTk
import os

class ARIGrassGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARI - Grass Visualization")
        self.root.geometry("800x600")
        
        # Canvas for grass animation
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load animated grass GIF
        self.bg_image = None
        self.gif_frames = []
        self.current_frame = 0
        self.frame_delay = 50  # milliseconds between frames
        self.load_background_image()
        
        # Animation parameters
        self.speaking = False
        self.speaking_intensity = 0.0
        
        # Start animation
        self.animate_grass()
    
    def load_background_image(self):
        """Load the animated grass GIF"""
        try:
            image_path = os.path.join(os.path.dirname(__file__), 'grass_animated.gif')
            if os.path.exists(image_path):
                # Load animated GIF
                self.bg_image = Image.open(image_path)
                
                # Extract all frames
                try:
                    while True:
                        # Resize frame to fit canvas
                        frame = self.bg_image.copy()
                        frame = frame.resize((800, 600), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(frame)
                        self.gif_frames.append(photo)
                        self.bg_image.seek(len(self.gif_frames))
                except EOFError:
                    pass  # End of frames
                
                print(f"✅ Loaded animated grass: {image_path} ({len(self.gif_frames)} frames)")
            else:
                print(f"⚠️ Grass image not found: {image_path}")
                self.canvas.configure(bg='#87CEEB')  # Sky blue fallback
        except Exception as e:
            print(f"❌ Failed to load grass image: {e}")
            self.canvas.configure(bg='#87CEEB')  # Sky blue fallback
    
    def animate_grass(self):
        """Animate the grass GIF"""
        self.canvas.delete("all")
        
        # Draw current frame if available
        if self.gif_frames:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gif_frames[self.current_frame])
            
            # Advance to next frame
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            
            # Adjust speed when speaking
            delay = self.frame_delay
            if self.speaking:
                # Speed up animation when speaking
                delay = int(self.frame_delay * (0.5 + (1 - self.speaking_intensity) * 0.5))
        else:
            delay = self.frame_delay
        
        # Continue animation loop
        self.root.after(delay, self.animate_grass)
    
    def start_speaking(self):
        """Called when ARI starts speaking"""
        self.speaking = True
    
    def stop_speaking(self):
        """Called when ARI stops speaking"""
        self.speaking = False
        self.speaking_intensity = 0.0
    
    def update_speaking_intensity(self, amplitude):
        """Update wind intensity based on voice amplitude (0.0 to 1.0)"""
        self.speaking_intensity = amplitude
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
    
    def destroy(self):
        """Clean up and close"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass

if __name__ == "__main__":
    gui = ARIGrassGUI()
    gui.run()
