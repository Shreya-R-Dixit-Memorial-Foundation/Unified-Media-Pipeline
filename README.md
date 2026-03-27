# 🌟 Shreya Dixit Foundation: Unified Media Pipeline

Welcome to the **Unified Media Pipeline**, a high-performance, AI-driven studio designed to transform stories, reports, and topics into professional-grade audio content. 

This system is built specifically to support the mission of the **Shreya Dixit Foundation**, enabling emotional storytelling, multilingual outreach, and impactful road safety awareness campaigns.

---

## 🚀 Scripting & Audio Features

### 🎤 1. Interactive Topic-to-Audio (Creative Studio)
Turn any idea into a mini-podcast or a moving story.
- **AI-Guided Scripting**: Simply provide a topic, and the system writes a 1–2 minute script with a natural, emotionally grounded tone.
- **Review & Refine**: You can review the script before generating audio. Use **`edit`** to refine, or **`trans`** to translate.
- **Monologue or Dialogue**: Choose between a single narrator or a two-person conversation with distinct voices.
- **Automatic Awareness Stats**: Every script automatically includes relevant, globally neutral statistics to ground the message in reality.

### 📖 2. Advanced Story-to-Audio (Content Processing)
Transform existing text into a rich audio experience.
- **Smart Dialogue Detection**: Automatically detects dialogue within "quotes" OR script labels (e.g., `Speaker1:`) and assigns unique voices.
- **Automatic Emotional Analysis**: Every story is automatically analyzed to add subtle human modulations like *[sigh]*, *[chuckle]*, or *[breath]* for a truly lifelike delivery. **No manual tagging required.**
- **Seamless Merging**: Uses **FFmpeg** to stitch character voices together with professional precision and no audio stutters.

### 🌍 3. Multi-Generational & Localized Voices
- **Generational Casting**: Select from four distinct character types for your story:
    - **`m`**: Male
    - **`f`**: Female
    - **`c`**: Child (e.g., Gigi, George)
    - **`e`**: Elderly (e.g., Mature, wise narrators)
- **Cultural Localization**: 
    - **Hindi**: Automatically uses professional Indian voices (Vijay, Aman, Kavita, Myra) for cultural authenticity.
    - **English**: Uses premium international voices (Brian, Sarah, Nicole, Bill).
    - **Multi-Voice De-duplication**: If you select two speakers of the same gender (e.g., two females), the system picks two *different* voices so they remain distinct.

---

## 🛠️ How to Use: "I want to..."

### "...create a new story from a topic"
1. Run `python main.py`.
2. Select Option **1** (Interactive Topic-to-Audio).
3. Type your topic (e.g., "A father remembering his daughter's legacy").
4. Choose **`m`** for a monologue or **`d`** for a dialogue.
5. Choose the **gender/age** of your characters (Male, Female, Child, or Elderly).
6. Review the script. Use `edit` to refine it or `trans` to translate it.
7. Confirm the filename and hits ENTER to generate the final audio.

### "...convert an existing report or story into audio"
1. Run `python main.py`.
2. Select Option **2** (Advanced Story-to-Audio).
3. Choose to either paste text (**`t`**) or use a JSON file (**`j`**).
4. Assign the **gender/age** for Speaker 1 (Narrator) and Speaker 2 (Dialogue).
5. The system will **automatically add emotion tags** and generate the smooth-merged audio.

---

## ⚙️ Professional Resilience

- **Network Auto-Retry**: If your internet flickers during generation, the system will **automatically retry up to 3 times** to ensure no lines are skipped.
- **MP3 Safety**: The system automatically ensures all outputs have the **`.mp3`** extension and checks for duplicates in the `outputs/` folder to prevent overwriting your work.

---

## ⚙️ Setup & Installation

### 1. Requirements
Ensure you have Python and **FFmpeg** installed, then run:
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
- **`core/`**: The "engine room" (Audio, Translation, Utilities).
- **`assets/`**: Reference images for personas (Vijay, Shreya).
- **`data/`**: Source files for stories and JSON data.
- **`outputs/`**: Where your final MP3 files are saved.
- **`archive/`**: Secure storage for all legacy scripts and previous versions.

---

*This pipeline was developed to honor the memory of Shreya Dixit and support a mission for distraction-free driving.*
