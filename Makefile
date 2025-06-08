BACKEND_DIR=./backend
FRONTEND_DIR=./frontend
BACKEND_TARGET=/var/www/jobfishing-backend
FRONTEND_TARGET=/var/www/jobfishing-frontend
VENV_PATH=/var/www/jobfishing-venv

deploy-backend:
	sudo rsync -avz --delete \
		--exclude '.git/' \
		--exclude '*.md' \
		--exclude 'Makefile' \
		$(BACKEND_DIR)/ $(BACKEND_TARGET)/
	sudo chown -R www-data:www-data $(BACKEND_TARGET)

deploy-frontend:
	sudo rsync -avz --delete \
		--exclude '.git/' \
		--exclude '*.md' \
		--exclude 'Makefile' \
		$(FRONTEND_DIR)/ $(FRONTEND_TARGET)/
	sudo chown -R www-data:www-data $(FRONTEND_TARGET)

deploy-all: deploy-backend deploy-frontend

venv:
	sudo rm -rf $(VENV_PATH)
	sudo -u www-data python3 -m venv $(VENV_PATH)
	sudo -u www-data $(VENV_PATH)/bin/pip install -r $(BACKEND_TARGET)/requirements.txt

restart:
	sudo systemctl restart jobfishing

logs:
	sudo journalctl -u jobfishing -e
