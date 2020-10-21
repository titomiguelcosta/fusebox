lint:
	flake8

lintstats:
	flake8 --statistics --count -qq

lintfix:
	autopep8 --aggressive -i -r --max-line-length=100 fusebox

.PHONY: docs
docs:
	apidoc --template docs/template/template/ -i meterping/http/ -o docs/api/v1/

.PHONY: tests
tests:
	cd fusebox && python manage.py test --noinput

.PHONY: predictions
predictions:
	cd fusebox && python manage.py slack_predict

.PHONY: jupyter
jupyter:
	jupyter notebook fusebox/api/machinelearning/fusebox.ipynb

.PHONY: docker-build
docker-build:
	docker build -t titomiguelcosta/fusebox -f Dockerfile .

.PHONY: docker-run
docker-run:
	docker-compose up

.PHONY: push
docker-push:
	docker push titomiguelcosta/fusebox:latest

.PHONY: deploy
deploy:
	 php dep deploy dev
