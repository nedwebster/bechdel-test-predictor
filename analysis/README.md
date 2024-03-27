# Analysis

This directory contains notebooks and scripts for data exploration and training of the ML model behind `bechdel-test-predictor`.

The notebooks provide some context on the modelling decisions, e.g. conversion of the categorical Bechedel Score to a binary target.

Preprocessing transformers are stored in `transformers.py` and `train.py` fits a simple Random Forest Classifier to predict whether a movie will pass or fail the test. This can be run from the root directory:

```
python train.py
```