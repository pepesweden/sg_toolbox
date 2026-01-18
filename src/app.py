# Import required modules from installt Python libraries
import logging
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from flask import Flask, render_template, request, send_file, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from auth.auth_manager import AuthManager
from auth.models import User
import os

# Import toolbox specific modules
from adapter.file_manager import write_file_to_storage
from summary_creation import generate_summary, save_summary_to_docx, trigger_generation, TRIGGER_SUMMARY, TRIGGER_KP, TRIGGER_REFERENCE, TRIGGER_JOB_AD
from adapter.save_to_docx import save_summary_to_docx
from adapter.summary_generation import generate_summary


# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Initiate Flask-app    
app = Flask(__name__,
            template_folder='../ui/templates',    # Redirects to a higher folder level, ui/templates
            static_folder='../ui/static',)         # Redirects to a higher folder level, ui/static

app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# Session security configuration
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Congiure user session timeout
app.config['SESSION_COOKIE_HTTPONLY'] = True
is_production = os.getenv('FLASK_ENV') == 'production'  #checks environemnt config for 
app.config['SESSION_COOKIE_SECURE'] = is_production     #Set coockie-secure basetd on bool-value
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'           #Allow samesite from secure sites but block xss and CSRF attempts
if is_production:
    Talisman(app, force_https=True)



# Definer folders where files from UI should be saved
UPLOAD_FOLDER = "data/input"
DOWNLOAD_FOLDER = "data/output"   
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER    

# Auth setup
DATABASE_URL = os.getenv('DATABASE_URL')
auth_manager = AuthManager(DATABASE_URL)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
login_manager.login_message = 'Du måste logga in för att komma åt denna sida.'
csrf = SeaSurf(app)

#create decorator to register get_user() with flask login
@login_manager.user_loader
def load_user(username):                    #create funktion to register in Login Manager
    return auth_manager.get_user(username)  #Call get_user function

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
    username = request.form['username']
    password = request.form['password']
    
    user = auth_manager.authenticate(username, password)
    
    if user:
        login_user(user)
        session.permanent = True  # ← Activate timeout config!
        flash(f'Välkommen {username}!')
        return redirect('/welcome_page')
    else:
        flash('Fel användarnamn eller lösenord')
        return redirect('/')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du har loggats ut')
    return redirect('/')

@app.route("/welcome_page")
@login_required
def welcome_page():
    return render_template("welcome_page.html")

@app.route("/generate-seo")
@login_required
def generate_seo_page():
    return render_template("generate_seo.html")

@app.route("/generate-offer")
@login_required
def generate_offer_page():
    return render_template("generate_offer.html")

@app.route("/generate_jobad", methods=["POST"])
@login_required
def generate_job_ad():
    # 📎 Hämta val, filer och namn från formuläret
    fil = request.files["intervjufil"]
    bolagsnamn = request.form["namn"]

    # Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # Spara intervju filen i input/
    intervju_path = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
    fil.save(intervju_path)
    
    # Generate summary
    try:
            trigger = TRIGGER_JOB_AD
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
        filename = f"sammanfattning_{bolagsnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, filepath)
    else:
        filename = f"sammanfattning_{bolagsnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

# Create Summary from uploaded files
@app.route("/generate", methods=["POST"])
@login_required
def generate():
    fil = request.files["intervjufil"]
    #transcript_file = request.files.get("transcript")
    candidate_name = request.form["namn"]
    cv_file = request.files["cv"]

    # Make sure it is a .docx file
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."


    ###Importerad filhanteringslogik###
    intervju_path = write_file_to_storage(fil.read(), fil.filename, UPLOAD_FOLDER) #REMEMBER Filestorage object from flask!!
    cv_path = write_file_to_storage(cv_file.read(), cv_file.filename, UPLOAD_FOLDER) #REMEMBER Filestorage object from flask!!

    # Skapa prompt och generera sammanfattning
    try:
        trigger = TRIGGER_SUMMARY
        prompt = trigger_generation(trigger, intervju_path, cv_path)
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
    save_summary_to_docx(summary, filepath)
    

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

# Create KP from uploaded files
@app.route("/generate_kp", methods=["POST"])
@login_required
def generate_kp():
    # Get infrormation (files and candidate name) from the web form
    fil = request.files["intervjufil"]
    kandidatnamn = request.form["namn"]
    cv_file = request.files["cv"]

    # Kontrollera att det är en .docx-fil
    if not fil or not fil.filename.endswith(".docx"):
        return "❌ Felaktig filtyp. Endast .docx tillåtet."

    # Imported file management logic
    intervju_path = write_file_to_storage(fil.read(), fil.filename, UPLOAD_FOLDER) #REMEMBER Filestorage object from flask!!
    cv_path = write_file_to_storage(cv_file.read(), cv_file.filename, UPLOAD_FOLDER) #REMEMBER Filestorage object from flask!!

    # Create prompt and generate summary
    try:
        trigger = TRIGGER_KP
        prompt = trigger_generation(trigger, intervju_path, cv_path)
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
        save_summary_to_docx(summary, filepath)
    else:
        filename = f"DOWNLOAD_FOLDER_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)
    #return send_file(filepath, as_attachment=True)

# Generera referenssammanfattning från uppladdade filee
#
@app.route("/generate_reference", methods=["POST"])
@login_required
def generate_reference():
    # 📎 Hämta val, filer och namn från formuläret
    #fil = request.files["intervjufil"]
    filer = request.files.getlist("intervjufil")
    kandidatnamn = request.form["namn"]

    # Skapa en tom lista för att spara alla paths
    sparade_paths = []

    # Loopa över varje fil
    for fil in filer:
        # Kontrollera att det är en .docx-fil
        if not fil or not fil.filename.endswith(".docx"):
            return "❌ Felaktig filtyp. Endast .docx tillåtet."
        ref_path = os.path.join(app.config["UPLOAD_FOLDER"], fil.filename)
        fil.save(ref_path)
        sparade_paths.append(ref_path)  # Spara path:en till listan

    # Nu har du: sparade_paths = ["data/input/ref1.docx", "data/input/ref2.docx"]

    # Generate summary
    try:
            trigger = TRIGGER_REFERENCE
            prompt = trigger_generation(trigger, sparade_paths)
            summary = generate_summary(prompt)
    except ValueError as e:
        return render_template("error.html", error=str(e))

    ###  Spara och returnera .docx ####
    # Skapa output-mapp om den inte finns
    os.makedirs(app.config["DOWNLOAD_FOLDER"], exist_ok=True)
    
    # Spara filen i output-mappen
    if summary:
        # Skapa filnamn och spara sammanfattningen
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)
        save_summary_to_docx(summary, filepath)
    else:
        filename = f"sammanfattning_{kandidatnamn.lower().replace(' ', '_')}.docx"  # fallback om något är knas
        filepath = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    print(f"✅ Fil sparad: {filepath}")
    return send_file(os.path.abspath(filepath), as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

