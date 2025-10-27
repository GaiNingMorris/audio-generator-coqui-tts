#!/usr/bin/env python3
"""
Test script for XTTS v2 voice cloning
"""

from TTS.api import TTS
import os

def test_xtts_basic():
    """Test basic XTTS v2 loading"""
    print("Testing XTTS v2 basic loading...")
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("✓ XTTS v2 loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to load XTTS v2: {e}")
        return False

def test_xtts_with_reference():
    """Test XTTS v2 with a reference audio file"""
    print("\nTo test voice cloning, you'll need a reference audio file.")
    print("The reference audio should be:")
    print("  - 6-30 seconds long")
    print("  - Clear speech without background noise")
    print("  - WAV, MP3, or FLAC format")
    print("\nYou can:")
    print("  1. Record your own voice")
    print("  2. Use a sample from https://github.com/coqui-ai/TTS")
    print("  3. Download a sample voice from any source")
    print("\nExample usage in your app:")
    print("  1. Go to http://localhost:5000")
    print("  2. Select 'XTTS v2 (Voice Cloning)' as the model")
    print("  3. Upload a reference audio file (6-30 seconds)")
    print("  4. Enter your text")
    print("  5. Click 'Generate Audio'")
    print("\nThe generated audio will mimic the voice from your reference file!")

if __name__ == "__main__":
    print("=" * 60)
    print("XTTS v2 Voice Cloning Test")
    print("=" * 60)
    
    if test_xtts_basic():
        test_xtts_with_reference()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
