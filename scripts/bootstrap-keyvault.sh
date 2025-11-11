#!/bin/bash
set -e


ENV=$1  # hämtar variable för den miljö vi kör ./scripts/bootstrap-keyvault.sh prod/qa
SP_OBJECT_ID="7a24e257-da72-4e6c-98a6-7079952a8b94"

echo "🔑 Bootstrapping Key Vault access for ${ENV}..."

# Här kommer az keyvault set-policy i nästa steg

echo "✅ Bootstrap script finished (no actions yet)."   