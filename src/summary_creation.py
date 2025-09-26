import time

import openai

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os


from domain.prompt_builder import create_prompt, create_kp_prompt, create_refsum_prompt, build_prompt_for_document_type, DOC_TYPE_SUMMARY, DOC_TYPE_KP, DOC_TYPE_REFERENCE
from adapter.summary_generation import generate_summary
from adapter.save_to_docx import save_summary_to_docx
from adapter.text_extractor import read_docx_text, extract_texts_from_docx


# Skapa en klient (plockar API-nyckel automatiskt från .env eller miljövariabel)
### Duplicerad kod???###
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


UPLOAD_FOLDER = "data/input"
DOWNLOAD_FOLDER = "data/output"   


# Function to load data and prep prompt info for summary generation
def trigger_summary_generation(file_path):
    # Load style template and referens for "summary"
    doc_type = DOC_TYPE_SUMMARY
    doc_text = read_docx_text(file_path)

    result = build_prompt_for_document_type(doc_type, doc_text)
    if "error" in result:
        raise ValueError(f"Prompt creation failed: {result['error']}")
    
    return result["prompt"]

def trigger_kp_generation(file_path):
    # Load style template and referens for "summary"
    doc_type = DOC_TYPE_KP
    doc_text = read_docx_text(file_path)

    result = build_prompt_for_document_type(doc_type, doc_text)
    if "error" in result:
        raise ValueError(f"Prompt creation failed: {result['error']}")
    
    return result["prompt"]

def trigger_reference_generation(file_path):
    # Load style template and referens for "summary"
    doc_type = DOC_TYPE_REFERENCE
    doc_text = read_docx_text(file_path)

    result = build_prompt_for_document_type(doc_type, doc_text)
    if "error" in result:
        raise ValueError(f"Prompt creation failed: {result['error']}")
    
    return result["prompt"]


# Kör hela flödet
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

    #  Låt användaren skriva in filnamn & skapa path till filen
    filnamn = input("📥 Ange filnamn i mappen 'input/' (inklusive .docx): ")
    intervju_path = f"data/input/{filnamn}"

    #  Låt användaren ange kandidatens namn
    candidate_name = input("👤 Ange kandidatens namn (för filnamn och rubrik): ")
      
    # Skapa prompt och generera sammanfattning eller KP
    if doc_choice == 1: #skapaa sammanfattning
        #prompt_text = trigger_summary_generation()
        try:
            prompt = trigger_summary_generation(intervju_path)
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
    elif doc_choice == 2: # skapa KP
        #prompt_text = trigger_kp_generation()
        try:
            prompt = trigger_kp_generation(intervju_path)
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
    elif doc_choice == 3: # skapa Referenssammanfattning
        try:
            prompt = trigger_reference_generation(intervju_path)
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)   
    else: 
        print("❌ Fel i dokument generering.")

    #  Visa exakt GPT-output
    #print("\n GPT-Output:\n" + "="*40)
    #print(summary)
    #print("="*40 + "\n")
    
    # Spara som Word-fil
    if summary:
        filename = f"sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        save_summary_to_docx(summary, candidate_name, filepath)
        print("✅ Sammanfattningenär klar.")
    else:
        print("❌ Sammanfattningen kunde inte genereras.")
