"""
OpenVoice TTS Service
Provides voice cloning and TTS generation using OpenVoice (MIT License)
"""

import os
import sys
import torch
import tempfile
from pathlib import Path

# Add OpenVoice to path
OPENVOICE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'OpenVoice')
sys.path.insert(0, OPENVOICE_PATH)

from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter


class OpenVoiceService:
    """OpenVoice TTS service with voice cloning support"""
    
    # Language code mapping: lowercase ISO codes -> OpenVoice format
    LANGUAGE_MAP = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'kr': 'Korean'
    }
    
    def __init__(self):
        """Initialize OpenVoice models"""
        self.base_path = OPENVOICE_PATH
        self.ckpt_base = os.path.join(self.base_path, 'checkpoints/base_speakers/EN')
        self.ckpt_converter = os.path.join(self.base_path, 'checkpoints/converter')
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        self.base_speaker_tts = None
        self.tone_color_converter = None
        self.source_se = None
        
        print(f"🎤 OpenVoice initializing on device: {self.device}")
        self._load_models()
    
    def _load_models(self):
        """Load OpenVoice models and embeddings"""
        try:
            # Load base speaker TTS
            print("📝 Loading OpenVoice base speaker TTS...")
            self.base_speaker_tts = BaseSpeakerTTS(
                f'{self.ckpt_base}/config.json', 
                device=self.device
            )
            self.base_speaker_tts.load_ckpt(f'{self.ckpt_base}/checkpoint.pth')
            
            # Load tone color converter
            print("🎨 Loading OpenVoice tone color converter...")
            self.tone_color_converter = ToneColorConverter(
                f'{self.ckpt_converter}/config.json', 
                device=self.device
            )
            self.tone_color_converter.load_ckpt(f'{self.ckpt_converter}/checkpoint.pth')
            
            # Load default source embedding
            print("🎵 Loading default source embedding...")
            self.source_se = torch.load(
                f'{self.ckpt_base}/en_default_se.pth', 
                map_location=self.device,
                weights_only=False
            )
            
            print("✅ OpenVoice models loaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to load OpenVoice models: {e}")
            raise
    
    def extract_voice_embedding(self, audio_path):
        """
        Extract voice embedding from reference audio
        
        Args:
            audio_path: Path to reference audio file (6-30 seconds recommended)
            
        Returns:
            Voice embedding tensor
        """
        try:
            print(f"🎤 Extracting voice embedding from: {audio_path}")
            
            # Create temporary directory for processed audio
            with tempfile.TemporaryDirectory() as temp_dir:
                target_se, _ = se_extractor.get_se(
                    audio_path, 
                    self.tone_color_converter, 
                    target_dir=temp_dir,
                    vad=True
                )
            
            print("✅ Voice embedding extracted successfully")
            return target_se
            
        except Exception as e:
            print(f"❌ Failed to extract voice embedding: {e}")
            raise
    
    def generate_audio(self, text, output_path, speaker_wav=None, language='en', speed=1.0):
        """
        Generate audio using OpenVoice
        
        Args:
            text: Text to synthesize
            output_path: Path to save output audio
            speaker_wav: Optional path to reference audio for voice cloning
            language: Language code (default: 'en')
            speed: Speech speed multiplier (default: 1.0)
            
        Returns:
            Path to generated audio file
        """
        try:
            print(f"🔊 Generating audio with OpenVoice...")
            print(f"   Text length: {len(text)} characters")
            print(f"   Voice cloning: {'Yes' if speaker_wav else 'No (default voice)'}")
            
            # Create temporary file for base audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_base_path = temp_file.name
            
            try:
                # Step 1: Generate base audio with base speaker
                print("📝 Step 1: Generating base audio...")
                
                # Map language code to OpenVoice format
                openvoice_language = self.LANGUAGE_MAP.get(language.lower(), 'English')
                print(f"   Language: {language} -> {openvoice_language}")
                
                self.base_speaker_tts.tts(
                    text,
                    temp_base_path,
                    speaker='default',
                    language=openvoice_language,
                    speed=speed
                )
                
                # Step 2: Convert tone color if reference audio provided
                if speaker_wav and os.path.exists(speaker_wav):
                    print("🎨 Step 2: Converting to target voice...")
                    
                    # Extract target voice embedding
                    target_se = self.extract_voice_embedding(speaker_wav)
                    
                    # Convert tone color
                    encode_message = "@MyShell"  # Watermark (required by OpenVoice)
                    self.tone_color_converter.convert(
                        audio_src_path=temp_base_path,
                        src_se=self.source_se,
                        tgt_se=target_se,
                        output_path=output_path,
                        message=encode_message
                    )
                    
                    print("✅ Voice cloning completed")
                else:
                    # No voice cloning, use base audio
                    print("📄 Using default voice (no cloning)")
                    import shutil
                    shutil.move(temp_base_path, output_path)
                
                print(f"✅ Audio generated: {output_path}")
                return output_path
                
            finally:
                # Clean up temporary base audio
                if os.path.exists(temp_base_path):
                    try:
                        os.remove(temp_base_path)
                    except:
                        pass
                        
        except Exception as e:
            print(f"❌ Failed to generate audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_long_form(self, text, output_path, speaker_wav=None, language='en', speed=1.0, chunk_size=1000):
        """
        Generate audio for long text by splitting into chunks
        
        This method automatically splits long text into manageable chunks,
        generates audio for each chunk, and concatenates them into one file.
        
        Args:
            text: Long text to synthesize
            output_path: Path to save final output
            speaker_wav: Optional path to reference audio for voice cloning
            language: Language code (default: 'en')
            speed: Speech speed multiplier (default: 1.0)
            chunk_size: Maximum characters per chunk (default: 1000)
            
        Returns:
            Path to generated audio file
        """
        try:
            print(f"📚 Generating long-form audio with OpenVoice...")
            print(f"   Total text length: {len(text)} characters")
            
            # Extract voice embedding once if cloning
            target_se = None
            if speaker_wav and os.path.exists(speaker_wav):
                print("🎤 Extracting voice embedding (one-time)...")
                target_se = self.extract_voice_embedding(speaker_wav)
            
            # Split text into chunks at sentence boundaries
            import re
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
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
            
            print(f"   Split into {len(chunks)} chunks")
            
            # Generate audio for each chunk
            from pydub import AudioSegment
            audio_segments = []
            
            openvoice_language = self.LANGUAGE_MAP.get(language.lower(), 'English')
            
            for i, chunk in enumerate(chunks):
                print(f"\n   📝 Chunk {i+1}/{len(chunks)}: {len(chunk)} chars")
                
                # Create temp files
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_base:
                    temp_base_path = temp_base.name
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_final:
                    temp_final_path = temp_final.name
                
                try:
                    # Generate base audio
                    print(f"      Generating base audio...")
                    self.base_speaker_tts.tts(
                        chunk,
                        temp_base_path,
                        speaker='default',
                        language=openvoice_language,
                        speed=speed
                    )
                    
                    # Convert tone if cloning
                    if target_se is not None:
                        print(f"      Converting to cloned voice...")
                        self.tone_color_converter.convert(
                            audio_src_path=temp_base_path,
                            src_se=self.source_se,
                            tgt_se=target_se,
                            output_path=temp_final_path,
                            message="@MyShell"
                        )
                        audio_segments.append(AudioSegment.from_wav(temp_final_path))
                    else:
                        audio_segments.append(AudioSegment.from_wav(temp_base_path))
                    
                    print(f"      ✅ Chunk {i+1} complete")
                    
                finally:
                    # Cleanup temp files
                    for temp_path in [temp_base_path, temp_final_path]:
                        if os.path.exists(temp_path):
                            try:
                                os.remove(temp_path)
                            except:
                                pass
            
            # Concatenate all chunks
            print(f"\n🔗 Concatenating {len(audio_segments)} audio chunks...")
            combined = audio_segments[0]
            for segment in audio_segments[1:]:
                combined += segment
            
            # Export final audio
            combined.export(output_path, format="wav")
            
            duration = len(combined) / 1000.0  # milliseconds to seconds
            file_size = os.path.getsize(output_path) / 1024  # bytes to KB
            
            print(f"\n✅ Long-form audio generated!")
            print(f"   Output: {output_path}")
            print(f"   Duration: {duration:.1f} seconds")
            print(f"   Size: {file_size:.1f} KB")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Failed to generate long-form audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def get_model_info(self):
        """Get OpenVoice model information"""
        return {
            'name': 'OpenVoice',
            'version': 'v2',
            'license': 'MIT',
            'voice_cloning': True,
            'multilingual': True,
            'device': self.device,
            'languages': ['en', 'es', 'fr', 'zh', 'ja', 'kr']
        }


# Singleton instance
_openvoice_service = None

def get_openvoice_service():
    """Get or create OpenVoice service singleton"""
    global _openvoice_service
    if _openvoice_service is None:
        _openvoice_service = OpenVoiceService()
    return _openvoice_service
