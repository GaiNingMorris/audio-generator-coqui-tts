import os
import logging
import json
from typing import Tuple, List, Optional, Union
import torch
import tempfile

logger = logging.getLogger(__name__)

# Import OpenVoice service
try:
    from services.openvoice_service import get_openvoice_service
    OPENVOICE_AVAILABLE = True
except Exception as e:
    logger.warning(f"OpenVoice not available: {e}")
    OPENVOICE_AVAILABLE = False

class TTSService:
    """Service class for handling Text-to-Speech operations using Coqui TTS."""
    
    def __init__(self):
        """Initialize the TTS service."""
        self.tts = None
        self.current_model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"TTS Service initialized with device: {self.device}")
        
        # Default model to load
        self.default_model = "tts_models/en/ljspeech/tacotron2-DDC"
        # Don't load model immediately to avoid import issues
        logger.info("TTS Service initialized - models will be loaded on demand")
    
    def _load_model(self, model_name: str) -> bool:
        """Load a specific TTS model."""
        try:
            if self.current_model != model_name:
                logger.info(f"Loading TTS model: {model_name}")
                # Try to import TTS with error handling for compatibility issues
                try:
                    from TTS.api import TTS
                    self.tts = TTS(model_name=model_name).to(self.device)
                    self.current_model = model_name
                    logger.info(f"Successfully loaded model: {model_name}")
                    return True
                except (TypeError, SyntaxError) as e:
                    # Handle Python version compatibility issues
                    logger.error(f"Python compatibility issue with TTS library: {str(e)}")
                    logger.info("This appears to be a Python version compatibility issue.")
                    logger.info("Coqui TTS requires Python 3.10+ for the latest features.")
                    return False
                except Exception as e:
                    # Handle other TTS-specific errors
                    logger.error(f"TTS loading error: {str(e)}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            return False
    
    def generate_audio(self, 
                      text: str, 
                      output_path: str,
                      model_name: Optional[str] = None,
                      speaker: Optional[str] = None,
                      language: Optional[str] = None,
                      speed: float = 1.0,
                      speaker_wav: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Generate audio from text using the specified TTS model.
        
        Args:
            text: Text to convert to speech
            output_path: Path where the audio file will be saved
            model_name: TTS model to use (optional)
            speaker: Speaker name for multi-speaker models (optional)
            language: Language code (optional)
            speed: Speech speed multiplier (optional)
            speaker_wav: Path to reference audio for voice cloning (optional)
            
        Returns:
            Tuple of (success, output_path, error_message)
        """
        try:
            # Use default model if none specified
            if not model_name:
                model_name = self.default_model
            
            # Check if OpenVoice model is requested
            if model_name == 'openvoice' or model_name == 'tts_models/multilingual/openvoice':
                if not OPENVOICE_AVAILABLE:
                    return False, "", "OpenVoice is not available"
                
                try:
                    logger.info("Using OpenVoice for generation")
                    openvoice = get_openvoice_service()
                    
                    # Use default language if not specified
                    if not language:
                        language = 'en'
                    
                    # Generate audio with OpenVoice
                    openvoice.generate_audio(
                        text=text,
                        output_path=output_path,
                        speaker_wav=speaker_wav,
                        language=language,
                        speed=speed
                    )
                    
                    logger.info(f"OpenVoice audio generated successfully: {output_path}")
                    return True, output_path, None
                    
                except Exception as e:
                    error_msg = f"OpenVoice generation error: {str(e)}"
                    logger.error(error_msg)
                    return False, "", error_msg
            
            # Load model if different from current
            if not self._load_model(model_name):
                return False, "", f"Failed to load model: {model_name}"
            
            # Prepare synthesis parameters
            synthesis_kwargs = {}
            
            # Add speaker if specified and supported
            if speaker and hasattr(self.tts, 'speakers') and self.tts.speakers:
                if speaker in self.tts.speakers:
                    synthesis_kwargs['speaker'] = speaker
                else:
                    logger.warning(f"Speaker '{speaker}' not found in model. Using default.")
            
            # Add language - required for multilingual models like XTTS v2
            if language:
                # For XTTS and other multilingual models, always pass language
                if 'xtts' in model_name.lower() or 'your_tts' in model_name.lower():
                    synthesis_kwargs['language'] = language
                    logger.info(f"Using language: {language}")
                # For other models, check if language is supported
                elif hasattr(self.tts, 'languages') and self.tts.languages:
                    if language in self.tts.languages:
                        synthesis_kwargs['language'] = language
                    else:
                        logger.warning(f"Language '{language}' not found in model. Using default.")
            
            # Add speaker_wav for voice cloning models (XTTS, YourTTS)
            if speaker_wav and os.path.exists(speaker_wav):
                synthesis_kwargs['speaker_wav'] = speaker_wav
                logger.info(f"Using speaker reference audio: {speaker_wav}")
            
            # Generate audio
            logger.info(f"Generating audio for text: {text[:50]}...")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate the audio
            self.tts.tts_to_file(text=text, file_path=output_path, **synthesis_kwargs)
            
            # Apply speed modification if needed
            if speed != 1.0:
                self._modify_audio_speed(output_path, speed)
            
            logger.info(f"Audio generated successfully: {output_path}")
            return True, output_path, None
            
        except Exception as e:
            error_msg = f"Error generating audio: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def _modify_audio_speed(self, audio_path: str, speed: float):
        """Modify the speed of an audio file."""
        try:
            from pydub import AudioSegment
            import numpy as np
            
            # Load audio
            audio = AudioSegment.from_wav(audio_path)
            
            # Change speed by changing frame rate
            # This maintains pitch while changing speed
            new_sample_rate = int(audio.frame_rate * speed)
            
            # Export with new sample rate
            modified_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
            modified_audio = modified_audio.set_frame_rate(audio.frame_rate)
            
            # Save back to the same file
            modified_audio.export(audio_path, format="wav")
            
        except Exception as e:
            logger.warning(f"Failed to modify audio speed: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available TTS models."""
        try:
            # Get models from TTS manager
            models = []
            
            # Common English models
            english_models = [
                "tts_models/en/ljspeech/tacotron2-DDC",
                "tts_models/en/ljspeech/tacotron2-DCA",
                "tts_models/en/ljspeech/glow-tts",
                "tts_models/en/ljspeech/speedy-speech",
                "tts_models/en/ljspeech/neural_hmm",
                "tts_models/en/vctk/vits",
                "tts_models/en/vctk/fast_pitch",
                "tts_models/en/sam/tacotron-DDC",
                "tts_models/en/blizzard2013/capacitron-t2-c50",
                "tts_models/en/blizzard2013/capacitron-t2-c150_v2"
            ]
            
            # Multi-language models
            multilingual_models = [
                "tts_models/multilingual/multi-dataset/bark",  # Highest quality
                "tts_models/multilingual/multi-dataset/your_tts",
                "tts_models/multilingual/multi-dataset/xtts_v2"
            ]
            
            # Add OpenVoice if available
            if OPENVOICE_AVAILABLE:
                multilingual_models.insert(0, "tts_models/multilingual/openvoice")  # Add at top
            
            models.extend(english_models)
            models.extend(multilingual_models)
            
            return models
            
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return [self.default_model]
    
    def get_speakers(self, model_name: str) -> List[str]:
        """Get available speakers for a specific model."""
        try:
            # Load model if different from current
            if not self._load_model(model_name):
                return []
            
            if hasattr(self.tts, 'speakers') and self.tts.speakers:
                return list(self.tts.speakers)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting speakers for model {model_name}: {str(e)}")
            return []
    
    def get_languages(self, model_name: str) -> List[str]:
        """Get available languages for a specific model."""
        try:
            # Load model if different from current
            if not self._load_model(model_name):
                return ['en']
            
            if hasattr(self.tts, 'languages') and self.tts.languages:
                return list(self.tts.languages)
            else:
                # Return common languages as fallback
                return ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh']
                
        except Exception as e:
            logger.error(f"Error getting languages for model {model_name}: {str(e)}")
            return ['en']
    
    def get_model_info(self, model_name: str) -> dict:
        """Get detailed information about a specific model."""
        try:
            model_info = {
                'name': model_name,
                'speakers': self.get_speakers(model_name),
                'languages': self.get_languages(model_name),
                'loaded': model_name == self.current_model
            }
            return model_info
            
        except Exception as e:
            logger.error(f"Error getting model info for {model_name}: {str(e)}")
            return {'name': model_name, 'speakers': [], 'languages': ['en'], 'loaded': False}
    
    def cleanup_old_files(self, directory: str, max_age_hours: int = 24):
        """Clean up old generated audio files."""
        try:
            import time
            current_time = time.time()
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > (max_age_hours * 3600):  # Convert hours to seconds
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {filename}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old files: {str(e)}")
    
    def health_check(self) -> dict:
        """Perform a health check of the TTS service."""
        try:
            status = {
                'service': 'healthy',
                'current_model': self.current_model,
                'device': self.device,
                'cuda_available': torch.cuda.is_available()
            }
            
            # Try a simple generation to test functionality
            test_text = "Hello, this is a test."
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as tmp_file:
                success, _, error = self.generate_audio(test_text, tmp_file.name)
                status['generation_test'] = 'passed' if success else f'failed: {error}'
            
            return status
            
        except Exception as e:
            return {
                'service': 'unhealthy',
                'error': str(e),
                'current_model': self.current_model,
                'device': self.device
            }