SRC=$(shell pwd)
TARGET=/var/www/jobfishing-backend
SERVICE=jobfishing

deploy:

	sudo rsync -av --delete \
     --exclude 'venv/' \
     --exclude '.git/' \
     --exclude '.env' \
     --exclude 'scripts/' \
     $(SRC)/ $(TARGET)/
	sudo chown -R www-data:www-data $(TARGET)
	sudo systemctl restart $(SERVICE)

logs:
	sudo journalctl -u $(SERVICE) -f

status:
	sudo systemctl status $(SERVICE)
