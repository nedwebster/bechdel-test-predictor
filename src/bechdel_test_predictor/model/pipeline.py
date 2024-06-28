from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

import bechdel_test_predictor.model.transformers as tr
from bechdel_test_predictor.model.settings import RANDOM_SEED

female_pronouns = ["she", "her", "her's", "women", "woman", "lady", "lady's"]


def get_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("genre_tagging", tr.OneHotEncodeFromTags("genres")),
            ("pronoun_matching", tr.FlagIfStrContains("title", "pronouns_in_title", tokens_to_match=female_pronouns)),
            ("log", tr.LogAfterZeroReplacement(["revenue", "popularity", "budget"], zero_replacement=1)),
            (
                "drop",
                tr.ColumnDropper(
                    [
                        "title",
                        "genres",
                        "popularity",
                        "revenue",
                        "budget",
                    ]
                ),
            ),
            ("model", RandomForestClassifier(random_state=RANDOM_SEED)),
        ]
    )
