# Salesgroup Toolbox - adminstrative atuomation tools

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


##
