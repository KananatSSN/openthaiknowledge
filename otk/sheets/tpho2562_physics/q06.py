"""Theory 2.1-2.2: a load using P_L at V_L draws I = P_L/V_L, so the wire loses I^2 R_w and the ratio of wire power to load power is P_L R_w/V_L^2 = 0.207 for 1.0 kW at 220 V through 10 ohm. Adapted: the load power (kW), voltage and wire resistance vary."""


def solve(power=1.0, voltage=220.0, wire=10.0):
    return power * 1e3 * wire / voltage**2


def check(power=1.0, voltage=220.0, wire=10.0):
    # the load resistance, then the series circuit's power split
    load = voltage**2 / (power * 1e3)
    current = voltage / load
    return current**2 * wire / (current**2 * load)


PARAMS = {"power": 1.0, "voltage": 220.0, "wire": 10.0}
VARIANTS = [{"power": 2.5}, {"voltage": 110.0}, {"wire": 2.0}]
ANSWER = 0.2066115702479339
TOL = 1e-9
