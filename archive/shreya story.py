import os
import re
from groq import Groq
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load API Keys
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# VOICE IDs
NARRATOR_VOICE = "H6QPv2pQZDcGqLwDTIJQ"
VIJAY_VOICE = "6MoEUz34rbRrmmyxgRm4"

def translate_semantic(text, target_lang="Hindi"):
    """Translates text while strictly maintaining quote marks."""
    prompt = f"""
    SYSTEM: You are a professional translator for sensitive storytelling.
    TASK: Translate the text below into {target_lang}.
    - Keep ALL dialogue inside "quotation marks" exactly as they are.
    - Use a somber, respectful tone. Avoid words like 'Jashn' for commemoration.
    - Do not summarize. Translate every sentence.
    
    TEXT:
    {text}
    """
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return completion.choices[0].message.content.strip()

def split_text_smart(text):
    """
    State-based parser that handles smart quotes, straight quotes, 
    and multi-line segments reliably.
    """
    # Normalize all quote types to standard double quotes for easier parsing
    normalized = text.replace('“', '"').replace('”', '"').replace('«', '"').replace('»', '"')
    
    segments = []
    current_chunk = []
    in_quote = False
    
    for char in normalized:
        if char == '"':
            # Found a quote boundary
            chunk_str = "".join(current_chunk).strip()
            if chunk_str:
                segments.append((chunk_str, in_quote))
            current_chunk = []
            in_quote = not in_quote # Toggle state
        else:
            current_chunk.append(char)
            
    # Catch the last remaining bit
    final_chunk = "".join(current_chunk).strip()
    if final_chunk:
        segments.append((final_chunk, in_quote))
        
    return segments

def generate_multivoice_audio(translated_text):
    segments = split_text_smart(translated_text)
    filename = "final_partitioned_story.mp3"
    
    print(f"Split into {len(segments)} segments. Generating audio...")

    with open(filename, "wb") as f:
        for i, (text, is_quote) in enumerate(segments):
            voice_id = VIJAY_VOICE if is_quote else NARRATOR_VOICE
            label = "VIJAY" if is_quote else "NARRATOR"
            
            # Add a small pause only if it's Vijay speaking
            processed_text = f"... {text}" if is_quote else text
            
            print(f"Part {i+1} [{label}]: {text[:40]}...")

            try:
                audio_stream = el_client.text_to_speech.convert(
                    text=processed_text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    voice_settings={"stability": 0.8, "similarity_boost": 0.7}
                )
                for chunk in audio_stream:
                    if chunk: f.write(chunk)
            except Exception as e:
                print(f"Error in Part {i+1}: {e}")

    print(f"✅ Finished! Audio saved to {os.path.abspath(filename)}")

if __name__ == "__main__":
    story = """
Eden Prairie bids goodbye to Vijay Dixit, whose tragic loss sparked a mission against distracted driving.
On a beautiful spring day, Vijay Dixit sits on a bench at the Minnesota Landscape Arboretum in Chaska. The bench is dedicated to the memory of his daughter, Shreya, who was killed while riding with a distracted driver on Nov. 1, 2007.
“This is where we come when we are sad and missing Shreya,” he said. The bench is also where he and his wife, Rekha, commemorate Shreya’s birthday and the anniversary of her loss every year.
As children play and laugh in the nearby maze and walkers admire the trees bursting with blooms, Dixit reflects on Shreya’s life, his mission since her loss, and his family’s next chapter.
Dixit and Rekha will be moving to New Jersey this month to be nearer their surviving daughter, Nayha, and her family.
Of his time here, Dixit said, “I would say my Minnesota story is much more powerful than my pre-Minnesota story. It is a marker on my life journey.”
    """
    
    # 1. Translate
    hindi_text = translate_semantic(story, "Hindi")
    print(f"\n--- TRANSLATION ---\n{hindi_text}\n")
    
    # 2. Generate
    generate_multivoice_audio(hindi_text)