![Bechdel Test](docs/diagrams/bechdel_test.png)

# bechdel-test-predictor
This repo contains an ML model for predicting whether a film will pass or fail the [Bechdel test](https://en.wikipedia.org/wiki/Bechdel_test). The `src/bechdel_test_predictor/` directory contains code to train the ML model, as well as code to serve the model. The `services/` directory contains the multiple services used to deploy and orchestrate the inference service, including an Mlflow server, a PSQL database, and a Flask frontend. The `analysis/` folder contains the notebooks for the model development.

## Downloading Data for Analysis and Model Development
The repo uses [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master) to download the training data. The package requires a `kaggle.json` file within the root directory of this project. Follow steps in the opendatasets `README.md` to generate your own `kaggle.json` if needed.

Then run the following command to download the data:
```sh
make download-data
```

## Local Deployment - Docker Compose
The model can be deployed via a flask app (and it's supporting services) through docker and docker-compose. Before running this, make sure you have defined the required environment variables listed in the section below, and then run:
```sh
make deploy-service
```

This will deploy/run the following services:
1. `postgres-db`: Deploy the PSQL database in a docker container
2. `mlflow-server`: Deploy the Mlflow instance in a docker container, using the PSQL database as it's artifact storage.
3. `init-data`: Download the training data from [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master), and ingest it into the PSQL database as the `movies` table. This is to simulate a standard use-case scenario of having data stored in SQL at model training time.
4. `cleanup-mlflow`: Clear the mlflow data and metadata, in case anything had been persisted from the previous initialisation.
5. `train-model`: Train the machine learning model and register it in the mlflow model registry.
6. `bechdel-flask-app`: Deploy the flask app.

You can access the deployed app by going to `http://localhost:5000`, and you can check the mlflow server by going to `http://localhost:5001`. For more details, check out the [system_architecture](https://github.com/nedwebster/bechdel-test-predictor/blob/main/docs/system_architecture.md) docs.

## Local Deployment - Kubernetes
The model can also be deployed through kubernetes. This requires a running Kubernetes cluster. For local development, [Minikube](https://minikube.sigs.k8s.io/) is a good option, go to their docs and follow their setup guide. Kubernetes deployment also requires the environment variables listed below to be set. To deploy the app to kubernetes, make sure you have a Kubernetes cluster running on your machine, and then run the following make command:
```sh
make deploy-service-kubernetes
```

Once deployed, you can view the app by forwarding the exposed port to a port on your local host. To do this, run:
```sh
kubectl port-forward <name-of-flask-pod> 5000:5000
```


## Environment Variables
- `TMDB_API_TOKEN`: In order to access TheMovieDB api, the `TMDB_API_TOKEN` env var needs to be set. To generate your own token, you can follow the steps in this guide: https://www.educative.io/courses/movie-database-api-python/set-up-the-credentials. The `TMDB_API_TOKEN` is the `API Read Access Token` assigned to your TheMovieDB account.
- `DB_CONNECTION_STRING`: In order for the python tasks to acces the PSQL database, the `DB_CONNECTION_STRING` needs to be set. When running this app locally, the value should be set to `postgresql://postgres:postgres123@postgres-db:5432/postgres`
- `USERNAME`: Metaflow requires a username to be set in order to run its workflows. This can be set to anything you want.
- `KAGGLE_USERNAME`: This is the same username defined in the `kaggle.json` described above. The kaggle credentials are passed as environment variables to prevent hardcoded secrets being pushed to docker hub.
- `KAGGLE_KEY`: This is the same key defined in the `kaggle.json` described above. The kaggle credentials are passed as environment variables to prevent hardcoded secret files being pushed to docker hub.

## Tests
`bechdel-test-predictor` uses pytest to run the unit tests. To run the unit tests, use the following command:
```sh
make unit-test
```