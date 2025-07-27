
import pytest
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper


class MockDownloader:
    def __init__(self, html):
        self.html = html

    def get_html(self, url: str) -> str:
        return self.html


def test_get_json_and_metascore():
    with open("tests/scraper/sample_imdb_movie.html") as f:
        html = f.read()

    scraper = BfspRequestScraper(downloader=MockDownloader(html))
    data = scraper.get_data("https://fakeurl.com")

    assert data["@type"] == "Movie"
    assert data["name"] == "Test Movie"
    assert data["aggregateRating"]["ratingValue"] == "8.1"
    assert data["metascore"] == 87
