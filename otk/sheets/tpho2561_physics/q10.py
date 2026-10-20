"""Theory 2.5: dividing m g = I N 2 pi r B_r by V = 2 pi r N B_r u removes the coil and the field, m = V I/(u g). Adapted: V (mV), I (A), u (mm/s) and g vary; returns m in kg."""


def solve(voltage=400.0, current=1.928, speed=78.54, g=9.8122567):
    return voltage * 1e-3 * current / (speed * 1e-3 * g)


def check(voltage=400.0, current=1.928, speed=78.54, g=9.8122567):
    # Power balance (the watt in the watt balance): the mechanical power m g u
    # equals the electrical V I; bisect m.
    from otk.sheets.tpho2561_physics._shared import bisect

    return bisect(lambda m: m * g * speed * 1e-3 - voltage * 1e-3 * current, 0.0, 1e3)


PARAMS = {"voltage": 400.0, "current": 1.928, "speed": 78.54, "g": 9.8122567}
VARIANTS = [{"voltage": 250.0}, {"speed": 50.0}, {"current": 3.5, "g": 9.78}]
ANSWER = 1.0007076565206146
TOL = 1e-9
