from abc import ABC, abstractmethod



class BaseScraper(ABC):

    @abstractmethod
    def get_movies(self) -> str:
        pass