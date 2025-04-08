####BACKUP 2025-04-03
import time

#import openai
from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

# 🔑 1. Ange din API-nyckel från OpenAI
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = client = OpenAI()

#Skickar deafult prompt till OpenAI GPT-4
def generate_summary(prompt, retries=1, delay=5):
    """
    Skickar prompt till OpenAI med felhantering och retry.
    - retries: hur många gånger vi försöker om det blir fel.
    - delay: antal sekunder att vänta innan retry.
    """
    for attempt in range(retries):
        try:
            response =  client.chat.completions.create(
                model="gpt-4",
                messages=prompt,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        #except     openai.RateLimitError:
        #    print(f"⚠️ Rate limit – försöker igen om {delay} sekunder... ({attempt+1}/{retries})")
        #    time.sleep(delay)
        #except openai.AuthenticationError:
        #    print("❌ Fel: Ogiltig API-nyckel. Kontrollera din .env-fil.")
        #    break
        #except openai.NotFoundError:
        #    print("❌ Fel: Modellnamnet är ogiltigt eller otillgängligt för denna nyckel.")
        #    break
        #except openai.APIError as e:
        #    print(f"💥 OpenAI API-fel: {e}")
        #    break
        #except Exception as e:
        #    print(f"❗ Ovänterat fel: {e}")
        #    break

    return None  # Om det misslyckas helt