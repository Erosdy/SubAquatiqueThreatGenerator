import math
from enum import Enum


class GrowthMode(Enum):
    LINEAR = "linear"
    SIGMOIDAL = "sigmoïdal"
    EXPONENTIEL = "exponentiel"


def linear_growth(x, a, b) -> float:
    if a == 0:
        return 0
    if x <= a:
        return x / a
    elif b >= x > a:
        return 1
    elif x > b:
        return (1 - x) / (1 - b)
    else:
        return 0


def simgmoidal_growth(x, a, b) -> float:
    if a == 0:
        return 0
    if x <= a:
        return 1 / (1 + math.exp(-10 * (x / a - 0.5)))
    elif b >= x > a:
        return 1
    elif x > b:
        return 1 - (1 / (1 + math.exp(-10 * ((x - b) / (1 - b) - 0.5))))
    else:
        return 0


def exponentiel_growth(x, a, b):
    if a == 0:
        return 0
    if x <= a:
        return (math.exp(x / a) - 1) / (math.exp(1) - 1)
    elif b >= x > a:
        return 1
    elif x > b:
        return (math.exp((1 - x) / (1 - b)) - 1) / (math.exp(1) - 1)
    else:
        return 0


def compute_growth(x, mode, a, b) -> float:
    """
    Définit une croissance de 0 à A, une croissance stable de A à B et une décroissance de B à 1.
    """
    x = max(0.0, min(x, 1.0))
    if mode == GrowthMode.LINEAR:
        return linear_growth(x, a, b)
    elif mode == GrowthMode.SIGMOIDAL:
        return simgmoidal_growth(x, a, b)
    elif mode == GrowthMode.EXPONENTIEL:
        return exponentiel_growth(x, a, b)

    return 0
