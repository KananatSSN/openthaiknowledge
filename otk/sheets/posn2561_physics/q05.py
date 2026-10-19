"""MC5 figure: 3kg on frictionless table3m from edge; hanging2kg has2m to floor. Speed increases until hanging mass hits floor, then table block coasts. Adaptation explicitly asks maximum speed WHILE ON TABLE; later falling off an unspecified-height table is outside the source data."""

from math import sqrt
import numpy as np


def solve(table_mass=3, hanging_mass=2, height=2, edge_distance=3, g=9.8):
    if not 0 < height < edge_distance:
        raise ValueError("hanging mass must hit floor before table edge")
    return sqrt(2 * hanging_mass * g * height / (table_mass + hanging_mass))


def check(table_mass=3, hanging_mass=2, height=2, edge_distance=3, g=9.8):
    acceleration, tension = np.linalg.solve(
        [[table_mass, -1], [hanging_mass, 1]], [0, hanging_mass * g]
    )
    time = sqrt(2 * height / acceleration)
    assert tension > 0 and height < edge_distance
    return float(acceleration * time)


PARAMS = {"table_mass": 3, "hanging_mass": 2, "height": 2, "edge_distance": 3, "g": 9.8}
VARIANTS = [{"height": 1}, {"table_mass": 4}, {"hanging_mass": 1}]
ANSWER = 3.9597979746446663
