"""Source p12, MC44: 240 g LiOH absorbs 5 mol CO2, about 205 L (ค)."""

from decimal import Decimal, ROUND_HALF_UP


def solve(lioh_g=240, pressure_atm=1.0, temperature_k=500):
    # 2LiOH + CO2 -> Li2CO3 + H2O; M(LiOH)=24 g/mol.
    co2_mol = Decimal(str(lioh_g)) / Decimal(48)
    volume = co2_mol * Decimal("0.082") * Decimal(str(temperature_k)) / Decimal(str(pressure_atm))
    return int(volume.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def check(lioh_g=240, pressure_atm=1.0, temperature_k=500):
    lithium_moles = lioh_g / (7 + 16 + 1)
    carbon_dioxide_moles = lithium_moles / 2
    return round(carbon_dioxide_moles * 0.082057 * temperature_k / pressure_atm)


PARAMS = {"lioh_g": 240, "pressure_atm": 1.0, "temperature_k": 500}
VARIANTS = [
    {"lioh_g": 96, "pressure_atm": 1.0, "temperature_k": 500},
    {"lioh_g": 144, "pressure_atm": 1.0, "temperature_k": 400},
    {"lioh_g": 192, "pressure_atm": 2.0, "temperature_k": 700},
]
ANSWER = 205
