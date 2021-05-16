dockerrun:
	docker-compose down --rmi all --volumes
	docker-compose down && docker-compose up