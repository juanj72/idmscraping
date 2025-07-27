import json
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper
from src.orchestrator import BfspRequestScraper as OrchestratorBfspRequestScraper
import time
from src.database.crud import Crud
from src.scraper.proxys.get_proxys import fetch_proxies
from src.config import Config
from src.utils.logger import logger

if __name__ == "__main__":

    start_time = time.time()
    logger.info("Iniciando el scraper de películas de IMDB...")
    config = Config()
    logger.info(f"Configuración cargada ..")
    fetch_proxies("https") # Uncomment to fetch proxies and cache them
    logger.info("Proxies cacheados correctamente.")
    logger.info("Iniciando el downloader helper...")
    crud = Crud()
    downloader = DownloaderHelper(config)
    url = "https://www.imdb.com/chart/top/?groups=top_250&count=250"
    scraper = BfspRequestScraper(downloader)

    orchestrator_scraper = OrchestratorBfspRequestScraper(scraper, crud, 12, 0)
    movies = orchestrator_scraper.get_movies(url)
    print(movies)
    # with open("movies.json", "w") as f:
    #     f.write(json.dumps(movies, indent=4, ensure_ascii=False))
    end_time = time.time()
    logger.info(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")
