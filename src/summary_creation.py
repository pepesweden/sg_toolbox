import time

import openai

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os


from domain.prompt_builder import create_prompt, create_kp_prompt, create_refsum_prompt, build_prompt_for_document_type, DOC_TYPE_SUMMARY, DOC_TYPE_KP, DOC_TYPE_REFERENCE, DOC_TYPE_JOB_AD
from adapter.summary_generation import generate_summary
from adapter.save_to_docx import save_summary_to_docx
from adapter.text_extractor import read_docx_text, extract_texts_from_docx, read_pdf_text

UPLOAD_FOLDER = "data/input"
DOWNLOAD_FOLDER = "data/output"   

#Prompt trigger constants
TRIGGER_SUMMARY = "summary_trigger"
TRIGGER_KP = "kp_trigger"
TRIGGER_REFERENCE = "reference_trigger"
TRIGGER_JOB_AD = "job_ad_trigger"

# Function to load data and prep prompt info for summary generation
def trigger_generation(trigger, file_path, cv_path=None): 
    
    #Call functions to extract text from uploaded Docs
    doc_text = read_docx_text(file_path)
    if cv_path.endswith(".docx"):
        cv_text = read_docx_text(cv_path)
    else:
        cv_text = read_pdf_text(cv_path)
                                                
    if trigger == TRIGGER_SUMMARY:
        # Load style template and referens for "summary"
        doc_type = DOC_TYPE_SUMMARY
    
    elif trigger == TRIGGER_KP:
        # Load style template and referens for "KP"
        doc_type = DOC_TYPE_KP
    
    elif trigger == TRIGGER_REFERENCE:
        # Load style template and referens for "Reference"
        doc_type = DOC_TYPE_REFERENCE

    elif trigger == TRIGGER_JOB_AD:
        # Load style template and referens for "Reference"
        doc_type = DOC_TYPE_JOB_AD

    result = build_prompt_for_document_type(doc_type, doc_text, cv_text)
    if "error" in result:
        raise ValueError(f"Prompt creation failed: {result['error']}")
    return result["prompt"]

# Run the pipeline/flow
if __name__ == "__main__":
    # Let user choose document type to generate
    print("❓ Välj 1.Sammanfattning, 2.KP, 3. Referenssammanfattning eller 4. Jobbanons:")
    while True:
        doc_choice = input()
        if doc_choice in ["1", "2", "3", "4"]: 
            doc_choice = int(doc_choice)
            break
        else:
            print("Ogiltigt val. Vänligen välj 1-3.")

    # Let user enter filename for notes
    filnamn = input("📥 Ange filnamn i mappen 'input/' (inklusive .docx): ")
    # Create path to file
    intervju_path = f"data/input/{filnamn}"

    # Let user enter "Candidate Name"
    candidate_name = input("👤 Ange kandidatens namn (för filnamn och rubrik): ")

    #  Låt användaren lägga in CV av intervjun   
    cv_doc = input("📥 Ange filnamn på CV i mappen 'input/' (inklusive .docx eller .pdf): ")
    cv_text = None
    cv_path = None
    if cv_doc:
        cv_path = f"data/input/{cv_doc}"

    # Skapa prompt och generera sammanfattning eller KP
    if doc_choice == 1: #skapaa sammanfattning
        try:
            trigger = TRIGGER_SUMMARY
            prompt = trigger_generation(trigger, intervju_path, cv_path) 
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
    elif doc_choice == 2: # skapa KP
        #prompt_text = trigger_kp_generation()
        try:
            trigger = TRIGGER_KP
            prompt = trigger_generation(trigger, intervju_path, cv_path)
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)
    elif doc_choice == 3: # skapa Referenssammanfattning
        try:
            trigger = TRIGGER_REFERENCE
            prompt = trigger_generation(trigger, intervju_path)
            summary = generate_summary(prompt)
        except ValueError as e:
            print(f"Fel: {e}")
            exit(1)  
    elif doc_choice == 4: # skapa Referenssammanfattning
        try:
            trigger = TRIGGER_JOB_AD
            prompt = trigger_generation(trigger, intervju_path)
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
    
    # Save as word file
    if summary:
        filename = f"sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        save_summary_to_docx(summary, candidate_name, filepath)
        print("✅ Sammanfattningenär klar.")
    else:
        print("❌ Sammanfattningen kunde inte genereras.")
