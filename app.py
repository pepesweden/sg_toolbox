from flask import Flask, render_template, request, send_file
import os
from summary_creation import read_docx_text, create_prompt, create_kp_prompt, generate_summary, save_summary_to_docx, save_kp_to_docx

# 🚀 Initiera Flask-app
app = Flask(__name__)
UPLOAD_FOLDER = "input"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🌐 Visar startsidan med formuläret
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-summary")
def generate_summary_page():
    return render_template("generate_summary.html")

@app.route("/generate-seo")
def generate_seo_page():
    return render_template("generate_seo.html")

@app.route("/generate-offer")
def generate_offer_page():
    return render_template("generate_offer.html")

# 🔁 Tar emot formuläret, kör summering och skickar tillbaka Word-fil
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
        mall_text = read_docx_text("reference/mall_sammanfattning.docx")
        style_text = read_docx_text("reference/Sammanfattning-claes.docx")
        prompt = create_prompt(doc_text, mall_text, style_text, transcript_text)
    elif doc_choice == "2":
        kpmall_text = read_docx_text("reference/kp_mall.docx")
        kpstyle_text = read_docx_text("reference/kp_ic.docx")
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
    os.makedirs("output", exist_ok=True)
    # Spara filen i output-mappen
    
    if doc_choice == "1":
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join("output", filename)
        save_summary_to_docx(summary, kandidatnamn)
    elif doc_choice == "2":
        filename = f"kp_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join("output", filename)
        save_kp_to_docx(summary, kandidatnamn)
    else:
        filename = f"output_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas

   


    print(f"✅ Fil sparad: {filepath}")
    return send_file(filepath, as_attachment=True)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

