from dataclasses import dataclass
from typing import List


@dataclass
class Actor:
    name: str


@dataclass
class Movie:
    title: str
    year: int
    qualification: int
    duration: float
    metascore: float
    url: str
    actors: List[Actor]
