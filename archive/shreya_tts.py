import os
import re
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# ---------- Load environment ----------
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in .env")

# ---------- ElevenLabs Client ----------
el_client = ElevenLabs(api_key=API_KEY)

# ---------- Voice IDs ----------
NARRATOR_VOICE = "H6QPv2pQZDcGqLwDTIJQ"
VIJAY_VOICE = "6MoEUz34rbRrmmyxgRm4"

# ---------- Emotion-tuned voice settings ----------
NARRATOR_SETTINGS = {
    "stability": 0.30,
    "similarity_boost": 0.85,
    "style": 0.75,
    "use_speaker_boost": True
}

VIJAY_SETTINGS = {
    "stability": 0.20,
    "similarity_boost": 0.90,
    "style": 0.90,
    "use_speaker_boost": True
}

# ---------- Split narration vs dialogue ----------
def split_text_by_quotes(text):
    parts = re.split(r'([“"][^”"]+[”"])', text)
    segments = []

    for part in parts:
        clean = part.strip()
        if not clean:
            continue

        if clean[0] in '“"' and clean[-1] in '”"':
            segments.append((clean.strip('“”" '), True))   # Vijay speaks
        else:
            segments.append((clean, False))                # Narrator speaks

    return segments

# ---------- Generate emotional audio ----------
def generate_audio(text):
    segments = split_text_by_quotes(text)
    output_file = "shreya_story_en.mp3"

    print(f"🎧 Generating emotional audio ({len(segments)} segments)...")

    with open(output_file, "wb") as f:
        for segment_text, is_quote in segments:
            if is_quote:
                voice_id = VIJAY_VOICE
                voice_settings = VIJAY_SETTINGS
                speaker = "Vijay Dixit"
            else:
                voice_id = NARRATOR_VOICE
                voice_settings = NARRATOR_SETTINGS
                speaker = "Narrator"

            print(f"🔊 {speaker}: {segment_text[:45]}...")

            audio_stream = el_client.text_to_speech.convert(
                text=segment_text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1",
                voice_settings=voice_settings
            )

            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)

    print(f"\n✅ Emotional audio saved as: {output_file}")

# ---------- EXECUTION ----------
if __name__ == "__main__":
    story_text = """
On a beautiful spring day, Vijay Dixit sits on a bench at the Minnesota Landscape Arboretum in Chaska.
The bench is dedicated to the memory of his daughter, Shreya, who was killed while riding with a distracted driver on November 1, 2007.

“This is where we come… when we are sad, and missing Shreya.”

The bench is also where he and his wife, Rekha, commemorate Shreya’s birthday and the anniversary of her loss every year.
"""

    generate_audio(story_text)
