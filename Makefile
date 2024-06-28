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
	docker compose run --no-deps --entrypoint "python train_model.py" python-tasks
