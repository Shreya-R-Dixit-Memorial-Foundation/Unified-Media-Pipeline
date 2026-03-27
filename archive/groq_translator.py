import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_semantic(text, target_lang="Hindi"):
    print(f"--- Translating to {target_lang} via Groq ---")
    
    # Updated Prompt for cleaner output
    prompt = f"Translate the following text into {target_lang}. Preserve the emotional and semantic meaning. Return ONLY the translated text, no conversational filler:\n\n{text}"

    try:
        completion = client.chat.completions.create(
            # Using the updated Llama 3.1 model
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, 
            max_tokens=2048
        )
        
        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error during translation: {e}"

if __name__ == "__main__":
    original_text = '''
Eden Prairie bids goodbye to Vijay Dixit, whose tragic loss sparked a mission against distracted driving.
On a beautiful spring day, Vijay Dixit sits on a bench at the Minnesota Landscape Arboretum in Chaska. The bench is dedicated to the memory of his daughter, Shreya, who was killed while riding with a distracted driver on Nov. 1, 2007.
“This is where we come when we are sad and missing Shreya,” he said. The bench is also where he and his wife, Rekha, commemorate Shreya’s birthday and the anniversary of her loss every year.
As children play and laugh in the nearby maze and walkers admire the trees bursting with blooms, Dixit reflects on Shreya’s life, his mission since her loss, and his family’s next chapter.
Dixit and Rekha will be moving to New Jersey this month to be nearer their surviving daughter, Nayha, and her family.
Of his time here, Dixit said, “I would say my Minnesota story is much more powerful than my pre-Minnesota story. It is a marker on my life journey.”
'''
    print(translate_semantic(original_text, "Hindi"))