import os
from groq import Groq
from dotenv import load_dotenv

class ContentTranslator:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found")
        self.client = Groq(api_key=self.api_key)

    def generate_script(self, topic, mode='m'):
        """Generates an initial script based on a topic and mode (monologue/dialogue)."""
        print(f"🤖 Generating emotional script for topic: {topic}...")
        
        style_rule = (
            "Write this as a two-person dialogue with clear labels like 'Speaker1:' and 'Speaker2:'. "
            "Ensure they interact and react to each other."
        ) if mode == 'd' else "Write this as a single-speaker monologue."

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

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instr},
                    {"role": "user", "content": f"Topic: {topic}"}
                ],
                temperature=0.8
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating script: {e}"

    def translate(self, text, target_lang="Hindi", preserve_quotes=True):
        """Translates text while maintaining tone and optionally preserving quotes for voice splitting."""
        print(f"--- Translating to {target_lang} via Groq ---")
        
        quote_instr = "KEEP ALL dialogue inside \"quotation marks\" exactly as they are." if preserve_quotes else ""
        
        prompt = f"""
        SYSTEM: You are a professional translator for sensitive and empathetic storytelling.
        TASK: Translate the text below into {target_lang}.
        - {quote_instr}
        - Use a somber, respectful, and emotionally grounded tone.
        - Return ONLY the translated text, no introductory or conversational filler.
        
        TEXT:
        {text}
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during translation: {e}"

    def add_emotion_tags(self, raw_text):
        """Uses LLM to analyze dialogue and add emotion/voice modulation tags."""
        print("🤖 Analyzing dialogue for emotion tags...")
        
        prompt = f"""
        You are an expert dialogue annotation specialist for TTS synthesis.
        Analyze the script and add bracketed tags like [chuckle], [sobbing], [pause], [breath] naturally.
        Distinguish between NARRATOR and CHARACTERS (e.g., Speaker1, Speaker2).
        
        RULES:
        1. Keep sound effects like <breath>, <pause> if already present.
        2. Preserve ALL original text.
        3. Output ONLY the annotated script.
        
        SCRIPT:
        {raw_text}
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Tagging Error: {e}")
            return raw_text
