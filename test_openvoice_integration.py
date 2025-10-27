#!/usr/bin/env python3
"""
Test OpenVoice integration with the Flask app
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.openvoice_service import get_openvoice_service

def test_basic_generation():
    """Test basic audio generation without voice cloning"""
    print("\n" + "="*60)
    print("TEST 1: Basic Audio Generation (Default Voice)")
    print("="*60)
    
    try:
        openvoice = get_openvoice_service()
        
        test_text = "Hello! This is OpenVoice, a high-quality text-to-speech system with voice cloning capabilities. It is licensed under MIT, making it perfect for commercial use."
        output_path = "outputs/test_openvoice_default.wav"
        
        os.makedirs("outputs", exist_ok=True)
        
        print(f"\n📝 Generating audio...")
        print(f"   Text: {test_text[:80]}...")
        print(f"   Output: {output_path}")
        
        result = openvoice.generate_audio(
            text=test_text,
            output_path=output_path,
            language='en'
        )
        
        if os.path.exists(result):
            file_size = os.path.getsize(result) / 1024  # KB
            print(f"\n✅ SUCCESS: Audio generated!")
            print(f"   File: {result}")
            print(f"   Size: {file_size:.1f} KB")
            return True
        else:
            print(f"\n❌ FAILED: Output file not created")
            return False
            
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_voice_cloning():
    """Test voice cloning with reference audio"""
    print("\n" + "="*60)
    print("TEST 2: Voice Cloning with Reference Audio")
    print("="*60)
    
    try:
        openvoice = get_openvoice_service()
        
        # Use the sample voice we created earlier
        reference_audio = "sample_voice_reference.wav"
        
        if not os.path.exists(reference_audio):
            print(f"\n⚠️  SKIPPED: Reference audio not found: {reference_audio}")
            print("   Run generate_sample_voice.py first to create a sample")
            return None
        
        test_text = "This is a test of voice cloning using OpenVoice. The cloned voice should sound similar to the reference audio."
        output_path = "outputs/test_openvoice_cloned.wav"
        
        print(f"\n📝 Generating audio with voice cloning...")
        print(f"   Text: {test_text[:80]}...")
        print(f"   Reference: {reference_audio}")
        print(f"   Output: {output_path}")
        
        result = openvoice.generate_audio(
            text=test_text,
            output_path=output_path,
            speaker_wav=reference_audio,
            language='en'
        )
        
        if os.path.exists(result):
            file_size = os.path.getsize(result) / 1024  # KB
            print(f"\n✅ SUCCESS: Voice cloned audio generated!")
            print(f"   File: {result}")
            print(f"   Size: {file_size:.1f} KB")
            return True
        else:
            print(f"\n❌ FAILED: Output file not created")
            return False
            
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_info():
    """Test getting model information"""
    print("\n" + "="*60)
    print("TEST 3: Model Information")
    print("="*60)
    
    try:
        openvoice = get_openvoice_service()
        info = openvoice.get_model_info()
        
        print(f"\n📋 OpenVoice Model Info:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        print("\n✅ Model info retrieved successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎤 OpenVoice Integration Test Suite")
    print("="*60)
    
    results = {
        'Basic Generation': test_basic_generation(),
        'Voice Cloning': test_voice_cloning(),
        'Model Info': test_model_info()
    }
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⚠️  SKIPPED"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r is True)
    total = len([r for r in results.values() if r is not None])
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total and total > 0:
        print("\n🎉 All tests passed! OpenVoice is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Start the Flask app: python app.py")
        print("   2. Open http://localhost:5000 in your browser")
        print("   3. Select 'OpenVoice (MIT License - Voice Cloning)' from the model dropdown")
        print("   4. Enter text and optionally upload a voice sample")
        print("   5. Generate your audio!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
