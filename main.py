import json
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper
from src.scraper.parser import parse_json_ld

if __name__ == "__main__":
    downloader = DownloaderHelper()
    url = "https://www.imdb.com/chart/top/?groups=top_250&count=250"
    scraper = BfspRequestScraper(downloader, url)
    movies = scraper.get_movies()
    print(movies)
