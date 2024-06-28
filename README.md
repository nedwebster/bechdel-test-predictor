![Bechdel Test](docs/diagrams/bechdel_test.png)

# bechdel-test-predictor
This repo contains an ML model for predicting whether a film will pass or fail the [Bechdel test](https://en.wikipedia.org/wiki/Bechdel_test). The `src/bechdel_test_predictor/` directory contains code to train the ML model, as well as code to serve the model. The `services/` directory contains the multiple services used to deploy and orchestrate the inference service, including an Mlflow server, a PSQL database, and a Flask frontend. The `analysis/` folder contains the notebooks for the model development.

## Downloading Data for Analysis
The repo uses [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master) to download the training data. The package requires a `kaggle.json` file within the root directory of this project. Follow steps in the opendatasets `README.md` to generate your own `kaggle.json` if needed.

Then run the following command to download the data:
```sh
make download-data
```

## Local Deployment
The model can be deployed via a flask app (and it's supporting services) through docker and docker-compose:
### Setup Infrastructure
To deploy the required infrastructure for the inference service, run the following command
```sh
make init-infra
```
This will do four things:
1. Deploy the PSQL database in a docker container
2. Download the training data from [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master), and ingests it into the PSQL database as the `movies` table. This is to simulate the standard use-case scenario of having data stored in SQL at model training time.
3. Deploy the Mlflow instance in a docker container, using the PSQL database as it's artifact storage.
4. Deploy the flask app. If no model exists in Mlflow, the app will not deploy and will endlessly retry to find a model. As soon as a model is trained, the app will deploy fully and the url will be available.

For more details, check out the [system_architecture](https://github.com/nedwebster/bechdel-test-predictor/blob/main/docs/system_architecture.md) docs.

### Train Model
To train a new version of the model, run the following command
```sh
make train-model
```
This will run the model training pipeline as a standalone task in it's own docker container. The model will be registered to the Mlflow model registry.

You can access the deployed app by going to `http://localhost:5000`, and you can check the mlflow server by going to `http://localhost:5001`. To run successfully, you need the `kaggle.json` file in the root directory, as specified in the section above. You also need a `.env` file in the root directory, containing the environment variables listed in the section below.


## Environment Variables
- `TMDB_API_TOKEN`: In order to access TheMovieDB api, the `TMDB_API_TOKEN` env var needs to be set. To generate your own token, you can follow the steps in this guide: https://www.educative.io/courses/movie-database-api-python/set-up-the-credentials. The `TMDB_API_TOKEN` is the `API Read Access Token` assigned to your TheMovieDB account.
- `DB_CONNECTION_STRING`: In order for the python tasks to acces the PSQL database, the `DB_CONNECTION_STRING` needs to be set. When running this app locally, the value should be set to `postgresql://postgres:postgres123@postgres-db:5432/postgres`
- `USERNAME`: Metaflow requires a username to be set in order to run its workflows. This can be set to anything you want.

## Tests
`bechdel-test-predictor` uses pytest to run the unit tests. To run the unit tests, use the following command:
```sh
make unit-test
```