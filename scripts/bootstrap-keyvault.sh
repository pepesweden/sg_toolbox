#!/bin/bash
set -e

ENV=$1
SP_OBJECT_ID="7a24e257-da72-4e6c-98a6-7079952a8b94"

echo "🔑 Bootstrapping Key Vault access for ${ENV}..."

# Verifiera att vi är inloggade
echo "🔍 Verifying Azure login..."
az account show

# Sätt permissions
echo "🔐 Setting Key Vault permissions..."
az keyvault set-policy \
  --name "kv-toolbox-${ENV}-v2" \
  --object-id "${SP_OBJECT_ID}" \
  --secret-permissions get list set delete

echo "✅ Bootstrap complete!"