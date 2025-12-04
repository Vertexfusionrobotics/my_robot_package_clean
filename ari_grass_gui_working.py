#!/usr/bin/env python3
"""
ARI Grass GUI - Animated grass visualization for ARI assistant
"""
import tkinter as tk
import math
import random

class ARIGrassGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARI - Grass Visualization")
        self.root.geometry("800x600")
        self.root.configure(bg='#87CEEB')  # Sky blue background
        
        # Canvas for grass animation
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='#87CEEB', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animation parameters
        self.grass_blades = []
        self.wind_offset = 0
        self.speaking = False
        self.speaking_intensity = 0.0
        
        # Create grass
        self.create_grass_blades()
        
        # Start animation
        self.animate_grass()
    
    def create_grass_blades(self):
        """Create grass blade objects"""
        # Ground area
        ground_y = 400
        
        # Create 100 grass blades
        for i in range(100):
            x = random.randint(0, 800)
            height = random.randint(60, 120)
            width = random.randint(3, 6)
            color = random.choice(['#228B22', '#32CD32', '#00FF00', '#008000'])
            
            blade = {
                'x': x,
                'base_y': ground_y,
                'height': height,
                'width': width,
                'color': color,
                'sway_offset': random.uniform(0, math.pi * 2)
            }
            self.grass_blades.append(blade)
    
    def animate_grass(self):
        """Animate grass swaying in wind"""
        self.canvas.delete("all")
        
        # Update wind offset
        wind_speed = 0.05
        if self.speaking:
            wind_speed = 0.15 + (self.speaking_intensity * 0.2)
        
        self.wind_offset += wind_speed
        
        # Draw each grass blade
        for blade in self.grass_blades:
            x = blade['x']
            base_y = blade['base_y']
            height = blade['height']
            width = blade['width']
            
            # Calculate sway using sine wave
            sway = math.sin(self.wind_offset + blade['sway_offset']) * 20
            if self.speaking:
                sway *= (1.5 + self.speaking_intensity)
            
            # Draw blade as curved line (quadratic bezier curve)
            top_x = x + sway
            top_y = base_y - height
            mid_x = x + (sway / 2)
            mid_y = base_y - (height / 2)
            
            # Draw grass blade
            self.canvas.create_line(
                x, base_y,
                mid_x, mid_y,
                top_x, top_y,
                width=width,
                fill=blade['color'],
                smooth=True
            )
        
        # Continue animation
        self.root.after(30, self.animate_grass)
    
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
