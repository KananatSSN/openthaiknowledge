"""Theory 1.1 b): the elastic bounce reverses the mass's velocity (impulse 2mv) and, since its speed is unchanged, the beam's spin too, so 2 (ML^2/12) omega = 2mv (L/2) and ML omega = 6mv. Adapted: M, L, m and v vary; returns omega in rad/s."""


def solve(beam=2.0, length=1.0, mass=0.1, speed=3.0):
    return 6 * mass * speed / (beam * length)


def check(beam=2.0, length=1.0, mass=0.1, speed=3.0):
    # Elastic impact at the end: momentum-like impulse balance plus energy
    # conservation; bisect the beam's incoming spin for which the mass leaves
    # with -v (its exact reversal).
    from otk.sheets.tpho2561_physics._shared import bisect

    inertia = beam * length**2 / 12
    arm = length / 2

    def rebound(w):
        # end speed along the normal (toward the mass) = w arm; elastic
        # collision of m with an effective mass I/arm^2
        eff = inertia / arm**2
        u_end = -w * arm                     # end moving into the mass
        v_after = ((mass - eff) * speed + 2 * eff * u_end) / (mass + eff)
        return v_after + speed

    return abs(bisect(rebound, 0.0, 1e3))


PARAMS = {"beam": 2.0, "length": 1.0, "mass": 0.1, "speed": 3.0}
VARIANTS = [{"mass": 0.3}, {"beam": 5.0, "length": 2.0}, {"speed": 6.0}]
ANSWER = 0.9000000000000001
TOL = 1e-9
