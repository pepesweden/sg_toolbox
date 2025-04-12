#This Module...
#Loads the docx as input
#Extraxts the text
#Anonymises it to be ready for the promptpa

#Laddar docx modulen
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# Läser in en Word-fil och extraherar texten
def read_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])