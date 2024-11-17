SOURCES_FOLDER = src/bechdel_test_predictor

download-data:
	python analysis/download_data.py

unit-test:
	uv run pytest tests/.

lint:
	uv run ruff check $(SOURCES_FOLDER)

deploy-service:
	docker compose up --build

build-and-push:
	sh scripts/build_and_push_images.sh

deploy-service-kubernetes:
	kubectl apply -f kubernetes/. --recursive -n bechdel-test-predictor

delete-service-kubernetes:
	kubectl delete -f kubernetes/. --recursive -n bechdel-test-predictor