Backup! 

def save_summary_to_docx(summary_text, candidate_name):
    doc = Document()

    # 🖼️ Lägg till logotyp i sidhuvud
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    run = header_paragraph.add_run()
    run.add_picture("static/logo/standard.png", width=Inches(1.5))
    header_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    # 🎯 Dela upp GPT-texten i stycken
    paragraphs = summary_text.strip().split("\n\n")

    # 🎯 Första stycket → punktlista
    bullet_text = paragraphs[0]
    bullet_points = [line.strip("-• ") for line in bullet_text.split("\n") if line.strip()]
    add_bullet_list(bullet_points, doc)

    # 📄 Formatera innehåll
    for i, para in enumerate(summary_text.split("\n")):
        if not para.strip():
            continue

        paragraph = doc.add_paragraph()
        run = paragraph.add_run(para.strip())

        # Rubrik 1: första raden (ex: "Kandidatsammanfattning")
        if i == 0:
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.name = "Arial"
            run.font.color.rgb = RGBColor(106, 13, 173)  # Mörklila
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        # Rubrik 2: nästa rubriker (t.ex. **Bakgrund**, **Tekniska Färdigheter**)
        elif para.startswith("**") and para.endswith("**"):
            run.text = para.replace("**", "")
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.name = "Arial"
            run.font.color.rgb = RGBColor(106, 13, 173)

        # Brödtext
        else:
            run.font.size = Pt(10)
            run.font.name = "Arial"
            run.font.color.rgb = RGBColor(0, 0, 0)

    # 💾 Spara fil
    filename = f"output/sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
    doc.save(filename)