import requests
from src.scraper.proxys.get_ip import get_ip_request
from src.scraper.proxys.get_proxys import get_random_proxy
from src.config import Config
from src.utils.logger import logger


class DownloaderHelper:
    def __init__(self, config: Config):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.max_retries = 3
        self.config = config
        self.ip_rotation = config.config.get("proxy", {}).get("ip_rotation")
        
        logger.info(
            f"DownloaderHelper initialized with IP rotation: {self.ip_rotation}"
        )

    def get_html(self, url: str) -> str:

        for attempt in range(1, self.max_retries + 1):
            session = requests.Session()
            session.headers.update(self.headers)
            if not self.ip_rotation:
                break
          
            proxy_rotation = get_random_proxy()
            proxy = {
                "http": proxy_rotation,
                "https": proxy_rotation,
            }

            logger.info(f"Attempt {attempt} with proxy: {proxy}")
            try:
                response = session.get(
                    url,
                    allow_redirects=True,
                    proxies=proxy,
                    timeout=10,
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.error(f"Attempt {attempt} failed: {e}")
                if attempt == self.max_retries:
                    logger.warning("Max retries reached, fallback to no proxy.")
        try:
            session = requests.Session()
            session.headers.update(self.headers)
            logger.info(f"intentando con ip: {get_ip_request()} ")
            response = session.get(
                url,
                allow_redirects=True,
                timeout=10,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            raise RuntimeError(f"Failed to fetch URL: {e}")
