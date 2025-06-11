.PHONY: backend frontend deploy-backend deploy-frontend deploy-all venv restart logs status
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
	sudo rsync -avz ./jobfishing.us.conf /etc/apache2/sites-available/jobfishing.us.conf
	sudo rsync -avz ./jobfishing.service  /etc/systemd/system/jobfishing.service
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
	[ -f $(BACKEND_TARGET)/requirements.txt ] && \
		sudo -u www-data $(VENV_PATH)/bin/pip install -r $(BACKEND_TARGET)/requirements.txt || \
	echo ">> requirements.txt não encontrado ainda no destino."

restart:
	echo ">> Reiniciando serviço JobFishing e Apache..."
	sudo systemctl restart jobfishing || { echo "Erro ao reiniciar o serviço"; exit 1; }
	sudo systemctl reload apache2
logs:
	sudo journalctl -u jobfishing -e

status:
	sudo systemctl status jobfishing
