"""Theory 2.7-2.9: the secondary loop gives I_L R_L = -i omega (L_L I_L + M I_S), so with V_L = I_L R_L the primary current is |I_S| = V_L sqrt(R_L^2 + omega^2 L_L^2)/(omega M R_L). Adapted: the load voltage, load resistance, secondary inductance and M (henries) vary at 50 Hz; returns amperes."""

from math import pi, sqrt


def solve(voltage=220.0, load=48.4, secondary=0.2, mutual=2.0, frequency=50.0):
    w = 2 * pi * frequency
    return voltage * sqrt(load**2 + (w * secondary) ** 2) / (w * mutual * load)


def check(voltage=220.0, load=48.4, secondary=0.2, mutual=2.0, frequency=50.0):
    w = 2 * pi * frequency
    i_load = complex(voltage / load)
    i_source = -(load + 1j * w * secondary) * i_load / (1j * w * mutual)
    return abs(i_source)


PARAMS = {"voltage": 220.0, "load": 48.4, "secondary": 0.2, "mutual": 2.0, "frequency": 50.0}
VARIANTS = [{"secondary": 0.5}, {"mutual": 5.0}, {"load": 100.0}]
ANSWER = 0.5737684223231204
TOL = 1e-9
