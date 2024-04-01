import os
from typing import Any, Dict, Optional

import requests

from bechdel_test_predictor.error import MovieNotFoundError
from bechdel_test_predictor.logging.utils import db_logger


class MovieDbClient:
    """Class to connect and request data using TheMovieDB API."""

    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3/"
        self._cache = {}

    def get_headers(self) -> Dict[str, str]:
        return {"accept": "application/json", "Authorization": f"Bearer {os.environ['TMDB_API_TOKEN']}"}

    def get(self, url: str, params: Optional[Dict[str, str]] = None):
        response = requests.get(url, headers=self.get_headers(), params=params)

        return response.json()

    def get_movie(self, title: str) -> Dict[str, Any]:
        """Search for the movie ID from the title string, and then return the movie data corresponding to that ID.

        Note: The data returned from the movie search request is limited, hence the request via ID is necessarry.

        """
        movie_id = self.search_movie(title=title)
        url = self.base_url + f"movie/{movie_id}"
        return self.get(url=url)

    def search_movie(self, title: str) -> int:
        """Search the MovieDB for a movie with a given title, and return it's ID if it exists."""
        url = self.base_url + "search/movie"
        params = {"query": title}
        search_results = self.get(url=url, params=params)
        if search_results["total_results"] > 0:
            movie = search_results["results"][0]
            if movie["original_title"].lower() != title.lower():
                db_logger.warn(f"Requested movie: {title}, returned movie: {movie['original_title']}")
            return movie["id"]
        else:
            error = MovieNotFoundError(title)
            db_logger.error(repr(error))
            raise error

    def get_credits(self, movie_id: int) -> Dict[str, Any]:
        """Get the credits for a given movie id."""
        if movie_id in self._cache.keys():
            credits = self._cache[movie_id]["credits"]
        else:
            url = self.base_url + f"movie/{movie_id}/credits"
            credits = self.get(url)
            self._cache[movie_id] = {"credits": credits}
        return credits

    def get_cast(self, movie_id: int) -> Dict[str, Any]:
        """Get the cast for a given movie id."""
        credits = self.get_credits(movie_id)
        return credits["cast"]

    def get_crew(self, movie_id: int) -> Dict[str, Any]:
        """Get the crew for a given movie id."""
        credits = self.get_credits(movie_id)
        return credits["crew"]
