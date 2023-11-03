SOURCES_FOLDER = src/bechdel_test_predictor

download-data:
	python helpers/download_data.py

unit-test:
	pytest tests/.

lint:
	pflake8 $(SOURCES_FOLDER)
	black --check $(SOURCES_FOLDER)
	isort --check-only $(SOURCES_FOLDER)