# bechdel-test-predictor


## Downloading Data
The repo uses [opendatasets](https://github.com/JovianHQ/opendatasets/tree/master) to download the data. The package requires a `kaggle.json` file within the root directory of this project. Follow steps in the opendatasets `README.md` to generate your own `kaggle.json` if needed.

Then run the following command to download the data:
```sh
make download-data
```


## Tests
`bechdel-test-predictor` uses pytest to run the unit tests. To run the unit tests, use the following command:
```sh
make unit-test
```