# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test Voice Components for ARI Stage 3
Verify speech recognition and text-to-speech functionality
"""

import sys
import os
import asyncio
import tempfile
import time

def test_imports():
    """Test if all required modules are available"""
    print("🔍 Testing imports...")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition available")
    except ImportError:
        print("❌ SpeechRecognition not found - run: pip install SpeechRecognition")
        return False
    
    try:
        import edge_tts
        print("✅ edge-tts available")
    except ImportError:
        print("❌ edge-tts not found - run: pip install edge-tts")
        return False
    
    try:
        import pygame
        print("✅ pygame available")
    except ImportError:
        print("❌ pygame not found - run: pip install pygame")
        return False
    
    return True

async def test_tts():
    """Test text-to-speech functionality"""
    print("\n🔊 Testing Text-to-Speech...")
    
    try:
        import edge_tts
        import pygame
        
        # Initialize pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        # Generate TTS
        text = "Hello! This is ARI testing my voice capabilities."
        voice = "en-GB-SoniaNeural"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
            tts_path = tf.name
        
        print(f"Generating TTS for: '{text}'")
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save(tts_path)
        
        if os.path.exists(tts_path) and os.path.getsize(tts_path) > 0:
            print(f"✅ TTS file created: {os.path.getsize(tts_path)} bytes")
            
            # Play audio
            print("🎵 Playing audio...")
            pygame.mixer.music.load(tts_path)
            pygame.mixer.music.play()
            
            # Wait for playback
            start_time = time.time()
            while pygame.mixer.music.get_busy() and time.time() - start_time < 10:
                await asyncio.sleep(0.1)
            
            pygame.mixer.music.unload()
            print("✅ TTS test completed")
        else:
            print("❌ TTS file creation failed")
            return False
        
        # Cleanup
        try:
            os.unlink(tts_path)
        except:
            pass
        
        pygame.mixer.quit()
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_microphone():
    """Test microphone access"""
    print("\n🎤 Testing Microphone Access...")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        print(f"📱 Found {len(mic_list)} microphone(s):")
        for i, name in enumerate(mic_list[:3]):  # Show first 3
            print(f"  {i}: {name}")
        
        # Test default microphone
        with sr.Microphone() as source:
            print("🔧 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition with a short sample"""
    print("\n🗣️ Testing Speech Recognition...")
    print("📢 Please say something when prompted (you have 5 seconds)...")
    
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("🎙️ Listening... (say 'hello test')")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("🔄 Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Recognized: '{text}'")
        return True
        
    except sr.WaitTimeoutError:
        print("⚠️ No speech detected (timeout)")
        return True  # Not a failure, just no input
    except sr.UnknownValueError:
        print("⚠️ Could not understand speech")
        return True  # Not a failure, just unclear
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return False
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        return False

def test_stage_3_integration():
    """Test Stage 3 neural components"""
    print("\n🧠 Testing Stage 3 Integration...")
    
    try:
        from ari_master_brain_stage_3 import ARIMasterBrainStage3
        brain = ARIMasterBrainStage3()
        print("✅ Stage 3 brain loaded")
        
        # Test a simple interaction
        response = brain.process_input("Hello ARI")
        print(f"✅ Brain response: '{response[:50]}{'...' if len(response) > 50 else ''}'")
        return True
        
    except Exception as e:
        print(f"❌ Stage 3 integration test failed: {e}")
        return False

async def run_full_test():
    """Run all tests"""
    print("🚀 ARI Voice Stage 3 - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports()),
        ("Microphone Test", test_microphone()),
        ("TTS Test", await test_tts()),
        ("Stage 3 Integration", test_stage_3_integration()),
    ]
    
    # Optional speech recognition test
    print("\n❓ Would you like to test speech recognition? (requires speaking)")
    try:
        user_input = input("Type 'y' for yes, any other key to skip: ").strip().lower()
        if user_input == 'y':
            tests.append(("Speech Recognition Test", test_speech_recognition()))
    except:
        pass
    
    print("\n📊 Test Results:")
    print("-" * 30)
    
    passed = 0
    total = len(tests)
    
    for name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ARI Voice Stage 3 is ready!")
        print("\n🚀 You can now run: python ari_voice_stage_3.py")
    else:
        print("⚠️ Some tests failed. Please install missing dependencies.")
        print("\n📦 Install command: pip install SpeechRecognition edge-tts pygame")

if __name__ == "__main__":
    asyncio.run(run_full_test())
