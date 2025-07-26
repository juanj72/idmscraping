from src.scraper.base import BaseScraper
from src.entities.movies import Movie, Actor
from typing import List
from datetime import datetime
from src.utils.dict_get import dict_get
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from threading import Lock
from dataclasses import asdict
from src.utils.convert_to_minutes import convert_duration_to_minutes_iso


class BfspRequestScraper:
    def __init__(self, scraper: BaseScraper, max_workers: int = 3, delay: float = 1.0):
        self.scraper = scraper
        self.max_workers = max_workers
        self.delay = delay  # Delay between requests
        self.lock = Lock()  # to thread-safe operations

    def _convert_to_dict(self, movies: List[Movie]) -> List[dict]:
        return [asdict(movie) for movie in movies]

    def get_movies(self, base_url: str) -> List[dict]:
        movies = self.scraper.get_data(base_url).get("itemListElement", [])

        movie_urls = [
            movie.get("item").get("url")
            for movie in movies
            if movie.get("item") and movie.get("item").get("url")
        ]

        print(f"Procesando {len(movie_urls)} películas...")

        movie_objects = []
        processed_count = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self._process_movie_with_retry, url, index): (
                    url,
                    index,
                )
                for index, url in enumerate(movie_urls)
            }

            for future in as_completed(future_to_url):
                url, index = future_to_url[future]
                try:
                    movie_obj = future.result()
                    if movie_obj:
                        movie_objects.append(movie_obj)

                    processed_count += 1

                    with self.lock:
                        print(
                            f"Progreso: {processed_count}/{len(movie_urls)} "
                            f"({processed_count/len(movie_urls)*100:.1f}%)"
                        )

                except Exception as e:
                    print(f"✗ Error en {url}: {e}")

        return self._convert_to_dict(movie_objects)
    
    def _process_movie_with_retry(  # type: ignore
        self, url_detail: str, index: int, max_retries: int = 3
    ) -> Movie:  # type: ignore

        for attempt in range(max_retries):
            try:
                # Rate limiting
                if self.delay > 0:
                    time.sleep(self.delay * (index % self.max_workers))

                detail = self.scraper.get_data(url_detail)

                actors = [
                    Actor(name=actor.get("name")) for actor in detail.get("actor", [])
                ]

                movie = Movie(
                    title=detail.get("name", "Unknown"),
                    year=self._parse_year(detail.get("datePublished", "1970-01-01")),
                    qualification=dict_get(
                        detail, ["review", "reviewRating", "worstRating"], "N/A"
                    ),
                    duration=convert_duration_to_minutes_iso(
                        detail.get("duration", "N/A")
                    ),
                    metascore=float(
                        detail.get("aggregateRating", {}).get("ratingValue", 0)
                    ),
                    url=url_detail,
                    actors=actors,
                )

                return movie

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Reintento {attempt + 1}/{max_retries} para {url_detail}")
                    time.sleep(2**attempt)  # Backoff exponencial
                else:
                    print(f"Falló después de {max_retries} intentos: {url_detail}")
                    raise e

    # TODO: move to utils
    def _parse_year(self, date_str: str) -> int:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").year
        except Exception as e:
            print(f"Error al parsear el año: {e}")
            return 1970
