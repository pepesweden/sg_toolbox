#Funktion för att formatera och  spara summering i word

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

#Definera mappar för static content


# Definierar punktlista definerar punklista
def add_bullet_list(items, doc):
    for item in items:
        paragraph = doc.add_paragraph(style='List Bullet')
        run = paragraph.add_run(item)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0, 0, 0)



# Formatterar och Sparar sammanfattning i en word fil
def save_summary_to_docx(summary_text, candidate_name, filepath):
    doc = Document()

    # Lägg till logotyp i sidhuvud
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    run = header_paragraph.add_run()
    run.add_picture("ui/static/logo/standard.png", width=Inches(1.5))
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    #  Extrahera rubriken (första raden)
    lines = summary_text.strip().split("\n")
    title_line = lines[0].strip()
    remaining_lines = lines[1:]

    # Lägg till rubriken
    title_paragraph = doc.add_paragraph()
    title_run = title_paragraph.add_run(title_line)
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.name = "Arial"
    title_run.font.color.rgb = RGBColor(106, 13, 173)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    # Första stycket → punktlista
    paragraphs = "\n".join(remaining_lines).strip().split("\n\n")
    bullet_text = paragraphs[0]
    bullet_points = [line.strip("-• ") for line in bullet_text.split("\n") if line.strip()]
    add_bullet_list(bullet_points, doc)

    # Formatera resterande innehåll
    for para in "\n".join(paragraphs[1:]).split("\n"):
        if not para.strip():
            continue

        paragraph = doc.add_paragraph()
        
        # Rubrik 2 (mindre rubriker)
        if para.strip().startswith("##"): #and para.strip().endswith("**"):
            clean_text = para.strip().replace("##", "")
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

    #  Spara fil
    # filename = f"data/output/sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
    doc.save(filepath)

"""
    # Sparar kp i en word fil
def save_kp_to_docx(summary_text, candidate_name):
    doc = Document()

    # Lägg till logotyp i sidhuvud
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    run = header_paragraph.add_run()
    run.add_picture("static/logo/standard.png", width=Inches(1.5))
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    #  Extrahera rubriken (första raden)
    lines = summary_text.strip().split("\n")
    title_line = lines[0].strip()
    remaining_lines = lines[1:]

    # Lägg till rubriken
    title_paragraph = doc.add_paragraph()
    title_run = title_paragraph.add_run(title_line)
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.name = "Arial"
    title_run.font.color.rgb = RGBColor(106, 13, 173)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    # Första stycket → punktlista
    paragraphs = "\n".join(remaining_lines).strip().split("\n\n")
    bullet_text = paragraphs[0]
    bullet_points = [line.strip("-• ") for line in bullet_text.split("\n") if line.strip()]
    add_bullet_list(bullet_points, doc)

    # Formatera resterande innehåll
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

    # Spara fil
    filename = f"output/kp_{candidate_name.lower().replace(' ', '_')}.docx"
    doc.save(filename)
"""

"""
def save_refsum_to_docx(summary_text, candidate_name):
    doc = Document()

    #  Lägg till logotyp i sidhuvud
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    run = header_paragraph.add_run()
    run.add_picture("static/logo/standard.png", width=Inches(1.5))
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    #  Extrahera rubriken (första raden)
    lines = summary_text.strip().split("\n")
    title_line = lines[0].strip()
    remaining_lines = lines[1:]

    # Lägg till rubriken
    title_paragraph = doc.add_paragraph()
    title_run = title_paragraph.add_run(title_line)
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_run.font.name = "Arial"
    title_run.font.color.rgb = RGBColor(106, 13, 173)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

    # Första stycket → punktlista
    paragraphs = "\n".join(remaining_lines).strip().split("\n\n")
    bullet_text = paragraphs[0]
    bullet_points = [line.strip("-• ") for line in bullet_text.split("\n") if line.strip()]
    add_bullet_list(bullet_points, doc)

    # Formatera resterande innehåll
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

    # Spara fil
    filename = f"output/refsum_{candidate_name.lower().replace(' ', '_')}.docx"
    doc.save(filename)
"""
