import requests


class DownloaderHelper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def get_html(self, url: str) -> str:
        session = requests.Session()
        session.headers.update(self.headers)
        try:
            response = session.get(
                url, allow_redirects=True, timeout=30
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch movies: {e}")
