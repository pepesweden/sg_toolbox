from flask import Flask, render_template, request, send_file
import os
from summary_creation import read_docx_text, create_prompt, create_kp_prompt, generate_summary, save_summary_to_docx, create_refsum_prompt
from adapter.save_to_docx import save_summary_to_docx
from domain.prompt_builder import create_prompt, create_kp_prompt, create_refsum_prompt
from adapter.summary_generation import generate_summary
from adapter.text_extractor import read_docx_text
from flask import redirect

# Initiate Flask-app
app = Flask(__name__,
            template_folder='../ui/templates',    # Redirects to a higher folder level, ui/templates
            static_folder='../ui/static',)         # Redirects to a higher folder level, ui/static

# Definer folders where files from UI should be saved
UPLOAD_FOLDER = "data/input"
DOWNLOAD_FOLDER = "data/output"   
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER    


# render start-page with login form
@app.route("/")
def index():
    return render_template("index.html")

# render Summary creation page with login form
@app.route("/generate-summary")
def generate_summary_page():
    return render_template("generate_summary.html")

# render start-page with login form
@app.route('/login', methods=['POST'])
def login():
    #username = request.form['username']
    #password = request.form['password']
    
    # For now - just redirect
    return redirect('/welcome_page')
    
    # Later - add proper authentication
    #return render_template("welcome_page.html")

@app.route("/welcome_page")
def welcome_page():
    return render_template("welcome_page.html")


@app.route("/generate-seo")
def generate_seo_page():
    return render_template("generate_seo.html")

@app.route("/generate-offer")
def generate_offer_page():
    return render_template("generate_offer.html")

# Create Summary from uploaded files
@app.route("/generate", methods=["POST"])
def generate():
    # 📎 Hämta val, filer och namn från formuläret
    doc_choice = request.form.get("doc_choice")
    fil = request.files["intervjufil"]
    transcript_file = request.files.get("transcript")
    kandidatnamn = request.form["namn"]

    # ⚠️ Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # 💾 Spara intervju filen i input/
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(filepath)

    # 💾 Spara transcript (om det finns)
    transcript_path = None
    if transcript_file and transcript_file.filename.endswith(".docx"):
        os.makedirs("transcript", exist_ok=True)
        transcript_path = os.path.join("transcript", transcript_file.filename)
        transcript_file.save(transcript_path)

    #läs innehållet i filerna efter att de sparats
    doc_text = read_docx_text(filepath)
    transcript_text = read_docx_text(transcript_path) if transcript_path else None

    # Bygg prompt baserat på val av dokumenttyp
    if doc_choice == "1":
        mall_text = read_docx_text("data/reference/mall_sammanfattning.docx")
        style_text = read_docx_text("data/reference/Sammanfattning-claes.docx")
        prompt = create_prompt(doc_text, mall_text, style_text, transcript_text)
    elif doc_choice == "2":
        kpmall_text = read_docx_text("data/reference/kp_mall.docx")
        kpstyle_text = read_docx_text("data/reference/kp_ic.docx")
        prompt = create_kp_prompt(doc_text, kpmall_text, kpstyle_text, transcript_text)
    else:
        return "❌ Ogiltigt val. Vänligen välj 1 eller 2."

    # Skapa prompt och generera sammanfattning eller KP
    #prompt = create_prompt(doc_text, mall_text, style_text, transcript_text)
    summary = generate_summary(prompt)
    if summary is None:
        print("❌ Sammanfattningen kunde inte genereras.")
        return render_template("generate_summary.html", error="Sammanfattningen kunde inte genereras.")

    # 💾 Spara och returnera .docx
     # Skapa output-mapp om den inte finns
    os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)
    # Spara filen i output-mappen
    
    if doc_choice == "1":
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, kandidatnamn, filepath)
    elif doc_choice == "2":
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, kandidatnamn, filepath)
    else:
        filename = f"DOWNLOAD_FOLDER_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas

   


    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

@app.route("/generate_kp", methods=["POST"])
def generate_kp():
    # 📎 Hämta  filer och namn från formuläret
    fil = request.files["intervjufil"]
    transcript_file = request.files.get("transcript")
    kandidatnamn = request.form["namn"]

    # Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    #  Spara intervju filen i input/
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(filepath)

    # Spara transcript (om det finns)
    transcript_path = None
    if transcript_file and transcript_file.filename.endswith(".docx"):
        os.makedirs("data/transcript", exist_ok=True)
        transcript_path = os.path.join("data/transcript", transcript_file.filename)
        transcript_file.save(transcript_path)

    #läs innehållet i filerna efter att de sparats
    doc_text = read_docx_text(filepath)
    transcript_text = read_docx_text(transcript_path) if transcript_path else None

    # Bygg prompt baserat på val av dokumenttyp
    ###Borde kunna hämtas från Summary creation###
    kpmall_text = read_docx_text("data/reference/kp_mall.docx")
    kpstyle_text = read_docx_text("data/reference/kp_ic.docx")
    prompt = create_kp_prompt(doc_text, kpmall_text, kpstyle_text, transcript_text)
    
    # Skapa prompt och generera sammanfattning eller KP
    #prompt = create_prompt(doc_text, mall_text, style_text, transcript_text)
    summary = generate_summary(prompt)
    if summary is None:
        print("❌ KP kunde inte genereras.")
        return render_template("generate_summary.html", error="Sammanfattningen kunde inte genereras.")

    # 💾 Spara och returnera .docx
     # Skapa output-mapp om den inte finns
    os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)
    # Spara filen i output-mappen
    if summary:
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, kandidatnamn, filepath)
    else:
        filename = f"DOWNLOAD_FOLDER_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

# 🚀 Generera referenssammanfattning från uppladdade filer
@app.route("/generate_reference", methods=["POST"])
def generate_reference():
    # 📎 Hämta val, filer och namn från formuläret
    fil = request.files["intervjufil"]
    kandidatnamn = request.form["namn"]

    # ⚠️ Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # 💾 Spara intervju filen i input/
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(filepath)

    #läs innehållet i filerna efter att de sparats
    doc_text = read_docx_text(filepath)

    # Bygg prompt baserat på val av dokumenttyp
    refmall_text = read_docx_text("data/reference/refsum_mall.docx")
    refstyle_text = read_docx_text("data/reference/refsum_referencev2.docx")


    # Skapa prompt och generera sammanfattning eller KP
    #prompt = create_prompt(doc_text, mall_text, style_text, transcript_text)
    prompt = create_refsum_prompt(doc_text, refmall_text, refstyle_text)
    summary = generate_summary(prompt) 
    if summary is None:
        print("❌ Referensummeringe kunde inte genereras.")
        return render_template("generate_summary.html", error="Sammanfattningen kunde inte genereras.")

    #  Spara och returnera .docx
     # Skapa output-mapp om den inte finns
    os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)
    # Spara filen i output-mappen
    if summary:
        # Skapa filnamn och spara sammanfattningen
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, kandidatnamn, filepath)
    else:
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

