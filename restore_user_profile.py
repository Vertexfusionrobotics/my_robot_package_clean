# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Restore the original user profile after testing new user recognition.
"""

import shutil
import os

def restore_user_profile():
    """Restore the original user profile"""
    backup_profile = "user_profile_original_backup.json"
    original_profile = "user_profile.json"
    
    if os.path.exists(backup_profile):
        shutil.copy(backup_profile, original_profile)
        print(f"✅ Restored original user profile from {backup_profile}")
        
        # Show restored content
        try:
            import json
            with open(original_profile, 'r') as f:
                data = json.load(f)
            print(f"📝 Restored profile: {data}")
        except:
            pass
            
        return True
    else:
        print(f"❌ Backup profile {backup_profile} not found")
        print("💡 Using default profile instead...")
        
        # Create default profile
        default_data = {"name": "Mr. Murray", "preferences": {}, "interactions": 0}
        with open(original_profile, 'w') as f:
            import json
            json.dump(default_data, f, indent=2)
        
        print(f"✅ Created default user profile")
        return True

if __name__ == "__main__":
    restore_user_profile()
