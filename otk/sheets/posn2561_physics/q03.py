"""MC3: successive balls share vertical launch speed9.8m/s, delay1s, g9.8. The second and third meet at3.675m (rounded source choice3.7). The first ball does not affect their crossing."""


def solve(speed=9.8, delay=1, g=9.8):
    if not 0 < delay < 2 * speed / g:
        raise ValueError("crossing must occur above launch point")
    return speed * speed / (2 * g) - g * delay * delay / 8


def check(speed=9.8, delay=1, g=9.8):
    # Find the intersection of two independent position-time trajectories.
    lo, hi = 0.0, 2 * speed / g - delay
    for _ in range(100):
        time = (lo + hi) / 2
        newer = speed * time - g * time * time / 2
        older = speed * (time + delay) - g * (time + delay) ** 2 / 2
        if newer < older:
            lo = time
        else:
            hi = time
    time = (lo + hi) / 2
    return speed * time - g * time * time / 2


PARAMS = {"speed": 9.8, "delay": 1, "g": 9.8}
VARIANTS = [{"delay": 0.5}, {"speed": 19.6}, {"g": 10}]
ANSWER = 3.6750000000000003
