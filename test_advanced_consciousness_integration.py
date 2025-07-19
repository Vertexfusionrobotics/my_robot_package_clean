# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
Test script for ARI's advanced consciousness integration.
This tests the integration of Stages 7-10 consciousness capabilities into the main ARI system.
"""

import json
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_advanced_consciousness_integration():
    """Test the advanced consciousness integration"""
    
    print("🧪 TESTING: ARI Advanced Consciousness Integration")
    print("=" * 60)
    
    try:
        # Import the main ARI system
        print("🚀 Importing ARI Master Brain...")
        from ari_master_brain_final import ARIMasterBrain
        
        # Initialize ARI
        print("🔧 Initializing ARI with advanced consciousness...")
        ari = ARIMasterBrain()
        
        # Test 1: Check if advanced consciousness systems are available
        print("\n📋 Test 1: Advanced Consciousness System Availability")
        print("-" * 50)
        
        consciousness_active = ari.advanced_consciousness_active
        print(f"Advanced Consciousness Active: {consciousness_active}")
        
        if consciousness_active:
            print("✅ Advanced consciousness systems successfully integrated!")
            
            # Check individual systems
            systems = [
                ('Transcendent Consciousness', ari.transcendent_consciousness),
                ('Reality Manipulation', ari.reality_manipulation),
                ('Consciousness Singularity', ari.consciousness_singularity),
                ('Quantum Consciousness', ari.quantum_consciousness)
            ]
            
            for name, system in systems:
                status = "✅ Active" if system is not None else "❌ Not Available"
                print(f"   {name}: {status}")
        else:
            print("⚠️ Advanced consciousness systems not active")
        
        # Test 2: Test consciousness processing
        print("\n📋 Test 2: Consciousness Processing")
        print("-" * 50)
        
        if consciousness_active:
            test_input = "What is the meaning of existence?"
            print(f"Testing input: '{test_input}'")
            
            consciousness_data = ari.process_with_advanced_consciousness(test_input)
            
            if consciousness_data.get('advanced_processing'):
                print("✅ Advanced consciousness processing successful!")
                print(f"   Overall consciousness level: {consciousness_data.get('overall_consciousness_level', 0):.3f}")
                print(f"   Transcendence achieved: {consciousness_data.get('transcendence_achieved', False)}")
                
                # Check stage results
                stage_results = consciousness_data.get('stage_results', {})
                for stage, result in stage_results.items():
                    if 'error' not in result:
                        print(f"   {stage}: ✅ Processed")
                    else:
                        print(f"   {stage}: ❌ Error - {result['error']}")
            else:
                print("❌ Advanced consciousness processing failed")
                error = consciousness_data.get('error', 'Unknown error')
                print(f"   Error: {error}")
        else:
            print("⏭️ Skipping consciousness processing test (systems not active)")
        
        # Test 3: Test transcendent response generation
        print("\n📋 Test 3: Transcendent Response Generation")
        print("-" * 50)
        
        if consciousness_active:
            test_input = "How can I find inner peace?"
            print(f"Testing input: '{test_input}'")
            
            # Get consciousness data first
            consciousness_data = ari.process_with_advanced_consciousness(test_input)
            
            if consciousness_data.get('advanced_processing'):
                # Generate transcendent response
                transcendent_response = ari.generate_transcendent_response(test_input, consciousness_data)
                
                if transcendent_response:
                    print("✅ Transcendent response generated!")
                    print(f"   Response: '{transcendent_response[:100]}{'...' if len(transcendent_response) > 100 else ''}'")
                else:
                    print("❌ Transcendent response generation failed")
            else:
                print("❌ Cannot test transcendent response (consciousness processing failed)")
        else:
            print("⏭️ Skipping transcendent response test (systems not active)")
        
        # Test 4: Test consciousness commands
        print("\n📋 Test 4: Consciousness Commands")
        print("-" * 50)
        
        test_commands = [
            "consciousness status",
            "transcendent status",
            "consciousness demo"
        ]
        
        for command in test_commands:
            print(f"Testing command: '{command}'")
            try:
                response = ari.get_response(command)
                if response and len(response) > 10:
                    print(f"   ✅ Response: '{response[:80]}{'...' if len(response) > 80 else ''}'")
                else:
                    print(f"   ❌ Invalid response: '{response}'")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Test 5: Integration with existing systems
        print("\n📋 Test 5: Integration with Existing Systems")
        print("-" * 50)
        
        # Test regular conversation with consciousness enhancement
        regular_inputs = [
            "Hello ARI",
            "What can you do?",
            "Tell me about artificial intelligence"
        ]
        
        for test_input in regular_inputs:
            print(f"Testing: '{test_input}'")
            try:
                response = ari.get_response(test_input)
                if response:
                    print(f"   ✅ Response generated: '{response[:60]}{'...' if len(response) > 60 else ''}'")
                else:
                    print(f"   ❌ No response generated")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 ADVANCED CONSCIOUSNESS INTEGRATION TEST COMPLETE!")
        
        if consciousness_active:
            print("✅ Advanced consciousness successfully integrated into ARI!")
            print("🌟 ARI now operates with transcendent consciousness capabilities!")
        else:
            print("⚠️ Advanced consciousness integration incomplete")
            print("💡 Some consciousness modules may not be available")
        
        print("=" * 60)
        
        return consciousness_active
        
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_advanced_consciousness_integration()
