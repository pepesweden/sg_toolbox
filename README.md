# Salesgroup Toolbox - adminstrative atuomation tools
🚧 **UNDER CONSTUCTION** 🚧

## What is SG Toolbox?
SG Toolbox is a Flask-based web application that automates the creation of recruitment documents using OpenAI's API. It processes CVs, interview notes, and reference materials to generate professional Swedish-language recruitment summaries, candidate presentations (KP), reference summaries, and job advertisements.

The system is designed to integrate with Salesgroup's ATS (Ponty) and follows established document templates and writing styles to maintain consistency across the organization.

## Features

### Current Capabilities
- **Candidate Summaries** - Generate traditional candidate summaries from interview notes and CVs
- **Candidate Presentations (KP)** - Create formal candidate presentations following Salesgroup templates
- **Reference Summaries** - Compile structured summaries from multiple reference interviews
- **Job Advertisements** - Generate job ads from requirement profiles for Salesgroup's website
- **User Authentication** - Secure login system with PostgreSQL backend
- **Document Processing** - OCR support for PDFs, DOCX text extraction, automated formatting

### Document Processing
- Accepts `.docx` and `.pdf` files
- OCR capabilities using Tesseract for scanned documents
- Structured output with Salesgroup branding and formatting
- Downloads as ready-to-use Word documents

## Project Structure
```
sg_toolbox/
├── src/                          # Application source code
│   ├── app.py                    # Main Flask application
│   ├── auth/                     # Authentication module
│   │   ├── auth_manager.py       # User management & auth logic
│   │   └── models.py             # User model
│   ├── adapter/                  # External integrations
│   │   ├── file_manager.py       # File upload/download handling
│   │   ├── save_to_docx.py       # Word document formatting
│   │   ├── summary_generation.py # OpenAI API calls
│   │   └── text_extractor.py     # Document text extraction
│   ├── domain/                   # Business logic
│   │   └── prompt_builder.py     # LLM prompt construction
│   └── summary_creation.py       # Document generation orchestration
│
├── ui/                           # Frontend templates and assets
│   ├── templates/                # Jinja2 HTML templates
│   └── static/                   # CSS, logos, backgrounds
│
├── infrastructure/               # Infrastructure as Code
│   ├── terraform/                # Azure infrastructure
│   │   ├── main.tf               # Resource definitions
│   │   ├── variables.tf          # Input variables
│   │   ├── backend.tf            # Remote state config
│   │   └── environments/         # Environment-specific configs
│   ├── docker/                   # Container configuration
│   │   └── Dockerfile            # Production container image
│   └── compose.yaml              # Local development setup
│
├── data/                         # Data directories
│   ├── input/                    # Uploaded files (gitignored)
│   ├── output/                   # Generated documents (gitignored)
│   ├── reference/                # Template documents & style guides
│   └── postgres/                 # Local database storage (gitignored)
│
├── .github/workflows/            # CI/CD pipelines
│   └── deploy-qa.yml             # QA deployment workflow
│
└── scripts/                      # Utility scripts
    ├── deploy_summary_docker.sh  # Local Docker deployment
    └── bootstrap-keyvault.sh     # Key Vault access setup
```

## Tech Stack
**Backend:**
- Python 3.12 with Flask
- PostgreSQL 16 (via psycopg2)
- OpenAI API (GPT-4o)
- Docker & Docker Compose

**Infrastructure:**
- Azure Container Apps
- Azure Container Registry
- Azure PostgreSQL Flexible Server
- Azure Key Vault (secrets management)
- Terraform (Infrastructure as Code)
- GitHub Actions (CI/CD)

**Document Processing:**
- python-docx (Word document generation)
- PyPDF2 (PDF text extraction)
- pytesseract (OCR)
- pdf2image (PDF to image conversion)


## Quick Start
### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development without Docker)
- OpenAI API key
- PostgreSQL (handled by Docker Compose)

### Local Development with Docker Compose

1. **Clone the repository:**
 ```bash
 git clone git@github.com:pepesweden/sg_toolbox.git
 cd sg_toolbox
 ```
2. **Create `.env` file in project root:**

```bash
# Flask
SECRET_KEY=your-secret-key-here
HOST_PORT=8000
   
#PostgreSQL
POSTGRES_PASSWORD=your-secure-password
DB_PORT=5432
DATABASE_URL=postgresql://sg_user:your-secure-password@postgres:5432/sg_toolbox
   
# OpenAI
OPENAI_API_KEY=your-openai-api-key   

# Admin user (flask app admin user)
ADMIN_PASSWORD=your-admin-password
```

3. **Add required files:**
   ```bash
   # Copy logos and backgrounds to ui/static/
   ui/static/logo/           # Company logos
   ui/static/backgrounds/    # UI backgrounds
   
   # Add reference templates to data/reference/
   data/reference/           # Template documents for style reference
   ```

4. **Start the application:**
   ```bash
   docker compose -f infrastructure/compose.yaml up -d --build
   ```

5. **Access the application:**
   - Open browser: `http://localhost:8000`
   - Login with username `admin` and your `ADMIN_PASSWORD`

6. **Stop the application:**
   ```bash
   docker compose -f infrastructure/compose.yaml down
   ```

##
