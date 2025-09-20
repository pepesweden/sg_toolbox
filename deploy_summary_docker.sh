#!/usr/bin/env bash
set -Eeuo pipefail

# === Inställningar (kan överstyras via env) ===
IMAGE_NAME="${IMAGE_NAME:-slaskapp}"
IMAGE_TAG="${IMAGE_TAG:-dev}"     # kan sättas med: IMAGE_TAG=prod ./deploy_summary_docker.sh
HOST_PORT="${HOST_PORT:-8000}"    # port på din dator
APP_PORT_IN_IMAGE="8000"          # porten Gunicorn lyssnar på i containern

# === Paths ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}"

# === Snabb sanity-checks ===
command -v docker >/dev/null 2>&1 || { echo "❌ docker saknas i PATH"; exit 1; }

[ -f "${PROJECT_ROOT}/Dockerfile" ] || { echo "❌ Hittar ingen Dockerfile i ${PROJECT_ROOT}"; exit 1; }
[ -f "${PROJECT_ROOT}/wsgi.py" ] || { echo "❌ Hittar ingen wsgi.py i ${PROJECT_ROOT}"; exit 1; }
[ -f "${PROJECT_ROOT}/requirements.txt" ] || { echo "❌ Hittar ingen requirements.txt i ${PROJECT_ROOT}"; exit 1; }
[ -f "${PROJECT_ROOT}/.env" ] || { echo "❌ Hittar ingen .env i ${PROJECT_ROOT} (lägg nycklar här, checka INTE in i git)"; exit 1; }

# Valfritt: varna om .dockerignore saknas (byggen blir tyngre utan den)
if [ ! -f "${PROJECT_ROOT}/.dockerignore" ]; then
  echo "⚠️  Ingen .dockerignore hittad – rekommenderas för snabbare/säkrare builds."
fi

echo "🔧 Bygger image: ${IMAGE_NAME}:${IMAGE_TAG}"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${PROJECT_ROOT}/Dockerfile" "${PROJECT_ROOT}"

# Städa ev. gammal container med samma namn
CONTAINER_NAME="${IMAGE_NAME}_run"
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "🧹 Tar bort gammal container ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
fi

echo "🚀 Startar container → http://localhost:${HOST_PORT}"
docker run --rm \
  --name "${CONTAINER_NAME}" \
  -p "${HOST_PORT}:${APP_PORT_IN_IMAGE}" \
  --env-file "${PROJECT_ROOT}/.env" \
  "${IMAGE_NAME}:${IMAGE_TAG}"
