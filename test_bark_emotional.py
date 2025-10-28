"""
Test script for Bark with emotional tags
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.bark_service import get_bark_service

def test_emotional_tags():
    """Test Bark with your emotional text"""
    
    # Your test text with emotional tags
    text = """[peacefully] The road stretched ahead like a ribbon of packed earth, winding through tall grass that bent and whispered in the morning breeze. Ash sat on the driver's bench of his wagon, reins loose in his hands as his two draft horses, Copper and Clay, plodded forward at their steady pace. [warmly] The wagon creaked and rattled with the comfortable sounds of a home on wheels, its colorful panels faded by sun and weather, collections of salvaged parts tied to the exterior like strange wind chimes.

[with wonder] The sky was impossibly blue, the kind of blue that the old world had almost forgotten existed before the collapse. [thoughtfully] Ash had seen pictures in the archives, photographs from a hundred years ago where the sky looked gray even on clear days. [appreciatively] Now, eight decades after everything fell apart, the air was clean enough to taste. Sweet, almost.

[descriptively] He was twenty-three years old, with the kind of lean build that came from constant travel and physical work. His clothes were practical, layers that could be added or removed as the day demanded, all of them showing the marks of his trade. Grease stains on his sleeves. A burn mark on one knee from a soldering accident. Pockets bulging with small tools, wire, and the odd screw or bolt that might prove useful."""
    
    print("=" * 60)
    print("🐶 Testing Bark with Emotional Tags")
    print("=" * 60)
    
    try:
        # Get Bark service
        bark = get_bark_service()
        
        # Show model info
        info = bark.get_model_info()
        print(f"\n📊 Model Info:")
        print(f"   Name: {info['name']}")
        print(f"   License: {info['license']}")
        print(f"   Emotional Tags: {info['emotional_tags']}")
        print(f"   Supported Tags: {', '.join(info['supported_tags'])}")
        
        # Test preprocessing
        print(f"\n📝 Original Text Length: {len(text)} characters")
        processed = bark.preprocess_emotional_tags(text)
        print(f"📝 Processed Text Length: {len(processed)} characters")
        
        print(f"\n🔄 Preprocessing Example:")
        print(f"   Before: {text[:150]}...")
        print(f"   After:  {processed[:150]}...")
        
        # Generate short sample
        short_text = """[peacefully] The road stretched ahead like a ribbon of packed earth. [warmly] The wagon creaked and rattled with comfortable sounds."""
        
        print(f"\n🎵 Generating short audio sample...")
        print(f"   Text: {short_text}")
        
        output_path = "outputs/test_bark_emotional.wav"
        os.makedirs("outputs", exist_ok=True)
        
        bark.generate_audio(
            text=short_text,
            output_path=output_path,
            voice_preset=6,  # Use speaker 6
            language='en'
        )
        
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"\n✅ SUCCESS!")
            print(f"   Generated: {output_path}")
            print(f"   Size: {size_kb:.1f} KB")
            print(f"\n💡 Tip: Emotional tags like [peacefully] and [warmly] are")
            print(f"   converted to pauses and emphasis that Bark understands!")
        else:
            print(f"\n❌ FAILED: Audio file not created")
        
        # Test with long-form generation for full text
        print(f"\n" + "=" * 60)
        print(f"📚 Testing Long-Form Generation")
        print(f"=" * 60)
        print(f"   Full text length: {len(text)} characters")
        print(f"   This will be split into multiple chunks...")
        
        output_long = "outputs/test_bark_emotional_long.wav"
        
        bark.generate_long_form(
            text=text,
            output_path=output_long,
            voice_preset=6,
            language='en',
            chunk_size=250
        )
        
        if os.path.exists(output_long):
            size_kb = os.path.getsize(output_long) / 1024
            print(f"\n✅ SUCCESS!")
            print(f"   Generated: {output_long}")
            print(f"   Size: {size_kb:.1f} KB")
        else:
            print(f"\n❌ FAILED: Long-form audio not created")
        
        print(f"\n" + "=" * 60)
        print(f"🎉 All tests completed!")
        print(f"=" * 60)
        print(f"\n💡 To use Bark in the web UI:")
        print(f"   1. Run: python app.py")
        print(f"   2. Select '🐶 Bark (MIT License - Emotional Tags)'")
        print(f"   3. Use emotional tags in your text:")
        print(f"      - [laughs], [sighs], [gasps]")
        print(f"      - [peacefully], [warmly], etc. (auto-converted)")
        print(f"      - ... for pauses")
        print(f"      - CAPS for emphasis")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = test_emotional_tags()
    sys.exit(0 if success else 1)
