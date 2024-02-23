from enum import Enum


class Results(Enum):
    GOOD = 1
    PARTIAL = 2
    BAD = 3
    SUPERIOR = 69
    INFERIOR = 420


class Categories(Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"
    HABITAT = "habitat"
    COLOR = "color"
    EVOLUTION_STAGE = "evolutionStageGen1"
    HEIGHT = "height"
    WEIGHT = "weight"
    