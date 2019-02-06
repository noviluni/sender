build:
	docker-compose build

up:
	docker-compose up

build-test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up
