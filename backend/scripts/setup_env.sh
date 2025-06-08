#!/bin/bash

set -e

VENV_PATH="/var/www/jobfishing-venv"
PROJECT_PATH="/var/www/jobfishing-backend"
REQUIREMENTS="$PROJECT_PATH/requirements.txt"

echo "👉 Removendo venv anterior (se existir)..."
sudo rm -rf "$VENV_PATH"

echo "📦 Criando novo ambiente virtual em $VENV_PATH"
sudo -u www-data python3 -m venv "$VENV_PATH"

echo "📥 Instalando dependências do requirements.txt"
sudo -u www-data "$VENV_PATH/bin/pip" install -r "$REQUIREMENTS"

echo "✅ Ambiente configurado com sucesso!"
