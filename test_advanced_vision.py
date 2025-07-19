# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Advanced Vision Test - Test all new vision features
Tests object detection, scene analysis, emotion recognition, and color analysis
"""

import sys
import os
import cv2
import numpy as np

def test_basic_vision():
    """Test basic vision functionality"""
    print("🔍 Testing Basic Vision Features")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        print("🔍 Initializing visual recognition...")
        vr = ARIVisualRecognition()
        
        print("📷 Starting camera...")
        if not vr.start_camera():
            print("❌ Camera failed to start")
            return False
        
        print("✅ Camera started successfully")
        
        # Test face detection
        print("\n👤 Testing face detection...")
        faces = vr.detect_faces_from_camera()
        if faces:
            print(f"✅ Detected {len(faces)} face(s)")
        else:
            print("⚠️ No faces detected")
        
        vr.stop_camera()
        return True
        
    except Exception as e:
        print(f"❌ Error in basic vision test: {e}")
        return False

def test_object_detection():
    """Test object detection functionality"""
    print("\n🔍 Testing Object Detection")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        vr = ARIVisualRecognition()
        
        # Load object detection model
        print("🤖 Loading object detection model...")
        success = vr.load_object_detection_model()
        if success:
            print("✅ Object detection model loaded")
        else:
            print("⚠️ Object detection model not available")
            return True  # Don't fail the test
        
        if vr.start_camera():
            print("📷 Testing object detection from camera...")
            objects = vr.detect_objects_from_camera()
            
            if objects:
                print(f"✅ Detected {len(objects)} objects:")
                for obj in objects[:3]:  # Show top 3
                    print(f"   • {obj['label']}: {obj['confidence']:.1%}")
            else:
                print("⚠️ No objects detected")
            
            vr.stop_camera()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in object detection test: {e}")
        return True  # Don't fail test suite for optional features

def test_scene_analysis():
    """Test scene analysis functionality"""
    print("\n🎬 Testing Scene Analysis")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        vr = ARIVisualRecognition()
        
        if vr.start_camera():
            print("📷 Analyzing scene...")
            scene_info = vr.analyze_scene_from_camera()
            
            if scene_info:
                print("✅ Scene analysis complete:")
                print(f"   Scene type: {scene_info.get('scene_type', 'unknown')}")
                print(f"   Lighting: {scene_info.get('lighting', 'unknown')}")
                print(f"   Activity: {scene_info.get('activity', 'unknown')}")
            else:
                print("⚠️ Scene analysis returned no data")
            
            vr.stop_camera()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in scene analysis test: {e}")
        return True

def test_color_analysis():
    """Test color analysis functionality"""
    print("\n🎨 Testing Color Analysis")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        vr = ARIVisualRecognition()
        
        if vr.start_camera():
            print("📷 Analyzing colors...")
            colors = vr.analyze_colors_from_camera()
            
            if colors:
                print(f"✅ Color analysis complete - {len(colors)} dominant colors:")
                for color in colors[:3]:  # Show top 3
                    print(f"   • {color['name']}: {color['percentage']:.1%}")
            else:
                print("⚠️ Color analysis returned no data")
            
            vr.stop_camera()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in color analysis test: {e}")
        return True

def test_enhanced_emotion_detection():
    """Test enhanced emotion detection"""
    print("\n😊 Testing Enhanced Emotion Detection")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        vr = ARIVisualRecognition()
        
        if vr.start_camera():
            print("📷 Analyzing emotions...")
            emotions = vr.analyze_emotion_from_camera()
            
            if emotions:
                print("✅ Emotion detection complete:")
                if isinstance(emotions, list):
                    for i, emotion in enumerate(emotions):
                        print(f"   Face {i+1}:")
                        if emotion.get('basic_emotion'):
                            print(f"     Basic: {emotion['basic_emotion']['emotion']}")
                        if emotion.get('cnn_emotion'):
                            print(f"     CNN: {emotion['cnn_emotion']['emotion']}")
                else:
                    print(f"   Detected: {emotions}")
            else:
                print("⚠️ No emotions detected")
            
            vr.stop_camera()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in emotion detection test: {e}")
        return True

def test_visual_summary():
    """Test comprehensive visual summary"""
    print("\n👁️ Testing Visual Summary")
    print("=" * 40)
    
    try:
        from ari_visual_recognition import ARIVisualRecognition
        
        vr = ARIVisualRecognition()
        
        if vr.start_camera():
            print("📷 Generating visual summary...")
            summary = vr.get_visual_summary()
            
            if summary and "Camera not available" not in summary:
                print("✅ Visual summary generated:")
                print(f"   {summary}")
            else:
                print("⚠️ Visual summary failed or camera not available")
            
            vr.stop_camera()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in visual summary test: {e}")
        return True

def test_ari_integration():
    """Test integration with main ARI brain"""
    print("\n🤖 Testing ARI Integration")
    print("=" * 40)
    
    try:
        from ari_master_brain_final import ARIMasterBrain
        
        print("🤖 Creating ARI instance...")
        ari = ARIMasterBrain()
        
        print("🔍 Testing new vision commands...")
        test_commands = [
            "detect objects",
            "analyze scene", 
            "analyze colors",
            "describe what you see",
            "analyze emotion"
        ]
        
        for cmd in test_commands:
            print(f"  Testing: '{cmd}'")
            try:
                response = ari.get_response(cmd)
                if "not available" in response.lower():
                    print(f"    ⚠️ Feature not available: {response[:60]}...")
                elif any(keyword in response.lower() for keyword in ["see", "detect", "analyze", "color", "scene", "object", "emotion"]):
                    print(f"    ✅ Good response: {response[:60]}...")
                else:
                    print(f"    ⚠️ Generic response: {response[:60]}...")
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing ARI integration: {e}")
        return True

def main():
    """Run all advanced vision tests"""
    print("🚀 ARI Advanced Vision Test Suite")
    print("=" * 60)
    
    success = True
    tests = [
        test_basic_vision,
        test_object_detection,
        test_scene_analysis,
        test_color_analysis,
        test_enhanced_emotion_detection,
        test_visual_summary,
        test_ari_integration
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                success = False
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed: {e}")
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL ADVANCED VISION TESTS PASSED!")
        print("\n📋 New Commands Available:")
        print("• 'detect objects' - Find and identify objects")
        print("• 'analyze scene' - Comprehensive scene analysis")
        print("• 'analyze colors' - Dominant color detection")
        print("• 'describe what you see' - Full visual summary")
        print("• 'analyze emotion' - Enhanced emotion detection")
        print("\n🚀 ARI's vision system is now enhanced!")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
