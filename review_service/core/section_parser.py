import re
from typing import Dict, List, Tuple

def parse_document(text: str) -> Dict:
    """
    Parsar ett AI-genererat dokument i sektioner.
    
    Args:
        text: Fullständig dokumenttext
        
    Returns:
        Dict med 'metadata' och 'sections'
    """
    lines = text.strip().split('\n')
    
    # TODO: Extrahera rubrik
    #Steg 1
    title = lines[0].strip() if lines else ""

    #Steg 2
    heading_pattern = r'\*\*(.+?)\*\*'
    heading_matches = []
    
    for i, line in enumerate(lines):
        match = re.search(heading_pattern, line)
        if match:
            heading_name = match.group(1).strip()
            heading_matches.append((heading_name, i))  # (namn, radnummer)

    
    # TODO: Extrahera punktlista
    bullets_pattern = r'^[-•]\s*(.+)$'
    bullets_matches = []

    first_section_line = heading_matches[0][1] if heading_matches else len(lines)

    for line in lines[1:first_section_line]:
        match = re.search(bullets_pattern, line)
        if match:
            bullets_text = match.group(1).strip()  # ✅ Ren text
            bullets_matches.append(bullets_text)


    # TODO: Extrahera sektioner
    section_pattern = r'\*\*(.+?)\*\*(.+)\*\*'
    section_matches = []

    for line in lines[1:first_section_line]:
        match = re.search(section_pattern, line)
        if match:
            section_text = match.group(1).strip()  # ✅ Ren text
            bullets_matches.append(bullets_text)
    
    return {
        "metadata": {
            "title": title,
            "bullet_points": []
        },
        "sections": {}
    }