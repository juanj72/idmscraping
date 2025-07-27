import requests
from src.scraper.proxys.get_ip import get_ip_request
from src.scraper.proxys.get_proxys import get_random_proxy


class DownloaderHelper:
    def __init__(self, ip_rotation: bool = True):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        self.max_retries = 3
        self.ip_rotation = ip_rotation

    def get_html(self, url: str) -> str:

        for attempt in range(1, self.max_retries + 1):
            session = requests.Session()
            session.headers.update(self.headers)
            if not self.ip_rotation:
                break
            proxy = get_random_proxy()
            print(f"Attempt {attempt} with proxy: {proxy}")
            try:
                response = session.get(
                    url,
                    allow_redirects=True,
                    proxies={"http": f"{proxy}", "https": f"{proxy}"},
                    timeout=10,
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt == self.max_retries:
                    print("Max retries reached, fallback to no proxy.")
        try:
            session = requests.Session()
            session.headers.update(self.headers)
            response = session.get(
                url,
                allow_redirects=True,
                timeout=10,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            raise RuntimeError(f"Failed to fetch URL: {e}")
