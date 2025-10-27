#!/usr/bin/env python3
"""
Generate a sample voice audio file for testing voice cloning
"""

from TTS.api import TTS
import os

def generate_sample_voice():
    """Generate a sample voice file using Tacotron2"""
    print("Generating sample voice audio...")
    
    # Sample text for the reference voice (10-15 seconds of speech)
    sample_text = """
    Hello, my name is the sample voice. This is a demonstration of text to speech technology.
    I'm speaking clearly and naturally so that my voice can be used as a reference.
    The quality of this recording will determine how well the voice cloning works.
    """
    
    output_file = "sample_voice_reference.wav"
    
    try:
        # Use Tacotron2 to generate a clean voice sample
        print("Loading Tacotron2 model...")
        tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
        
        print(f"Generating audio to: {output_file}")
        tts.tts_to_file(text=sample_text.strip(), file_path=output_file)
        
        print(f"✓ Sample voice created: {output_file}")
        print(f"\nYou can now use this file to test voice cloning:")
        print(f"  1. Go to http://localhost:5000")
        print(f"  2. Select 'XTTS v2 (Voice Cloning)'")
        print(f"  3. Upload '{output_file}'")
        print(f"  4. Enter any text you want")
        print(f"  5. Generate audio!")
        
        # Get file size
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f"\nFile size: {file_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating sample voice: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Sample Voice Generator")
    print("=" * 60)
    print()
    
    generate_sample_voice()
    
    print("\n" + "=" * 60)
