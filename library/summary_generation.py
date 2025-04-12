import os
import time
import openai
from dotenv import load_dotenv

from .prompt_builder import create_prompt

# Ladda API-nyckeln från .env
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#lista tillgänliga modeller
#if __name__ == "__main__":
    # Testa att lista tillgängliga modeller
#    models = client.models.list()

#    print("\n📦 Tillgängliga modeller:\n")
#    for model in models.data:
#        print(f"🔹 {model.id}")    

# Skicka prompt till OpenAU
def generate_summary(prompt, retries=1, delay=5):
    for attempt in range(retries):
        try:
            #print("📤 Skickar följande prompt till OpenAI:")
            #print(prompt[:1000])  # Förkortad debug

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
                )

            print("✅ Response mottagen")
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Fel i generate_summary: {e}")
            

    return None
