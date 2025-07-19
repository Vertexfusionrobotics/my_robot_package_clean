# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script for ARI's new user recognition and greeting system.
This script demonstrates how ARI handles new users vs. known users.
"""

import json
import shutil
import os
import sys

def test_new_user_recognition():
    """Test the new user recognition feature"""
    
    print("🧪 Testing ARI's New User Recognition System")
    print("=" * 50)
    
    # Backup original user profile
    original_profile = "user_profile.json"
    backup_profile = "user_profile_original_backup.json"
    
    if os.path.exists(original_profile):
        shutil.copy(original_profile, backup_profile)
        print(f"✅ Backed up original profile to {backup_profile}")
    
    # Test 1: New user scenario
    print("\n📋 Test 1: New User Scenario")
    print("-" * 30)
    
    # Create empty user profile to simulate new user
    with open(original_profile, 'w') as f:
        json.dump({}, f)
    
    print("✅ Created empty user profile (simulating new user)")
    print("🚀 Starting ARI with new user profile...")
    print("📝 Expected behavior:")
    print("   - ARI should detect this as a new user")
    print("   - Should ask: 'hello may i ask your name so i can remember you?'")
    print("   - After receiving name, should say: 'I'll remember you now how may i assist you?'")
    print("\n" + "="*60)
    print("🎯 RUN THE FOLLOWING COMMAND TO TEST:")
    print("python ari_master_brain_final.py")
    print("="*60)
    
    # Test 2: Known user scenario
    print("\n📋 Test 2: Known User Scenario (run after Test 1)")
    print("-" * 30)
    print("📝 After completing Test 1 and providing a name:")
    print("   - Restart ARI with the same user profile")
    print("   - ARI should greet you personally with your saved name")
    print("   - Should proceed directly to normal conversation")
    
    # Test 3: Restore original profile
    print("\n📋 Test 3: Restore Original Profile")
    print("-" * 30)
    print("📝 To restore your original user profile after testing:")
    print(f"   - Copy {backup_profile} back to {original_profile}")
    print(f"   - Or run: python restore_user_profile.py")
    
    print("\n" + "="*60)
    print("🎉 Test Setup Complete!")
    print("🚀 Ready to test ARI's new user recognition feature!")
    print("="*60)

def restore_original_profile():
    """Restore the original user profile"""
    backup_profile = "user_profile_original_backup.json"
    original_profile = "user_profile.json"
    
    if os.path.exists(backup_profile):
        shutil.copy(backup_profile, original_profile)
        print(f"✅ Restored original profile from {backup_profile}")
        return True
    else:
        print(f"❌ Backup profile {backup_profile} not found")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        restore_original_profile()
    else:
        test_new_user_recognition()
