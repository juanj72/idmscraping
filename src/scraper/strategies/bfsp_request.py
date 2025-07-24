import requests
from src.entities.movies import Movie
from scraper.base import BaseScraper
from typing import List

class BfspRequestScraper(BaseScraper):
    def __init__(self, url: str):
        self.url = url

    def get_movies(self) -> str:
        response = requests.get(self.url)
        response.raise_for_status()  
        movies_data = response.json()  

        movies = []
        for item in movies_data:
            movie = Movie(
                title=item['title'],
                year=item['year'],
                director=item['director'],
                genre=item['genre']
            )
            movies.append(movie)

        return movies