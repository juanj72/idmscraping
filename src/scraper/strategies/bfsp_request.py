from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper
from src.scraper.dowloader import DownloaderHelper
from src.scraper.parser import parse_json_ld


class BfspRequestScraper(BaseScraper):
    def __init__(self, downloader: DownloaderHelper):
        self.downloader = downloader

    # def get_movies(self) -> str:
    #     html_content = self.downloader.get_html(self.url)

    #     soup = BeautifulSoup(html_content, "html.parser")
    #     movies = []

    #     movie_items = soup.find_all("li", class_="ipc-metadata-list-summary-item")

    #     for item in movie_items:
    #         try:
    #             movie_data = {}

    #             # Título de la película
    #             title_element = item.find("h3", class_="ipc-title__text")
    #             if title_element:
    #                 title_text = title_element.get_text(strip=True)
    #                 # Extraer el ranking y el título
    #                 if ". " in title_text:
    #                     ranking, title = title_text.split(". ", 1)
    #                     movie_data["ranking"] = ranking
    #                     movie_data["title"] = title
    #                 else:
    #                     movie_data["title"] = title_text

    #             # URL de la película
    #             title_link = item.find("a", class_="ipc-title-link-wrapper")
    #             if title_link:
    #                 movie_data["url"] = "https://www.imdb.com" + title_link.get(
    #                     "href", ""
    #                 )

    #             # Año de lanzamiento
    #             year_element = item.find("span", class_="sc-15ac7568-7")
    #             if year_element:
    #                 movie_data["year"] = year_element.get_text(strip=True)

    #             # Rating
    #             rating_element = item.find("span", class_="ipc-rating-star--rating")
    #             if rating_element:
    #                 movie_data["rating"] = rating_element.get_text(strip=True)

    #             # Número de votos
    #             votes_element = item.find("span", class_="ipc-rating-star--voteCount")
    #             if votes_element:
    #                 votes_text = votes_element.get_text(strip=True)
    #                 # Limpiar el texto de votos (ej: "(2.5M)" -> "2.5M")
    #                 movie_data["votes"] = votes_text.strip("()")

    #             # Clasificación (R, PG-13, etc.)
    #             rating_cert = item.find("span", class_="sc-15ac7568-7")
    #             if rating_cert:
    #                 movie_data["certification"] = rating_cert.get_text(strip=True)

    #             # Solo agregar películas con datos válidos
    #             if movie_data.get("title"):
    #                 movies.append(movie_data)

    #         except Exception as e:
    #             print(f"Error parsing movie item: {e}")
    #             continue

    #     return movies
    def _get_json(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        script_element = soup.find("script", type="application/ld+json")

        if script_element:
            return parse_json_ld(script_element.string) # type: ignore
        return {}

    def get_data(self, url: str) -> dict:
        html_content = self.downloader.get_html(url)
        return self._get_json(html_content)
