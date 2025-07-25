import json
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper

if __name__ == "__main__":
    downloader = DownloaderHelper()
    url = "https://www.imdb.com/chart/top/"
    scraper = BfspRequestScraper(downloader, url)
    movies = scraper.get_movies()
    with open("movies.json", "w") as file:
        json.dump(movies, file, ensure_ascii=False, indent=4)