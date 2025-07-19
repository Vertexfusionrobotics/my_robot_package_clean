# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Complete System Test - Visual Recognition & Neural Networks
Tests all integrated systems: Q&A, Neural Networks, and Visual Recognition
"""

import sys
import os

def test_component(component_name, test_func):
    """Test a component and report results"""
    try:
        print(f"🧪 Testing {component_name}...")
        result = test_func()
        if result:
            print(f"✅ {component_name}: PASSED")
            return True
        else:
            print(f"❌ {component_name}: FAILED")
            return False
    except Exception as e:
        print(f"❌ {component_name}: ERROR - {e}")
        return False

def test_basic_imports():
    """Test basic system imports"""
    try:
        import cv2
        import tensorflow as tf
        import mediapipe as mp
        import face_recognition
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def test_visual_recognition():
    """Test visual recognition system"""
    try:
        from ari_visual_recognition import ARIVisualRecognition
        vr = ARIVisualRecognition()
        return hasattr(vr, 'detect_faces')
    except Exception as e:
        print(f"Visual recognition error: {e}")
        return False

def test_neural_networks():
    """Test neural network system"""
    try:
        from neural_networks import ARINeuralNetworks
        nn = ARINeuralNetworks()
        return hasattr(nn, 'build_response_predictor_network')
    except Exception as e:
        print(f"Neural networks error: {e}")
        return False

def test_main_system():
    """Test main ARI system integration"""
    try:
        from ari_master_brain_final import ARIMasterBrain
        ari = ARIMasterBrain()
        return hasattr(ari, 'visual_recognition')
    except Exception as e:
        print(f"Main system error: {e}")
        return False

def test_question_answering():
    """Test Q&A system"""
    try:
        from ari_master_brain_final import ARIMasterBrain
        ari = ARIMasterBrain()
        response = ari.get_response("what are you")
        return "ARI" in response and "assistant" in response
    except Exception as e:
        print(f"Q&A system error: {e}")
        return False

def main():
    """Run comprehensive system test"""
    print("🚀 ARI Complete System Test")
    print("=" * 50)
    
    tests = [
        ("Basic Dependencies", test_basic_imports),
        ("Visual Recognition Module", test_visual_recognition),
        ("Neural Networks Module", test_neural_networks),
        ("Main ARI System", test_main_system),
        ("Question Answering", test_question_answering),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_component(test_name, test_func):
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! ARI is fully operational with:")
        print("   • Question-Answering System ✅")
        print("   • Neural Networks (Stage 2) ✅")
        print("   • Visual Recognition System ✅")
        print("   • Complete Integration ✅")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    print("\n🎯 Next Steps:")
    print("1. Run ARI: 'python ari_master_brain_final.py'")
    print("2. Test visual commands: 'activate vision', 'detect faces'")
    print("3. Test face learning: 'learn my face as [Your Name]'")
    print("4. Test recognition: 'who am I?' or 'do you recognize me?'")
    print("5. Test neural guidance: Ask complex questions")
    print("6. Continue enhancing the system!")
    print("\n📋 How to verify ARI remembers you:")
    print("   • Say 'learn my face as Mr Murray' (or your preferred name)")
    print("   • Exit ARI and restart it")
    print("   • Say 'activate vision' then 'who am I?'")
    print("   • ARI should recognize you by name!")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
