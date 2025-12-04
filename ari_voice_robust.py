# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Robust ARI Voice System with Multiple Audio Playback Options
Uses Microsoft Sonia voice with multiple fallback audio players
"""

import asyncio
import sys
import os
import subprocess
import tempfile
import time
from pathlib import Path

class ARIVoiceSystem:
    def __init__(self):
        self.voice = "en-GB-SoniaNeural"  # Microsoft Sonia (Natural) - English (UK)
        self.temp_audio_file = None
        self.ensure_edge_tts()
    
    def ensure_edge_tts(self):
        """Ensure edge-tts-ari (pyttsx3-based) is installed"""
        try:
            import edge_tts_ari as edge_tts
            self.edge_tts = edge_tts
            print("✅ Edge-TTS-ARI (offline female voice) ready")
        except ImportError:
            print("📦 Installing pyttsx3 for offline TTS...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3", "gtts", "pydub"])
            import edge_tts_ari as edge_tts
            self.edge_tts = edge_tts
            print("✅ Edge-TTS-ARI (offline female voice) installed and ready")
    
    def find_audio_player(self):
        """Find the best available audio player on Windows"""
        players = [
            # Try pygame first (most reliable)
            ("pygame", self.play_with_pygame),
            # Try playsound (simple and reliable)
            ("playsound", self.play_with_playsound),
            # Try Windows built-in players
            ("powershell", self.play_with_powershell),
            ("wmplayer", self.play_with_wmplayer),
        ]
        
        for player_name, player_func in players:
            try:
                if player_name == "pygame":
                    import pygame
                elif player_name == "playsound":
                    import playsound
                print(f"✅ Found audio player: {player_name}")
                return player_func
            except ImportError:
                continue
        
        # Fallback to PowerShell (always available on Windows)
        print("⚠️ Using PowerShell as fallback audio player")
        return self.play_with_powershell
    
    def play_with_pygame(self, audio_file):
        """Play audio using pygame (most reliable)"""
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            return True
        except Exception as e:
            print(f"❌ Pygame playback failed: {e}")
            return False
    
    def play_with_playsound(self, audio_file):
        """Play audio using playsound library"""
        try:
            import playsound
            playsound.playsound(audio_file, True)  # Block until finished
            return True
        except Exception as e:
            print(f"❌ Playsound playback failed: {e}")
            return False
    
    def play_with_powershell(self, audio_file):
        """Play audio using PowerShell (always available on Windows)"""
        try:
            # Use PowerShell to play the audio file
            ps_command = f'''
            Add-Type -AssemblyName presentationCore
            $mediaPlayer = New-Object system.windows.media.mediaplayer
            $mediaPlayer.open([uri]"{audio_file}")
            $mediaPlayer.Play()
            Start-Sleep -Seconds 1
            while($mediaPlayer.NaturalDuration.HasTimeSpan -eq $false) {{
                Start-Sleep -Milliseconds 100
            }}
            $duration = $mediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
            Start-Sleep -Seconds $duration
            $mediaPlayer.Stop()
            $mediaPlayer.Close()
            '''
            
            result = subprocess.run([
                "powershell", "-Command", ps_command
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return True
            else:
                print(f"❌ PowerShell audio failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ PowerShell playback failed: {e}")
            return False
    
    def play_with_wmplayer(self, audio_file):
        """Play audio using Windows Media Player (fallback)"""
        try:
            # Use Windows Media Player in minimized mode
            subprocess.run([
                "wmplayer", "/close", audio_file
            ], check=True, timeout=30)
            return True
        except Exception as e:
            print(f"❌ WMPlayer playback failed: {e}")
            return False
    
    async def generate_and_speak(self, text):
        """Generate and speak using edge-tts-ari (handles playback internally)"""
        try:
            # edge_tts_ari.create_audio_from_text() generates AND plays the audio
            # It handles everything internally and cleans up temp files
            await self.edge_tts.create_audio_from_text(text)
            return True
            
        except Exception as e:
            print(f"❌ Speech generation/playback failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def speak(self, text):
        """Speak the given text using natural female voice (gTTS)"""
        print(f"🗣️ ARI speaking: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        try:
            # Let edge_tts_ari handle everything (generation + playback)
            success = asyncio.run(self.generate_and_speak(text))
            
            if success:
                print("✅ Speech completed")
            else:
                print("❌ Speech failed")
            
            return success
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_voice(self):
        """Test the voice system"""
        print("🧪 Testing ARI Voice System")
        print("=" * 40)
        
        test_phrases = [
            "Hello! I am ARI, your AI assistant.",
            "This is my natural Sonia voice speaking.",
            "Voice system test completed successfully."
        ]
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"\n🎬 Test {i}/3: {phrase}")
            success = self.speak(phrase)
            if not success:
                print(f"❌ Test {i} failed")
                return False
            time.sleep(1)  # Brief pause between tests
        
        print("\n✅ All voice tests passed!")
        return True

def main():
    """Test the voice system"""
    voice_system = ARIVoiceSystem()
    
    if len(sys.argv) > 1:
        # Speak provided text
        text = " ".join(sys.argv[1:])
        voice_system.speak(text)
    else:
        # Run test
        voice_system.test_voice()

if __name__ == "__main__":
    main()
