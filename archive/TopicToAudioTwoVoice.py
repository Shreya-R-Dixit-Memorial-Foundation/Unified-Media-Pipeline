import os
import json
import asyncio
import subprocess
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

el = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


async def tts(text, voice, file):

    loop = asyncio.get_running_loop()

    def sync():
        stream = el.text_to_speech.convert(
            text=text,
            voice_id=voice,
            model_id="eleven_v3"
        )

        with open(file, "wb") as f:
            for chunk in stream:
                f.write(chunk)

    await loop.run_in_executor(None, sync)


async def run_dialogue(script, output):

    fvoice = "EXAVITQu4vr4xnSDxMaL"
    mvoice = "VR6AewLTigWG4xSOukaG"

    temp_files = []

    i = 0

    for line in script.split("\n"):

        line = line.strip()
        if not line:
            continue

        if line.startswith("Speaker1:"):
            text = line.replace("Speaker1:", "").strip()
            voice = fvoice

        elif line.startswith("Speaker2:"):
            text = line.replace("Speaker2:", "").strip()
            voice = mvoice

        else:
            continue

        fname = f"chunk_{i}.mp3"
        await tts(text, voice, fname)

        temp_files.append(fname)
        i += 1

    with open("list.txt", "w") as f:
        for t in temp_files:
            f.write(f"file '{t}'\n")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "list.txt",
        "-c", "copy",
        output
    ])

    for t in temp_files:
        os.remove(t)

    os.remove("list.txt")

    print("✅ DONE:", output)


if __name__ == "__main__":

    with open("story_without_tags.json") as f:
        data = json.load(f)

    script = data["text"]
    out = data.get("output_filename", "final.mp3")

    asyncio.run(run_dialogue(script, out))