SRC := $(shell pwd)
TARGET := /var/www/jobfishing-frontend

deploy:
	sudo rsync -a --delete \
		--info=NAME \
		--exclude '.git/' \
		--exclude '*.md' \
		--exclude 'Makefile' \
		$(SRC)/ $(TARGET)/
	sudo chown -R www-data:www-data $(TARGET)

logs:
	sudo journalctl -xe
