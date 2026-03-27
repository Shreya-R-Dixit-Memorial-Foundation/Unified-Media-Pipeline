import os
import re
from groq import Groq
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

# Setup Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Your Specific Voice IDs
NARRATOR_VOICE = "H6QPv2pQZDcGqLwDTIJQ"
VIJAY_VOICE = "6MoEUz34rbRrmmyxgRm4"

def translate_content(text, target_lang="Hindi"):
    print(f"--- Translating text to {target_lang} ---")
    # Prompt ensures quotes are kept so we can split the audio later
    prompt = f"""
    Translate the following story into {target_lang}. 
    IMPORTANT: Keep all dialogue inside "quotation marks" exactly as they are. 
    Maintain the emotional, somber tone of the original.
    Return ONLY the translated text.

    Text:
    {text}
    """
    
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return completion.choices[0].message.content.strip()

def split_text_by_quotes(text):
    # Matches text inside any kind of double quotes
    parts = re.split(r'([“"][^”"]+[”"])', text)
    segments = []
    for part in parts:
        clean = part.strip()
        if not clean: continue
        if clean[0] in '“"' and clean[-1] in '”"':
            segments.append((clean.strip('“”" '), True)) # It's a quote
        else:
            segments.append((clean, False)) # It's narration
    return segments

def generate_multilingual_audio(translated_text):
    segments = split_text_by_quotes(translated_text)
    output_file = "translated_story.mp3"
    
    print(f"Generating audio with {len(segments)} voice changes...")
    
    with open(output_file, "wb") as f:
        for text, is_quote in segments:
            voice_id = VIJAY_VOICE if is_quote else NARRATOR_VOICE
            print(f"Speaking ({'Vijay' if is_quote else 'Narrator'}): {text[:30]}...")
            
            audio_stream = el_client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2" # Required for non-English
            )
            for chunk in audio_stream:
                if chunk: f.write(chunk)
                
    print(f"✅ Audio successfully saved as: {output_file}")

# --- EXECUTION ---
if __name__ == "__main__":
    english_text = '''
Eden Prairie bids goodbye to Vijay Dixit, whose tragic loss sparked a mission against distracted driving.
On a beautiful spring day, Vijay Dixit sits on a bench at the Minnesota Landscape Arboretum in Chaska. The bench is dedicated to the memory of his daughter, Shreya, who was killed while riding with a distracted driver on Nov. 1, 2007.
“This is where we come when we are sad and missing Shreya,” he said. The bench is also where he and his wife, Rekha, commemorate Shreya’s birthday and the anniversary of her loss every year.
'''

    # 1. Translate via Groq
    translated_story = translate_content(english_text, "Hindi")
    print(f"\nTranslated Story Preview:\n{translated_story}\n")
    
    # 2. Convert to Audio via ElevenLabs
    generate_multilingual_audio(translated_story)