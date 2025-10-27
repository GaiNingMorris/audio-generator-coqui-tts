# 🎤 Audio Generator - Coqui TTS

A modern web-based text-to-speech application powered by Coqui TTS that converts text into high-quality audio with support for multiple languages, speakers, and voices.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.1+-green.svg)
![TTS](https://img.shields.io/badge/coqui--tts-v0.22+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

- 🎯 **Easy-to-use web interface** - Clean, responsive design
- 🎙️ **Multiple TTS models** - Support for various Coqui TTS models
- 🌍 **Multi-language support** - Generate speech in multiple languages
- 🎭 **Multiple speakers** - Choose from different voices (model dependent)
- ⚡ **Speed control** - Adjust speech speed from 0.5x to 2.0x
- 📱 **Responsive design** - Works on desktop, tablet, and mobile
- 💾 **Auto-save form data** - Remembers your settings
- 🎵 **High-quality audio** - Generate WAV format audio files
- 🔧 **RESTful API** - Programmatic access to TTS functionality

## Quick Start

### Prerequisites

- **Python 3.10 or higher** (3.11+ recommended for best compatibility)
- pip (Python package installer)
- 4GB+ RAM recommended
- CUDA-compatible GPU (optional, for faster processing)

> **Note**: Coqui TTS requires Python 3.10+ for full compatibility. Python 3.9 may have compatibility issues with some dependencies.

### Installation

1. **Clone or download this repository:**
   ```bash
   cd /path/to/your/projects
   git clone <repository-url> audio-generator-coqui-tts
   cd audio-generator-coqui-tts
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   
   **Option A: Using the run script (Recommended)**
   ```bash
   ./run.sh
   ```
   
   **Option B: Manual activation (single command)**
   ```bash
   source venv/bin/activate && python app.py
   ```
   
   **Option C: Direct virtual environment execution**
   ```bash
   ./venv/bin/python app.py
   ```

5. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

### Web Interface

1. **Enter your text** in the text area (up to 1000 characters recommended)
2. **Select a TTS model** from the dropdown menu
3. **Choose language and speaker** (if available for the selected model)
4. **Adjust speed** using the slider (0.5x to 2.0x)
5. **Click "Generate Audio"** to create your speech file
6. **Listen to the result** using the built-in audio player
7. **Download the audio file** if satisfied with the result

### API Usage

You can also use the application programmatically via its REST API:

```python
import requests

# Generate audio
response = requests.post('http://localhost:5000/generate', json={
    'text': 'Hello, this is a test of the audio generator.',
    'model': 'tts_models/en/ljspeech/tacotron2-DDC',
    'language': 'en',
    'speed': 1.0
})

if response.ok:
    result = response.json()
    audio_url = result['audio_url']
    print(f"Audio generated: {audio_url}")
```

## Available Models

### English Models
- **LJSpeech Tacotron2** - High-quality single speaker
- **VCTK VITS** - Multi-speaker with various accents
- **SAM Tacotron** - Alternative single speaker model

### Multilingual Models
- **Bark** - Highest quality, most natural human-like speech with emotions
- **YourTTS** - Zero-shot multi-speaker multilingual
- **XTTS v2** - Advanced multilingual voice cloning

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key configuration options:
- `DEFAULT_TTS_MODEL` - Default model to load
- `TTS_DEVICE` - Processing device (auto, cpu, cuda)
- `MAX_TEXT_LENGTH` - Maximum text length allowed
- `AUDIO_FORMAT` - Output audio format

### Advanced Configuration

Edit `config.json` for detailed configuration:
- Model specifications
- Performance settings
- Cleanup policies
- Logging configuration

## Project Structure

```
audio-generator-coqui-tts/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── config.json            # Application configuration
├── .env.example           # Environment variables template
├── services/
│   ├── __init__.py
│   └── tts_service.py     # TTS service implementation
├── templates/
│   └── index.html         # Web interface template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── app.js         # Frontend JavaScript
├── generated_audio/       # Generated audio files (created automatically)
└── README.md             # This file
```

## API Endpoints

### POST /generate
Generate audio from text.

**Request body:**
```json
{
    "text": "Text to convert to speech",
    "model": "tts_models/en/ljspeech/tacotron2-DDC",
    "language": "en",
    "speaker": "speaker_name",
    "speed": 1.0
}
```

**Response:**
```json
{
    "success": true,
    "audio_url": "/download/audio_20241026_120000_abc123.wav",
    "filename": "audio_20241026_120000_abc123.wav",
    "text": "Text to convert to speech",
    "model": "tts_models/en/ljspeech/tacotron2-DDC"
}
```

### GET /models
Get available TTS models.

### GET /speakers/{model_name}
Get available speakers for a specific model.

### GET /languages/{model_name}
Get available languages for a specific model.

### GET /download/{filename}
Download a generated audio file.

### GET /health
Health check endpoint.

## Troubleshooting

### Common Issues

1. **Virtual environment activation doesn't persist:**
   ```
   source venv/bin/activate  # This works
   python app.py            # But this runs in a different session
   ```
   **Solution**: Use a single command or the run script:
   ```bash
   # Single command (recommended)
   source venv/bin/activate && python app.py
   
   # Or use the run script
   ./run.sh
   ```

2. **"Failed to load model" error:**
   ```
   ERROR: Failed to load model tts_models/en/ljspeech/tacotron2-DDC
   ```
   **Solution**: This is usually a Python version compatibility issue. 
   - **Recommended**: Upgrade to Python 3.10+ and reinstall dependencies
   - **Alternative**: Use Python 3.10+ with pyenv or conda:
     ```bash
     # Using pyenv (recommended)
     pyenv install 3.11.0
     pyenv local 3.11.0
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

2. **"No module named 'TTS'" error:**
   ```bash
   pip install TTS
   ```

3. **Python syntax errors with | operator:**
   ```
   TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
   ```
   **Solution**: This is a Python 3.10+ syntax issue. Upgrade Python version.

4. **CUDA out of memory:**
   - Set `TTS_DEVICE=cpu` in your `.env` file
   - Reduce batch size in configuration

5. **Audio generation is slow:**
   - Use GPU if available (`TTS_DEVICE=cuda`)
   - Choose faster models like `glow-tts`

6. **Port 5000 already in use:**
   - Change the port in `app.py`: `app.run(port=5001)`

### Performance Tips

- **Use GPU acceleration** for faster generation
- **Choose appropriate models** based on your needs
- **Limit text length** for better performance
- **Enable cleanup** to manage disk space

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Adding New Features

1. **Backend changes:** Modify `app.py` or add new services in `services/`
2. **Frontend changes:** Update `templates/index.html`, `static/css/style.css`, or `static/js/app.js`
3. **Configuration:** Update `config.json` for new settings

### Testing

```bash
# Test the health endpoint
curl http://localhost:5000/health

# Test audio generation
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","model":"tts_models/en/ljspeech/tacotron2-DDC"}'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **Coqui TTS** - For providing the excellent TTS framework
- **Flask** - For the web framework
- **Contributors** - Thanks to all who help improve this project

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Join our community discussions

---

**Happy speech generation!** 🎤✨