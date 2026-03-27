import os
import re
import subprocess
import asyncio
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

class AudioEngine:
    # --- Professional Multi-language Voice Library ---
    VOICE_LIBRARY = {
        "english": {
            "m": ["VR6AewLTigWG4xSOukaG", "pNInz6obpgDQGcFmaJgB"], # Brian, Adam
            "f": ["EXAVITQu4vr4xnSDxMaL", "AZnzvA97DchvMCzpBM6H"], # Sarah, Nicole
            "c": ["9BWtsRjCglG6f8pu4aaA", "JBFqnCBCl6GPmuD1G58Y"], # Gigi, George (Child)
            "e": ["H6QPv2pQZDcGqLwDTIJQ", "nPczC3z2tU9VmsYwNnL2"]  # Bill (Elderly Male), Paul
        },
        "hindi": {
            "m": ["z9fAnlkUCv9BvT5Lg5jN", "6MoEUz34rbRrmmyxgRm4"], # Aman, Vijay (Indian)
            "f": ["MF3mGyEYCl7XYW7Lp9lY", "ThT5KcBe7VK9v8v7T6T5"], # Myra, Kavita (Indian)
            "c": ["9BWtsRjCglG6f8pu4aaA"], # Gigi (Universal Child)
            "e": ["6MoEUz34rbRrmmyxgRm4", "ThT5KcBe7VK9v8v7T6T5"]  # Vijay, Kavita (Elderly Indian)
        },
        "spanish": {
            "m": ["onwK4e9ZLuTAKqWqLx49"], 
            "f": ["AZnzvA97DchvMCzpBM6H"],
            "c": ["9BWtsRjCglG6f8pu4aaA"],
            "e": ["H6QPv2pQZDcGqLwDTIJQ"]
        }
    }

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found")
        self.client = ElevenLabs(api_key=self.api_key)

    def get_voice_id(self, lang="english", gender="m", index=0):
        """Returns a voice ID based on language and gender (m/f/c/e). Index avoids duplicates."""
        lang_key = lang.lower() if lang.lower() in self.VOICE_LIBRARY else "english"
        gender_key = gender.lower() if gender.lower() in ["m", "f", "c", "e"] else "m"
        voices = self.VOICE_LIBRARY[lang_key].get(gender_key, self.VOICE_LIBRARY[lang_key]["m"])
        return voices[index % len(voices)]

    def generate_simple_audio(self, text, voice_id="H6QPv2pQZDcGqLwDTIJQ", model_id="eleven_v3", filename="output.mp3", settings=None):
        """Generates single-voice audio for a block of text."""
        print(f"⏳ Generating audio with Voice ID: {voice_id}...")
        
        default_settings = {"stability": 0.7, "similarity_boost": 0.7, "style": 0.3}
        
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            voice_settings=settings or default_settings
        )
        
        save(audio, filename)
        print(f"✅ Success! Generated: {filename}")
        return filename

    def generate_multi_voice_audio(self, segments, output_filename="final_story.mp3", model_id="eleven_v3"):
        """Generates audio for multiple segments using FFmpeg concatenation for smooth transitions."""
        print(f"🎭 Generating multi-voice audio with {len(segments)} segments...")
        
        settings = {
            "stability": 0.85,     # Increased stability for slower, more deliberate pace
            "similarity_boost": 0.8,
            "style": 0.2           # Minimal style for calm, steady delivery
        }
        
        temp_files = []
        
        # Step 1: Generate individual chunks
        for i, (text, voice_id) in enumerate(segments):
            print(f"Part {i+1} [{voice_id[:10]}...]: {text[:40]}...")
            
            chunk_filename = f"chunk_{i}.mp3"
            success = False
            for attempt in range(3):
                try:
                    audio_stream = self.client.text_to_speech.convert(
                        text=text,
                        voice_id=voice_id,
                        model_id=model_id,
                        voice_settings=settings
                    )
                    with open(chunk_filename, "wb") as f:
                        for chunk in audio_stream:
                            if chunk: f.write(chunk)
                    success = True
                    temp_files.append(chunk_filename)
                    break 
                except Exception as e:
                    print(f"⚠️  Attempt {attempt+1} failed for Part {i+1}: {e}")
                    if attempt < 2: 
                        print(f"🔄 Retrying Part {i+1} (Attempt {attempt+2})...")
                    else:
                        print(f"❌ Part {i+1} failed completely after 3 attempts.")
                        break
            
            if not success:
                print(f"❌ ERROR: Part {i+1} failed completely.")

        # Step 2: Use FFmpeg for smooth concatenation
        if temp_files:
            self._ffmpeg_merge(temp_files, output_filename)
        
        for t in temp_files: 
            if os.path.exists(t): os.remove(t)
            
        print(f"✅ Finished! Audio saved to {output_filename}")
        return output_filename

    async def generate_concatenated_audio(self, script, output_filename="concatenated.mp3"):
        """Generates audio chunks for Speaker1/Speaker2 scripts and uses ffmpeg to merge."""
        # This is now effectively a specific case of multi_voice_audio
        # We rewrite it to use the unified multi_voice logic for consistency
        fvoice = "EXAVITQu4vr4xnSDxMaL"
        mvoice = "VR6AewLTigWG4xSOukaG"
        segments = []
        
        for line in script.split("\n"):
            line = line.strip()
            if not line: continue
            if line.startswith("Speaker1:"):
                segments.append((line.replace("Speaker1:", "").strip(), fvoice))
            elif line.startswith("Speaker2:"):
                segments.append((line.replace("Speaker2:", "").strip(), mvoice))
            else:
                segments.append((line, fvoice))

        return self.generate_multi_voice_audio(segments, output_filename)

    def _ffmpeg_merge(self, temp_files, output_filename):
        """Helper to merge audio chunks smoothly using ffmpeg."""
        with open("list.txt", "w") as f:
            for t in temp_files:
                f.write(f"file '{t}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-fflags", "+genpts", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", output_filename
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # Keep log clean

        if os.path.exists("list.txt"):
            os.remove("list.txt")
