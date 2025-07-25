from src.scraper.base import BaseScraper
from src.entities.movies import Movie, Actor


class BfspRequestScraper:
    def __init__(self, scraper: BaseScraper):
        self.scraper = scraper

    def get_movies(self, base_url: str):
        movies = self.scraper.get_data(base_url).get("itemListElement", [])

        for movie in movies:
            if movie.get("item"):
                pass
