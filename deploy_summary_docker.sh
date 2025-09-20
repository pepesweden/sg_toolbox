#!/usr/bin/env bash
set -e

# 1) Städa bort ev. gammal kodmapp
rm -rf summary_automation

# 2) Hämta senaste koden
git clone --branch main git@github.com:pepesweden/summary_automation.git

# 3) Kopiera in .env från din dev-kopia till app-repot
cp ~/Documents/code_projects/summary_automation/.env ./summary_automation/

# 4) Kör Compose med .env inuti app-repot
cd summary_automation
docker compose -f infrastructure/compose.yaml --env-file .env up -d --build
