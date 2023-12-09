import pytest

import pandas as pd

from bechdel_test_predictor.movie import Movie, MovieProcessor
from bechdel_test_predictor.cast import Cast
from bechdel_test_predictor.crew import Crew


@pytest.fixture
def movie():
    movie = Movie(
        id=123,
        title="dummy_movie",
        imdb_id="abcd",
        budget=9001,
        revenue=666,
        runtime=100,
        popularity=1,
        vote_average=0.8,
        vote_count=10,
        genres=[{"id": 1, "name": "genre1"}, {"id": 2, "name": "genre2"}],
        production_companies=[{"id": 1, "name": "prodcomp1"}, {"id": 2, "name": "prodcomp2"}],
        production_countries=[{"name": "country1"}, {"name": "country2"}],
        release_date="1993-09-27",
    )

    movie.add_crew([
        Crew(**{"id": 1, "gender": 1, "popularity": 0.5}),
        Crew(**{"id": 2, "gender": 2, "popularity": 0.7}),
    ])
    movie.add_cast([
        Cast(**{"id": 1, "gender": 0, "popularity": 0.3}),
        Cast(**{"id": 2, "gender": 2, "popularity": 0.2}),
    ])

    return movie


@pytest.fixture
def expected_processed_movie():
    processed_movie = pd.DataFrame({
        "title": "dummy_movie",
        "year": 1993,
        "imdbid": "abcd",
        "tmdbId": 123,
        "genres": '["genre1", "genre2"]',
        "popularity": 1,
        "production_companies": '["prodcomp1", "prodcomp2"]',
        "production_countries": '["country1", "country2"]',
        "release_date": "27/09/1993",
        "revenue": 666,
        "vote_average": 0.8,
        "vote_count": 10,
        "cast": '[{"id": 1, "gender": 0, "popularity": 0.3}, {"id": 2, "gender": 2, "popularity": 0.2}]',
        "crew": '[{"id": 1, "gender": 1, "popularity": 0.5}, {"id": 2, "gender": 2, "popularity": 0.7}]',
        "budget": 9001,
        "cast_gender": "[0, 2]",
        "crew_gender": "[1, 2]",
        "cast_female_representation": 0.0,
        "crew_female_representation": 50.0,
    }, index=[0])

    return processed_movie


def test_process_movie(movie, expected_processed_movie):
    processor = MovieProcessor()
    processed_movie = processor.process_movie(movie)

    pd.testing.assert_frame_equal(processed_movie, expected_processed_movie)
