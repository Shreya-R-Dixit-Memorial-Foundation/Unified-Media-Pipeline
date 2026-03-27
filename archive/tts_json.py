import os
import json
import re
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from groq import Groq

# ---------- Load environment ----------
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in .env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

el_client = ElevenLabs(api_key=API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

V3_SETTINGS = {
    "stability": 0.2, 
    "similarity_boost": 0.90, 
    "style": 0.80, 
    "use_speaker_boost": True
}

def add_emotion_tags_with_llm(raw_text):
    """
    Uses Groq LLM to analyze dialogue and add emotion tags.
    Differentiates between narrator and character dialogue.
    Ensures proper voice modulations for each speaker.
    """
    print("🤖 Analyzing dialogue with LLM to add emotion tags...")
    
    prompt = f"""You are an expert dialogue annotation specialist. Your task is to analyze the following script and add emotion/voice modulation tags for text-to-speech synthesis.

IMPORTANT RULES:
1. For NARRATOR dialogue: Use tags like [authoritative narrator][neutral pitch][smooth baritone][cinematic tone][clear articulation]
2. For CHARACTER dialogue: Add character description + emotional state. Examples:
   - [young energetic male][higher pitch][bright tone][fast pace][slightly nasal][angry]
   - [older calm male][deep bass voice][slow pace][warm resonance][steady delivery]
3. For each line, determine the emotional context from the content
4. Keep sound effects/actions like <breath>, <pause>, <snarl>, <gasp> - they are important for voice modulation
5. Preserve ALL original text content - only ADD tags
6. Every speaker must have tags for proper voice differentiation
7. Tags should indicate:
   - Speaker type (age, gender, characteristics)
   - Emotional state (angry, calm, surprised, sad, etc.)
   - Voice quality (pitch, pace, tone, resonance)
   - Speaking style (aggressive, gentle, thoughtful, etc.)

INPUT SCRIPT:
{raw_text}

Now, output the SAME script but with emotion tags added to each speaker's dialogue. Return ONLY the annotated script, no explanations."""

    try:
        completion = groq_client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct",
        messages=[
            {"role": "system", "content": "You are an expert dialogue annotation specialist for voice synthesis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=4096
        )

        annotated_text = completion.choices[0].message.content.strip()
        print("✅ Emotion tags added successfully!")
        return annotated_text
    
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        print("⚠️ Using fallback neutral narrator tags.")
        return "[neutral narrator][clear tone] " + raw_text


def generate_human_audio(text, output_file):
    """
    Real multi-voice dialogue.
    Dynamically assigns male/female voices per speaker.
    Python 3.14 safe (no ffmpeg / no pydub)
    """

    print("🎭 Dynamic multi-voice generation starting...")

    g1 = input("Speaker1 gender (m/f): ").lower()
    g2 = input("Speaker2 gender (m/f): ").lower()

    female_voice = "EXAVITQu4vr4xnSDxMaL"
    male_voice = "VR6AewLTigWG4xSOukaG"

    voice1 = female_voice if g1 == "f" else male_voice
    voice2 = female_voice if g2 == "f" else male_voice

    try:
        with open(output_file, "ab") as final_audio:

            for line in text.split("\n"):

                line = line.strip()
                if not line:
                    continue

                if line.startswith("Speaker1:"):
                    voice_id = voice1
                    speak_text = line.replace("Speaker1:", "").strip()

                elif line.startswith("Speaker2:"):
                    voice_id = voice2
                    speak_text = line.replace("Speaker2:", "").strip()

                else:
                    continue

                audio_stream = el_client.text_to_speech.convert(
                    text=speak_text,
                    voice_id=voice_id,
                    model_id="eleven_v3",
                    voice_settings={
                        "stability": 0.35,
                        "similarity_boost": 0.9,
                        "style": 0.85,
                        "use_speaker_boost": True
                    }
                )

                for chunk in audio_stream:
                    if chunk:
                        final_audio.write(chunk)

        print(f"\n✅ Multi-voice audio saved as: {output_file}")

    except Exception as e:
        print(f"❌ API Error: {e}")

def strip_speaker_labels(text):
    # removes ANY label like "Driver 1:", "Narrator:", "Speaker A:", etc.
    return re.sub(r'^\s*\w+(\s*\d+)?:\s*', '', text, flags=re.MULTILINE)

# ---------- EXECUTION ----------
if __name__ == "__main__":
    # Input JSON now has plain text without emotion tags
    # The code will automatically add relevant tags using LLM
    json_path = "story_without_tags.json"
    
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
        raw_text = data.get("text")
        output_name = data.get("output_filename", "Road_Rage_V3.mp3")

        if raw_text:
            print(f"📖 Original text length: {len(raw_text)} characters")
            
            # 🤖 STEP 1: Add emotion tags using LLM
            enhanced_text = add_emotion_tags_with_llm(raw_text)
            
            print(f"📝 Enhanced text with tags length: {len(enhanced_text)} characters")
            print(f"📊 Tags added: +{len(enhanced_text) - len(raw_text)} characters")
            
            # 🎵 STEP 2: Generate audio from enhanced text
            generate_human_audio(enhanced_text, output_name)
        else:
            print("Error: No 'text' found in JSON.")

    except FileNotFoundError:
        print(f"Error: {json_path} not found.")
    except json.JSONDecodeError:
        print("Error: JSON syntax error. Check for unescaped newlines.")