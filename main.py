import os
import json
import asyncio
from dotenv import load_dotenv
from core import ContentTranslator, AudioEngine, sanitize_filename, split_text_smart

def get_unique_filename(prompt_text, default_name):
    """Prompts for a filename and ensures it doesn't already exist in outputs/."""
    while True:
        out_name = input(f"{prompt_text}: ") or default_name
        if not out_name.lower().endswith(".mp3"):
            out_name += ".mp3"
        
        full_path = f"outputs/{out_name}"
        if os.path.exists(full_path):
            print(f"⚠️  Warning: A file named '{out_name}' already exists in the outputs folder.")
            choice = input("Enter a different name? (y/n) - 'n' will overwrite: ").lower()
            if choice == 'y':
                continue
        return out_name

async def interactive_topic_pipeline(translator, audio_engine):
    """
    Unified Pipeline 1: Interactive Topic-to-Audio (Topic -> Script -> Audio)
    Includes customizable speaker genders (m/f/c/e) and localized voice selection.
    """
    print("\n--- 🎤 Interactive Topic-to-Audio ---")
    topic = input("Step 1: What is the topic? ")
    mode = input("Step 2: Monologue (m) or Dialogue (d)? ").lower()
    
    # Selection of characters
    lang = "english" # default for generation
    g1 = input("Speaker 1 gender (m/f/c - child / e - elderly): ").lower() or "m"
    g2 = "m" # placeholder
    if mode == 'd':
        g2 = input("Speaker 2 gender (m/f/c - child / e - elderly): ").lower() or "m"
        idx2 = 1 if g1 == g2 else 0
        v1 = audio_engine.get_voice_id(lang=lang, gender=g1, index=0)
        v2 = audio_engine.get_voice_id(lang=lang, gender=g2, index=idx2)
    else:
        v1 = audio_engine.get_voice_id(lang=lang, gender=g1, index=0)
    
    # Generate initial script with tags
    current_text = translator.generate_script(topic, mode=mode)
    
    # Review/Edit/Translate Loop
    current_lang = "english"
    while True:
        print(f"\n--- GENERATED SCRIPT (Language: {current_lang.upper()}) ---\n{current_text}\n-------------------------")
        action = input("\nCommands: [ok] to proceed, [edit] to change, [trans] to translate: ").lower()
        
        if action == 'ok': break
        elif action == 'edit':
            feedback = input("What changes are required? ")
            current_text = translator.translate(f"Update this: {current_text}. Change: {feedback}", target_lang=current_lang, preserve_quotes=True)
        elif action == 'trans':
            current_lang = input("Target language (e.g., Hindi, English, Spanish)? ").lower()
            current_text = translator.translate(current_text, target_lang=current_lang, preserve_quotes=True)
            # Re-fetch voices for the new language
            v1 = audio_engine.get_voice_id(lang=current_lang, gender=g1, index=0)
            if mode == 'd':
                idx2 = 1 if g1 == g2 else 0
                v2 = audio_engine.get_voice_id(lang=current_lang, gender=g2, index=idx2)

    # Generate Audio
    default_filename = f"{sanitize_filename(topic)}.mp3"
    out_name = get_unique_filename("Enter output filename", default_filename)
    filename = f"outputs/{out_name}"
    
    if mode == 'd':
        print(f"🎭 Using synchronized multi-voice ({current_lang}) for Speaker1/Speaker2...")
        segments = [(seg_text, v2 if is_speaker2 else v1) for seg_text, is_speaker2 in split_text_smart(current_text)]
        audio_engine.generate_multi_voice_audio(segments, output_filename=filename)
    else:
        audio_engine.generate_simple_audio(current_text, voice_id=v1, filename=filename)

async def story_converter_pipeline(translator, audio_engine):
    """
    Unified Pipeline 2: Advanced Story Converter (Text/JSON -> Audio)
    Includes localized voice selection based on language used.
    """
    print("\n--- 📖 Advanced Story Converter ---")
    source = input("Input source: [t] for manual text, [j] for data/story_without_tags.json: ").lower()
    
    if source == 'j':
        with open("data/story_without_tags.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            text = data["text"]
    else:
        text = input("Enter/Paste your story: ")

    print("\nOptions: [1] Direct Audio (English), [2] Translate first")
    opt = input("Select path: ")
    
    current_lang = "english"
    processed_text = text
    if opt == '2':
        current_lang = input("Target language (e.g., Hindi)? ").lower()
        processed_text = translator.translate(text, target_lang=current_lang)
    
    # ALWAYS add emotion tags automatically
    processed_text = translator.add_emotion_tags(processed_text)
    
    multi_voice = input("Use multi-voice (y/n)? ").lower() == 'y'
    g1 = input("Speaker 1 gender (m/f/c - child / e - elderly): ").lower() or "m"
    g2 = "m"
    if multi_voice: g2 = input("Speaker 2 gender (m/f/c - child / e - elderly): ").lower() or "m"
    
    # Voice selection
    v1 = audio_engine.get_voice_id(lang=current_lang, gender=g1, index=0)
    v2 = audio_engine.get_voice_id(lang=current_lang, gender=g2, index=(1 if g1 == g2 else 0))
    
    # Output file handling with duplicate check
    out_name = get_unique_filename("Enter output filename", "story_final.mp3")
    filename = f"outputs/{out_name}"
    
    if multi_voice:
        segments = [(seg_text, v2 if is_speaker2 else v1) for seg_text, is_speaker2 in split_text_smart(processed_text)]
        audio_engine.generate_multi_voice_audio(segments, output_filename=filename)
    else:
        audio_engine.generate_simple_audio(processed_text, voice_id=v1, filename=filename)

async def main():
    load_dotenv()
    translator = ContentTranslator()
    audio_engine = AudioEngine()
    
    # Ensure outputs directory exists
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    print("\n🌟 Shreya Dixit Foundation Unified Media System 🌟")
    print("--------------------------------------------------")
    print("⚠️  PLEASE READ THE README.md THOROUGHLY BEFORE PROCEEDING ⚠️")
    print("--------------------------------------------------")
    print("1. 🎤 Topic-to-Audio (Draft, Translate, Review, Speak)")
    print("2. 📖 Story-to-Audio (Process existing Text/JSON to Audio)")
    print("3. 📁 Archive (Access Legacy Scripts)")
    
    choice = input("\nSelect workflow (1-3): ")
    
    if choice == '1':
        await interactive_topic_pipeline(translator, audio_engine)
    elif choice == '2':
        await story_converter_pipeline(translator, audio_engine)
    elif choice == '3':
        print("Archive is located in the 'archive/' folder.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    asyncio.run(main())
