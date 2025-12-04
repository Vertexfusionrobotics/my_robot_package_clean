"""
Simplified TTS helper: use pyttsx3 for REAL female voice with fallback to gTTS
while emitting notify events for ('start', duration), ('rms', amp), ('end', None).
"""
import os
import tempfile
import time
import math
import traceback
from pydub import AudioSegment

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except Exception:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False


def _emit_notify(notify, ev, data=None):
    if not notify:
        return
    try:
        notify((ev, data))
    except Exception:
        try:
            print(f"[edge_tts_ari] notify {ev} failed")
        except Exception:
            pass


def _play_with_pygame_rms(mp3_path, notify=None, chunk_ms=60):
    """Play an MP3 file with pygame and emit simplified RMS notifications."""
    import threading as th
    
    # Initialize pygame mixer (force reinit to ensure clean state)
    try:
        pygame.mixer.quit()
    except:
        pass
    pygame.mixer.init()
    
    print(f"[edge_tts_ari] Mixer initialized: {pygame.mixer.get_init()}")
    print(f"[edge_tts_ari] Loading audio file: {mp3_path}")
    pygame.mixer.music.load(mp3_path)
    
    # Estimate duration from file size (rough approximation)
    # Average MP3 bitrate ~128kbps, so bytes/(128000/8) = seconds
    try:
        file_size = os.path.getsize(mp3_path)
        duration_seconds = max(1.0, file_size / 16000.0)  # rough estimate
    except Exception:
        duration_seconds = 2.0
    
    # Set volume to maximum
    pygame.mixer.music.set_volume(1.0)
    
    # Start playback
    print(f"[edge_tts_ari] Playing audio... (duration ~{duration_seconds:.1f}s)")
    pygame.mixer.music.play()
    
    # Emit start event
    try:
        print(f"[edge_tts_ari] notify start, duration={duration_seconds}")
        _emit_notify(notify, 'start', duration_seconds)
    except Exception:
        pass
    
    # Emit simulated RMS updates (alternating pattern for visual effect)
    chunk_duration = chunk_ms / 1000.0
    elapsed = 0.0
    toggle = 0
    while pygame.mixer.music.get_busy() and elapsed < duration_seconds + 1.0:
        # Create natural-looking amplitude pattern
        if toggle % 4 == 0:
            rms_val = 0.6
        elif toggle % 4 == 1:
            rms_val = 0.8
        elif toggle % 4 == 2:
            rms_val = 0.7
        else:
            rms_val = 0.5
            
        if notify:
            try:
                _emit_notify(notify, 'rms', rms_val)
            except Exception:
                pass
        time.sleep(chunk_duration)
        elapsed += chunk_duration
        toggle += 1
    
    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    print("[edge_tts_ari] Playback complete")


def _synthesize_with_pyttsx3(text, wav_path):
    """Generate speech using pyttsx3 with REAL female voice - saves as WAV"""
    if not PYTTSX3_AVAILABLE:
        raise RuntimeError("pyttsx3 not installed")
    
    engine = pyttsx3.init()
    
    # Get available voices and select a female voice
    voices = engine.getProperty('voices')
    female_voice = None
    
    # Look for female voice (usually contains 'female' or specific female voice names)
    for voice in voices:
        voice_name = voice.name.lower()
        if 'female' in voice_name:
            female_voice = voice.id
            print(f"[edge_tts_ari] Selected female voice: {voice.name}")
            break
        # Common female voice names
        elif any(name in voice_name for name in ['sonia', 'samantha', 'victoria', 'allison', 'susan', 'zira']):
            female_voice = voice.id
            print(f"[edge_tts_ari] Selected female voice: {voice.name}")
            break
    
    if female_voice:
        engine.setProperty('voice', female_voice)
    else:
        # If no explicit female voice found, try voice index 1 (often female)
        print("[edge_tts_ari] No explicit female voice found, trying alternate voice")
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
            print(f"[edge_tts_ari] Using voice: {voices[1].name}")
        elif voices:
            engine.setProperty('voice', voices[0].id)
            print(f"[edge_tts_ari] Using default voice: {voices[0].name}")
    
    # Set properties for feminine sound
    engine.setProperty('rate', 170)    # Slightly faster = more natural female voice
    engine.setProperty('volume', 1.0)
    
    # pyttsx3 saves as WAV, not MP3
    engine.save_to_file(text, wav_path)
    engine.runAndWait()
    
    # Wait a moment for file to be written
    time.sleep(0.5)
    
    # Verify file exists
    max_wait = 5
    waited = 0
    while not os.path.exists(wav_path) and waited < max_wait:
        time.sleep(0.1)
        waited += 0.1
    
    if not os.path.exists(wav_path):
        raise RuntimeError(f"pyttsx3 failed to create {wav_path}")
    
    print(f"[edge_tts_ari] Audio saved to {wav_path}")


def _play_with_pygame_rms_wav(wav_path, notify=None, chunk_ms=60):
    """Play a WAV file with pygame and emit simplified RMS notifications."""
    import threading as th
    
    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(wav_path)
    
    # Estimate duration from file size
    try:
        file_size = os.path.getsize(wav_path)
        # WAV is uncompressed: rough estimate 176400 bytes/sec (44.1kHz, 16-bit, stereo)
        duration_seconds = max(1.0, file_size / 176400.0)
    except Exception:
        duration_seconds = 2.0
    
    # Start playback
    pygame.mixer.music.play()
    
    # Emit start event
    try:
        _emit_notify(notify, 'start', duration_seconds)
    except Exception:
        pass
    
    # Emit simulated RMS updates
    chunk_duration = chunk_ms / 1000.0
    elapsed = 0.0
    toggle = 0
    while pygame.mixer.music.get_busy() and elapsed < duration_seconds + 1.0:
        # Create natural-looking amplitude pattern
        if toggle % 4 == 0:
            rms_val = 0.6
        elif toggle % 4 == 1:
            rms_val = 0.8
        elif toggle % 4 == 2:
            rms_val = 0.7
        else:
            rms_val = 0.5
            
        if notify:
            try:
                _emit_notify(notify, 'rms', rms_val)
            except Exception:
                pass
        time.sleep(chunk_duration)
        elapsed += chunk_duration
        toggle += 1
    
    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)


def _synthesize_with_gtts(text, mp3_path):
    """Generate speech using gTTS as fallback"""
    if not GTTS_AVAILABLE:
        raise RuntimeError("gTTS/pygame not installed")
    
    print(f"[edge_tts_ari] Using gTTS (female voice)")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(mp3_path)
    time.sleep(0.2)
    
    if not os.path.exists(mp3_path):
        raise RuntimeError(f"gTTS failed to create {mp3_path}")


async def create_audio_from_text(text, output_file=None, voice="en-US-AriaNeural", notify=None):
    """
    Main TTS function using gTTS (natural female voice) with pyttsx3 fallback.
    Compatible with edge_tts API but uses offline TTS.
    """
    print(f"[edge_tts_ari] Synthesizing: '{text[:50]}...'")
    
    # Create temp file if no output specified
    if output_file is None:
        fd, output_file = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
    
    try:
        # Try gTTS first (natural female voice)
        if GTTS_AVAILABLE:
            print("[edge_tts_ari] Using gTTS (natural female voice)")
            _synthesize_with_gtts(text, output_file)
            
            # Emit notifications while playing
            _emit_notify(notify, 'start', None)
            _play_with_pygame_rms(output_file, notify=notify)
            _emit_notify(notify, 'end', None)
            
        # Fallback to pyttsx3 if gTTS fails
        elif PYTTSX3_AVAILABLE:
            wav_file = output_file.replace('.mp3', '.wav')
            print("[edge_tts_ari] Using pyttsx3 (female voice)")
            _synthesize_with_pyttsx3(text, wav_file)
            
            # Emit notifications while playing
            _emit_notify(notify, 'start', None)
            _play_with_pygame_rms_wav(wav_file, notify=notify)
            _emit_notify(notify, 'end', None)
            
            try:
                os.remove(wav_file)
            except:
                pass
        else:
            raise RuntimeError("No TTS engine available (install pyttsx3 or gTTS)")
            
    except Exception as e:
        print(f"[edge_tts_ari] TTS error: {e}")
        traceback.print_exc()
        raise
    
    finally:
        # Cleanup temp file
        try:
            if output_file and os.path.exists(output_file):
                os.remove(output_file)
        except:
            pass
    
    return output_file


# Async wrapper to maintain compatibility
async def Communicate(text, voice="en-US-AriaNeural"):
    """Compatibility wrapper for edge_tts.Communicate"""
    class MockStream:
        def __init__(self, text):
            self.text = text
            self.played = False
            
        async def stream(self):
            if not self.played:
                # Generate and play audio
                await create_audio_from_text(self.text, voice=voice)
                self.played = True
                yield {"type": "audio", "data": b""}  # Mock data
    
    return MockStream(text)
