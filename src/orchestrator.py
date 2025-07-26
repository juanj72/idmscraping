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
from src.database.crud import Crud


class BfspRequestScraper:
    def __init__(
        self,
        scraper: BaseScraper,
        crud: Crud,
        max_workers: int = 3,
        delay: float = 1.0,
    ):
        self.scraper = scraper
        self.max_workers = max_workers
        self.delay = delay  # Delay between requests
        self.lock = Lock()  # to thread-safe operations
        self.crud = crud

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

        return movie_objects

    def _save_movie(self, movie: Movie) -> dict:
        try:
            movie_dict = self.crud.addMovie(movie)
            if isinstance(movie_dict, str):
                print(f"Error al guardar la película {movie.title}: {movie_dict}")
                return {"error": movie_dict}

            actors = self._save_actors(movie.actors)
            if isinstance(actors, str):
                print(f"Error al guardar los actores de {movie.title}: {actors}")
                return {"error": actors}

            for actor in actors:
                self.crud.addActorToMovie(movie_dict.get("id"), actor.get("id"))

            return movie_dict

        except Exception as e:
            print(f"Error inesperado al guardar la película {movie.title}: {e}")
            return {"error": str(e)}

    def _save_actors(self, actors: List[Actor]) -> List[dict] | str:
        actor_list = []
        try:
            for a in actors:
                actor_dict = self.crud.getActor(a.name)
                if isinstance(actor_dict, str):  # si hubo error
                    return actor_dict  # corto circuito

                if actor_dict is None:  # actor no existe, se crea
                    actor_dict = self.crud.addActor(a)
                    if isinstance(actor_dict, str):
                        return actor_dict

                actor_list.append(actor_dict)

            return actor_list
        except Exception as e:
            print(f"Error al guardar actor {a.name}: {e}")
            return str(e)

    def _exists_movie(self, url: str) -> bool:
        movie = self.crud.getMovieByUrl(url)

        # Si movie es string, es un error
        if isinstance(movie, str):
            print(f"Pelicula no existe, se procede a guardar: {movie}")
            return False

        return movie is not None

    def _process_movie_with_retry(  # type: ignore
        self, url_detail: str, index: int, max_retries: int = 3
    ) -> dict:  # type: ignore

        if self._exists_movie(url_detail):
            print(f"✓ Película ya existe, se omite: {url_detail}")
            return None

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
                        detail, ["aggregateRating", "ratingValue"], 0
                    ),
                    duration=convert_duration_to_minutes_iso(
                        detail.get("duration", "")
                    ),
                    metascore=float(dict_get(detail, ["metascore"])),
                    url=url_detail,
                    actors=actors,
                )
                movie = self._save_movie(movie)

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
