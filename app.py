import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, url_for
from flask_cors import CORS
from services.tts_service import TTSService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'generated_audio'
app.config['SPEAKER_UPLOAD_FOLDER'] = 'speaker_audio'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize TTS service
tts_service = TTSService()

@app.route('/')
def index():
    """Main page with the audio generation form."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_audio():
    """Generate audio from text using Coqui TTS."""
    try:
        # Check if request contains files (for voice cloning)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle file upload for voice cloning
            text = request.form.get('text', '').strip()
            model_name = request.form.get('model', 'tts_models/en/ljspeech/tacotron2-DDC')
            speaker = request.form.get('speaker', None)
            language = request.form.get('language', 'en')
            speed = float(request.form.get('speed', 1.0))
            
            # Get speaker audio file if provided
            speaker_wav_path = None
            if 'speaker_audio' in request.files:
                speaker_file = request.files['speaker_audio']
                if speaker_file.filename:
                    # Save uploaded speaker audio
                    speaker_filename = f"speaker_{uuid.uuid4().hex}.wav"
                    speaker_wav_path = os.path.join(app.config['SPEAKER_UPLOAD_FOLDER'], speaker_filename)
                    os.makedirs(app.config['SPEAKER_UPLOAD_FOLDER'], exist_ok=True)
                    speaker_file.save(speaker_wav_path)
                    logger.info(f"Saved speaker audio to {speaker_wav_path}")
        else:
            # Handle JSON request (original behavior)
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({'error': 'No text provided'}), 400
            
            text = data['text'].strip()
            model_name = data.get('model', 'tts_models/en/ljspeech/tacotron2-DDC')
            speaker = data.get('speaker', None)
            language = data.get('language', 'en')
            speed = data.get('speed', 1.0)
            speaker_wav_path = None
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        logger.info(f"Generating audio for text: {text[:50]}...")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"audio_{timestamp}_{unique_id}.wav"
        
        # Generate audio
        success, audio_path, error_msg = tts_service.generate_audio(
            text=text,
            output_path=os.path.join(app.config['UPLOAD_FOLDER'], filename),
            model_name=model_name,
            speaker=speaker,
            language=language,
            speed=speed,
            speaker_wav=speaker_wav_path
        )
        
        # Clean up uploaded speaker file after generation
        if speaker_wav_path and os.path.exists(speaker_wav_path):
            try:
                os.remove(speaker_wav_path)
                logger.info(f"Cleaned up speaker audio: {speaker_wav_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up speaker audio: {e}")
        
        if success:
            audio_url = url_for('download_audio', filename=filename)
            return jsonify({
                'success': True,
                'audio_url': audio_url,
                'filename': filename,
                'text': text,
                'model': model_name
            })
        else:
            logger.error(f"Audio generation failed: {error_msg}")
            return jsonify({'error': error_msg}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in generate_audio: {str(e)}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_audio(filename):
    """Download generated audio file."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({'error': 'Error downloading file'}), 500

@app.route('/models')
def get_models():
    """Get available TTS models."""
    try:
        models = tts_service.get_available_models()
        return jsonify({'models': models})
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return jsonify({'error': 'Error fetching models'}), 500

@app.route('/speakers/<path:model_name>')
def get_speakers(model_name):
    """Get available speakers for a specific model."""
    try:
        speakers = tts_service.get_speakers(model_name)
        return jsonify({'speakers': speakers})
    except Exception as e:
        logger.error(f"Error getting speakers for model {model_name}: {str(e)}")
        return jsonify({'error': 'Error fetching speakers'}), 500

@app.route('/languages/<path:model_name>')
def get_languages(model_name):
    """Get available languages for a specific model."""
    try:
        languages = tts_service.get_languages(model_name)
        return jsonify({'languages': languages})
    except Exception as e:
        logger.error(f"Error getting languages for model {model_name}: {str(e)}")
        return jsonify({'error': 'Error fetching languages'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['SPEAKER_UPLOAD_FOLDER'], exist_ok=True)
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)