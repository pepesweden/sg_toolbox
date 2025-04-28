#Skapar prompten som används vid API anropet till OpenAI
#🧠 GPT prioriterar:
#Tydliga instruktioner i prompten
#Tidigare innehåll i prompten (det som kommer först)
#Det som är mest konkret och strukturerat
#➡️ Det betyder att intervjuanteckningar vinner över transcriptet i nästan alla fall – så länge prompten säger det.

#rad för att git skall plocka upp


def create_prompt(doc_text, mall_text, style_text, transcript_text=None):
        if transcript_text:
            transcript_section = f"""
📚 This is a complementary transcript from the interview.  
🟡 Use it *only* to support or expand upon the information in the interview notes.  
🟡 If there are discrepancies – prioritize the interview notes.  
🟡 You do not need to summarize the entire transcript – only extract relevant details:
{transcript_text}
"""
        else:
            transcript_section = ""
        return f"""
You are a professional recruiter tasked with writing a detailed summary based on an interview.

📄 Below are the interview notes about the candidate:
{doc_text}
{transcript_section}

🎯 Your task:
1. Write a highly detailed and structured summary based on the interview notes (primary) and the transcript (secondary).
2. Pay **special attention** to technical knowledge, skills, tools, environments, and examples. This is **extremely important** – include as much technical detail and depth as possible.
3. Follow the structure provided in this format template:
{mall_text}
4. Use the tone, language, and structure of this style reference:
{style_text}

📌 Important guidelines:
- Begin with a **bullet point list** containing key facts (e.g. skills, goals, salary expectations, availability).
- The summary must be **as detailed as possible**, based only on the information in the files.
- Write in a **chronological, reflective and concrete** style – just like a recruiter describing a candidate.
- Avoid bullet points in the main body (unless the template specifically uses them).
- Use a **professional but relaxed** tone – it should sound like it was written by a person.

🛠️ Formatting:
- Add **double asterisks** before and after all headings (e.g. **General**, **Technical skills**, etc.).
- Leave one empty line before each heading.

🚫 Limitations:
You may not invent, guess, or add any information that cannot be clearly derived from the interview notes or transcript. All content must be directly based on what is written above.
"""

def create_kp_prompt(doc_text, kpmall_text, kpstyle_text, transcript_text=None):
    if transcript_text:
            transcript_section = f"""
📚 This is a complementary transcript from the interview.  
🟡 Use it *only* to support or expand upon the information in the interview notes.  
🟡 If there are discrepancies – prioritize the interview notes.  
🟡 You do not need to summarize the entire transcript – only extract relevant details:
{transcript_text}
"""
    else:
        transcript_section = ""
    return f"""
Du är en erfaren rekryterare som skriver professionella kandidatpresentationer för ett svenskt rekryteringsbolag. 

Skriv en komplett **kandidatpresentation** baserad på innehållet i följande intervjutext och CV. Presentationen ska:

1. **Följa strukturen i dokumentmallen {kpmall_text}**:
   - Rubriker: ALLMÄNT, Drivkrafter, Kompetens, utbildning, NYCKELTAL, Rekryterarens kommentarer, privat
   - Överst: Grunddata (namn, ålder, befattning, kontakt, uppsägningstid, publicerad, lönenivå, förmåner, nivå)
   - Alla fält fylls i, även om du får uppskatta vissa (t.ex. ålder) utifrån innehållet.

2. **Använda tonaliteten från tidigare presentationer som finns i dokumenten {kpstyle_text}** (ex: Dotun, Lou, Joachim):
   - Reflekterande, personlig och konkret
   - Skriven i tredje person men utifrån rekryterarens perspektiv
   - Kombinera teknisk beskrivning med observationer om arbetssätt, kommunikation och personlighet

3. **Prioritera rekryteringsrelevant innehåll**:
   - Beskriv teknisk kontext, ansvar, övergångar och sammanhang
   - Lyft exempel på driv, problemlösning, och hur kandidaten kommunicerar
   - Avslöja inte att texten är AI-genererad

Här är underlaget för presentationen:
---
{doc_text}
{transcript_section}
---

Returnera endast texten till kandidatpresentationen enligt ovan – utan extrakommentarer eller förklaringar.

🚫 Begräsningsar:
Du får inte hitta på, gissa eller lägga till någon information som inte tydligt kan härledas från intervjuanteckningarna eller transkriptionen. Allt innehåll måste vara direkt baserat på det som står ovan.
"""