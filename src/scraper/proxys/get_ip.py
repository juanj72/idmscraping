import requests


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
            return response.json().get("ip")
    except Exception as e:
        print(f"Error al obtener IP: {e}")
        return None
