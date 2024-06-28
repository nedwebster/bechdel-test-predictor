TARGET = "bt_pass"
FEATURES = [
    "genres",
    "title",
    "revenue",
    "popularity",
    "budget",
    "vote_average",
    "vote_count",
    "cast_female_representation",
    "crew_female_representation",
    "year",
]

RANDOM_SEED = 932024
DATA_URL = "https://www.kaggle.com/datasets/vinifm/female-representation-in-cinema/"
QUERY = "select * from movies"
TEST_SIZE = 0.3
