import requests
from scraper.base import BaseScraper


class BfspRequestScraper(BaseScraper):
    def __init__(self, url: str):
        self.url = url

    def get_movies(self) -> str:
        try:
            response = requests.get(self.url)
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch movies: {e}")
