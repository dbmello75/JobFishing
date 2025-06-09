.PHONY: backend frontend deploy-backend deploy-frontend deploy-all venv restart logs
SHELL := /bin/bash
.ONESHELL:

BACKEND_DIR=./backend
FRONTEND_DIR=./frontend
BACKEND_TARGET=/var/www/jobfishing-backend
FRONTEND_TARGET=/var/www/jobfishing-frontend
VENV_PATH=/var/www/jobfishing-venv

deploy-backend: backend restart

deploy-frontend: frontend

deploy-all: deploy-backend deploy-frontend

backend:
	sudo rsync -avz --delete \
		--exclude '.git/' \
		--exclude '*.md' \
		--exclude 'Makefile' \
		--exclude 'requirements.txt' \
		--exclude 'jbfh_squema.sql' \
		--exclude 'jobfishing.db' \
		--chown=www-data:www-data \
		$(BACKEND_DIR)/ $(BACKEND_TARGET)/

frontend:
	sudo rsync -avz --delete \
		--exclude '.git/' \
		--exclude '*.md' \
		--exclude 'Makefile' \
		--chown=www-data:www-data \
		$(FRONTEND_DIR)/ $(FRONTEND_TARGET)/

venv:
	sudo rm -rf $(VENV_PATH)
	sudo -u www-data python3 -m venv $(VENV_PATH)
	sudo -u www-data $(VENV_PATH)/bin/pip install -r $(BACKEND_TARGET)/requirements.txt

restart:
	echo ">> Reiniciando serviço jobfishing..."
	sudo systemctl restart jobfishing || { echo "Erro ao reiniciar o serviço"; exit 1; }
	
logs:
	sudo journalctl -u jobfishing -e
