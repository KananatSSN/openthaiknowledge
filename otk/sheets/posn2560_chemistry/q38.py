"""Source p11, MC38: combined gas law gives 0.40 L at STP (ข)."""

from decimal import Decimal, ROUND_HALF_UP


def solve(volume_l=0.40, pressure_atm=2.0, initial_celsius=273):
    initial_kelvin = Decimal(str(initial_celsius)) + Decimal("273.15")
    final_kelvin = Decimal("273.15")
    result = Decimal(str(volume_l)) * Decimal(str(pressure_atm)) * final_kelvin / initial_kelvin
    return float(result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def check(volume_l=0.40, pressure_atm=2.0, initial_celsius=273):
    # Find the amount n from the first ideal-gas state and use it at STP.
    amount_over_r = pressure_atm * volume_l / (initial_celsius + 273.15)
    return round(amount_over_r * 273.15, 2)


PARAMS = {"volume_l": 0.40, "pressure_atm": 2.0, "initial_celsius": 273}
VARIANTS = [
    {"volume_l": 0.60, "pressure_atm": 1.5, "initial_celsius": 27},
    {"volume_l": 0.80, "pressure_atm": 3.0, "initial_celsius": 127},
    {"volume_l": 1.20, "pressure_atm": 2.5, "initial_celsius": 327},
]
ANSWER = 0.40
