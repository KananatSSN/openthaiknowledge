"""Theory 1.2 (a) figure: about the pivot the net torque is tau + mgl - MgL/2 on I = ML^2/3 + ml^2; d(alpha)/dl = 0 gives ml^2 + 2(tau/g - ML/2) l - ML^2/3 = 0, so l = [-(tau/g - ML/2) + sqrt((tau/g - ML/2)^2 + mML^2/3)]/m. Adapted: tau, M, L and m vary; returns l in metres with g = 9.8."""

from math import sqrt


def solve(torque=150.0, beam=20.0, length=1.5, weight=10.0, g=9.8):
    b = torque / g - beam * length / 2
    return (-b + sqrt(b * b + weight * beam * length**2 / 3)) / weight


def check(torque=150.0, beam=20.0, length=1.5, weight=10.0, g=9.8):
    from otk.sheets.tpho2558_physics._shared import golden_max

    def alpha(arm):
        return (torque + weight * g * arm - beam * g * length / 2) / (beam * length**2 / 3 + weight * arm * arm)

    return golden_max(alpha, 0.0, 10 * length)


PARAMS = {"torque": 150.0, "beam": 20.0, "length": 1.5, "weight": 10.0, "g": 9.8}
VARIANTS = [{"torque": 300.0}, {"weight": 30.0}, {"beam": 40.0, "length": 3.0, "torque": 800.0}]
ANSWER = 1.194515140126836
TOL = 1e-7
