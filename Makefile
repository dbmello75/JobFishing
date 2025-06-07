deploy:
	sudo rsync -avz --delete ./ /var/www/jobfishing-backend/
	sudo chown -R www-data:www-data /var/www/jobfishing-backend/
	sudo systemctl restart jobfishing
