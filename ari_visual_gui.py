# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Visual GUI - Avatar Display System with Real-Time Monitoring
Provides visual representation of ARI with futuristic monitoring overlays.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk
import os
import random
import psutil
import math

class ARIVisualGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARI - AI Assistant")
        
        # Initialize camera feed state
        self.setup_camera_feed_pending = False  # Don't auto-start camera
        self.camera_feed_active = False
        
        # Get screen dimensions first
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Start in windowed mode for testing (can use standard Windows controls)
        # Set to a large window size (fullscreen functionality removed)
        window_width = int(self.screen_width * 0.8)  # 80% of screen width for better visibility
        window_height = int(self.screen_height * 0.8)  # 80% of screen height 
        x_offset = (self.screen_width - window_width) // 2
        y_offset = (self.screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
        self.root.title("ARI - AI Assistant - AVATAR ACTIVE")
        
        # Add proper window close handling to prevent hanging
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Make window more prominent and ensure it's visible
        self.root.deiconify()  # Ensure not minimized
        self.root.lift()       # Bring to front
        self.root.focus_force()  # Force focus
        self.root.attributes('-topmost', True)  # Temporarily on top
        
        # Flash the taskbar icon to get attention (Windows)
        try:
            self.root.attributes('-toolwindow', False)  # Make sure it shows in taskbar
            self.root.iconify()  # Minimize briefly
            self.root.deiconify()  # Restore - this causes a taskbar flash
        except:
            pass
            
        self.root.after(3000, lambda: self.root.attributes('-topmost', False))  # Remove topmost after 3 seconds
        
        print(f"🎨 ARI GUI window created - Size: {window_width}x{window_height} at position ({x_offset}, {y_offset})")
        print("🎨 GUI should be visible on screen now!")
        
        # Always run in windowed mode (fullscreen functionality removed)
        self.root.resizable(True, True)  # Allow resizing
        
        # Initialize animation control first
        self.animation_running = True
        self.avatar_frames = []
        self.current_frame = 0
        self.animation_speed = 100  # milliseconds between frames
        self.is_speaking = False
        self.is_listening = False
        self.is_processing = False
        self.user_speaking = False  # New state for when user is talking
        
        # Real-time monitoring data
        self.audio_level = 0.0
        self.system_cpu = 0.0
        self.system_memory = 0.0
        self.consciousness_level = 0.85
        self.vision_active = True
        self.microphone_active = True
        
        # Audio activity tracking
        self.audio_activity = {
            'microphone': 'inactive',
            'speaker': 'inactive',
            'level': 0.0
        }
        
        # Load the GIF first
        self.load_avatar_gif()
        
        # Create GUI elements (will set background color)
        self.setup_gui()
        
        # Start the animation and monitoring immediately - ALWAYS
        self.root.after(10, self.animate_avatar)  # Start animation IMMEDIATELY
        self.root.after(20, self.start_monitoring)  # Start monitoring IMMEDIATELY
        
        # Force initial display of the first frame
        if self.avatar_frames:
            self.avatar_label.configure(image=self.avatar_frames[0])
            self.root.update()
            self.root.update_idletasks()
        
        # Add keyboard controls
        # Only keep Escape to close the application
        self.root.bind('<Escape>', self.close_application)
        self.root.focus_set()  # Make sure window can receive key events
        # Camera feed integration
        self.camera_label = None
        self.camera_running = False
        self.camera_thread = None
        self.setup_camera_feed_pending = True  # Delay camera setup until GUI elements are ready
    
    def load_avatar_gif(self):
        """Load the avatar GIF and extract frames"""
        try:
            gif_path = "ari_avatar_video.gif"
            if not os.path.exists(gif_path):
                print(f"❌ Avatar GIF not found: {gif_path}")
                return
            
            # Open the GIF and extract all frames
            gif = Image.open(gif_path)
            
            # Calculate size to fill screen while maintaining aspect ratio
            gif_width, gif_height = gif.size
            
            # Scale to fill the entire screen
            scale_x = self.screen_width / gif_width
            scale_y = self.screen_height / gif_height
            scale = max(scale_x, scale_y)  # Use larger scale to fill screen completely
            
            new_width = int(gif_width * scale)
            new_height = int(gif_height * scale)
            
            print(f"📐 Screen: {self.screen_width}x{self.screen_height}")
            print(f"📐 Scaling GIF to: {new_width}x{new_height}")
            
            # Get all frames from the animated GIF
            frame_count = 0
            try:
                while True:
                    # Convert frame to PhotoImage for tkinter
                    frame = gif.copy()
                    frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(frame)
                    self.avatar_frames.append(photo)
                    frame_count += 1
                    
                    # Move to next frame
                    gif.seek(frame_count)
            except EOFError:
                # End of frames
                pass
            
            print(f"✅ Loaded {len(self.avatar_frames)} frames from avatar GIF")
            
        except Exception as e:
            print(f"❌ Error loading avatar GIF: {e}")
            # Create a simple placeholder if GIF fails to load
            self.create_placeholder_avatar()
    
    def get_gif_background_color(self):
        """Extract the dominant background color from the GIF"""
        try:
            if self.avatar_frames:
                # Get the first frame and analyze its background
                # For now, we'll use a common background color that works well
                # You can adjust this based on your specific GIF
                return '#1a1a1a'  # Dark gray that works with most avatars
            else:
                return 'black'  # Fallback to black
        except:
            return 'black'  # Safe fallback

    def create_placeholder_avatar(self):
        """Create a simple placeholder if GIF loading fails"""
        # Create a placeholder that fills the screen
        placeholder = Image.new('RGB', (self.screen_width, self.screen_height), color='blue')
        photo = ImageTk.PhotoImage(placeholder)
        self.avatar_frames = [photo]
    
    def setup_gui(self):
        """Setup the GUI elements with futuristic monitoring overlays"""
        # Get the background color from the GIF
        self.bg_color = self.get_gif_background_color()
        
        # Set the window background to match the GIF (not the bright blue)
        self.root.configure(bg=self.bg_color)
        
        # Avatar display - fills the entire screen (ARI stays untouched)
        self.avatar_label = tk.Label(
            self.root, 
            bg=self.bg_color, 
            bd=0, 
            highlightthickness=0,
            width=self.screen_width,
            height=self.screen_height
        )
        self.avatar_label.pack(fill='both', expand=True)
        
        # Show the first frame immediately
        if self.avatar_frames:
            self.avatar_label.configure(image=self.avatar_frames[0])
        
        # Create futuristic monitoring overlays
        self.create_monitoring_overlays()
        # Add camera feed panel (right side, below vision overlay)
        self.camera_label = tk.Label(self.root, bg='black', text="Camera Feed Initializing...", fg='white')
        cam_width = 320  # Increased size for better visibility
        cam_height = 240
        # Vision overlay is at x=self.screen_width-190, y=self.screen_height//2-100, height=200
        # Place camera feed just below: y=self.screen_height//2+110
        self.camera_label.place(x=self.screen_width-330, y=self.screen_height//2+110, width=cam_width, height=cam_height)
        # Now start camera feed after GUI elements are ready
        if self.setup_camera_feed_pending:
            self.setup_camera_feed()
            self.setup_camera_feed_pending = False
        # Now start camera feed after GUI elements are ready
        if self.setup_camera_feed_pending:
            self.setup_camera_feed()
            self.setup_camera_feed_pending = False
    def setup_camera_feed(self):
        """Start the camera feed in a background thread and update the GUI label."""
        import cv2
        from PIL import Image, ImageTk
        import time

        try:
            # Check if we already have a camera running
            if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
                print("[GUI Camera] Camera already initialized")
                return True

            from ari_visual_recognition import ARIVisualRecognition
            if not hasattr(self, 'vision_system'):
                # Create vision system in GUI mode so it won't auto-start camera
                self.vision_system = ARIVisualRecognition(gui_mode=True)
            
            print("[GUI Camera] Opening camera feed...")
            
            # Open camera directly in GUI rather than through vision system
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("[GUI Camera] Could not open camera directly.")
                if hasattr(self, 'camera_label'):
                    self.camera_label.configure(text="Camera not available")
                return False
            
            # Give vision system access to our camera
            self.vision_system.camera = self.cap
            self.vision_system.camera_active = True
            print("[GUI Camera] Camera initialized successfully")
            return True
            
        except Exception as e:
            print(f"[GUI Camera] Error setting up camera: {e}")
            if hasattr(self, 'camera_label'):
                self.camera_label.configure(text="Camera Error")
            return False

        print("[GUI Camera] Camera initialized successfully")
        self.camera_running = True

        def update_camera_frame():
            if not self.camera_running:
                return
                
            try:
                ret, frame = self.cap.read()
                if ret:
                    # Convert BGR to RGB and resize
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (320, 240))
                    
                    # Convert to PhotoImage
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    
                    # Update label with new image
                    if self.camera_label and self.camera_label.winfo_exists():
                        self.camera_label.configure(image=imgtk)
                        self.camera_label.image = imgtk  # Keep reference!
                
                # Schedule next update if still running
                if self.camera_running and self.root.winfo_exists():
                    self.root.after(30, update_camera_frame)
                    
            except Exception as e:
                print(f"Camera update error: {e}")
                if self.camera_running and self.root.winfo_exists():
                    self.root.after(1000, update_camera_frame)  # Retry after 1 second on error
            
            # Schedule next update if still running
            if self.camera_running and self.root.winfo_exists():
                self.root.after(30, update_camera_frame)
        
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[GUI Camera] Could not open camera.")
            return
            
        print("[Camera Feed] Starting camera feed in GUI...")
        self.camera_running = True

        # Schedule next frame update
        if self.camera_running and self.root.winfo_exists():
            self.root.after(30, update_camera_frame)  # Update every 30ms (~33 fps)
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("[GUI Camera] Could not open camera.")
            return
            
        # Start the camera updates
        self.root.after(0, update_camera_frame)
        return True
    
    def create_monitoring_overlays(self):
        """Create professional, futuristic monitoring displays"""
        # Futuristic color scheme with sci-fi transparent effects
        self.colors = {
            'primary': '#00FFFF',      # Cyan
            'secondary': '#FFA500',    # Amber/Orange  
            'success': '#00FF41',      # Matrix Green
            'warning': '#FFFF00',      # Yellow
            'error': '#FF0040',        # Red
            'bg_overlay': '#001122',   # Dark blue-teal for sci-fi glass effect
            'bg_transparent': '#000a1a',  # Very dark with blue tint for transparency
            'glass_overlay': '#003344', # Lighter blue for glass borders
            'text_dim': '#4080FF'      # Dim blue
        }
        
        # Fonts
        self.fonts = {
            'small': ('Consolas', 8, 'normal'),
            'medium': ('Consolas', 10, 'bold'),
            'large': ('Consolas', 12, 'bold')
        }
        
        # TOP CENTER - Control Panel with minimize button
        self.create_control_panel()
        
        # TOP LEFT - System Status
        self.create_top_left_overlay()
        
        # TOP RIGHT - Consciousness Level
        self.create_top_right_overlay()
        
        # LEFT SIDE - Audio Monitoring
        self.create_left_audio_overlay()
        
        # RIGHT SIDE - Vision Status
        self.create_right_vision_overlay()
        
        # BOTTOM - System Performance Strip
        self.create_bottom_performance_overlay()
    
    def create_control_panel(self):
        """Create control panel with exit button only - top center"""
        control_panel = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1,
                                highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        control_panel.place(x=self.screen_width//2-60, y=10, width=120, height=35)  # Smaller width - only exit button
        
        # Control buttons frame
        buttons_frame = tk.Frame(control_panel, bg=self.colors['bg_transparent'])
        buttons_frame.pack(expand=True, fill='both', pady=3)
        
        # Only keep the exit button - fullscreen functionality removed
        
        # Exit button
        exit_btn = tk.Button(buttons_frame, text="✕", 
                           font=('Consolas', 10, 'bold'),
                           fg=self.colors['error'], bg=self.colors['bg_transparent'],
                           bd=1, highlightthickness=1,
                           highlightbackground=self.colors['glass_overlay'],
                           command=self.close_application,
                           width=3, height=1)
        exit_btn.pack(side='left', padx=5)
        
        # Status indicator (removed fullscreen mode indicator)
        self.status_label = tk.Label(buttons_frame, text="ARI ACTIVE", 
                                 font=self.fonts['small'], 
                                 fg=self.colors['success'], 
                                 bg=self.colors['bg_transparent'])
        self.status_label.pack(side='right', padx=10)
    
    def create_top_left_overlay(self):
        """System status overlay - top left corner with sci-fi glass effect"""
        # Create glass panel effect
        overlay = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1, 
                          highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        overlay.place(x=10, y=10, width=200, height=80)
        
        # Title with futuristic styling
        title = tk.Label(overlay, text="SYSTEM STATUS", 
                        font=self.fonts['small'], 
                        fg=self.colors['primary'], 
                        bg=self.colors['bg_transparent'])
        title.pack(pady=2)
        
        # Status indicators
        self.system_status_label = tk.Label(overlay, text="● OPERATIONAL", 
                                          font=self.fonts['small'], 
                                          fg=self.colors['success'], 
                                          bg=self.colors['bg_transparent'])
        self.system_status_label.pack()
        
        self.neural_status_label = tk.Label(overlay, text="● NEURAL ACTIVE", 
                                          font=self.fonts['small'], 
                                          fg=self.colors['primary'], 
                                          bg=self.colors['bg_transparent'])
        self.neural_status_label.pack()
        
        self.transcendent_status_label = tk.Label(overlay, text="● TRANSCENDENT", 
                                                font=self.fonts['small'], 
                                                fg=self.colors['secondary'], 
                                                bg=self.colors['bg_transparent'])
        self.transcendent_status_label.pack()
    
    def create_top_right_overlay(self):
        """Consciousness level overlay - top right corner with sci-fi glass effect"""
        overlay = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1,
                          highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        overlay.place(x=self.screen_width-210, y=10, width=200, height=80)
        
        # Title
        title = tk.Label(overlay, text="CONSCIOUSNESS", 
                        font=self.fonts['small'], 
                        fg=self.colors['primary'], 
                        bg=self.colors['bg_transparent'])
        title.pack(pady=2)
        
        # Consciousness level
        self.consciousness_label = tk.Label(overlay, text="LEVEL: 0.850", 
                                          font=self.fonts['medium'], 
                                          fg=self.colors['secondary'], 
                                          bg=self.colors['bg_transparent'])
        self.consciousness_label.pack()
        
        # Status
        self.awareness_label = tk.Label(overlay, text="TRANSCENDENT ACTIVE", 
                                      font=self.fonts['small'], 
                                      fg=self.colors['success'], 
                                      bg=self.colors['bg_transparent'])
        self.awareness_label.pack()
    
    def create_left_audio_overlay(self):
        """Audio monitoring overlay - left side with sci-fi glass effect"""
        overlay = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1,
                          highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        overlay.place(x=10, y=self.screen_height//2-100, width=180, height=200)
        
        # Title
        title = tk.Label(overlay, text="AUDIO MONITOR", 
                        font=self.fonts['small'], 
                        fg=self.colors['primary'], 
                        bg=self.colors['bg_transparent'])
        title.pack(pady=2)
        
        # Microphone status
        self.mic_status_label = tk.Label(overlay, text="🎤 ACTIVE", 
                                       font=self.fonts['small'], 
                                       fg=self.colors['success'], 
                                       bg=self.colors['bg_transparent'])
        self.mic_status_label.pack()
        
        # Audio level display
        self.audio_level_label = tk.Label(overlay, text="LEVEL: 0%", 
                                        font=self.fonts['small'], 
                                        fg=self.colors['text_dim'], 
                                        bg=self.colors['bg_transparent'])
        self.audio_level_label.pack()
        
        # Visual audio bars
        self.audio_bars_frame = tk.Frame(overlay, bg=self.colors['bg_transparent'])
        self.audio_bars_frame.pack(pady=5)
        
        self.audio_bars = []
        for i in range(10):
            bar = tk.Label(self.audio_bars_frame, text="▌", 
                          font=('Consolas', 8), 
                          fg=self.colors['text_dim'], 
                          bg=self.colors['bg_transparent'])
            bar.grid(row=0, column=i)
            self.audio_bars.append(bar)
        
        # Speech detection
        self.speech_label = tk.Label(overlay, text="SPEECH: NONE", 
                                   font=self.fonts['small'], 
                                   fg=self.colors['text_dim'], 
                                   bg=self.colors['bg_transparent'])
        self.speech_label.pack()
    
    def create_right_vision_overlay(self):
        """Vision monitoring overlay - right side with sci-fi glass effect"""
        overlay = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1,
                          highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        overlay.place(x=self.screen_width-190, y=self.screen_height//2-100, width=180, height=200)
        
        # Title
        title = tk.Label(overlay, text="VISION SYSTEM", 
                        font=self.fonts['small'], 
                        fg=self.colors['primary'], 
                        bg=self.colors['bg_transparent'])
        title.pack(pady=2)
        
        # Camera status
        self.camera_status_label = tk.Label(overlay, text="📷 ACTIVE", 
                                          font=self.fonts['small'], 
                                          fg=self.colors['success'], 
                                          bg=self.colors['bg_transparent'])
        self.camera_status_label.pack()
        
        # Face detection
        self.face_detection_label = tk.Label(overlay, text="FACES: 0", 
                                           font=self.fonts['small'], 
                                           fg=self.colors['text_dim'], 
                                           bg=self.colors['bg_transparent'])
        self.face_detection_label.pack()
        
        # Object detection
        self.object_detection_label = tk.Label(overlay, text="OBJECTS: 0", 
                                             font=self.fonts['small'], 
                                             fg=self.colors['text_dim'], 
                                             bg=self.colors['bg_transparent'])
        self.object_detection_label.pack()
        
        # Scene analysis
        self.scene_label = tk.Label(overlay, text="SCENE: ANALYZING", 
                                  font=self.fonts['small'], 
                                  fg=self.colors['text_dim'], 
                                  bg=self.colors['bg_transparent'])
        self.scene_label.pack()
    
    def create_bottom_performance_overlay(self):
        """System performance strip - bottom of screen with sci-fi glass effect"""
        overlay = tk.Frame(self.root, bg=self.colors['bg_transparent'], bd=1,
                          highlightthickness=1, highlightbackground=self.colors['glass_overlay'])
        overlay.place(x=200, y=self.screen_height-40, width=self.screen_width-400, height=35)
        
        # Performance indicators in a horizontal layout
        perf_frame = tk.Frame(overlay, bg=self.colors['bg_transparent'])
        perf_frame.pack(expand=True, fill='x', pady=5)
        
        # CPU
        self.cpu_label = tk.Label(perf_frame, text="CPU: 0%", 
                                font=self.fonts['small'], 
                                fg=self.colors['text_dim'], 
                                bg=self.colors['bg_transparent'])
        self.cpu_label.pack(side='left', padx=20)
        
        # Memory
        self.memory_label = tk.Label(perf_frame, text="MEM: 0%", 
                                   font=self.fonts['small'], 
                                   fg=self.colors['text_dim'], 
                                   bg=self.colors['bg_transparent'])
        self.memory_label.pack(side='left', padx=20)
        
        # Response time
        self.response_label = tk.Label(perf_frame, text="RESPONSE: 0ms", 
                                     font=self.fonts['small'], 
                                     fg=self.colors['text_dim'], 
                                     bg=self.colors['bg_transparent'])
        self.response_label.pack(side='left', padx=20)
        
        # Neural networks
        self.neural_label = tk.Label(perf_frame, text="NEURAL: ACTIVE", 
                                   font=self.fonts['small'], 
                                   fg=self.colors['success'], 
                                   bg=self.colors['bg_transparent'])
        self.neural_label.pack(side='left', padx=20)
        
        # Timestamp
        self.timestamp_label = tk.Label(perf_frame, text="", 
                                      font=self.fonts['small'], 
                                      fg=self.colors['text_dim'], 
                                      bg=self.colors['bg_transparent'])
        self.timestamp_label.pack(side='right', padx=20)
    
    def close_application(self, event=None):
        """Close the application"""
        print("🔄 GUI: Close application called")
        self.stop()
        # Force exit if needed
        import sys
        sys.exit(0)
    
    def animate_avatar(self):
        """Animate the avatar GIF with different speeds based on state"""
        if not self.animation_running or not self.avatar_frames:
            return
        
        # Get current frame and update the avatar label
        frame = self.avatar_frames[self.current_frame]
        self.avatar_label.configure(image=frame)
        
        # Force the update to happen immediately
        try:
            self.root.update_idletasks()
            self.root.update()  # Force immediate screen update
        except:
            pass
        
        # Calculate animation speed based on state with VERY dramatic differences
        if self.user_speaking:
            speed = 400  # Very slow when user talks (almost still)
        elif self.is_speaking:
            speed = 15   # Super fast when ARI talks (very animated)
        elif self.is_processing:
            speed = 40   # Fast when processing
        elif self.is_listening:
            speed = 200  # Slow, attentive when listening
        else:
            speed = self.animation_speed  # Normal idle speed (100ms)
        
        # Move to next frame
        self.current_frame = (self.current_frame + 1) % len(self.avatar_frames)
        
        # Schedule next frame - this is the critical part that makes it animate
        if self.animation_running:
            self.root.after(speed, self.animate_avatar)
    
    def start_monitoring(self):
        """Start real-time monitoring updates"""
        self.update_monitoring_data()
    
    def update_monitoring_data(self):
        """Update all monitoring displays with real-time data"""
        if not self.animation_running:
            return
        
        try:
            # Update system performance
            self.system_cpu = psutil.cpu_percent()
            self.system_memory = psutil.virtual_memory().percent
            
            # Audio levels are now controlled by state changes from external systems
            # Add some variation to make it look more realistic
            if self.is_speaking:
                # High activity with variation when ARI is speaking
                self.audio_level = random.uniform(0.7, 1.0)
            elif self.user_speaking:
                # High activity when user is speaking
                self.audio_level = random.uniform(0.6, 0.9)
            elif self.is_listening:
                # Medium activity when listening
                self.audio_level = random.uniform(0.2, 0.5)
            elif self.is_processing:
                # Low activity when processing
                self.audio_level = random.uniform(0.1, 0.3)
            else:
                # Minimal activity when idle
                self.audio_level = random.uniform(0.0, 0.15)
            
            # Update consciousness level with slight variations
            base_consciousness = 0.85
            variation = random.uniform(-0.02, 0.02)
            self.consciousness_level = max(0.0, min(1.0, base_consciousness + variation))
            
            # Update all displays
            self.update_system_status()
            self.update_consciousness_display()
            self.update_audio_display()
            self.update_vision_display()
            self.update_performance_display()
            
        except Exception as e:
            print(f"Monitoring error: {e}")
        
        # Schedule next update
        self.root.after(100, self.update_monitoring_data)  # Update every 100ms
    
    def update_system_status(self):
        """Update system status indicators"""
        # System operational status
        if self.system_cpu < 80:
            self.system_status_label.configure(text="● OPERATIONAL", fg=self.colors['success'])
        else:
            self.system_status_label.configure(text="● HIGH LOAD", fg=self.colors['warning'])
    
    def update_consciousness_display(self):
        """Update consciousness level display"""
        level_text = f"LEVEL: {self.consciousness_level:.3f}"
        self.consciousness_label.configure(text=level_text)
        
        # Color based on consciousness level
        if self.consciousness_level > 0.9:
            color = self.colors['success']
        elif self.consciousness_level > 0.7:
            color = self.colors['secondary']
        else:
            color = self.colors['warning']
        
        self.consciousness_label.configure(fg=color)
    
    def update_audio_display(self):
        """Update audio monitoring display"""
        # Update audio level percentage
        level_percent = int(self.audio_level * 100)
        self.audio_level_label.configure(text=f"LEVEL: {level_percent}%")
        
        # Update visual audio bars
        active_bars = int(self.audio_level * 10)
        for i, bar in enumerate(self.audio_bars):
            if i < active_bars:
                if self.audio_level > 0.7:
                    color = self.colors['warning']
                elif self.audio_level > 0.4:
                    color = self.colors['secondary']
                else:
                    color = self.colors['success']
                bar.configure(fg=color)
            else:
                bar.configure(fg=self.colors['text_dim'])
        
        # Update speech detection
        if self.user_speaking:
            self.speech_label.configure(text="SPEECH: USER", fg=self.colors['success'])
        elif self.is_speaking:
            self.speech_label.configure(text="SPEECH: ARI", fg=self.colors['secondary'])
        else:
            self.speech_label.configure(text="SPEECH: NONE", fg=self.colors['text_dim'])
    
    def update_vision_display(self):
        """Update vision system display"""
        # Simulate vision data (replace with actual vision system data later)
        face_count = random.randint(0, 2) if self.vision_active else 0
        object_count = random.randint(0, 5) if self.vision_active else 0
        
        self.face_detection_label.configure(text=f"FACES: {face_count}")
        self.object_detection_label.configure(text=f"OBJECTS: {object_count}")
        
        # Scene analysis
        scenes = ["ANALYZING", "INDOOR", "OFFICE", "PERSON", "UNKNOWN"]
        scene = random.choice(scenes)
        self.scene_label.configure(text=f"SCENE: {scene}")
    
    def update_performance_display(self):
        """Update system performance strip"""
        # CPU
        self.cpu_label.configure(text=f"CPU: {self.system_cpu:.1f}%")
        if self.system_cpu > 80:
            self.cpu_label.configure(fg=self.colors['warning'])
        else:
            self.cpu_label.configure(fg=self.colors['text_dim'])
        
        # Memory
        self.memory_label.configure(text=f"MEM: {self.system_memory:.1f}%")
        if self.system_memory > 80:
            self.memory_label.configure(fg=self.colors['warning'])
        else:
            self.memory_label.configure(fg=self.colors['text_dim'])
        
        # Response time (simulated)
        response_time = random.randint(50, 200)
        self.response_label.configure(text=f"RESPONSE: {response_time}ms")
        
        # Timestamp
        current_time = time.strftime("%H:%M:%S")
        self.timestamp_label.configure(text=current_time)
    
    def set_speaking_state(self, speaking=True):
        """Set ARI to speaking state"""
        self.is_speaking = speaking
        self.is_listening = False
        self.is_processing = False
        self.user_speaking = False
        
        # Trigger audio activity
        self.set_audio_activity('speaking', speaking)
        
        # Add visual feedback for speaking state
        if speaking:
            self.add_visual_effect('speaking')
        else:
            self.clear_visual_effects()
    
    def set_listening_state(self, listening=True):
        """Set ARI to listening state"""
        self.is_listening = listening
        self.is_speaking = False
        self.is_processing = False
        
        # Trigger audio activity
        self.set_audio_activity('listening', listening)
        
        # Update audio device activity
        if listening:
            self.audio_activity['microphone'] = 'active'
            self.add_visual_effect('listening')
        else:
            self.audio_activity['microphone'] = 'inactive'
            self.clear_visual_effects()
    
    def set_processing_state(self, processing=True):
        """Set ARI to processing state"""
        self.is_processing = processing
        self.is_speaking = False
        self.is_listening = False
        
        # Low audio activity when processing
        if processing:
            self.set_audio_activity('processing', True)
            self.add_visual_effect('processing')
        else:
            self.set_audio_activity('idle', True)
            self.clear_visual_effects()
    
    def set_user_speaking_state(self, user_speaking=True):
        """Set user speaking state (ARI listening attentively)"""
        # Use thread-safe GUI updates
        def _update_user_speaking_state():
            self.user_speaking = user_speaking
            self.is_speaking = False
            self.is_listening = user_speaking  # ARI is listening when user speaks
            self.is_processing = False
            # Trigger audio activity
            self.set_audio_activity('user_speaking', user_speaking)
            # Add visual feedback
            if user_speaking:
                self.add_visual_effect('listening')  # Use listening effect for user speaking
            else:
                self.clear_visual_effects()
        
        # Schedule the update in the main GUI thread
        try:
            self.root.after(0, _update_user_speaking_state)
        except Exception as e:
            print(f"GUI: Error scheduling user speaking state update: {e}")
            # Fallback to direct update
            _update_user_speaking_state()
    
    def reset_state(self):
        """Reset to idle state"""
        self.is_speaking = False
        self.is_listening = False
        self.is_processing = False
        self.user_speaking = False
        # Reset audio to idle
        self.set_audio_activity('idle', True)
        # Clear visual effects
        self.clear_visual_effects()
    
    def flash_acknowledgment(self):
        """Flash to acknowledge user input"""
        original_bg = self.root.cget('bg')
        
        # Flash briefly to show acknowledgment
        self.root.configure(bg='darkgreen')
        self.root.after(100, lambda: self.root.configure(bg=original_bg))
    
    def start(self):
        """Start the GUI - non-blocking version"""
        print("🎨 ARI Visual GUI is ready and animating...")
        # Don't call mainloop here - let the main program handle the event loop
        # The animation is already running via root.after() calls
    
    def on_closing(self):
        """Handle window close button click properly"""
        print("👋 GUI: Window close requested")
        self.stop()
    
    def stop(self):
        """Stop the GUI"""
        print("🔄 GUI: Stopping animation and GUI...")
        self.animation_running = False
        self.camera_running = False
        
        # Clean up camera
        if hasattr(self, 'cap'):
            try:
                self.cap.release()
            except:
                pass
            
        try:
            # Cancel any pending after() calls safely
            if self.root.winfo_exists():
                pass  # Don't cancel - let them finish naturally
        except:
            pass
        try:
            # Destroy the root window properly
            if self.root.winfo_exists():
                self.root.quit()
                self.root.destroy()
                print("✅ GUI: Stopped successfully")
        except Exception as e:
            print(f"⚠️ GUI: Error during stop: {e}")
        
    def _start_update_timer(self):
        """Start a timer to continuously update the GUI"""
        def gui_update():
            if self.animation_running:
                try:
                    self.root.update()
                    self.root.update_idletasks()
                    # Schedule next update
                    self.root.after(50, gui_update)  # Update every 50ms
                except Exception as e:
                    print(f"GUI update error: {e}")
                    # Retry after a longer delay
                    self.root.after(100, gui_update)
        
        # Start the update loop
        try:
            self.root.after(10, gui_update)  # Start after 10ms
        except Exception as e:
            print(f"Failed to start GUI update timer: {e}")
    
    def _continuous_update(self):
        """Continuous update for non-blocking mode"""
        if self.animation_running:
            try:
                self.root.update()
                self.root.update_idletasks()
                # Schedule next update immediately
                self.root.after(16, self._continuous_update)  # ~60 FPS
            except Exception as e:
                # Retry after delay
                self.root.after(50, self._continuous_update)
    
    def manual_animate_frame(self):
        """Manually advance animation frame - called from update()"""
        if not self.animation_running or not self.avatar_frames:
            return
        
        # Calculate if it's time for next frame based on current state
        current_time = time.time()
        if not hasattr(self, '_last_frame_time'):
            self._last_frame_time = current_time
            return
        
        # Calculate animation speed based on state
        if self.user_speaking:
            speed_ms = 400  # Very slow when user talks
        elif self.is_speaking:
            speed_ms = 15   # Super fast when ARI talks
        elif self.is_processing:
            speed_ms = 40   # Fast when processing
        elif self.is_listening:
            speed_ms = 200  # Slow, attentive when listening
        else:
            speed_ms = self.animation_speed  # Normal idle speed (100ms)
        
        # Check if enough time has passed for next frame
        time_since_last = (current_time - self._last_frame_time) * 1000  # Convert to ms
        if time_since_last >= speed_ms:
            # Update to next frame
            frame = self.avatar_frames[self.current_frame]
            self.avatar_label.configure(image=frame)
            self.current_frame = (self.current_frame + 1) % len(self.avatar_frames)
            self._last_frame_time = current_time
    
    def set_audio_level(self, level):
        """Set the current audio level (0.0 to 1.0)"""
        self.audio_level = max(0.0, min(1.0, level))
    
    def add_visual_effect(self, effect_type):
        """Add visual effects for different states - REMOVED COLORED BORDERS"""
        try:
            # Only update status text, no colored borders
            if effect_type == 'speaking':
                if hasattr(self, 'status_label'):
                    self.status_label.configure(text="ARI SPEAKING", fg=self.colors['primary'])
                
            elif effect_type == 'listening':
                if hasattr(self, 'status_label'):
                    self.status_label.configure(text="ARI LISTENING", fg=self.colors['secondary'])
                    
            elif effect_type == 'processing':
                if hasattr(self, 'status_label'):
                    self.status_label.configure(text="ARI PROCESSING", fg=self.colors['success'])
                    
        except Exception as e:
            print(f"Error adding visual effect: {e}")
    
    def clear_visual_effects(self):
        """Clear all visual effects and return to normal state"""
        try:
            # Reset status only, no border changes
            if hasattr(self, 'status_label'):
                self.status_label.configure(text="ARI ACTIVE", fg=self.colors['success'])
        except Exception as e:
            print(f"Error clearing visual effects: {e}")
        
    def set_audio_activity(self, activity_type, active=True):
        """Set audio activity type and level"""
        if activity_type == 'speaking' and active:
            # High activity when ARI is speaking
            self.audio_level = random.uniform(0.7, 1.0)
        elif activity_type == 'listening' and active:
            # Medium activity when listening
            self.audio_level = random.uniform(0.3, 0.6)
        elif activity_type == 'user_speaking' and active:
            # High activity when user is speaking
            self.audio_level = random.uniform(0.6, 0.9)
        else:
            # Low activity when idle
            self.audio_level = random.uniform(0.0, 0.2)

def main():
    """Main function to run the GUI"""
    print("🚀 ARI Visual GUI System")
    print("=" * 40)
    
    # Create and start the GUI
    gui = ARIVisualGUI()
    gui.start()
    # Start the Tkinter main loop to ensure the window is displayed and responsive
    try:
        gui.root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Shutting down ARI Visual GUI...")
        gui.stop()

if __name__ == "__main__":
    main()
