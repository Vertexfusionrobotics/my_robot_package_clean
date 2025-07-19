# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
"""
Quick test for ARI's audio system
"""
from ari_master_brain_final import ARIMasterBrain

# Create the brain
brain = ARIMasterBrain()

# Test audio output
result = brain.test_audio_output()

# Report result
print(f"\nAudio test result: {'SUCCESS' if result else 'FAILED'}")

# Test greeting directly
print("\nTesting greeting directly...")
brain.greet_user()
print("Greeting test complete.")

input("\nPress Enter to exit...")
