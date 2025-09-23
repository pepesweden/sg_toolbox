import time

import openai

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os


from domain.prompt_builder import create_kp_prompt, create_refsum_prompt, create_prompt
from adapter.summary_generation import generate_summary
from adapter.save_to_docx import save_summary_to_docx
from adapter.text_extractor import read_docx_text, extract_texts_from_docx


# Skapa en klient (plockar API-nyckel automatiskt från .env eller miljövariabel)
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")




#  5. Kör hela flödet
if __name__ == "__main__":
    # Låt användaren välja KP/Sammanfattning
    print("❓ Välj 1.Sammanfattning, 2.KP eller 3. Referenssammanfattning:")
    while True:
        doc_choice = input()
        if doc_choice in ["1", "2", "3"]: 
            doc_choice = int(doc_choice)
            break
        else:
            print("Ogiltigt val. Vänligen välj 1-3.")

    #  Låt användaren skriva in filnamn
    
    filnamn = input("📥 Ange filnamn i mappen 'input/' (inklusive .docx): ")
    intervju_path = f"input/{filnamn}"

    #  Låt användaren ange kandidatens namn
    candidate_name = input("👤 Ange kandidatens namn (för filnamn och rubrik): ")


    # Sammanfattning Ladda mall och stilreferens
    mall_text = read_docx_text("reference/mall_sammanfattning.docx")
    style_text = read_docx_text("reference/Sammanfattning-claes.docx")
    doc_text = read_docx_text(intervju_path)

     # KP Ladda mall och stilreferens
    kpmall_text = read_docx_text("reference/kp_mall.docx")
    kpstyle_text = read_docx_text("reference/kp_ic.docx")

    # Referenss Ladda mall och stilreferens
    refmall_text = read_docx_text("reference/refsum_mall.docx")
    refstyle_text = read_docx_text("reference/refsum_referencev2.docx")
    
    
    # Skapa prompt och generera sammanfattning eller KP
    if doc_choice == 1: #skapaa sammanfattning
        prompt = create_prompt(doc_text, mall_text, style_text)
        summary = generate_summary(prompt)
    elif doc_choice == 2: # skapa KP
        prompt = create_kp_prompt(doc_text, kpmall_text, style_text)
        summary = generate_summary(prompt)
    elif doc_choice == 3: # skapa Referenssammanfattning
        prompt = create_refsum_prompt(doc_text, refmall_text, refstyle_text)
        summary = generate_summary(prompt)    
    else: 
        print("❌ Fel i KP generering.")

    #  Visa exakt GPT-output
    #print("\n GPT-Output:\n" + "="*40)
    #print(summary)
    #print("="*40 + "\n")

    # Spara som Word-fil
    if summary:
        save_summary_to_docx(summary, candidate_name=candidate_name)
        print("✅ Sammanfattningenär klar.")
    else:
        print("❌ Sammanfattningen kunde inte genereras.")
