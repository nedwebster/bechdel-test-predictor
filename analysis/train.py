"""Runs model training."""

import numpy as np
import pandas as pd
import transformers as tr
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

female_pronouns = ["she", "her", "her's", "women", "woman", "lady", "lady's"]
y_col = "bt_pass"
RANDOM_SEED = 932024

# Define Pipeline
pipeline = Pipeline(
    steps=[
        ("genre_tagging", tr.OneHotEncodeFromTags("genres")),
        ("pronoun_matching", tr.FlagIfStrContains("title", "pronouns_in_title", tokens_to_match=female_pronouns)),
        ("log", tr.LogAfterZeroReplacement(["revenue", "popularity", "budget"], zero_replacement=1)),
        (
            "drop",
            tr.ColumnDropper(
                [
                    y_col,
                    "title",
                    "bt_score",
                    "dubious",
                    "imdbid",
                    "tmdbId",
                    "genres",
                    "popularity",
                    "production_companies",
                    "production_countries",
                    "release_date",
                    "revenue",
                    "cast",
                    "crew",
                    "budget",
                    "cast_gender",
                    "crew_gender",
                ]
            ),
        ),
        ("model", RandomForestClassifier(random_state=RANDOM_SEED)),
    ]
)

if __name__ == "__main__":
    df = pd.read_csv("data/female-representation-in-cinema/movies.csv", index_col=0)
    print("Input data shape:", df.shape)

    # Drop duplicates
    n = df.shape[0]
    df = df.drop_duplicates()
    # Single remaining duplicate with different values for dubious.
    # TODO are these from different reviewers? If so keep dubious == 0
    # instead of dubious == 1
    index_to_drop = df[(df["imdbid"] == 2180411) & (df["dubious"] == 0)].index
    df = df.drop(index_to_drop, axis=0)
    print(f"{n - df.shape[0]} rows dropped as duplicates")

    # Add binary target
    df[y_col] = np.where(df["bt_score"].isin([2, 3]), 1, 0)

    # Split intro train and test
    train, test = train_test_split(df, test_size=0.3, random_state=RANDOM_SEED)
    print("Train shape:", df.shape)
    print("Test shape:", df.shape)

    # Fit pipeline
    pipeline.fit(train.copy(), train[y_col])

    # Predict
    preds = pipeline.predict_proba(test.copy())[:, 1]
    test["label_prediction"] = pipeline.predict(test.copy())
    test["prediction"] = preds

    # Evaluate
    print("===== Model Performance on Test Set =====")
    print("AUC: {0:.3f}".format(roc_auc_score(test[y_col], test["prediction"], average="weighted")))
    print("Average Precision: {0:.3f}".format(average_precision_score(test[y_col], test["prediction"])))
    print("Precision: {0:.3f}".format(precision_score(test[y_col], test["label_prediction"], average="weighted")))
    print("Recall: {0:.3f}".format(recall_score(test[y_col], test["label_prediction"], average="weighted")))
