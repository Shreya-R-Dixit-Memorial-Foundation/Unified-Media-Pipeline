import os
import re
from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

# Initialize Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def sanitize_filename(name):
    """Cleans the topic to make it a safe filename."""
    clean_name = re.sub(r'[^\w\s-]', '', name).strip()
    return clean_name.replace(' ', '_')

def get_emotional_script(prompt, mode):
    """Requests a script from Groq based on the mode (m/d)."""
    
    # Define structural rules based on the user's mode choice
    if mode == 'd':
        style_rule = (
            "Write this as a two-person dialogue with clear labels like 'Narrator:' and 'Vijay:'. "
            "Ensure they interact and react to each other."
        )
    else:
        style_rule = "Write this as a single-speaker monologue."

    system_instr = (
        f"You are a master scriptwriter for ElevenLabs v3. {style_rule} "
        "Use bracketed audio tags like [chuckle], [sobbing], [sighs], [gasp], [pause], or [breath] "
        "to direct the emotion naturally without overacting. "
        "The final script must be suitable for text-to-speech audio lasting between 1 and 2 minutes "
        "(approximately 150 to 280 words). "
        "At the very end of the script, add 2–3 short, credible, globally neutral statistics related "
        "to the topic to increase awareness and realism. "
        "Ensure the statistics sound natural in spoken audio and are not overly technical. "
        "Maintain a humane, emotionally grounded tone suitable for podcasts."
    )

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instr},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return completion.choices[0].message.content

def run_pipeline():
    # --- STEP 1: ASK TOPIC FIRST ---
    topic = input("🎤 Step 1: What is the topic for your audio? ")
    
    # --- STEP 2: ASK MODE SECOND ---
    mode = input("📝 Step 2: Would you like a monologue (m) or a dialogue (d)? ").lower()
    
    # Generate the initial content
    current_text = get_emotional_script(f"Topic: {topic}", mode)
    
    # STEP 3: REVIEW & EDIT LOOP
    while True:
        print(f"\n--- GENERATED CONTENT ---\n{current_text}\n-------------------------")
        action = input("\nCommands: [ok] to proceed, [edit] to change, [trans] to translate: ").lower()
        
        if action == 'ok':
            break
        elif action == 'edit':
            feedback = input("What changes are required? ")
            current_text = get_emotional_script(f"Update this: {current_text}. Change: {feedback}", mode)
        elif action == 'trans':
            lang = input("Which language would you like to translate to? ")
            current_text = get_emotional_script(f"Translate this to {lang}, keeping [tags] and format:\n{current_text}", mode)

    # STEP 4: CALL ELEVENLABS API
    filename = f"{sanitize_filename(topic)}.mp3"
    print(f"⏳ Calling ElevenLabs v3 to generate: {filename}...")
    
    audio = el_client.text_to_speech.convert(
        text=current_text,
        voice_id="H6QPv2pQZDcGqLwDTIJQ", # A high-quality v3 compatible voice
        model_id="eleven_v3",
        voice_settings={
            "stability": 0.5, # v3 Natural threshold
            "similarity_boost": 0.8,
            "style": 0.5
        }
    )
    
    save(audio, filename)
    print(f"✅ Success! Your audio is ready: {filename}")

if __name__ == "__main__":
    run_pipeline()