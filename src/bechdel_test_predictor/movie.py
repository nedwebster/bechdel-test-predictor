from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any, Dict, List

from bechdel_test_predictor.movie_db_client import MovieDbClient
from bechdel_test_predictor.cast import Cast
from bechdel_test_predictor.crew import Crew


@dataclass
class Movie:
    id: int
    title: str
    budget: int
    revenue: int
    runtime: int
    popularity: float
    vote_average: float
    vote_count: int
    genres: List[str]
    year: int
    crew: List[Crew] = field(init=False)
    cast: List[Cast] = field(init=False)

    @classmethod
    def from_dict(cls, dict_):
        class_fields = [field.name for field in fields(cls)]
        return cls(**{k: v for k, v in dict_.items() if k in class_fields})

    def add_crew(self, crew: List[Crew]) -> None:
        self.crew = crew

    def add_cast(self, cast: List[Cast]) -> None:
        self.cast = cast


class MovieClient:

    def __init__(self):
        self.movie_db_client = MovieDbClient()

    def get_movie(self, title: str) -> Movie:
        movie_data = self.movie_db_client.get_movie(title)
        movie_data = self._clean_movie_data(movie_data)

        movie = Movie.from_dict(movie_data)

        crew = self._get_crew(movie.id)
        cast = self._get_cast(movie.id)

        movie.add_crew(crew)
        movie.add_cast(cast)

        return movie

    def _get_crew(self, movie_id: int) -> List[Crew]:
        crew_data = self.movie_db_client.get_crew(movie_id=movie_id)
        return [Crew.from_dict(x) for x in crew_data]

    def _get_cast(self, movie_id: int) -> List[Cast]:
        cast_data = self.movie_db_client.get_cast(movie_id=movie_id)
        return [Cast.from_dict(x) for x in cast_data]

    def _clean_movie_data(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        movie_data["genres"] = [genre["name"] for genre in movie_data["genres"]]
        movie_data["year"] = int(movie_data["release_date"][:4])

        return movie_data