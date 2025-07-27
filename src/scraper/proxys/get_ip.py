import requests
from src.utils.logger import logger

def get_ip_request(proxy: str | None = None) -> str | None:
    try:
        if proxy:
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
        else:   
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            response.raise_for_status()
            logger.info(f"IP obtenida: {response.json().get('ip')}")

            return response.json().get("ip")
    except Exception as e:
        logger.error(f"Error al obtener IP: {e}")
        return None
