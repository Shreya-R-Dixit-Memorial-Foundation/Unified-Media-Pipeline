import os
import json
import base64
import requests
from dotenv import load_dotenv

# ---------- Load .env ----------
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise ValueError("❌ ELEVENLABS_API_KEY not found in .env file")

# ---------- Helper to encode images ----------
def encode_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

vijay_image = encode_image("vijay.png")
shreya_image = encode_image("shreya.png")

# ---------- ElevenLabs Video Endpoint ----------
url = "https://api.elevenlabs.io/v1/video/generate"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

# ---------- Prompt ----------
video_prompt = """
Create a fully animated, cinematic storytelling video in a soft 2D–3D cartoon style.

Vijay Dixit:
- Elderly Indian man
- Closely resemble the provided reference image
- Bald head, sunglasses, pink shirt
- Calm and dignified presence

Shreya Dixit:
- Young Indian woman
- Closely resemble the provided reference image
- Warm smile, long dark hair
- Shown only in glowing memory scenes

Setting:
- Minnesota Landscape Arboretum in spring
- Wooden memorial bench, flowers, sunlight

Tone:
- Emotional, respectful, hopeful
- No accident visuals
"""

# ---------- Payload ----------
payload = {
    "style": "animated",
    "aspect_ratio": "9:16",
    "prompt": video_prompt,
    "audio_sync": True,
    "references": {
        "characters": [
            {"name": "Vijay Dixit", "image_base64": vijay_image},
            {"name": "Shreya Dixit", "image_base64": shreya_image}
        ]
    }
}

# ---------- API Call ----------
response = requests.post(url, headers=headers, data=json.dumps(payload))

# ---------- Handle Response ----------
if response.status_code == 200:
    with open("shreya_story_video.mp4", "wb") as f:
        f.write(response.content)
    print("✅ Video generated: shreya_story_video.mp4")
else:
    print("❌ API Error:", response.status_code)
    print(response.text)
