SOURCES_FOLDER = src/bechdel_test_predictor

download-data:
	python analysis/download_data.py

unit-test:
	pytest tests/.

lint:
	pflake8 $(SOURCES_FOLDER)
	black --check $(SOURCES_FOLDER)
	isort --check-only $(SOURCES_FOLDER)

deploy-service:
	docker compose up --build

deploy-service-kubernetes:
	kubectl apply -f kubernetes/. --recursive -n bechdel-test-predictor

delete-service-kubernetes:
	kubectl delete -f kubernetes/. --recursive -n bechdel-test-predictor