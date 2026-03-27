import os
import json
import asyncio
from dotenv import load_dotenv
from core import ContentTranslator, AudioEngine, sanitize_filename, split_text_by_quotes

# Default IDs
NARRATOR_VOICE = "H6QPv2pQZDcGqLwDTIJQ"
VIJAY_VOICE = "6MoEUz34rbRrmmyxgRm4"

async def interactive_topic_pipeline(translator, audio_engine):
    """
    Unified Pipeline 1: Interactive Topic-to-Audio
    Integrates the review-edit-translate loop from TopicToAudio.py 
    with the high-speed ffmpeg dialogue engine from TopicToAudioTwoVoice.py.
    """
    print("\n--- 🎤 Interactive Topic-to-Audio ---")
    topic = input("Step 1: What is the topic? ")
    mode = input("Step 2: Monologue (m) or Dialogue (d)? ").lower()
    
    # Initial Script Generation
    current_text = translator.generate_script(topic, mode=mode)
    
    # Review/Edit/Translate Loop
    while True:
        print(f"\n--- GENERATED SCRIPT ---\n{current_text}\n-------------------------")
        action = input("\nCommands: [ok] to proceed, [edit] to change, [trans] to translate: ").lower()
        
        if action == 'ok': break
        elif action == 'edit':
            feedback = input("What changes are required? ")
            mode_str = "dialogue (Speaker1/Speaker2)" if mode == 'd' else "monologue"
            current_text = translator.translate(f"Update this {mode_str} script: {current_text}. Change: {feedback}", preserve_quotes=True)
        elif action == 'trans':
            lang = input("Target language? ")
            current_text = translator.translate(current_text, target_lang=lang, preserve_quotes=True)

    # Generate Audio
    filename = f"outputs/{sanitize_filename(topic)}.mp3"
    if mode == 'd':
        print("🎭 Using synchronized multi-voice engine...")
        await audio_engine.generate_concatenated_audio(current_text, output_filename=filename)
    else:
        audio_engine.generate_simple_audio(current_text, voice_id=NARRATOR_VOICE, filename=filename)

async def story_converter_pipeline(translator, audio_engine):
    """
    Unified Pipeline 2: Advanced Story Converter
    Merges Story Translation, English Emotional Audio, and AI Tagging.
    """
    print("\n--- 📖 Advanced Story Converter ---")
    source = input("Input source: [t] for manual text, [j] for data/story_without_tags.json: ").lower()
    
    if source == 'j':
        with open("data/story_without_tags.json") as f:
            data = json.load(f)
            text = data["text"]
    else:
        text = input("Enter/Paste your story: ")

    print("\nOptions: [1] Direct TTS, [2] Translate first, [3] Add AI Emotional Tags")
    opt = input("Select processing level: ")
    
    processed_text = text
    if opt == '2':
        lang = input("Target language? ")
        processed_text = translator.translate(text, target_lang=lang)
    elif opt == '3':
        processed_text = translator.add_emotion_tags(text)
    
    multi_voice = input("Use multi-voice (Narrator/Vijay) for quotes? (y/n): ").lower() == 'y'
    filename = input("Output filename (default: outputs/story_final.mp3): ") or "outputs/story_final.mp3"
    
    if multi_voice:
        segments = [(seg_text, VIJAY_VOICE if is_quote else NARRATOR_VOICE) for seg_text, is_quote in split_text_by_quotes(processed_text)]
        audio_engine.generate_multi_voice_audio(segments, output_filename=filename)
    else:
        audio_engine.generate_simple_audio(processed_text, voice_id=NARRATOR_VOICE, filename=filename)

async def main():
    load_dotenv()
    translator = ContentTranslator()
    audio_engine = AudioEngine()
    
    print("\n🌟 Shreya Dixit Foundation Unified Media System 🌟")
    print("--------------------------------------------------")
    print("⚠️  PLEASE READ THE README.md THOROUGHLY BEFORE PROCEEDING ⚠️")
    print("--------------------------------------------------")
    print("1. 🎤 Topic-to-Audio (Topic → Script → Multi-Voice Audio)")
    print("2. 📖 Story-to-Audio (Text/JSON → Translation/Tagging → Audio)")
    print("3. 📁 Archive (Secure storage for original versions)")
    
    choice = input("\nSelect workflow (1-3): ")
    
    if choice == '1':
        await interactive_topic_pipeline(translator, audio_engine)
    elif choice == '2':
        await story_converter_pipeline(translator, audio_engine)
    elif choice == '3':
        print("Archive is located in the 'archive/' folder. Use it to restore older scripts.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    asyncio.run(main())
