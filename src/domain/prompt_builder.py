#Skapar prompten som används vid API anropet till OpenAI

#Imports
from adapter.text_extractor import read_docx_text  # Needed for build_prompt_for_document_type()

#Doctype constants
DOC_TYPE_SUMMARY = "summary"
DOC_TYPE_KP = "kp" 
DOC_TYPE_REFERENCE = "reference"
#DOC_TYPE_JOB_AD = "job-ad"

#rad för att git skall plocka upp

#Function to build prompt dependen on documen chosen to generate
def build_prompt_for_document_type(doc_type, doc_text):
    """Bygger prompt för given dokumenttyp"""
    
    if doc_type == DOC_TYPE_SUMMARY:
        mall_text = read_docx_text("data/reference/mall_sammanfattning.docx")
        style_text = read_docx_text("data/reference/Sammanfattning-claes.docx")
        
        #Create the LLM summary creation prompt
        prompt = create_prompt(doc_text, mall_text, style_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_SUMMARY,
            "mall_files_used": ["mall_sammanfattning.docx", "Sammanfattning-claes.docx"]
        }
        
    elif doc_type == DOC_TYPE_KP:
        kpmall_text = read_docx_text("data/reference/kp_mall.docx")
        kpstyle_text = read_docx_text("data/reference/kp_ic.docx")

        #Create the LLM "kandidatpresentation" creation prompt
        prompt = create_kp_prompt(doc_text, kpmall_text, kpstyle_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_KP,
            "mall_files_used": ["rkp_mall.docx", "kp_ic.docx"]
        }

    elif doc_type == DOC_TYPE_REFERENCE:
        refmall_text = read_docx_text("data/reference/refsum_mall.docx")
        refstyle_text = read_docx_text("data/reference/refsum_mall.docx.docx")

        #Create the LLM reference creation prompt
        prompt = create_refsum_prompt(doc_text, refmall_text, refstyle_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_REFERENCE,
            "mall_files_used": ["refsum_mall.docx", "refsum_mall.docx"]
        }

    #elif doc_type == DOC_TYPE_JOB_AD 

    else:
         return {"error": "Invalid document type"}


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
Du är en erfaren rekryterare som skriver professionella och detaljerade kandidatpresentationer för ett svenskt rekryteringsbolag.

 Din uppgift:
Skriv en **komplett och strukturerad kandidatpresentation** baserad på innehållet i följande intervjutext och CV.

 Presentationen ska:

1. **Följa strukturen i dokumentmallen {kpmall_text}**:
   - Rubriker: ALLMÄNT, Drivkrafter, Kompetens, utbildning, NYCKELTAL, Rekryterarens kommentarer, privat
   - Överst: Grunddata (namn, ålder, befattning, kontakt, uppsägningstid, publicerad, lönenivå, förmåner, nivå)
   - Alla fält fylls i. Om ett fält saknas i materialet, skriv "Ej angivet"

2. **Använda tonaliteten från tidigare presentationer i {kpstyle_text}**:
   - Reflekterande, konkret och personlig
   - Skriven i tredje person och med rekryterarens öga för nyanser
   - Kombinera beskrivning av kompetens och ansvar med observationer kring arbetssätt, kommunikation och driv

3. **För varje sektion, följ dessa riktlinjer**:

   - **ALLMÄNT**: Kronologisk, löpande sammanfattning av karriären. Sätt erfarenheterna i kontext. Lyft fram yrkesroll, ansvar, miljö, förändringar och exempel.
   - **Drivkrafter**: En kommaseparerad lista med ord (ex: nyfikenhet, ansvar, problemlösning)
   - **Kompetens**: En kommaseparerad lista med ord om kandidatens yrkesmässiga kompetenser, metoder, verktyg eller områden – oavsett roll (t.ex. försäljning, utveckling, ledarskap, analys, marknad etc.)
   - **Utbildning**: Punktlista med utbildningar, certifikat och eventuella kurser
   - **NYCKELTAL**: Punktlista med siffror *om de finns i materialet* (ex: teamstorlek, budgetansvar, antal kunder, försäljningsmål, projektantal, etc.)
   - **Rekryterarens kommentarer**: Reflekterande text om kandidatens arbetssätt, kommunikationsstil, personlighet och professionella nivå
   - **Privat**: Endast om relevant information finns – håll det kort

4. **Prioritera konkret yrkesmässig kontext och detaljer**:
   - Beskriv miljö, ansvar, prestationer, förändringar och metoder
   - Lyft exempel på problemlösning, driv, anpassning, och kommunikation
   - Oavsett om kandidaten arbetar med teknik, sälj, analys, projektledning eller något annat – inkludera yrkesspecifika detaljer

 Begränsningar:
- Du får **inte gissa, lägga till eller anta** något som inte framgår tydligt i materialet
- Hela texten ska bygga på {doc_text} och {transcript_section}
- Använd aldrig spekulationer, generaliseringar eller fluff – var tydlig, faktabaserad och detaljerad

🛠️ Underlag:
---
{doc_text}
{transcript_section}
---

✍️ Returnera endast texten till kandidatpresentationen – utan några extrakommentarer, förklaringar eller rubriker utöver mallen.
"""


def create_refsum_prompt(doc_text, refmall_text, refstyle_text, transcript_text=None):
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
Här är referensanteckningar från kollegor till en kandidat:

Referens 1:
{doc_text}

Referens 2:
[KLIPP IN FULLTEXT FRÅN REFERENSINTERVJU 2]

Och här är mallen som sammanfattningen ska följa: {refmall_text}

Skriv en färdig referenssammanställning enligt mallen ovan. Håll en professionell och sammanhängande ton. Sammanfatta innehållet konkret och strukturera texten tydligt under varje rubrik. Inkludera en avslutande punkt med vilka gemensamma teman som återkommer i båda referenserna.
Använda tonaliteten från tidigare sammanfattning i {refstyle_text}, Obs ingen information från denna text ska användas i sammanfattningen.
"""