build:
	docker-compose build
start:
	docker-compose up -d
stop:
	docker-compose down
freeze:
	pip freeze > requirements.txt
install:
	pip install -r requirements.txt