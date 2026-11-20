"""Theory 2.1 (a): the sealed gas keeps its volume, so P_G = P0 T1/T0. Adapted: P0 (kPa) and the temperatures (Celsius) vary; returns P_G in kPa."""


def solve(pressure=100.0, start=27.0, end=100.0):
    return pressure * (end + 273.15) / (start + 273.15)


def check(pressure=100.0, start=27.0, end=100.0, volume=1e-3, R=8.314):
    # Count the moles at the start, then the pressure they exert when hot.
    n = pressure * 1e3 * volume / (R * (start + 273.15))
    return n * R * (end + 273.15) / volume / 1e3


PARAMS = {"pressure": 100.0, "start": 27.0, "end": 100.0}
VARIANTS = [{"end": 80.0}, {"pressure": 120.0, "start": 20.0}, {"end": 150.0}]
ANSWER = 124.32117274695986
TOL = 1e-9
