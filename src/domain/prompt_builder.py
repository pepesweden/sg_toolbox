#Skapar prompten som används vid API anropet till OpenAI

#Imports
from adapter.text_extractor import read_docx_text, read_md_text  # <-- Function to load and

from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")

#Doctype constants
DOC_TYPE_SUMMARY = "summary"
DOC_TYPE_KP = "kp" 
DOC_TYPE_REFERENCE = "reference"
DOC_TYPE_JOB_AD = "job_ad"

#Function to build prompt dependen on documen chosen to generate
def build_prompt_for_document_type(doc_type, doc_text, cv_text):
    """Bygger prompt för given dokumenttyp"""
    if doc_type == DOC_TYPE_SUMMARY:
        mall_text = read_md_text("data/reference/summary_template.md")
        style_text = read_docx_text("data/reference/Sammanfattning-claes.docx")
        
        #Create the LLM summary creation prompt
        prompt = create_prompt(doc_text, mall_text, style_text, cv_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_SUMMARY,
            "mall_files_used": ["summary_template.md", "Sammanfattning-claes.docx"]
        }
        
    elif doc_type == DOC_TYPE_KP:
        kpmall_text = read_md_text("data/reference/kp_template_json.md")
        kpmall_text = kpmall_text.replace("[dagens datum]", today)
        kpstyle_text = read_docx_text("data/reference/kp_ic.docx")

        #Create the LLM "kandidatpresentation" creation prompt
        prompt = create_kp_prompt(doc_text, kpmall_text, kpstyle_text, cv_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_KP,
            "mall_files_used": ["kp_template.md", "kp_ic.docx"]
        }

    elif doc_type == DOC_TYPE_REFERENCE:
        refmall_text = read_md_text("data/reference/reference_template.md")
        refstyle_text = read_docx_text("data/reference/refsum_referencev2.docx")

        #Create the LLM reference creation prompt
        prompt = create_refsum_prompt(doc_text, refmall_text, refstyle_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_REFERENCE,
            "mall_files_used": ["reference_template.md", "refsum_mall.docx"]
        }
    
    elif doc_type == DOC_TYPE_JOB_AD:
        job_ad_mall_text = read_md_text("data/reference/job_ad_template.md")
        job_ad_style_text = read_docx_text("data/reference/job_ad_example.docx")

        #Create the LLM job ad creation prompt
        prompt = create_job_ad_prompt(doc_text, job_ad_mall_text, job_ad_style_text)

        return {
            "prompt": prompt,
            "type": DOC_TYPE_JOB_AD,
            "mall_files_used": ["job_ad_template.md", "job_ad_example.docx"]
        }


    else:
         return {"error": "Invalid document type"}


def create_prompt(doc_text, mall_text, style_text, cv_text=None):
        if cv_text:
            cv_section = f"""
            <CV>
            {cv_text}
            </CV>
            """
        else:
            cv_section = ""
        return f"""
<INTERVJUANTECKNINGAR>
{doc_text}
</INTERVJUANTECKNINGAR>

{cv_section}

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

def create_kp_prompt(doc_text, mall_text, style_text, cv_text=None):
        if cv_text:
            cv_section = f"""
            <CV>
            {cv_text}
            </CV>
            """
        else:
            cv_section = ""
        return f"""
```
<INTERVJUANTECKNINGAR>
{doc_text}
</INTERVJUANTECKNINGAR>

<CV>
{cv_text}
</CV>

===

Du är en erfaren rekryterare på ett svenskt rekryteringsbolag. Din uppgift är att skriva en kandidatpresentation baserad på intervjuanteckningar och CV.

VIKTIGA REGLER FÖR KÄLLMATERIAL:
- CV är den auktoritativa källan för: årtal, jobbtitlar, företagsnamn, utbildning
- Intervjuanteckningar är den auktoritativa källan för: arbetsuppgifter, tekniska detaljer, personlighet, motivation, lön
- Om CV saknas: använd intervjun för allt, men var mer försiktig med årtal om de är otydliga
- Intervjuanteckningar är ofta korthuggna och informella (t.ex. "Jobbat 5 år, sålde bra, fick avancera") - tolka dessa naturligt men hitta ALDRIG på detaljer

GLOBALA SPRÅKREGLER (gäller för HELA texten):
UNDVIK dessa typer av "LLM-floskler" och vaga formuleringar:
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

ANVÄND istället konkreta detaljer, faktiska händelser och specifika exempel från intervjun.

SKRIV I DENNA ORDNING - STEG FÖR STEG:

STEG 1 - Extrahera fakta innan du skriver:
a) Från CV (om det finns): lista alla jobb med årtal, titlar, företag (kronologiskt, äldst först)
   Om CV saknas: extrahera denna info från intervjuanteckningar om möjligt
b) Från intervju: lista alla tekniska verktyg, system, kompetensområden (var specifik)
c) Från intervju: notera konkreta drivkrafter, personlighetsdrag, arbetssätt med exempel

STEG 2 - Skriv kandidatpresentationen enligt denna struktur:

<STRUKTURMALL>
{mall_text}
</STRUKTURMALL>

OUTPUT FORMAT:
- Använd strukturmallen
- Returnera först en huvurubrik me markdon format enligt STRUKTURMALL
- Returnera ett JSON-block för sektionen **GRUNDDATA** från STUKTURMALLEN:
- Resterande skall vara i markdown format enligt STRUKTURMALLEN ovan .

STEG 3 - Följ denna EXAKTA stil och ton:

<STILREFERENS - KOPIERA DENNA STIL>
{style_text}
</STILREFERENS>

DETALJERADE INSTRUKTIONER FÖR VARJE SEKTION:

**GRUNDDATA (Tabellformat från JSON):**
- Här skall JSON-block från STUKTURMALLEN läggas in
- Verifiera att blocket startar med [Start json]


VIKTIGT FÖR GRUNDDATA:
- Om information saknas: skriv "Ej angivet" istället för att gissa
- För lön: använd kandidatens exakta formulering från intervjun (t.ex. "60´000 fast och fördelning 50/50 fast och rörlig")
- Alla fält måste fyllas i (med "Ej angivet" om info saknas)

**ALLMÄNT (Kronologisk karriärberättelse i löpande text):**
1. Inled med kandidatens bakgrund - kan vara:
   - Tidiga år/utbildning om relevant för karriären
   - Första jobbet
   - En särskild händelse som format karriären

2. Skriv sedan STRIKT KRONOLOGISKT (äldst först → nyast sist):
   - För varje karriärsteg: beskriv sammanhang, val, utveckling, lärdomar
   - Nämn företag, roller, tidsperioder, huvudansvar
   - Inkludera VARFÖR personen bytte jobb eller gjorde karriärval
   - Använd tidsmarkörer: "Efter X år...", "2017 blev han...", "Sedan dess..."
   - Var narrativ och reflekterande - berätta en STORY om karriären

3. Avsluta med nuläget och varför personen söker sig vidare

4. TON: 
   - Tredje person ("Igor jobbade...", "Han utvecklade...")
   - Reflekterande och konkret
   - Inkludera kandidatens egna tankar och insikter från intervjun
   - Beskriv inte bara VAD hen gjorde, utan VAD hen lärde sig och HUR det format dem

**Drivkrafter (Kommaseparerad lista MED förklarande mening först):**
Format:
En förklarande mening om vad som driver kandidaten baserat på intervjun.

Om meningen inte räcker för att fånga komplexiteten, fortsätt med kommaseparerade nyckelord.

Exempel från stilreferens:
"Den stora drivkraften är att få känna en stolthet i hantverket för försäljning och affärsmannaskap."

VIKTIGT: Basera ENDAST på vad kandidaten faktiskt sa i intervjun om motivation, drivkrafter, mål.

**Kompetens (Kommaseparerad lista med ord/fraser):**
Format: word1, word2, word3, word4, etc.

- Lista kandidatens yrkesmässiga kompetenser, metoder, verktyg, områden
- Både generella (t.ex. "Account Executive", "ledarskap") och specifika (t.ex. "SaaS", "complex sales")
- Oavsett om kandidaten jobbar med försäljning, IT, analys, eller annat - anpassa till yrkesområdet
- Inkludera 5-15 termer beroende på kandidatens bredd

**Utbildning (Punktlista):**
- Lista utbildningar, certifikat, kurser
- Format: [Utbildning], [Institution], [År om känt]
- Om ingen formell utbildning finns dokumenterad: skriv "Ej dokumenterad"

**Nyckeltal (punktlista):**
- Teamstorlek, budgetansvar, försäljningsmål, antal kunder, projektantal, prestationsmått
- Format som punktlista
- Om inga konkreta siffror finns eller identifieras: skriv "Ej Angivet"
- Skriv ALLTID ut rubriken 

**Rekryterarens kommentarer (Löpande text):**

1. Inled med:
   "[Namn] ger ett [konkret adjektiv: strukturerat/entusiastiskt/analytiskt/metodiskt/etc] intryck"

2. Skriv om följande tre områden, med tydliga och konkreta exempel hämtade från intervjun:

   A) Arbetsstil  
      – Beskriv hur kandidaten arbetar i praktiken.  
      – Använd situationer kandidaten själv berättat om.  
      – Skriv i formen: observation → exempel → vad det visar.  
      – Fokus: hur kandidaten planerar, prioriterar, analyserar, driver arbete eller hanterar komplexitet.

   B) Kommunikationsstil  
      – Beskriv hur kandidaten resonerar, samarbetar och för dialog med andra.  
      – Använd exempel från situationer kandidaten beskrivit (kundmöten, teamarbete, leveransdialog etc).  
      – Lyft fram mönster i hur kandidaten lyssnar, ställer frågor, förklarar saker eller anpassar sitt språk.  
      – Inga tekniska verktyg eller system här.

   C) Kompetens (yrkesmässig förmåga — oavsett om kandidaten är säljare, chef, projektledare, tekniker etc)  
      – Beskriv kandidatens faktiska kompetens genom konkreta händelser från intervjun.  
      – Fokus på vad kandidaten GJORDE, inte vad kandidaten ÄR.  
      – Exempel:
        "Nils beskriver hur han genomför sin behovsanalys genom att ställa strukturerade frågor och koppla kundens svar till verksamhetslogik. Det visar att han arbetar metodiskt och med god förmåga att skapa klarhet."
      – Undvik tekniska listningar. Teknik hör hemma i TEKNISK KUNSKAP-sektionen.

   – Lyft även kandidatens styrkor samt motivation för att söka sig vidare, om detta framgår tydligt i intervjun.  
   – Om intervjun visar mognad, ansvarstagande eller utvecklingsområden kan detta beskrivas — men aldrig spekuleras.

3. VIKTIGT:
   – Beskriv endast det som faktiskt framgår i intervjumaterialet.  
   – Var konkret: observation → exempel → vad det innebär i praktiken.  
   – Undvik generiska värdeord eller säljande språk.  
   – Kommentaren ska vara reflekterande och professionell, inte marknadsförande.

4. FÖRBJUDNA AVSLUTNINGSFRASER:
   ❌ "Jag rekommenderar starkt att ni överväger…"  
   ❌ "Ni bör träffa…"  
   ❌ "Utmärkt kandidat för…"  
   ❌ Alla former av rekommendation eller matchningsbedömning.

5. Avsluta kommentaren när du beskrivit intryck, arbetsstil, kommunikationsstil, kompetens och motivation.  
   Ingen sammanfattande värdering eller rekommendation.

**STILINSTRUKTION FÖR REKRYTERARENS KOMMENTAR (NY SEKTOR – KRITISK):**

Skriv kommentaren i en rådgivande och reflekterande ton som liknar hur en erfaren senior rekryterare resonerar internt:

– Beskriv det du observerat och hur det tar sig uttryck i kandidatens arbetssätt.  
– Lägg till en kort tolkning: vad betyder detta i en praktisk arbetskontext?  
– Var nyanserad och undvik värdeord; fokusera på hur kandidaten faktiskt fungerar.  
– Lyft både styrkor och eventuella begränsningar om intervjun ger stöd för detta.  
– Skriv sakligt och professionellt, inte säljigt eller marknadsförande.  
– Var konkret: observation → konsekvens → vad det innebär för rätt rollmiljö.  
– Använd ett språk som är rådgivande snarare än marknadsförande, t.ex.:  
  "Det här visar att…", "I praktiken innebär det att…", "Utifrån intervjun framgår att…"

Undvik:
– känslomässiga adjektiv  
– rekommendationer  
– generiska lovord  
– sammanfattande slutsatser om rollmatchning

Kommentaren ska vara ett kort, reflekterande resonemang, inte en värdering.

**Privat:**
- Civilstånd, bostadsort, fritidsintressen
- Håll det mycket kort (1-3 meningar max)
- Om ingen sådan info finns: skriv "Ej angivet"
- Skriv ALLTID ut rubriken 

**Övrigt (kort text):**
- Inkludera sådant som inte passar in någonannanstans
- Om ingen sådan info finns: skriv "Ej angivet"
- Skriv ALLTID ut rubriken 

KRITISKA BEGRÄNSNINGAR:
🚫 Gissa ALDRIG årtal, lön, ålder om de inte finns i materialet
🚫 Hitta ALDRIG på detaljer som inte nämns
🚫 Använd ALDRIG spekulativa fraser ("troligtvis", "förmodligen", "det verkar som")
🚫 Kopiera INTE exakta citat från stilreferensen (kopiera stil, inte innehåll)
🚫 Lägg INTE till information som inte finns i källmaterialet
🚫 Skriv ALDRIG rekommendationer ("Jag rekommenderar...", "Bör träffa...", "Utmärkt för...") om inte rekryteraren explicit skrev detta i intervjun
🚫 Avsluta INTE Rekryterarens kommentarer med avslutningsfraser


OUTPUT FORMAT:
- Använd **dubbla asterisker** för rubriker
- Lämna en tom rad före varje ny sektion
- Inga extra kommentarer, förklaringar eller rubriker utöver strukturen
- Svara på svenska
"""


def create_refsum_prompt(doc_text, refmall_text, refstyle_text, transcript_text=None):
      return f"""
Här är referensanteckningar från kollegor till en kandidat:

Referens:
{doc_text}

Och här är mallen som sammanfattningen ska följa: {refmall_text}

Skriv en färdig referenssammanställning enligt mallen ovan. Håll en professionell och sammanhängande ton. Sammanfatta innehållet konkret och strukturera texten tydligt under varje rubrik. Inkludera en avslutande punkt med vilka gemensamma teman som återkommer i båda referenserna.
Använda tonaliteten från tidigare sammanfattning i {refstyle_text}, Obs ingen information från denna text ska användas i sammanfattningen.

VIKTIGT:
- Om de uppladdade referensdokumenten bara innehåller ett namn på en referensgivare, hänvisa till **Referenten** i texten OCH rubriker
- Om de uppladdade referensdokumenten innehåller två eller fler namn på referensgivare, hänvisa till **Referenterna** i texten OCH rubriker

KRITISKA BEGRÄNSNINGAR:
🚫 Hitta ALDRIG på detaljer som inte nämns
🚫 Använd ALDRIG spekulativa fraser ("troligtvis", "förmodligen", "det verkar som")
🚫 Lägg INTE till information som inte finns i källmaterialet
🚫 Skriv ALDRIG rekommendationer ("Jag rekommenderar...", "Bör träffa...", "Utmärkt för...") om inte rekryteraren explicit skrev detta i intervjun
"""

def create_job_ad_prompt(doc_text, job_ad_mall_text, job_ad_style_text):
        return f"""
Du är en erfaren rekryterare som skriver professionella jobbannonser för ett svenskt rekryteringsbolag.

📋 Din uppgift:
Skriv en komplett jobbannons baserad på kravprofilen nedan.

📄 Kravprofil att utgå från:
{doc_text}

🎯 Struktur att följa (från mall):
{job_ad_mall_text}

✍️ Tonalitet och stil (från tidigare annons):
{job_ad_style_text}

📌 Viktiga riktlinjer:

1. **Företagsnamn:**
   - Extrahera företagsnamnet från kravprofilens "Företagsinformation" → "Namn"
   - Använd företagsnamnet konsekvent genom hela annonsen
   - Ersätt [Företagsnamn] i mallen med det faktiska företagsnamnet

2. **Struktur:**
   - Följ exakt samma rubriker och ordning som i mallen
   - Varje sektion ska ha tydligt innehåll från motsvarande del i kravprofilen

3. **Mapping från kravprofil till annons:**
   - "Fakta om företaget" → "Om [Företagsnamn]"
   - "Befattningen → Arbetsuppgifter" → "Om rollen"
   - "Kravspecifikation → Förkunskaper och färdigheter" → "Vi söker"
   - Extra kompetenser från kravspec → "Det är meriterande med"
   - "Kravspecifikation → Personlighet/profil" → "Personliga egenskaper"
   - "Utveckling" + "Anställningsvillkor" → "Vi erbjuder"

4. **Språk och ton:**
   - Professionell men tillgänglig ton
   - Konkret och saklig - undvik marknadsföringsspråk
   - **UNDVIK** fraser som: "spännande möjlighet", "unik chans", "fantastisk roll"
   - Skriv om vad rollen innebär, inte hur "spännande" den är
   - Använd aktivt språk: "Du arbetar med..." istället för "Du kommer att få arbeta med..."

5. **Om rollen:**
   - Översiktlig beskrivning av arbetsuppgifterna
   - Förklara kontexten (team, organisation, arbetsmodell)
   - Håll det konkret och undvik vaga formuleringar

6. **Vi söker:**
   - Lista faktiska krav från kravspecifikationen
   - Var specifik: "minst X års erfarenhet av Y"
   - Prioritera tekniska kompetenser och erfarenheter
   - Inkludera utbildnings- och språkkrav

7. **Meriterande:**
   - Lista saker som nämns i kravprofilen som önskvärda men ej kritiska
   - Var konkret om vilka teknologier/verktyg/metoder

8. **Personliga egenskaper:**
   - Översätt personlighetsorden från kravprofilen till konkreta beteenden
   - Istället för "ansvarstagande" → "Du tar ansvar för..."
   - Istället för "lagspelare" → "Du samarbetar aktivt..."
   - Koppla egenskaperna till faktiska arbetsmoment när möjligt

9. **Vi erbjuder:**
   - Beskriv arbetsmiljö baserat på "Utveckling" i kravprofilen
   - Inkludera praktisk information (plats, arbetsmodell, omfattning)
   - Undvik att sälja - presentera fakta om arbetsplatsen

10. **Ansökan:**
    - Använd EXAKT denna text:
    
    "I denna rekryteringsprocess samarbetar [Företagsnamn] med Salesgroup.
    
    Salesgroup tillämpar en fördomsfri och inkluderande rekryteringsprocess och arbetar i enlighet med diskrimineringslagen för att motverka diskriminering och verka för lika rättigheter. Har du några frågor, eller behöver tekniskt stöd med att söka tjänsten är du alltid välkommen att höra av dig till oss på 08-26 20 00. Tillträde enligt överenskommelse. Vi tillämpar löpande urval i denna rekryteringsprocess och välkomnar därför din ansökan snarast."

🚫 Begränsningar:
- Du får INTE gissa eller lägga till information som inte finns i kravprofilen
- Du får INTE använda marknadsföringsspråk eller överdrivna formuleringar
- Du får INTE hoppa över någon sektion från mallen
- All information måste komma från kravprofilen

✅ Output:
Returnera endast den färdiga jobbannonsen - ingen förklaring eller kommentarer.
Använd **rubriknamn** för alla rubriker (ex: **Om rollen:**)
"""