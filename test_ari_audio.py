# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
"""
ARI Audio System Diagnostic Tool

This script tests various components of the audio system used by ARI to help
diagnose and fix issues with speech playback.
"""

import os
import sys
import time
import traceback

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_section(text):
    print("\n" + "-"*40)
    print(f" {text}")
    print("-"*40)

def print_result(success, message):
    if success:
        print(f"✓ SUCCESS: {message}")
    else:
        print(f"✗ FAILED: {message}")

def test_pygame_installation():
    print_section("Testing pygame installation")
    try:
        import pygame
        print(f"Pygame version: {pygame.version.ver}")
        print(f"Pygame path: {pygame.__file__}")
        return True, f"pygame {pygame.version.ver} installed correctly"
    except ImportError:
        print("pygame is not installed. Please install it with:")
        print("pip install pygame")
        return False, "pygame not installed"
    except Exception as e:
        print(f"Error importing pygame: {e}")
        return False, f"pygame import error: {e}"

def test_pygame_mixer():
    print_section("Testing pygame mixer initialization")
    try:
        import pygame
        
        # First try to quit any existing mixer
        try:
            pygame.mixer.quit()
        except:
            pass
        
        # Test different initialization parameters
        configs = [
            {"frequency": 44100, "size": -16, "channels": 2, "buffer": 4096},
            {"frequency": 22050, "size": -16, "channels": 1, "buffer": 2048},
            {"frequency": 16000, "size": -16, "channels": 1, "buffer": 1024}
        ]
        
        for i, config in enumerate(configs):
            print(f"\nTrying configuration {i+1}:")
            print(f"  {config}")
            
            try:
                pygame.mixer.init(**config)
                init_result = pygame.mixer.get_init()
                if init_result:
                    print(f"  ✓ Mixer initialized with: {init_result}")
                    pygame.mixer.quit()
                    return True, f"Mixer initialized successfully with config {i+1}"
                else:
                    print("  ✗ Mixer initialization returned None")
                    pygame.mixer.quit()
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        return False, "All mixer configurations failed"
    except Exception as e:
        print(f"Error testing mixer: {e}")
        return False, f"Mixer test error: {e}"

def test_edge_tts():
    print_section("Testing edge-tts installation")
    try:
        import edge_tts
        import asyncio
        
        print("edge-tts is installed")
        
        # Try listing available voices
        print("Attempting to list available voices...")
        async def list_voices():
            voices = await edge_tts.list_voices()
            print(f"Found {len(voices)} available voices")
            en_voices = [v for v in voices if v["Locale"].startswith("en")]
            print(f"Found {len(en_voices)} English voices")
            return len(voices) > 0
        
        result = asyncio.run(list_voices())
        return result, "edge-tts is working correctly"
    except ImportError:
        print("edge-tts is not installed. Please install it with:")
        print("pip install edge-tts")
        return False, "edge-tts not installed"
    except Exception as e:
        print(f"Error with edge-tts: {e}")
        return False, f"edge-tts error: {e}"

def test_audio_playback():
    print_section("Testing audio playback")
    try:
        import pygame
        
        # Try to quit any existing mixer
        try:
            pygame.mixer.quit()
        except:
            pass
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # Test 1: Generate and play a simple tone
        print("\nTest 1: Generating and playing a simple tone")
        try:
            import numpy as np
            
            # Create a simple sine wave
            sample_rate = 44100
            duration = 1.0  # seconds
            frequency = 440  # A4 note
            t = np.arange(0, duration, 1/sample_rate)
            wave = np.sin(2 * np.pi * frequency * t) * 32767 * 0.5
            wave = wave.astype(np.int16)
            
            # Convert to pygame Sound
            sound = pygame.sndarray.make_sound(wave)
            sound.set_volume(0.5)  # Medium volume
            
            print("Playing tone now... (you should hear a 1-second beep)")
            sound.play()
            time.sleep(1.5)  # Wait for tone to complete
            pygame.mixer.quit()
            
            print("Did you hear the tone? (y/n)")
            response = input().strip().lower()
            if response == 'y':
                return True, "User confirmed audio playback is working"
            else:
                print("\nAudio playback issues detected. Please check:")
                print("1. Is your volume turned up?")
                print("2. Are your speakers/headphones connected properly?")
                print("3. Is another program using the audio device?")
                return False, "User did not hear the test tone"
            
        except Exception as e:
            print(f"Error generating/playing tone: {e}")
            return False, f"Tone test error: {e}"
    except Exception as e:
        print(f"Error setting up audio playback test: {e}")
        return False, f"Audio playback setup error: {e}"

def test_tts_generation():
    print_section("Testing TTS generation")
    try:
        import edge_tts
        import asyncio
        import os
        
        test_file = "_test_tts.mp3"
        
        # Remove previous test file if it exists
        if os.path.exists(test_file):
            try:
                os.remove(test_file)
            except:
                pass
        
        print("Generating test TTS file...")
        async def generate_tts():
            communicate = edge_tts.Communicate("This is a test of the ARI text to speech system.", 
                                              voice="en-GB-SoniaNeural")
            await communicate.save(test_file)
            
        asyncio.run(generate_tts())
        
        if os.path.exists(test_file) and os.path.getsize(test_file) > 1000:
            print(f"Generated TTS file: {test_file} ({os.path.getsize(test_file)} bytes)")
            
            # Try to play the generated file
            print("\nAttempting to play the generated TTS file...")
            try:
                import pygame
                
                try:
                    pygame.mixer.quit()
                except:
                    pass
                    
                pygame.mixer.init()
                pygame.mixer.music.load(test_file)
                pygame.mixer.music.play()
                
                start_time = time.time()
                max_wait = 5
                
                print("Playing TTS audio... (you should hear speech)")
                while pygame.mixer.music.get_busy() and time.time() - start_time < max_wait:
                    time.sleep(0.1)
                
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                
                print("Did you hear the test speech? (y/n)")
                response = input().strip().lower()
                if response == 'y':
                    return True, "TTS generation and playback successful"
                else:
                    return False, "User did not hear the TTS playback"
                
            except Exception as e:
                print(f"Error playing TTS file: {e}")
                return False, f"TTS playback error: {e}"
        else:
            return False, "Failed to generate TTS file or file is too small"
    except Exception as e:
        print(f"Error in TTS generation test: {e}")
        return False, f"TTS test error: {e}"

def main():
    print_header("ARI AUDIO SYSTEM DIAGNOSTIC TOOL")
    print("\nThis tool will test components of ARI's audio system to help diagnose issues.")
    print("Follow the prompts and answer any questions when asked.\n")
    
    # Get system info
    print("System Information:")
    print(f"Python version: {sys.version}")
    print(f"Operating system: {sys.platform}")
    
    # Run tests
    tests = [
        ("Pygame Installation", test_pygame_installation),
        ("Pygame Mixer", test_pygame_mixer),
        ("Edge TTS", test_edge_tts),
        ("Audio Playback", test_audio_playback),
        ("TTS Generation", test_tts_generation)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success, message = test_func()
            results.append((name, success, message))
        except Exception as e:
            print(f"Error running test {name}: {e}")
            traceback.print_exc()
            results.append((name, False, f"Test crashed: {e}"))
    
    # Print summary
    print_header("TEST RESULTS SUMMARY")
    
    passed = sum(1 for _, success, _ in results if success)
    failed = len(results) - passed
    
    for name, success, message in results:
        status = "PASS" if success else "FAIL"
        print(f"{status}: {name} - {message}")
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if failed > 0:
        print("\nRecommendations for fixing audio issues:")
        print("1. Ensure your audio device is connected and not muted")
        print("2. Try running 'pip install --upgrade pygame edge-tts numpy' to update packages")
        print("3. Restart your computer to free up audio resources")
        print("4. Check if other applications are using the audio device")
        print("5. Try running ARI with administrator privileges")
    else:
        print("\nAll tests passed! If you're still having issues with ARI's audio:")
        print("1. Check for errors in the console output when running ARI")
        print("2. Try running the 'Generate ARI Greeting Audio' task in VS Code")
        print("3. Restart your computer and try again")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
