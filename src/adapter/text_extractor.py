#This Module...
#Loads the docx as input
#Extraxts the text


#Laddar docx modulen
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import List, Union
from pathlib import Path
from werkzeug.datastructures import FileStorage

####Gammal import av en(1) fil, funktionen används inte nu###
# Läser in en Word-fil och extraherar texten
def read_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])
    
###ny funktion som extraherar text från en eller flera docx-filer
def extract_texts_from_docx(files: List[Union[str, Path, FileStorage]]) -> List[str]:
    results = []

    for file in files:
        try:
            filename = file.filename if isinstance(file, FileStorage) else str(file)
            filename = filename.lower()

            if filename.endswith(".docx"):
                doc = Document(file)
                text = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
                if text:
                    results.append(text.strip())

        except Exception as e:
            print(f"[FEL] Kunde inte läsa {filename}: {e}")

    return results