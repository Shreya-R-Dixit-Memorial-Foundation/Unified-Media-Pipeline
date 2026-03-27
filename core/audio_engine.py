import os
import re
import subprocess
import asyncio
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

class AudioEngine:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_simple_audio(self, text, voice_id="H6QPv2pQZDcGqLwDTIJQ", model_id="eleven_v3", filename="output.mp3", settings=None):
        """Generates single-voice audio for a block of text."""
        print(f"⏳ Generating audio with Voice ID: {voice_id}...")
        
        default_settings = {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.5
        }
        
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            voice_settings=settings or default_settings
        )
        
        save(audio, filename)
        print(f"✅ Success! Generated: {filename}")
        return filename

    def generate_multi_voice_audio(self, segments, output_filename="final_story.mp3", model_id="eleven_multilingual_v2"):
        """Generates audio for multiple segments (text, voice_id) and merges them into one file."""
        print(f"🎭 Generating multi-voice audio with {len(segments)} segments...")
        
        with open(output_filename, "wb") as f:
            for i, (text, voice_id) in enumerate(segments):
                print(f"Part {i+1} [{voice_id[:10]}...]: {text[:40]}...")
                try:
                    audio_stream = self.client.text_to_speech.convert(
                        text=text,
                        voice_id=voice_id,
                        model_id=model_id,
                        voice_settings={"stability": 0.5, "similarity_boost": 0.8}
                    )
                    for chunk in audio_stream:
                        if chunk: f.write(chunk)
                except Exception as e:
                    print(f"Error in Part {i+1}: {e}")
        
        print(f"✅ Finished! Audio saved to {output_filename}")
        return output_filename

    async def generate_concatenated_audio(self, script, output_filename="concatenated.mp3"):
        """Generates audio chunks for Speaker1/Speaker2 and uses ffmpeg to merge."""
        fvoice = "EXAVITQu4vr4xnSDxMaL"
        mvoice = "VR6AewLTigWG4xSOukaG"
        temp_files = []
        i = 0
        
        loop = asyncio.get_running_loop()

        for line in script.split("\n"):
            line = line.strip()
            if not line: continue
            
            if line.startswith("Speaker1:"):
                text = line.replace("Speaker1:", "").strip()
                voice = fvoice
            elif line.startswith("Speaker2:"):
                text = line.replace("Speaker2:", "").strip()
                voice = mvoice
            else: continue

            fname = f"chunk_{i}.mp3"
            await loop.run_in_executor(None, self.save_tts_chunk, text, voice, fname)
            temp_files.append(fname)
            i += 1

        with open("list.txt", "w") as f:
            for t in temp_files:
                f.write(f"file '{t}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", output_filename
        ])

        for t in temp_files: os.remove(t)
        os.remove("list.txt")
        print("✅ Concatenation DONE:", output_filename)
        return output_filename

    def save_tts_chunk(self, text, voice_id, filename):
        stream = self.client.text_to_speech.convert(
            text=text, voice_id=voice_id, model_id="eleven_v3"
        )
        with open(filename, "wb") as f:
            for chunk in stream: f.write(chunk)
