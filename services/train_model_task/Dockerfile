FROM python:3.10

RUN pip install poetry==1.6.1

WORKDIR /app

# copy the poetry.lock and pyproject.toml file to the image
COPY poetry.lock pyproject.toml /app/

# copy the app source code, and README.md for the poetry install command
COPY src/ /app/src/
COPY README.md /app/

# install the dependencies and packages in the requirements file
RUN poetry config virtualenvs.create false --local
RUN poetry install

# copy environment variables and config to the image
COPY kaggle.json /app/

COPY services/train_model_task/train_model.py /app/

ENV ENV=DOCKER

ENTRYPOINT ["python"]