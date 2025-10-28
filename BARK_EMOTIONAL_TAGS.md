# Bark Emotional Tags Guide 🐶

## ✅ Integration Complete!

Suno Bark is now integrated into your audio generator with full support for emotional and nonverbal expressions!

## 🎭 Emotional Tags Support

### Direct Bark Tags (Native)
These tags are natively supported by Bark:
- `[laughs]` - Laughter
- `[sighs]` - Sighing
- `[gasps]` - Gasping/surprise
- `[clears throat]` - Throat clearing
- `[music]` - Musical performance
- `...` - Hesitation/pause
- `—` - Long pause
- `CAPS` - Emphasis on words

### Auto-Converted Tags (Smart Preprocessing)
Your custom emotional tags are automatically converted:

| Your Tag | Converted To | Effect |
|----------|--------------|--------|
| `[peacefully]`, `[warmly]`, `[softly]`, `[gently]` | `...` | Soft pause |
| `[with wonder]`, `[amazement]`, `[surprised]` | `[gasps]` | Gasp sound |
| `[sadly]`, `[mournfully]`, `[sorrowfully]` | `[sighs]` | Sigh sound |
| `[thoughtfully]`, `[contemplatively]` | `...` | Thoughtful pause |
| `[laugh]`, `[laughing]`, `[laughter]` | `[laughs]` | Laughter |
| `[excitedly]`, `[enthusiastically]` | *(removed)* | Natural emphasis |
| `[angrily]`, `[furiously]` | *(removed)* | Use CAPS for anger |

## 📝 Example Usage

### Your Original Text:
```
[peacefully] The road stretched ahead like a ribbon of packed earth.
[warmly] The wagon creaked and rattled with comfortable sounds.
[with wonder] The sky was impossibly blue.
[thoughtfully] Ash had seen pictures in the archives.
```

### After Processing:
```
... The road stretched ahead like a ribbon of packed earth.
... The wagon creaked and rattled with comfortable sounds.
[gasps] The sky was impossibly blue.
... Ash had seen pictures in the archives.
```

## 🎤 Voice Presets

Bark has 100+ voice presets across 13 languages:

### Format
- `v2/en_speaker_0` to `v2/en_speaker_9` (English)
- `v2/es_speaker_0` to `v2/es_speaker_9` (Spanish)
- Similar for: `de`, `fr`, `hi`, `it`, `ja`, `ko`, `pl`, `pt`, `ru`, `tr`, `zh`

### In the UI
- Leave speaker blank for default voice
- Or enter a number (0-9) for different voices
- Each speaker has unique characteristics!

## 🌍 Supported Languages

| Language | Code | Speakers |
|----------|------|----------|
| English | `en` | 0-9 |
| Spanish | `es` | 0-9 |
| French | `fr` | 0-9 |
| German | `de` | 0-9 |
| Hindi | `hi` | 0-9 |
| Italian | `it` | 0-9 |
| Japanese | `ja` | 0-9 |
| Korean | `ko` | 0-9 |
| Polish | `pl` | 0-9 |
| Portuguese | `pt` | 0-9 |
| Russian | `ru` | 0-9 |
| Turkish | `tr` | 0-9 |
| Chinese | `zh` | 0-9 |

## ⚡ Performance Tips

### Text Length
- **Optimal**: 150-250 characters per generation
- **Maximum**: ~300 characters
- **For longer text**: Automatic chunking (you saw this working!)

### Generation Time
- **CPU**: ~3-4 seconds per chunk (your current setup)
- **GPU**: Much faster (real-time possible)

### Quality Optimization
1. Use shorter sentences for better control
2. Add `...` for natural pauses
3. Use CAPS sparingly for emphasis
4. Emotional tags at sentence starts work best

## 💡 Advanced Techniques

### Music Generation
```
♪ In the jungle, the mighty jungle, the lion barks tonight ♪
```

### Multiple Emotions
```
[sighs] I've been walking for hours... [laughs] but I'm not tired yet!
```

### Emphasis
```
The treasure was NOT where the map said it would be!
```

### Dialogue
```
[MAN] Hello there! [WOMAN] Good morning! [MAN] Beautiful day, isn't it?
```

## 🚀 Using Bark in Your App

### Via Web UI
1. Start server: `python app.py`
2. Open http://localhost:5000
3. Select "🐶 Bark (MIT License - Emotional Tags)"
4. Paste your text with emotional tags
5. Click "Generate Audio"

### Via API
```bash
curl -X POST http://localhost:5000/generate \
  -F "text=[peacefully] Hello world" \
  -F "model=tts_models/multilingual/bark" \
  -F "language=en"
```

### Programmatic Usage
```python
from services.bark_service import get_bark_service

bark = get_bark_service()

# Short text
bark.generate_audio(
    text="[warmly] Hello there!",
    output_path="output.wav",
    voice_preset=6,
    language='en'
)

# Long text (automatic chunking)
bark.generate_long_form(
    text="Your long story with [emotional] tags here...",
    output_path="long_output.wav",
    voice_preset=6,
    language='en',
    chunk_size=250
)
```

## 📊 Comparison: Bark vs OpenVoice

| Feature | Bark | OpenVoice |
|---------|------|-----------|
| **License** | ✅ MIT | ✅ MIT |
| **Emotional Tags** | ✅ Yes | ❌ No |
| **Voice Cloning** | ❌ No (presets only) | ✅ Yes |
| **Languages** | 13 | 6 |
| **Max Length** | ~250 chars/chunk | Unlimited |
| **Nonverbal Sounds** | ✅ Yes | ❌ No |
| **Generation Speed** | Slower | Faster |
| **Best For** | Expressive narration | Voice cloning |

## 🎯 When to Use Bark

✅ **Perfect for:**
- Storytelling and narration
- Emotional content
- Character voices
- Audiobooks with expression
- Creative projects
- Content with [emotional] tags

❌ **Not ideal for:**
- Voice cloning specific people
- Very long texts without breaks
- Production TTS (slower)

## ⚙️ Memory Optimization

If you have low VRAM (<4GB):

### Add to `.env`:
```bash
USE_SMALL_BARK_MODELS=True
BARK_OFFLOAD_CPU=True
```

This will:
- Use smaller model variants
- Offload to CPU when needed
- Reduce memory usage significantly

## 📄 License

**Bark License**: MIT  
**Commercial Use**: ✅ Fully permitted  
**Attribution**: Not required  
**Restrictions**: None

Your audio generator can now be used commercially with confidence!

## 🎓 Learn More

- **GitHub**: https://github.com/suno-ai/bark
- **Voice Presets Library**: https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683
- **Discord Community**: https://suno.ai/discord
- **Paper**: Bark: A Universal Transformer for Audio

---

**Integration Date**: October 27, 2025  
**Status**: ✅ Fully Operational  
**Test Results**: All tests passing (short + long-form)  
**Commercial Ready**: ✅ Yes (MIT License)
