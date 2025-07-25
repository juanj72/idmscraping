from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def get_data(self, url: str) -> dict:
        pass
