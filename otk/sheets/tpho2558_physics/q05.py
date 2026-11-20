"""Theory 1.2 (b): the motor barely lifted the bare beam, so tau is about MgL/2; then the quadratic leaves ml^2 = ML^2/3 and l = L sqrt(M/(3m)). Adapted: M, L and m vary; returns l in metres."""

from math import sqrt


def solve(beam=20.0, length=1.5, weight=10.0):
    return length * sqrt(beam / (3 * weight))


def check(beam=20.0, length=1.5, weight=10.0, g=9.8):
    # Maximise the angular acceleration numerically with tau = MgL/2.
    from otk.sheets.tpho2558_physics._shared import golden_max

    torque = beam * g * length / 2

    def alpha(arm):
        return (torque + weight * g * arm - beam * g * length / 2) / (beam * length**2 / 3 + weight * arm * arm)

    return golden_max(alpha, 0.0, 10 * length)


PARAMS = {"beam": 20.0, "length": 1.5, "weight": 10.0}
VARIANTS = [{"weight": 30.0}, {"beam": 40.0, "length": 3.0}, {"weight": 5.0}]
ANSWER = 1.224744871391589
TOL = 1e-7
