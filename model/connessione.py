from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Connessione:
    v0: Airport
    v1: Airport
    n: int
