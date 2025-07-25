import json
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper
from src.orchestrator import BfspRequestScraper as OrchestratorBfspRequestScraper
if __name__ == "__main__":
    downloader = DownloaderHelper()
    url = "https://www.imdb.com/chart/top/?groups=top_250&count=250"
    scraper = BfspRequestScraper(downloader)
    orchestrator_scraper = OrchestratorBfspRequestScraper(scraper)
    movies = orchestrator_scraper.get_movies(url)
    print(movies)
