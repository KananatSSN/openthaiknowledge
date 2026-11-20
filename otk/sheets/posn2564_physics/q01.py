"""MC1 figure: plank B rests on plank A on level ground; A is pulled right with acceleration a. Friction coefficient mu between A and B only. B slips when a > mu g (answer 1). Adapted quantity: with a > mu g, the magnitude of B's acceleration relative to A, a - mu g; zero when B does not slip."""


def solve(mu=0.3, accel=5, g=10):
    return max(accel - mu * g, 0)


def check(mu=0.3, accel=5, g=10):
    # Step both plates in time: B sticks unless the friction it needs exceeds mu m g.
    dt, steps = 1e-4, 10000
    va = vb = xa = xb = 0.0
    for _ in range(steps):
        va += accel * dt
        if vb < va:
            vb = min(va, vb + mu * g * dt)
        xa += va * dt
        xb += vb * dt
    t = dt * steps
    return 2 * (xa - xb) / (t * t)


PARAMS = {"mu": 0.3, "accel": 5, "g": 10}
VARIANTS = [{"mu": 0.5, "accel": 8}, {"mu": 0.1, "accel": 2}, {"accel": 6}]
TOL = 1e-2
ANSWER = 2.0
