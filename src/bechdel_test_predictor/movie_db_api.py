import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


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

    def search_movie(self, title: str) -> Dict[str, Any]:
        url = self.base_url + "search/movie"
        params = {"query": title}
        search_results = self.get(url=url, params=params)
        if search_results["total_results"] > 0:
            movie = search_results["results"][0]
            if movie["original_title"].lower() != title.lower():
                logger.warn(f"Requested movie: {title}, returned movie: {movie['original_title']}")
            return movie
        else:
            raise ValueError("No movie found!")

    def get_credits(self, movie_id: str) -> Dict[str, Any]:
        if movie_id in self._cache.keys():
            credits = self._cache[movie_id]["credits"]
        else:
            url = self.base_url + f"movie/{movie_id}/credits"
            credits = self.get(url)
            self._cache[movie_id] = {"credits": credits}
        return credits

    def get_cast(self, movie_id: str) -> Dict[str, Any]:
        credits = self.get_credits(movie_id)
        return credits["cast"]

    def get_crew(self, movie_id: str) -> Dict[str, Any]:
        credits = self.get_credits(movie_id)
        return credits["crew"]
