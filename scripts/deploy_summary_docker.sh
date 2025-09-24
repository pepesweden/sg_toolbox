#!/usr/bin/env bash
set -e

# 1) Städa bort ev. gammal kodmapp
rm -rf sg_toolbox

# 2) Hämta senaste koden
git clone --branch main git@github.com:pepesweden/sg_toolbox.git

# 3) Kopiera in .env från din dev-kopia till app-repot
cp -R ~/Documents/code_projects/sg_toolbox/ui/static/logo ./sg_toolbox/ui/static/logo/
cp -R ~/Documents/code_projects/sg_toolbox/ui/static/backgrounds ./sg_toolbox/ui/static/backgrounds/
cp -R ~/Documents/code_projects/sg_toolbox/data/reference/*  ./sg_toolbox/data/reference/
cp ~/Documents/code_projects/sg_toolbox/.env ./sg_toolbox/

# 4) Kör Compose med .env inuti app-repot
cd sg_toolbox
docker compose -f infrastructure/compose.yaml --env-file .env up -d --build
