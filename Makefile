up:
	docker-compose up

build:
	docker-compose build

build-test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml up
