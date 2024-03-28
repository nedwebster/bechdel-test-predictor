# bechdel-test-predictor
This repo contains an ML model for predicting whether a film will pass or fail the [Bechdel test](https://en.wikipedia.org/wiki/Bechdel_test). The `src/bechdel_test_predictor/` directory contains code to train the ML model, as well as code to serve the model. The `services/` directory contains the multiple services used to deploy the model, including an Mlflow server, a PSQL database, and a Flask app. The `analysis/` folder contains the notebooks for the model development.

## Downloading Data
The repo uses [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master) to download the training data. The package requires a `kaggle.json` file within the root directory of this project. Follow steps in the opendatasets `README.md` to generate your own `kaggle.json` if needed.

Then run the following command to download the data:
```sh
make download-data
```

## Local Deployment
The model can be deployed via a flask app (and it's supporting services) with the `docker-compose` command (see `docs/system_architecture.md` for more detail):
```sh
docker compose up --build
```

You can access the deployed app by going to `http://localhost:5000`, and you can check the mlflow server by going to `http://localhost:5001`. To run successfully, you need the `kaggle.json` file in the root directory, as specified in the section above. You also need a `.env` file in the root directory, containing the environment variables listed in the section below.


## Environment Variables
In order to access TheMovieDB api, the `TMDB_API_TOKEN` env var needs to be set. To generate your own token, you can follow the steps in this guide: https://www.educative.io/courses/movie-database-api-python/set-up-the-credentials. The `TMDB_API_TOKEN` is the `API Read Access Token` assigned to your TheMovieDB account.


## Tests
`bechdel-test-predictor` uses pytest to run the unit tests. To run the unit tests, use the following command:
```sh
make unit-test
```