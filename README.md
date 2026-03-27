# 🌟 Shreya Dixit Foundation: Unified Media Pipeline

Welcome to the **Unified Media Pipeline**, a high-performance, AI-driven studio designed to transform stories, reports, and topics into professional-grade audio content. 

This system is built specifically to support the mission of the **Shreya Dixit Foundation**, enabling emotional storytelling, multilingual outreach, and impactful road safety awareness campaigns.

---

## 🚀 Scripting & Audio Features

### 🎤 1. Interactive Topic-to-Audio (Creative Studio)
Turn any idea into a mini-podcast or a moving story.
- **AI-Guided Scripting**: Simply provide a topic, and the system writes a 1–2 minute script with a natural, emotionally grounded tone.
- **Review & Refine**: You can review the script before generating audio. Don't like a line? Ask for an "edit." Want it in another language? Ask for a "translation."
- **Monologue or Dialogue**: Choose between a single narrator or a two-person conversation with distinct voices.
- **Automatic Awareness Stats**: Every script automatically includes relevant, globally neutral statistics to ground the message in reality.

### 📖 2. Advanced Story-to-Audio (Content Processing)
Transform existing text into a rich audio experience.
- **Multi-Character Attribution**: Automatically detects dialogue within "quotes" and assigns different voices (e.g., Narrator vs. Vijay).
- **Semantic Translation**: Translate your stories (e.g., to Hindi) while ensuring the emotional weight and character voices remain consistent.
- **AI Emotional Tagging**: Our system analyzes the text to add human modulations like *[sighs]*, *[chuckle]*, or *[sobbing]* for a truly lifelike delivery.

### 🌍 3. Global Reach & Emotions
- **Multilingual Support**: High-fidelity narration in English, Hindi, and more.
- **Human-Centric Design**: Built-in "breath" and "pause" markers to ensure the narration feels empathetic and respectful, especially for sensitive topics.

---

## 🛠️ How to Use: "I want to..."

### "...create a new story from a topic"
1. Run `python main.py`.
2. Select Option **1** (Interactive Topic-to-Audio).
3. Type your topic (e.g., "A father remembering his daughter's legacy").
4. Choose `m` for a monologue or `d` for a dialogue.
5. Review the script. Use `edit` to refine it or `trans` to translate it.
6. Type `ok` to generate the final audio.

### "...convert an existing report or story into audio"
1. Run `python main.py`.
2. Select Option **2** (Advanced Story Converter).
3. Choose to either paste text (`t`) or use a JSON file (`j`).
4. Select `Translate` (2) if you want it in another language, or `Add AI Tags` (3) for maximum emotional depth.
5. Enable `multi-voice` (y) to have the Narrator and Vijay speak separately.

---

## ⚙️ Setup & Installation

### 1. Requirements
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. API Configuration
1. Rename `.env.example` to `.env`.
2. Add your **Groq** and **ElevenLabs** API keys into the file.

### 3. Running the System
```bash
python main.py
```

---

## 📁 Project Structure
- **`main.py`**: Your single entry point for all workflows.
- **`core/`**: The "engine room" containing automation logic.
- **`assets/`**: Reference images for personas (Vijay, Shreya).
- **`data/`**: Source files for stories and JSON data.
- **`outputs/`**: Where your final MP3 files are saved.
- **`archive/`**: Secure storage for all legacy scripts and previous versions.

---

*This pipeline was developed to honor the memory of Shreya Dixit and support a mission for distraction-free driving.*
