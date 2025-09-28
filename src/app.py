from flask import Flask, render_template, request, send_file, redirect
import os
from adapter.file_manager import write_file_to_storage
from summary_creation import generate_summary, save_summary_to_docx, trigger_generation, TRIGGER_SUMMARY, TRIGGER_KP, TRIGGER_REFERENCE
from adapter.save_to_docx import save_summary_to_docx
from adapter.summary_generation import generate_summary

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
    fil = request.files["intervjufil"]
    #transcript_file = request.files.get("transcript")
    candidate_name = request.form["namn"]

    # Make sure it is a .docx file
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # Save the file to input/
    #intervju_path = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename) 
    #fil.save(intervju_path)

    ###Importerad filhanteringslogik###
    intervju_path = write_file_to_storage(fil.read(), fil.filename, UPLOAD_FOLDER)#REMEMBER Filestorage object from flask!!

    # Skapa prompt och generera sammanfattning
    try:
        trigger = TRIGGER_SUMMARY
        prompt = trigger_generation(trigger, intervju_path)
        summary = generate_summary(prompt)
    except ValueError as e:
        return render_template("error.html", error=str(e))

    if summary is None:
        print("❌ Sammanfattningen kunde inte genereras.")
        return render_template("generate_summary.html", error="Sammanfattningen kunde inte genereras.")
    
    ### Save and return .docx file ###
    # 1. Create output folder if it is missing
    os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)

    # 2. Save the file to the output folder
    filename = f"sammanfattning_{candidate_name.lower().replace(' ', '_')}.docx"
    filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
    save_summary_to_docx(summary, candidate_name, filepath)
    

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

@app.route("/generate_kp", methods=["POST"])
def generate_kp():
    # Get infrormation (file and candidate name) from the web form
    fil = request.files["intervjufil"]
    #transcript_file = request.files.get("transcript")
    kandidatnamn = request.form["namn"]

    # Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    #  Spara intervju filen i input/
    intervju_path = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(intervju_path)

    # Spara transcript (om det finns)
    #transcript_path = None
    #if transcript_file and transcript_file.filename.endswith(".docx"):
    #    os.makedirs("data/transcript", exist_ok=True)
    #    transcript_path = os.path.join("data/transcript", transcript_file.filename)
    #    transcript_file.save(transcript_path)

    #transcript_text = read_docx_text(transcript_path) if transcript_path else None    

     # Skapa prompt och generera sammanfattning
    try:
        trigger = TRIGGER_KP
        prompt = trigger_generation(trigger, intervju_path)
        summary = generate_summary(prompt)
    except ValueError as e:
        return render_template("error.html", error=str(e))

    if summary is None:
        print("❌ KP kunde inte genereras.")
        return render_template("generate_summary.html", error="Sammanfattningen kunde inte genereras.")

    # Spara och returnera .docx
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

# Generera referenssammanfattning från uppladdade filer
@app.route("/generate_reference", methods=["POST"])
def generate_reference():
    # 📎 Hämta val, filer och namn från formuläret
    fil = request.files["intervjufil"]
    kandidatnamn = request.form["namn"]

    # Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # Spara intervju filen i input/
    intervju_path = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(intervju_path)
    
    # Generate summary
    try:
            trigger = TRIGGER_REFERENCE
            prompt = trigger_generation(trigger, intervju_path)
            summary = generate_summary(prompt)
    except ValueError as e:
        return render_template("error.html", error=str(e))

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

