"""Source p10, MC36: Charles's law gives 96.6 cm^3 (choice ข)."""

from decimal import Decimal, ROUND_HALF_UP


def solve(initial_volume=100, initial_celsius=20, final_celsius=10):
    kelvin_initial = Decimal(str(initial_celsius)) + Decimal("273.15")
    kelvin_final = Decimal(str(final_celsius)) + Decimal("273.15")
    value = Decimal(str(initial_volume)) * kelvin_final / kelvin_initial
    return float(value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def check(initial_volume=100, initial_celsius=20, final_celsius=10):
    # Calculate nR/P from the initial state, then the final volume from PV=nRT.
    gas_factor = initial_volume / (initial_celsius + 273.15)
    return round(gas_factor * (final_celsius + 273.15), 1)


PARAMS = {"initial_volume": 100, "initial_celsius": 20, "final_celsius": 10}
VARIANTS = [
    {"initial_volume": 120, "initial_celsius": 30, "final_celsius": 0},
    {"initial_volume": 150, "initial_celsius": 25, "final_celsius": 45},
    {"initial_volume": 200, "initial_celsius": 0, "final_celsius": 40},
]
ANSWER = 96.6
