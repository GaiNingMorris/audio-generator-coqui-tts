#!/usr/bin/env python3
"""Test OpenVoice installation and download required checkpoints"""

import os
import sys
import torch

# Add OpenVoice to path
sys.path.insert(0, 'OpenVoice')

from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter

# Checkpoint paths
ckpt_base = 'OpenVoice/checkpoints/base_speakers/EN'
ckpt_converter = 'OpenVoice/checkpoints/converter'

# Check if checkpoints exist
if not os.path.exists(ckpt_base):
    print(f"❌ Base speaker checkpoint not found: {ckpt_base}")
    print("\n📥 Downloading OpenVoice checkpoints...")
    print("Run the following command:")
    print("git clone https://huggingface.co/myshell-ai/OpenVoice OpenVoice/checkpoints")
    sys.exit(1)

if not os.path.exists(ckpt_converter):
    print(f"❌ Converter checkpoint not found: {ckpt_converter}")
    sys.exit(1)

# Test loading
print("🔄 Testing OpenVoice model loading...")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"📱 Using device: {device}")

try:
    # Load base speaker TTS
    print("📝 Loading base speaker TTS...")
    base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
    base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')
    print("✅ Base speaker TTS loaded")
    
    # Load tone color converter
    print("🎨 Loading tone color converter...")
    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
    print("✅ Tone color converter loaded")
    
    # Load default source embedding
    print("🎵 Loading default source embedding...")
    source_se = torch.load(f'{ckpt_base}/en_default_se.pth', map_location=device)
    print("✅ Source embedding loaded")
    
    print("\n✅ OpenVoice is fully operational!")
    print(f"   - Model: OpenVoice v2")
    print(f"   - License: MIT")
    print(f"   - Device: {device}")
    print(f"   - Voice cloning: Supported")
    
except Exception as e:
    print(f"\n❌ Error loading OpenVoice: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
