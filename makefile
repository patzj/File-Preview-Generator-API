build:
	docker-compose build
freeze:
	pip freeze > requirements.txt
install:
	pip install -r requirements.txt