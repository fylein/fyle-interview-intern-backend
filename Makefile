build:
	docker build -t fyle_app .

run:
	docker run --name fyle -p 7755:7755 -d fyle_app

stop:
	docker stop fyle

rm:
	docker rm fyle

clean:
	docker stop fyle && docker rm fyle

purge:
	docker stop fyle && docker rm fyle && docker rmi fyle_app

update:
	docker stop fyle && docker rm fyle && docker build -t fyle_app . && docker run --name fyle -p 7755:7755 -d fyle_app

logs:
	docker logs fyle --follow

production:
	docker-compose up -d
