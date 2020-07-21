
server:
	./main.sh all

stop:
	./main.sh kill

docker:
	COMPOSE_HTTP_TIMEOUT=100 sudo docker-compose -f docker-compose.yaml up --force-recreate