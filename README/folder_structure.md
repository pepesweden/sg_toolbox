summary_automation/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── anonymizer.py
│   │   │   ├── chunker.py
│   │   │   ├── prompt_engine.py
│   │   │   └── interfaces.py          # gränssnitt (summarizer, formatter...)
│   │   ├── core/
│   │   │   └── orchestrator.py        # pipeline 1→5
│   │   ├── adapters/
│   │   │   ├── doc_reader.py
│   │   │   ├── openai_summarizer.py
│   │   │   ├── docx_renderer.py
│   │   │   ├── ats_client.py
│   │   │   └── storage_fs.py
│   │   └── api/
│   │       └── http.py                # Flask endpoints
│   └── wsgi.py
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
