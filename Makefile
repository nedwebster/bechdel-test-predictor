SOURCES_FOLDER = src/bechdel_test_predictor

download-data:
	python analysis/download_data.py

unit-test:
	pytest tests/.

lint:
	pflake8 $(SOURCES_FOLDER)
	black --check $(SOURCES_FOLDER)
	isort --check-only $(SOURCES_FOLDER)

init-infra:
	docker compose up --build

train-model:
	docker compose run --build --no-deps --entrypoint "python scripts/train_model.py run" python-tasks

cleanup-mlflow:
	docker compose run --build --no-deps --entrypoint "python scripts/cleanup_mlflow.py run" python-tasks