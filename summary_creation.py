import time

import openai

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import os

from library.prompt_builder import create_prompt
from library.summary_generation import generate_summary


# Skapa en klient (plockar API-nyckel automatiskt från .env eller miljövariabel)
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Läser in en Word-fil och extraherar texten
def read_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# Definierar punktlista definerar punklista
def add_bullet_list(items, doc):
    for item in items:
        paragraph = doc.add_paragraph(style='List Bullet')
        run = paragraph.add_run(item)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)

#5. Sparar documentet i en word fil
def save_summary_to_docx(summary_text, candidate_name):
    doc = Document()

    # 🖼️ Lägg till logotyp i sidhuvud
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    run = header_paragraph.add_run()
    run.add_picture("static/logo/standard.png", width=Inches(1.5))
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    # 🎯 Extrahera rubriken (första raden)
    lines = summary_text.strip().split("\n")
    title_line = lines[0].strip()
    remaining_lines = lines[1:]

    # ➕ Lägg till rubriken
    title_paragraph = doc.add_paragraph()
    title_run = title_paragraph.add_run(title_line)
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.name = "Arial"
    title_run.font.color.rgb = RGBColor(106, 13, 173)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    # 🎯 Första stycket → punktlista
    paragraphs = "\n".join(remaining_lines).strip().split("\n\n")
    bullet_text = paragraphs[0]
    bullet_points = [line.strip("-• ") for line in bullet_text.split("\n") if line.strip()]
    add_bullet_list(bullet_points, doc)

    # 📄 Formatera resterande innehåll
    for para in "\n".join(paragraphs[1:]).split("\n"):
        if not para.strip():
            continue

        paragraph = doc.add_paragraph()
        
        # Rubrik 2 (mindre rubriker)
        if para.strip().startswith("**") and para.strip().endswith("**"):
            clean_text = para.strip().replace("**", "")
            run = paragraph.add_run(clean_text)
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.name = "Arial"
            run.font.color.rgb = RGBColor(106, 13, 173)
        # Brödtext
        else:
            run = paragraph.add_run(para.strip())
            run.font.size = Pt(10)
            run.font.name = "Arial"
            run.font.color.rgb = RGBColor(0, 0, 0)

    # 💾 Spara fil
    filename = f"output/sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
    doc.save(filename)


def generate_summary(prompt):
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


#lista tillgänliga modeller
#if __name__ == "__main__":
    # Testa att lista tillgängliga modeller
#    models = client.models.list()

#    print("\n📦 Tillgängliga modeller:\n")
#    for model in models.data:
#        print(f"🔹 {model.id}")    


# 📦 5. Kör hela flödet
if __name__ == "__main__":
    # 📥 Låt användaren skriva in filnamn
    filnamn = input("📥 Ange filnamn i mappen 'input/' (inklusive .docx): ")
    intervju_path = f"input/{filnamn}"

    # 👤 Låt användaren ange kandidatens namn
    candidate_name = input("👤 Ange kandidatens namn (för filnamn och rubrik): ")

    # Ladda mall och stilreferens
    mall_text = read_docx_text("reference/mall_sammanfattning.docx")
    style_text = read_docx_text("reference/Sammanfattning-claes.docx")
    doc_text = read_docx_text(intervju_path)
    
    # Skapa prompt och generera sammanfattning
    prompt = create_prompt(doc_text, mall_text, style_text)
    summary = generate_summary(prompt)

    # 🔍 Visa exakt GPT-output
    #print("\n📥 GPT-Output:\n" + "="*40)
    #print(summary)
    #print("="*40 + "\n")

    # Spara som Word-fil
    if summary:
        save_summary_to_docx(summary, candidate_name=candidate_name)
    else:
        print("❌ Sammanfattningen kunde inte genereras.")
    