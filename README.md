# bechdel-test-predictor


## Downloading Data
The repo uses [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master) to download the data. The package requires a `kaggle.json` file within the root directory of this project. Follow steps in the opendatasets `README.md` to generate your own `kaggle.json` if needed.

Then run the following command to download the data:
```sh
make download-data
```

## Local Flask App
There is a temporary local flask app (currently in development) which can be run with the following command from inside the `/flask_app` directory
```sh
flask run
```


## Environment Variables
In order to access TheMovieDB api, the `TMDB_API_TOKEN` env var needs to be set. To generate your own token, you can follow the steps in this guide: https://www.educative.io/courses/movie-database-api-python/set-up-the-credentials. The `TMDB_API_TOKEN` is the `API Read Access Token` assigned to your TheMovieDB account.


## Tests
`bechdel-test-predictor` uses pytest to run the unit tests. To run the unit tests, use the following command:
```sh
make unit-test
```