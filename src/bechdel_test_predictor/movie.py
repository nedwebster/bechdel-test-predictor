from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Dict, List, Union

import pandas as pd

from bechdel_test_predictor.cast import Cast
from bechdel_test_predictor.crew import Crew
from bechdel_test_predictor.movie_db_client import MovieDbClient


@dataclass
class Movie:
    """DataClass representing a Movie object."""

    id: int
    title: str
    imdb_id: str
    budget: int
    revenue: int
    runtime: int
    popularity: float
    vote_average: float
    vote_count: int
    genres: List[Dict[str, Union[str, int]]]
    production_companies: List[Dict[str, Union[str, int]]]
    production_countries: List[Dict[str, str]]
    release_date: str
    crew: List[Crew] = field(init=False)
    cast: List[Cast] = field(init=False)

    @classmethod
    def from_dict(cls, dict_):
        class_fields = [field.name for field in fields(cls)]
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})

    def dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items()}

    def add_crew(self, crew: List[Crew]) -> None:
        self.crew = crew

    def add_cast(self, cast: List[Cast]) -> None:
        self.cast = cast


class MovieClient:
    """Class to interact with Movie objects, via the MovieDBClient and MovieProcessor."""

    def __init__(self):
        self.movie_db_client = MovieDbClient()
        self.movie_processor = MovieProcessor()

    def get_movie(self, title: str) -> Movie:
        movie_data = self.movie_db_client.get_movie(title)
        movie = Movie.from_dict(movie_data)

        crew = self._get_crew(movie.id)
        cast = self._get_cast(movie.id)
        movie.add_crew(crew)
        movie.add_cast(cast)

        return movie

    def get_processed_movie(self, title: str) -> pd.DataFrame:
        movie = self.get_movie(title)
        movie_data = self.movie_processor.process_movie(movie)
        return movie_data

    def _get_crew(self, movie_id: int) -> List[Crew]:
        crew_data = self.movie_db_client.get_crew(movie_id=movie_id)
        return [Crew.from_dict(x) for x in crew_data]

    def _get_cast(self, movie_id: int) -> List[Cast]:
        cast_data = self.movie_db_client.get_cast(movie_id=movie_id)
        return [Cast.from_dict(x) for x in cast_data]


class MovieProcessor:
    """Class to process movies into data items for ML project.

    This class takes a Movie class, which houses raw data as it is ingested from the MovieDB API, and processes
    it to match the data recieved in the training dataset.

    Note: I know this code is gross and could be re-thought and condensed, Don't be a hater.

    """

    def __init__(self):
        self.output_cols = [
            "title",
            "year",
            "imdbid",
            "tmdbId",
            "genres",
            "popularity",
            "production_companies",
            "production_countries",
            "release_date",
            "revenue",
            "vote_average",
            "vote_count",
            "cast",
            "crew",
            "budget",
            "cast_gender",
            "crew_gender",
            "cast_female_representation",
            "crew_female_representation",
        ]

    @staticmethod
    def get_names(list_of_objs: List[Dict[str, Any]]) -> List[str]:
        return [obj["name"] for obj in list_of_objs]

    def _format_genres(self, movie_data: dict) -> dict:
        movie_data["genres"] = self.get_names(movie_data["genres"])
        return movie_data

    def _format_production_companies(self, movie_data: dict) -> dict:
        movie_data["production_companies"] = self.get_names(movie_data["production_companies"])
        return movie_data

    def _format_production_countries(self, movie_data: dict) -> dict:
        movie_data["production_countries"] = self.get_names(movie_data["production_countries"])
        return movie_data

    def _get_year(self, movie_data: dict) -> dict:
        movie_data["year"] = int(movie_data["release_date"][:4])

        # reformat release date from YYYY-MM-DD to DD/MM/YYYY
        split_data = movie_data["release_date"].split("-")
        split_data.reverse()
        movie_data["release_date"] = "/".join(split_data)
        return movie_data

    def _get_crew_gender(self, movie_data: dict) -> dict:
        movie_data["crew_gender"] = [crew["gender"] for crew in movie_data["crew"]]
        movie_data["crew_female_representation"] = (
            len([x for x in movie_data["crew_gender"] if x == 1]) / len(movie_data["crew_gender"])
        ) * 100
        return movie_data

    def _get_cast_gender(self, movie_data: dict) -> dict:
        movie_data["cast_gender"] = [cast["gender"] for cast in movie_data["cast"]]
        movie_data["cast_female_representation"] = (
            len([x for x in movie_data["cast_gender"] if x == 1]) / len(movie_data["cast_gender"])
        ) * 100
        return movie_data

    def _rename_col(self, movie_data: dict, old_name: str, new_name: str) -> dict:
        movie_data[new_name] = movie_data[old_name]
        return movie_data

    def process_movie(self, movie: Movie) -> pd.DataFrame:
        movie_data = movie.dict()

        movie_data = self._format_genres(movie_data)
        movie_data = self._format_production_companies(movie_data)
        movie_data = self._format_production_countries(movie_data)
        movie_data = self._get_year(movie_data)
        movie_data = self._get_crew_gender(movie_data)
        movie_data = self._get_cast_gender(movie_data)
        movie_data = self._rename_col(movie_data, "id", "tmdbId")
        movie_data = self._rename_col(movie_data, "imdb_id", "imdbid")

        output_dict = {}
        for col in self.output_cols:
            if isinstance(movie_data[col], list):
                output_dict[col] = json.dumps(movie_data[col])
            else:
                output_dict[col] = movie_data[col]

        return pd.DataFrame(output_dict, index=[0])
