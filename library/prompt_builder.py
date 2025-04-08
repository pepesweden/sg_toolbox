#Skapar prompten som används vid API anropet till OpenAI
#🧠 GPT prioriterar:
#Tydliga instruktioner i prompten
#Tidigare innehåll i prompten (det som kommer först)
#Det som är mest konkret och strukturerat
#➡️ Det betyder att intervjuanteckningar vinner över transcriptet i nästan alla fall – så länge prompten säger det.


def create_prompt(doc_text, mall_text, style_text, transcript_text=None):
        if transcript_text:
            transcript_section = f"""
📚 Här är ett kompletterande transkript från samtalet.  
🟡 Använd det endast som *stöd* för att tolka eller förstärka information i intervjuanteckningarna.  
🟡 Om det finns skillnader – prioritera intervjuanteckningarna.  
🟡 Du behöver inte sammanfatta hela transcriptet – plocka bara relevanta delar:
{transcript_text}
"""
        else:
            transcript_section = ""
        return f"""
Du är en rekryterare som ska skapa en professionell sammanfattning efter en intervju. 

📄 Här är intervjuanteckningarna om kandidaten:
{doc_text}
{transcript_section}

🎯 Ditt uppdrag är att:
1. Skapa en så detaljerad sammanfattning utifrån anteckningarna & transcriptet det bara gå
2. Lyft särskilt fram kunskaper och kompetenser från filerna, denna del är extra viktigså detaljerade som möjligt, gärna med exempel.
2. Följ formatet i den här mallen:
{mall_text}
3. Använd språk, struktur och tonalitet som i detta exempel:
{style_text}

📌 Viktiga riktlinjer:
- Inledas med en **punktlista** över nyckelinformation (t.ex. kompetenser, mål, lön, tillgänglighet)
- Sammanfattningen ska vara **så detaljerad som möjligt** utifrån innehållet i anteckningarna
- Skriv kronologiskt, konkret och reflekterande – precis som en rekryterare skulle beskriva en kandidat
- Undvik punktlistor (om inte mallen uttryckligen innehåller det)
- Använd ett professionellt men avslappnat tonfall – det ska kännas skrivet av en människa

Formattering:
- Lägg till ** före och efter för alla rubriker (t.ex. **Allmänt**, **Teknisk kunskap och färdigheter** etc)
- Lämna en tom rad före varje rubrik

🚫 Begränsning:
Du får inte lägga till, gissa eller formulera information som inte tydligt kan härledas från intervjuanteckningarna ovan. Allt innehåll ska vara baserat på information som finns i texten.
"""