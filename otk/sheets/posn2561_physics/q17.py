"""MC17: closed constant-volume helium balloon; initial gauge260kPa, ambient100kPa,T27C=300K; final ambient60kPa,T-23C=250K. Final absolute300kPa, gauge240kPa. Use t+273 as source convention."""

from fractions import Fraction


def solve(gauge=260, ambient_start=100, ambient_end=60, temp_start=27, temp_end=-23):
    return Fraction((gauge + ambient_start) * (temp_end + 273), temp_start + 273) - ambient_end


def check(gauge=260, ambient_start=100, ambient_end=60, temp_start=27, temp_end=-23):
    # Same amount of gas, reconstructed independently with SI ideal-gas law.
    volume, gas_constant = 0.4, 8.3
    moles = (gauge + ambient_start) * 1000 * volume / (gas_constant * (temp_start + 273))
    lo, hi = -float(ambient_end), 10.0 * (gauge + ambient_start)
    for _ in range(100):
        trial = (lo + hi) / 2
        final_moles = (trial + ambient_end) * 1000 * volume / (gas_constant * (temp_end + 273))
        if final_moles < moles:
            lo = trial
        else:
            hi = trial
    return (lo + hi) / 2


PARAMS = {"gauge": 260, "ambient_start": 100, "ambient_end": 60, "temp_start": 27, "temp_end": -23}
VARIANTS = [{"gauge": 140}, {"ambient_end": 40}, {"temp_end": -3}]
ANSWER = Fraction(240, 1)
