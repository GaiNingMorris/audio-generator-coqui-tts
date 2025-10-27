#!/usr/bin/env python3
"""
Download free voice samples for XTTS v2 voice cloning
"""

import os
import requests
from pathlib import Path

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filename) / 1024  # KB
        print(f"✓ Downloaded: {filename} ({file_size:.1f} KB)")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def download_voice_samples():
    """Download free voice samples from various sources"""
    
    # Create voices directory
    voices_dir = "voice_samples"
    os.makedirs(voices_dir, exist_ok=True)
    
    print("=" * 60)
    print("Downloading Free Voice Samples")
    print("=" * 60)
    print()
    
    # List of free voice samples (you'll need to find actual URLs)
    samples = {
        # LJSpeech sample (if available publicly)
        "ljspeech_sample.wav": "https://example.com/ljspeech_sample.wav",
        
        # Note: You'll need to manually download from these sources:
        # - LibriVox: https://librivox.org/
        # - Common Voice: https://commonvoice.mozilla.org/
        # - VCTK: https://datashare.ed.ac.uk/handle/10283/3443
    }
    
    print("📚 Recommended Sources (Manual Download):")
    print()
    print("1. LibriVox (Audiobooks)")
    print("   → https://librivox.org/")
    print("   → Download any MP3, extract 10-15 seconds")
    print()
    print("2. Common Voice by Mozilla")
    print("   → https://commonvoice.mozilla.org/")
    print("   → Download validated clips")
    print()
    print("3. VCTK Corpus (110 speakers)")
    print("   → https://datashare.ed.ac.uk/handle/10283/3443")
    print("   → Download and extract WAV files")
    print()
    print("4. Record Your Own Voice")
    print("   → Use your phone or computer")
    print("   → Speak clearly for 10-15 seconds")
    print("   → Save as WAV or MP3")
    print()
    
    print("=" * 60)
    print("Voice Samples Directory Created:")
    print(f"  → {os.path.abspath(voices_dir)}")
    print()
    print("Place your downloaded voice samples in this folder!")
    print("=" * 60)

def create_recording_script():
    """Create a simple script to record your own voice"""
    script = """#!/usr/bin/env python3
'''
Record your own voice sample for XTTS v2
Requires: pip install sounddevice soundfile
'''

import sounddevice as sd
import soundfile as sf
import numpy as np

def record_voice():
    duration = 15  # seconds
    sample_rate = 22050  # Hz
    
    print("=" * 60)
    print("Voice Recording Tool")
    print("=" * 60)
    print()
    print(f"Recording for {duration} seconds...")
    print("Speak clearly and naturally!")
    print()
    print("3...")
    import time
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("🎙️ RECORDING NOW!")
    print()
    
    # Record audio
    recording = sd.rec(int(duration * sample_rate), 
                      samplerate=sample_rate, 
                      channels=1, 
                      dtype=np.float32)
    sd.wait()
    
    print("✓ Recording complete!")
    
    # Save to file
    filename = "voice_samples/my_voice.wav"
    sf.write(filename, recording, sample_rate)
    
    print(f"✓ Saved to: {filename}")
    print()
    print("Now you can use this file with XTTS v2!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        record_voice()
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("To install required packages:")
        print("  pip install sounddevice soundfile")
"""
    
    with open("record_voice.py", "w") as f:
        f.write(script)
    
    print("\n✓ Created: record_voice.py")
    print("  Run this to record your own voice!")

if __name__ == "__main__":
    download_voice_samples()
    create_recording_script()
    
    print("\n💡 Quick Tips:")
    print("  • Best quality: Studio recordings (VCTK, LibriVox)")
    print("  • Good quality: Clean phone recordings")
    print("  • Voice length: 10-15 seconds optimal")
    print("  • Content: Natural speech, not singing")
    print("  • Environment: Quiet room, no echo")
