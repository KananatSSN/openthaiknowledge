"""Source p11, MC37: helium is most ideal at 750 K and 150 mmHg (ค)."""


def solve(conditions=((50, 150), (50, 4560), (750, 150), (750, 4560))):
    hottest = max(temperature for temperature, _ in conditions)
    lowest_pressure = min(pressure for _, pressure in conditions)
    matches = [i for i, pair in enumerate(conditions)
               if pair == (hottest, lowest_pressure)]
    assert len(matches) == 1
    return matches[0]


def check(conditions=((50, 150), (50, 4560), (750, 150), (750, 4560))):
    # A low-density / weak-interaction proxy: P/T is least at the desired
    # corner; the same corner also minimizes the attraction scale P/T^2.
    scores = [pressure / temperature for temperature, pressure in conditions]
    return min(range(len(conditions)), key=lambda i: scores[i])


PARAMS = {"conditions": ((50, 150), (50, 4560), (750, 150), (750, 4560))}
VARIANTS = [
    {"conditions": ((300, 760), (900, 760), (300, 152), (900, 152))},
    {"conditions": ((120, 2280), (600, 2280), (120, 76), (600, 76))},
    {"conditions": ((400, 3040), (1000, 3040), (400, 304), (1000, 304))},
]
ANSWER = 2
