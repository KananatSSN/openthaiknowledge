"""Theory 2.10-2.11: the ratio of power in R_S to power in R_L is R_S (R_L^2 + omega^2 L_L^2)/(omega^2 M^2 R_L); with omega L_L >> R_L it is (R_S/R_L)(V_L/V_S)^2, and 1.00 kW at 220 V rms (R_L = 48.4 ohm) with V_S/V_L = 1000 and R_S = 10 ohm gives 2.07e-7. Adapted: the step-down ratio, load voltage, line resistance and load power (kW) vary."""


def solve(ratio=1000.0, voltage=220.0, line=10.0, power=1.0):
    load = voltage**2 / (power * 1e3)
    return line / load / ratio**2


def check(ratio=1000.0, voltage=220.0, line=10.0, power=1.0):
    # an ideal transformer: the line carries the load current over the ratio
    i_line = power * 1e3 / voltage / ratio
    return i_line**2 * line / (power * 1e3)


PARAMS = {"ratio": 1000.0, "voltage": 220.0, "line": 10.0, "power": 1.0}
VARIANTS = [{"ratio": 100.0}, {"power": 3.0}, {"line": 50.0}]
ANSWER = 2.066115702479339e-07
TOL = 1e-9
