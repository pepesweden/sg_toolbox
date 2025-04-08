# Toolbox Project – To-Do List

// ✅ Toolbox Project – To-Do List (inkl. GCP & Terraform)

✅ Flask-app med filuppladdning och summering
✅ Visuell styling enligt Salesgroup
✅ Word-formattering (rubriker, brödtext, logga)
✅ Automatisk punktlista av första stycket
✅ Webbgenerering fungerar med filval
✅ Coming soon-sidor för SEO och offert
✅ Hem-knapp och logotyp med länkar
✅ Gradient + bakgrundsbild fixad
✅ Toolbox startsida med blurb-navigering
✅ CSS-standardstruktur etablerad
✅ Lägg till startsidan toolbox.salesgroup
✅ Undersidor: summeringsautomation, SEO-text, offert
✅ Component-ifiera summary_creation.py – bryt ut funktioner till separata moduler (`create_prompt`, `generate_summary`)
✅ Prompten hanterar transcript korrekt – används endast som stöd
✅ Word-dokument genereras med formatering enligt Salesgroup-stil (logotyp, färger, rubriker, punktlista)
✅ Upload fungerar och resultat går att ladda ner
✅ Lokal DNS-entry toolbox.salesgroup via hosts-fil (fungerar endast lokalt)
✅ Layout för sammanfattningsverktyget (upload, knapp etc.) är fixad
✅ Flytta `create_prompt()` till `prompt_builder.py`
✅ Flytta `generate_summary()` till `summary_generation.py`
✅ Fixa `save_summary_to_docx()` med korrekt rubrikstruktur
✅ Hantera promptlängd och token overflow
✅ Felsökning: .docx-nedladdning, rubriker, GPT-prompt
✅ Debug-visning av GPT-svar i terminal
✅ Korrekt API-nyckelhantering via `.env`
✅ Strukturering av `generate()` i `app.py`
✅ Återställning av `openai.ChatCompletion.create()`
✅ Felsökning: `name 'openai' is not defined`, `None`-returns

🧠 **Arkitektur & Struktur**
☐ Översätt och byt till ny promot
☐ Bygg Openai chunks för prompt
☐ Skapa ett prompt-bibliotek (`prompt_library.py`)
☐ Skapa en `load_references()`-funktion för mall + stil
☐ Möjlighet att välja filnamn i terminal/web GUI
☐ Avancerat promptläge (visa/ändra prompt direkt)
☐ Hantera flera dokumenttyper (t.ex. sammanfattning vs. kandidatpresentation)
☐ Stöd för uppladdning av flera filer som input
☐ Lägg till möjlighet att hämta kandidatnamn automatiskt
☐ Lägg till CLI-läge för att köra `summary_creation.py`
☐ Lägg till roll (titel) som inputfält i gränssnitt + rad i .docx
☐ Lägg till testläge (GPT-output utan .docx)
☐ Component-ifiera ytterligare (ex. `document_writer.py`, `input_loader.py`)
☐ Anonymisera input-sträng till OpenAI-anropet (ta bort namn etc.)
☐ Kör en webbsökning (via OpenAI) för att testa om anonymiserad input ändå kan avslöja person – för framtida integritetsanalys (Proof of Concept)

🌐 **UI & Användarupplevelse**
☐ Lägg till språkval i gränssnittet (svenska/engelska)
☐ Lägg in översättningsflagga i backend
☐ Lägg till språkidentifiering i backend (fallback)
☐ Översätt prompt till engelska
☐ Visa “Skickar till GPT...” och liknande indikatorer i UI
☐ Lägg till progress-output (t.ex. "Läser fil", "Skickar till GPT", "Genererar svar..." etc.) i browsern

📥 **Filhantering & Nedladdning**
☐ Lägg till nedladdningsknapp för .docx istället för direktnedladdning
☐ Skapa HTML-dokument under blurben efter generering
☐ Formatera HTML snyggt med CSS och visa i sidan
☐ Lägg till nedladdningsknappar för HTML och DOCX
☐ Exportera sammanfattning som HTML och PDF
☐ Återställ .docx-nedladdning med korrekt filnamn
☐ Lägg till TikToken token-räknare som räknar antal tokens före anrop – stoppa om över gräns (för att undvika onödiga API-försök/kostnad)

🧰 **Webbapp-funktioner**
☐ Ladda upp referensmallar + återanvända
☐ Lägg till dokumentprocess (ex göra Lexbase-koll)
☐ Kunna välja vad man vill generera (Sammanfattning eller KP) – påverkar val av prompt
☐ Lägg till "tool" annons generering
☐ Lägg till "tool" generering säljmail

💾 **Långsiktig Plan (Minne & Användare)**
☐ Bygg eget 'minne' (referenser, instruktioner) i t.ex. MySQL
☐ Användarspecifik tonalitet/stil i webapp
☐ Webappen sparar intervjuer och summeringar
☐ Välj input- och referensfiler från databas
☐ Flera dokumentmallar (output templates)
☐ Skapa inloggningssystem
☐ Möjlighet att skicka GPT-anrop i sekvenser/steg:
1️⃣ Summera transkript
2️⃣ Summera intervjuanteckningar
3️⃣ Berika sammanfattning från transkript med intervjuanteckningar

🎨 **Designsystem**
☐ Skapa stylingmall (CSS) med komponentstruktur
☐ Lägg till Font Awesome (ikoner)
☐ Central hantering av färger, komponenter
☐ Snygga till logotyp och hem-ikon i undersidor
☐ Enhetlig stil på blurbs och Toolbox-utseende
☐ Ladda in Salesgroups riktiga CSS (om tillgänglig)
☐ Skapa centralt styling-/komponentbibliotek (React Design System)
☐ Förklara central komponenthantering (React-stil)

🔐 **Autentisering**
☐ Undersök och implementera Bearer Authentication vid behov

☁️ **Infra & DevOps**
☐ Lägg in projektet i git
☐ Koppla projekt till GitHub
☐ Skapa release pipeline
☐ Flytta till hostinglösning (GCP, Render, Azure)
☐ SSL-cert, DNS, och andra kringtjänster
☐ Terraform för infrastruktur
☐ Paketera appen för lokal installation
☐ Skapa `requirements.txt`
☐ Skapa README
☐ Lägg till `.gitignore`
☐ Bygg `start.sh` / `run.sh` för enkel start

✅ **Terraform + GCP – Infrastrukturkrav (Förberedelser)**

☁️ **GCP-resurser via Terraform**
☐ Cloud Run – Flask/web-appen
☐ Cloud SQL – användardata, prompts, sessions
☐ Cloud Storage – .docx och referensfiler
☐ IAM-roller – tjänstekonton
☐ VPC-nätverk – trafik mellan Cloud Run ↔ Cloud SQL
☐ HTTPS/SSL – via Cloud Run

🛠️ **To-Do: Setup för Terraform + GCP**
📌 1. **Lokalt förberedande**
☐ Installera Terraform CLI
☐ Installera Google Cloud CLI
☐ Initiera Terraform-projekt

🔐 2. **GCP Förberedelser**
☐ Skapa/aktivera GCP-projekt
☐ Aktivera API:er:
- Cloud Run
- Cloud SQL Admin
- IAM
- Cloud Storage
☐ Skapa service account + rätt roller
☐ Ladda ner JSON-nyckel

📁 3. **Terraform-struktur**
☐ `main.tf`
☐ `variables.tf`
☐ `outputs.tf`
☐ `terraform.tfvars`
☐ `provider.tf`

📦 **Andra funktioner & tekniker**
☐ Träningsblock: nested dictionaries & JSON
☐ Gör scriptet till clean code
☐ PATH-setup för Flask och OpenAI CLI

📚 **Webapp Struktur (Toolbox)**
☐ Skapa dashboard/startskärm: Toolbox
☐ Undersidor:
- Sammanfattningsverktyg
- SEO-generator (coming soon)
- Offertgenerator (coming soon)
