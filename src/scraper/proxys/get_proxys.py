import requests
import random
import pandas as pd
from src.utils.logger import logger

path_exported = "proxies_cache.csv"

def fetch_proxies(proxy_type="https") -> list[str]:
    url = f"https://www.proxy-list.download/api/v1/get?type={proxy_type}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = response.text.strip().split('\r\n')
        data = pd.DataFrame(proxies, columns=["proxy"])
        data.to_csv(path_exported, index=False, mode='w', header=False)
        return proxies
    except Exception as e:
        logger.error(f"Error al obtener proxies: {e}")
        return []


def get_random_proxy() -> str | None:
    proxies = pd.read_csv(path_exported, header=None, names=["proxy"])["proxy"].tolist()
    if proxies:
        proxy = random.choice(proxies)
        logger.info(f"Proxy aleatorio seleccionado: {proxy}")
        return proxy
    return None

# # Ejemplo de uso:
# random_proxy = get_random_proxy("http")
# print(f"Proxy aleatorio: {random_proxy}")