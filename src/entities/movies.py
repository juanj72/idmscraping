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
    duration: str
    metascore: float
    actors: List[Actor]
