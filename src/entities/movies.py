from dataclasses import dataclass
from typing import List

@dataclass
class Actor:
    name: str

@dataclass
class Movie:
    title: str
    year: int
    qualification: str
    duration: int
    metascore: float
    actors: List[Actor]