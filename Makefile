SRC=$(shell pwd)
TARGET=/var/www/jobfishing-frontend

deploy:
	sudo rsync -avz --delete --exclude '.git/' $(SRC)/ $(TARGET)/
	sudo chown -R www-data:www-data $(TARGET)

logs:
	sudo journalctl -xe
