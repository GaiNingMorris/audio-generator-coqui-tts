# Voice Cloning with XTTS v2 - Complete Guide

## Overview
Your audio generator now supports **voice cloning** using XTTS v2! This allows you to generate speech in any voice by providing a 6-30 second audio sample.

## ✅ What's Been Updated

### 1. Backend (Python)
- **app.py**: Added support for file uploads via multipart/form-data
- **tts_service.py**: Added `speaker_wav` parameter for voice cloning
- **Dependencies**: Downgraded PyTorch (2.5.1) and transformers (4.39.3) for XTTS v2 compatibility

### 2. Frontend (HTML/CSS/JS)
- **index.html**: Added file upload input for speaker reference audio
- **app.js**: Added logic to detect voice cloning models and handle file uploads
- **style.css**: Added styling for file input and voice cloning section

## 🚀 How to Use Voice Cloning

### Step 1: Start the App
```bash
source venv/bin/activate
python app.py
```

Then open http://localhost:5000 in your browser.

### Step 2: Prepare Your Reference Audio
You need a reference audio file (6-30 seconds) of the voice you want to clone:

**Requirements:**
- **Duration**: 6-30 seconds (optimal: 10-15 seconds)
- **Format**: WAV, MP3, M4A, FLAC, or other common audio formats
- **Quality**: Clear speech, minimal background noise
- **Content**: Natural speaking, not singing or whispering
- **Speaker**: Single speaker only (no multiple voices)

**Where to get reference audio:**
1. Record yourself speaking
2. Extract audio from a video
3. Use public domain audio
4. Ask someone to record a sample

### Step 3: Generate Cloned Voice
1. Select **"XTTS v2 (Voice Cloning)"** from the model dropdown
2. A new section will appear: "Speaker Audio (for Voice Cloning)"
3. Click **"Choose File"** and upload your reference audio
4. Select the language (17 languages supported!)
5. Enter your text (the words you want the cloned voice to say)
6. Adjust speed if needed (default: 1.0x)
7. Click **"Generate Audio"**

### Step 4: Listen & Download
- The generated audio will play automatically
- Click **"Download"** to save the WAV file
- The voice will match your reference audio!

## 📝 Example Use Cases

### 1. Personal Narration
Upload a recording of yourself reading 15 seconds of text, then generate hours of audiobook narration in your own voice.

### 2. Character Voices
Record different character voices and generate dialogue for each character.

### 3. Multilingual Content
Upload an English speaker, then generate speech in Spanish, French, German, etc. while maintaining voice characteristics.

### 4. Voice Consistency
Use the same reference audio across multiple generations to maintain consistent voice across all your audio files.

## 🌍 Supported Languages (XTTS v2)
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
- Russian (ru)
- Dutch (nl)
- Czech (cs)
- Arabic (ar)
- Chinese (zh)
- Japanese (ja)
- Hindi (hi)
- Hungarian (hu)
- Korean (ko)

## 🔧 Technical Details

### API Endpoint
**POST /generate**

With file upload (voice cloning):
```bash
curl -X POST http://localhost:5000/generate \
  -F "text=Hello, this is a cloned voice!" \
  -F "model=tts_models/multilingual/multi-dataset/xtts_v2" \
  -F "language=en" \
  -F "speed=1.0" \
  -F "speaker_audio=@/path/to/reference.wav"
```

Without file upload (regular TTS):
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "model": "tts_models/en/ljspeech/tacotron2-DDC",
    "language": "en",
    "speed": 1.0
  }'
```

### File Storage
- **Reference audio**: Temporarily saved to `speaker_audio/` (auto-deleted after generation)
- **Generated audio**: Saved to `generated_audio/`
- **Max file size**: 16MB

### Model Loading
XTTS v2 is loaded on-demand when first requested. First generation may take 30-60 seconds to load the model, subsequent generations are much faster (5-15 seconds depending on text length).

## ⚠️ Important Notes

### Licensing
- **XTTS v2** uses the CPML (Coqui Public Model License)
- **Free** for research and personal use
- **Commercial use** requires a license (but Coqui is shut down, so licensing is unclear)
- If you need guaranteed commercial licensing, use **YourTTS** or **Tacotron2** (both Apache 2.0)

### Performance
- **First generation**: 30-60 seconds (model loading)
- **Subsequent generations**: 5-15 seconds
- **Device**: CPU-only (no GPU required, but GPU would be faster)

### Quality Tips
For best voice cloning results:
1. Use high-quality reference audio (44.1kHz or 48kHz sample rate)
2. Avoid background noise, music, or other speakers
3. Use natural, conversational speech in the reference
4. Keep reference audio between 10-15 seconds
5. Ensure good pronunciation and clarity in reference

## 🐛 Troubleshooting

### "Invalid file: None" Error
This means XTTS v2 requires a reference audio file but none was provided.
- **Solution**: Upload a reference audio file when using XTTS v2

### Slow Generation
First generation is always slow (model loading). Subsequent generations are faster.
- **Solution**: Keep the server running for faster repeated generations

### File Upload Fails
Check that your file is under 16MB and in a supported format.
- **Solution**: Convert to WAV or MP3, reduce file size if needed

### Voice Doesn't Match
Quality of voice cloning depends on reference audio quality.
- **Solution**: Use clearer, longer (10-15s) reference audio with minimal noise

## 🎯 Next Steps

### Test It Now!
1. Start the app: `python app.py`
2. Visit http://localhost:5000
3. Select XTTS v2
4. Upload a voice sample
5. Generate your first cloned voice!

### Advanced Usage
- Try different languages with the same voice
- Experiment with speed adjustments (0.5x - 2.0x)
- Use multiple reference voices for different characters
- Batch process multiple texts with the same voice

## 📞 Need Help?
- Check the Flask app logs for error messages
- Verify your reference audio meets the requirements
- Try a different reference audio file
- Check that all dependencies are installed correctly

---

**Enjoy creating amazing voice-cloned audio!** 🎙️✨
