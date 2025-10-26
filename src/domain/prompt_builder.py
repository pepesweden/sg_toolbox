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
        refstyle_text = read_docx_text("data/reference/refsum_referencev2.docx")

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
<INTERVJUANTECKNINGAR>
{doc_text}
</INTERVJUANTECKNINGAR>



===

Du är en erfaren rekryterare på ett svenskt rekryteringsbolag. Din uppgift är att skriva en kandidatsammanfattning baserad på intervjuanteckningar och CV.

VIKTIGA REGLER FÖR KÄLLMATERIAL:
- CV är den auktoritativa källan för: årtal, jobbtitlar, företagsnamn, utbildning
- Intervjuanteckningar är den auktoritativa källan för: arbetsuppgifter, tekniska detaljer, personlighet, motivation
- Om CV saknas: använd intervjun för allt, men var mer försiktig med årtal om de är otydliga
- Intervjuanteckningar är ofta korthuggna och informella (t.ex. "Jobbat 5 år, sålde bra, fick avancera") - tolka dessa naturligt men hitta ALDRIG på detaljer

SKRIV I DENNA ORDNING - STEG FÖR STEG:

STEG 1 - Extrahera fakta innan du skriver:
a) Från CV: lista alla jobb med årtal, titlar, företag (kronologiskt, äldst först)
b) Från intervju: lista alla tekniska verktyg, system, programvaror (var specifik: "Intune", "PowerShell", "Cisco CLI" etc)
c) Från intervju: notera personlighetsdrag som har konkreta exempel

STEG 2 - Skriv sammanfattningen enligt denna struktur:

<STRUKTURMALL>
{mall_text}
</STRUKTURMALL>

STEG 3 - Följ denna EXAKTA stil och ton:

<STILREFERENS - KOPIERA DENNA STIL>
{style_text}
</STILREFERENS>

DETALJERADE INSTRUKTIONER FÖR VARJE SEKTION:

**ALLMÄNT (Kronologisk karriärberättelse):**
1. Inled med EN av dessa fraser (välj baserat på innehåll):
   - "[Namn] började sin karriär [år] hos [företag] som [titel]..."
   - "[Namn] har byggt sin karriär inom [område] och arbetar idag som..."
   - "Efter studier inom [område] började [Namn] [år] hos [företag]..."

2. Skriv sedan STRIKT KRONOLOGISKT (äldst först → nyast sist):
   - För varje jobb: företag, tidsperiod, jobbtitel, huvudansvar
   - Nämn tekniska OMRÅDEN/KATEGORIER här (t.ex. "molninfrastruktur", "M365-miljö", "automatisering")
   - Använd tidsmarkörer: "Efter X år...", "Under perioden...", "Sedan [år]..."
   - Spara specifika verktygsnamn till nästa sektion

3. UNDVIK dessa typer av "LLM-floskler" och vaga formuleringar:
    FÖRBJUDNA FRASTYPER:
    ❌ Generiska adjektiv utan konkret stöd: "driven", "passionerad", "dynamisk", "målinriktad"
    ❌ Vaga superlativer: "gedigen erfarenhet", "omfattande kunskap", "stark bakgrund", "bred kompetens"
    ❌ Abstraka beskrivningar: "har en passion för", "brinner för", "trivs i dynamisk miljö"
    ❌ Floskelaktiga kombinationer: "driven och målinriktad", "engagerad och strukturerad"
    ❌ Överdrifter utan belägg: "exceptionell", "outstanding", "expert inom"

    SPECIFIKA EXEMPEL PÅ FÖRBJUDNA FRASER:
    ❌ "driven och målinriktad"
    ❌ "passion för"
    ❌ "gedigen erfarenhet" 
    ❌ "omfattande kunskap"
    ❌ "dynamisk miljö"
    ❌ "stark bakgrund"
    ❌ "tar initiativ"
    ❌ "bred kompetens inom"

4. ANVÄND istället konkreta detaljer:
✅ "ökade försäljningen med 40%"
✅ "ansvarade för 1300 användare"
✅ "övergick från on-prem till hybrid-lösning"
✅ "byggde PowerShell-skript som automatiserade..."
✅ Beskriv VAD personen gjorde, inte HUR bra de var

**TEKNISK KUNSKAP OCH FÄRDIGHETER (Detaljerad genomgång):**
1. KRITISKT: Nämn ALLA specifika verktyg, system, programvaror från STEG 1b
2. Skriv i löpande text (inga punktlistor)
3. För varje teknologi: ge konkret exempel på VAD personen gjort
   - Exempel: "Han har använt PowerShell för att bygga skript som automatiskt byter standardskrivare vid omstart för 1300 användare"
   - INTE: "Han har erfarenhet av PowerShell och automatisering"

4. Gruppera logiskt (men täck ALLT):
   - Microsoft-miljö (M365, Azure, Intune, Exchange, etc)
   - Infrastruktur (nätverk, servrar, virtualisering)
   - Automatisering (PowerShell, scripting, etc)
   - Övriga verktyg/system

5. Prioritera DJUP och DETALJER över generella beskrivningar
6. Om intervjun nämner något tekniskt bara i förbigående - inkludera det ändå!

**PERSONLIGHET/PRAKTISKT:**
1. Basera ENDAST på konkreta exempel från intervjun
2. Beskriv VAD personen gör, inte HUR bra de är
3. Om intervjun nämner drivkrafter eller arbetssätt: använd personens egna ord
4. Inkludera: arbetssätt, preferenser för arbetskultur, vad som motiverar personen

**KOMMENTAR:**
1. Inled med: "[Namn] ger ett [välj konkret adjektiv: strukturerat/entusiastiskt/analytiskt/metodiskt] intryck"
2. Skriv ENDAST om:
   - Observationer rekryteraren faktiskt gjorde under intervjun (om dokumenterat)
   - Kandidatens styrkor som framgår tydligt från intervjun
   - Din rekommendation

3. VIKTIGT: Om rekryteraren INTE dokumenterade egna observationer i intervjun:
   - Basera detta på kandidatens beskrivningar av sitt arbetssätt
   - Var försiktig med att "hitta på" intryck som inte finns dokumenterade

KRITISKA BEGRÄNSNINGAR:
🚫 Gissa ALDRIG årtal om de inte finns i CV
🚫 Hitta ALDRIG på tekniska detaljer som inte nämns
🚫 Använd ALDRIG spekulativa fraser ("troligtvis", "förmodligen", "det verkar som")
🚫 Kopiera INTE exakta citat från stilreferensen (kopiera stil, inte innehåll)
🚫 Lägg INTE till information som inte finns i källmaterialet

OUTPUT FORMAT:
- Skriv endast sammanfattningen enligt strukturen ovan
- Använd **dubbla asterisker** runt rubriker för att markera dem
- Lämna en tom rad före varje rubrik
- Inga extra kommentarer, förklaringar eller rubriker utöver mallen
- Svara på svenska
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