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

# copy environment variables to the image
COPY .env /app/

# copy every content from the local file to the image
COPY ./services/flask_app /app

ENV ENV=DOCKER

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
