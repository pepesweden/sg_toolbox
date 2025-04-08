import os
import time
import openai
from dotenv import load_dotenv

# 🔐 Ladda API-nyckeln från .env
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(messages, retries=1, delay=5):
    for attempt in range(retries):
        try:
            print("📤 Skickar prompt till OpenAI...")
            response = client.chat.completions.create(
                model="gpt-4",
                #model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            print("✅ GPT-svar mottaget!")
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Fel i generate_summary (försök {attempt + 1}/{retries}): {e}")
            time.sleep(delay)

    return None
