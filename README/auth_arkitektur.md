Arkitektur - Quick Overview

Fysisk struktur:
´´´
Din Mac (Host)
├── sg_toolbox/ (kod)
│   ├── venv/ (Python packages)
│   ├── src/app.py (Flask app - körs LOKALT i venv)
│   └── data/postgres/ (databasfiler - persistent)
│
└── Docker
    └── PostgreSQL Container
        └── Läser/skriver till data/postgres/
´´´

Runtime flow (Development):

Du startar PostgreSQL:

bash   docker compose up -d  # PostgreSQL container igång

Du startar Flask:

bash   python src/app.py  # Lokal Python process

Connection:

   Flask (localhost:5001) 
      ↓ psycopg2
   PostgreSQL (localhost:5432 → Docker container)
      ↓
   Data files (./data/postgres/ på din Mac)
Varför denna setup?
Development:

Flask lokalt = snabb reload, enkel debugging
PostgreSQL i Docker = rätt databas, lätt setup
Data på host = överlever container restarts

Later (Production):

Flask i Docker container
PostgreSQL på AWS RDS/GCP Cloud SQL
Samma kod, olika connection string

Package-flöde:
pythonvenv packages (lokalt installerade):
├── flask → Web framework
├── flask-login → Session management
├── psycopg2 → PostgreSQL driver (pratar med Docker)
└── bcrypt → Password hashing

Docker container:
└── PostgreSQL server (tar emot connections från psycopg2)