import logging
import os
import requests
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


class MovieDbClient:
    """Class to connect and request data using TheMovieDB API."""

    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3/"
        self._headers = {"accept": "application/json", "Authorization": f"Bearer {os.environ['TMDB_API_TOKEN']}"}

    def get(self, url: str, params: Optional[Dict[str, str]] = None):
        response = requests.get(url, headers=self._headers, params=params)

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
        url = self.base_url + f"movie/{movie_id}/credits"
        credits = self.get(url)
        return credits


if __name__ == "__main__":
    client = MovieDbClient()
    the_big_short = client.search_movie("The Big Short")
    credits = client.get_credits(the_big_short["id"])
