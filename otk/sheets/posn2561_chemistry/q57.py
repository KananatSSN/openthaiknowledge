"""Source p13, MC57: molecular kinetic energy and ideal-gas limits."""


def solve(start_c=100, end_c=50, gas_a="A", gas_b="B"):
    assert start_c > end_c > -273 and gas_a != gas_b
    return 1


def check(start_c=100, end_c=50, gas_a="A", gas_b="B"):
    assert start_c > end_c > -273 and gas_a != gas_b
    pressure_ratio = (end_c + 273.15) / (start_c + 273.15)
    claims = (
        False,  # negligible particle volume does not imply zero mass
        True,  # mean translational KE = 3kT/2 for both gases
        False,  # high P and low T magnify non-ideal behavior
        abs(pressure_ratio - 2) < 1e-9,
    )
    return claims.index(True) if claims.count(True) == 1 else None


PARAMS = {"start_c": 100, "end_c": 50, "gas_a": "A", "gas_b": "B"}
VARIANTS = [
    {"start_c": 80, "end_c": 40, "gas_a": "He", "gas_b": "Ne"},
    {"start_c": 120, "end_c": 60, "gas_a": "N₂", "gas_b": "O₂"},
    {"start_c": 60, "end_c": 30, "gas_a": "CO₂", "gas_b": "He"},
]
ANSWER = 1
