"""
Suno Bark TTS Service
Provides emotionally expressive TTS with support for nonverbal communications
License: MIT (commercial-safe)
"""

import os
import re
import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io import wavfile


class BarkService:
    """
    Suno Bark TTS service with emotional tag support
    
    Bark natively supports these emotional tags:
    - [laughs], [laughter] - Laughter
    - [sighs] - Sighing  
    - [gasps] - Gasping
    - [clears throat] - Throat clearing
    - [music] - Music
    - ... - Pauses/hesitation
    - — - Longer pause
    - CAPS - Emphasis
    - [MAN], [WOMAN] - Gender hints
    """
    
    # Voice presets available in Bark
    # Format: language_speakernumber (e.g., v2/en_speaker_6)
    VOICE_PRESETS = {
        'en': list(range(10)),  # en_speaker_0 to en_speaker_9
        'de': list(range(10)),
        'es': list(range(10)),
        'fr': list(range(10)),
        'hi': list(range(10)),
        'it': list(range(10)),
        'ja': list(range(10)),
        'ko': list(range(10)),
        'pl': list(range(10)),
        'pt': list(range(10)),
        'ru': list(range(10)),
        'tr': list(range(10)),
        'zh': list(range(10)),
    }
    
    def __init__(self):
        """Initialize Bark models"""
        self.models_loaded = False
        print("🐶 Suno Bark TTS Service initializing...")
        
        # Set environment variables for memory optimization
        # Use small models if low on VRAM
        if os.environ.get('USE_SMALL_BARK_MODELS', 'False').lower() == 'true':
            os.environ["SUNO_USE_SMALL_MODELS"] = "True"
            print("   Using small models for lower memory usage")
        
        # Offload to CPU if needed
        if os.environ.get('BARK_OFFLOAD_CPU', 'False').lower() == 'true':
            os.environ["SUNO_OFFLOAD_CPU"] = "True"
            print("   CPU offloading enabled")
    
    def _ensure_models_loaded(self):
        """Lazy load Bark models on first use"""
        if not self.models_loaded:
            print("📦 Loading Bark models (this may take a minute on first run)...")
            preload_models()
            self.models_loaded = True
            print("✅ Bark models loaded successfully")
    
    def preprocess_emotional_tags(self, text):
        """
        Preprocess text for Bark TTS
        
        Bark natively supports these tags:
        - [laughs], [laughter] - Laughter
        - [sighs] - Sighing
        - [gasps] - Gasping
        - [clears throat] - Throat clearing
        - [music] - Music
        - ... - Pauses/hesitation
        - — - Longer pause
        - CAPS - Emphasis
        - [MAN], [WOMAN] - Gender hints
        
        This method only cleans up formatting, no tag conversion.
        
        Args:
            text: Input text with Bark-compatible tags
            
        Returns:
            Cleaned text
        """
        # Clean up multiple spaces
        cleaned_text = re.sub(r'\s+', ' ', text)
        
        # Clean up spaces before punctuation
        cleaned_text = re.sub(r'\s+([.,!?;:])', r'\1', cleaned_text)
        
        # Normalize ellipsis (4+ dots -> 3 dots)
        cleaned_text = re.sub(r'\.{4,}', '...', cleaned_text)
        
        return cleaned_text.strip()
    
    def generate_audio(self, text, output_path, voice_preset=None, language='en', **kwargs):
        """
        Generate audio using Bark with emotional expression
        
        Args:
            text: Text to synthesize (can include emotional tags)
            output_path: Path to save output audio
            voice_preset: Voice preset (e.g., 'v2/en_speaker_6') or speaker number (0-9)
            language: Language code (default: 'en')
            **kwargs: Additional parameters (ignored for compatibility)
            
        Returns:
            Path to generated audio file
        """
        try:
            self._ensure_models_loaded()
            
            print(f"🔊 Generating audio with Bark...")
            print(f"   Text length: {len(text)} characters")
            
            # Preprocess emotional tags
            processed_text = self.preprocess_emotional_tags(text)
            
            if processed_text != text:
                print(f"   Processed emotional tags")
                print(f"   Original: {text[:100]}...")
                print(f"   Processed: {processed_text[:100]}...")
            
            # Determine voice preset
            if voice_preset is None:
                # Use default voice for language
                voice_preset = f"v2/{language}_speaker_6"
            elif isinstance(voice_preset, int):
                # Convert speaker number to full preset
                voice_preset = f"v2/{language}_speaker_{voice_preset}"
            
            print(f"   Voice: {voice_preset}")
            print(f"   Language: {language}")
            
            # Generate audio
            # Note: Bark outputs ~13-14 seconds per generation
            # For longer text, you may need to split it
            if len(processed_text) > 250:
                print(f"   ⚠️  Text is long ({len(processed_text)} chars). Bark works best with <250 characters.")
                print(f"   Consider splitting into multiple segments for better quality.")
            
            audio_array = generate_audio(
                processed_text,
                history_prompt=voice_preset
            )
            
            # Save audio to file
            wavfile.write(output_path, SAMPLE_RATE, audio_array)
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            duration = len(audio_array) / SAMPLE_RATE
            
            print(f"✅ Audio generated: {output_path}")
            print(f"   Size: {file_size:.1f} KB")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Sample rate: {SAMPLE_RATE} Hz")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to generate audio with Bark: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_long_form(self, text, output_path, voice_preset=None, language='en', chunk_size=250):
        """
        Generate audio for longer text by splitting into chunks
        
        Bark is optimized for ~13-14 seconds (roughly 150-250 characters).
        This method splits longer text and concatenates the audio.
        
        Args:
            text: Long text to synthesize
            output_path: Path to save final output
            voice_preset: Voice preset to use
            language: Language code
            chunk_size: Maximum characters per chunk (default: 250)
            
        Returns:
            Path to generated audio file
        """
        try:
            self._ensure_models_loaded()
            
            # Preprocess emotional tags first
            processed_text = self.preprocess_emotional_tags(text)
            
            # Split text into chunks at sentence boundaries
            sentences = re.split(r'(?<=[.!?])\s+', processed_text)
            
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= chunk_size:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            print(f"📚 Generating long-form audio in {len(chunks)} chunks...")
            
            # Generate audio for each chunk
            audio_arrays = []
            
            # Determine voice preset
            if voice_preset is None:
                full_preset = f"v2/{language}_speaker_6"
            elif isinstance(voice_preset, int):
                full_preset = f"v2/{language}_speaker_{voice_preset}"
            else:
                full_preset = voice_preset
            
            for i, chunk in enumerate(chunks):
                print(f"   Chunk {i+1}/{len(chunks)}: {len(chunk)} chars")
                audio_array = generate_audio(
                    chunk,
                    history_prompt=full_preset
                )
                audio_arrays.append(audio_array)
            
            # Concatenate all audio arrays
            full_audio = np.concatenate(audio_arrays)
            
            # Save to file
            wavfile.write(output_path, SAMPLE_RATE, full_audio)
            
            duration = len(full_audio) / SAMPLE_RATE
            print(f"✅ Long-form audio generated: {duration:.1f} seconds")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to generate long-form audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_model_info(self):
        """Get Bark model information"""
        return {
            'name': 'Suno Bark',
            'version': '0.0.1a0',
            'license': 'MIT',
            'voice_cloning': False,  # Bark uses presets, not cloning
            'voice_presets': True,
            'emotional_tags': True,
            'nonverbal_sounds': True,
            'multilingual': True,
            'languages': list(self.VOICE_PRESETS.keys()),
            'max_generation_length': '~13-14 seconds',
            'supported_tags': [
                '[laughs]', '[sighs]', '[gasps]', '[clears throat]',
                '[music]', '...', 'CAPS for emphasis'
            ]
        }


# Singleton instance
_bark_service = None

def get_bark_service():
    """Get or create Bark service singleton"""
    global _bark_service
    if _bark_service is None:
        _bark_service = BarkService()
    return _bark_service
