summary_automation/
├── src/
│   ├── app/
│   │   ├── __init__.py                 # Finns inte ännu
│   │   ├── domain/
│   │   │   ├── anonymizer.py           # TBD - inte utvecklad ännu
│   │   │   ├── chunker.py              # TBD - inte utvecklad ännu
│   │   │   ├── prompt_builder.py
│   │   │   └── interfaces.py           # gränssnitt (summarizer, formatter...)
│   │   ├── core/
│   │   │   └── orchestrator.py         # pipeline 1→5 OBS används inte ännu
│   │   ├── adapters/
│   │   │   ├── text_extractor.py
│   │   │   ├── summary_generation.py   
│   │   │   ├── save_to_docx.py
│   │   │   ├── ats_client.py           # TBD - inte utvecklad ännu
│   │   │   └── storage_fs.py
│   │   └── api/
│   │       └── http.py                 # Flask endpoints - finns inte ännu
│   │
│   ├── review_service/
│   │
│   └── wsgi.py
│
├── infra/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── compose.yaml
│   ├── terraform/
│   └── k8s/
├── config/
│   ├── toolbox.conf
│   └── .env.example
├── data/                              # flyttat hit
│   ├── input/
│   ├── output/
│   ├── reference/
│   └── transcript/
├── docs/
│   ├── architecture.drawio
│   └── HOWTO.md
├── ui/                                # webb-UI (templates/static)
│   ├── templates/
│   │   ├── generate_offer.html
│   │   ├── generate_seo.html
│   │   ├── generate_summary.html
│   │   └── index.html
│   └── static/
│       ├── style.css
│       ├── logo/
│       └── backgrounds/
├── scripts/
│   ├── deploy_summary_docker.sh
│   └── helpers.py
├── tests/
│   └── test_orchestrator.py
├── requirements.txt
└── README.md
