"""MC15: in air treated as an ideal gas, v_rms(O2)/v_rms(N2) = sqrt(28/32) = (7/8)^(1/2) (answer 3). Adapted: any two gases at one temperature; ratio sqrt(M_other / M_asked)."""

from math import sqrt

GAS_CONSTANT = 8.314


def solve(asked=32, other=28):
    return sqrt(other / asked)


def check(asked=32, other=28, temperature=300):
    # Absolute rms speeds from (3RT/M), molar masses in kg/mol, then the ratio.
    speed = lambda molar: sqrt(3 * GAS_CONSTANT * temperature / (molar / 1000))
    return speed(asked) / speed(other)


PARAMS = {"asked": 32, "other": 28}
VARIANTS = [{"asked": 4, "other": 16}, {"asked": 44, "other": 2}, {"asked": 2, "other": 32}]
ANSWER = 0.9354143466934853
