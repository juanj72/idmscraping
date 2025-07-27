from bs4 import BeautifulSoup
from src.scraper.base import BaseScraper
from src.scraper.dowloader import DownloaderHelper
from src.scraper.parser import parse_json_ld
import re


class BfspRequestScraper(BaseScraper):
    def __init__(self, downloader: DownloaderHelper):
        self.downloader = downloader

    def _get_json(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        script_element = soup.find("script", type="application/ld+json")

        if script_element:
            return parse_json_ld(script_element.string)  # type: ignore
        return {}

    def get_data(self, url: str) -> dict:
        html_content = self.downloader.get_html(url)
        if not html_content:
            raise ValueError("No HTML content found")
        data_json = self._get_json(html_content)
        data_json["metascore"] = self._get_metascore_from_html(html_content)
        return data_json

    def _get_metascore_from_html(self, html: str) -> int | None:

        soup = BeautifulSoup(html, "html.parser")

        # Buscar el span específico con la clase metacritic-score-box
        metascore_element = soup.find("span", class_="metacritic-score-box")

        if metascore_element:
            score_text = metascore_element.get_text(strip=True)
            # Extraer solo los números del texto
            match = re.search(r"\d+", score_text)
            if match:
                return int(match.group())

        # Fallback: buscar por otras clases posibles
        fallback_selectors = [
            'span[class*="metacritic-score"]',
            ".sc-9fe7b0ef-0.hDuMnh",
            "span.metacritic-score-box",
        ]

        for selector in fallback_selectors:
            element = soup.select_one(selector)
            if element:
                score_text = element.get_text(strip=True)
                match = re.search(r"\d+", score_text)
                if match:
                    return int(match.group())

        return None

    def get_metascore(self, url: str) -> int | None:
        html_content = self.downloader.get_html(url)
        return self._get_metascore_from_html(html_content)
