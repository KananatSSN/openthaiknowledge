"""Short18 figure: a boat leaves the cliff at t = 0 at constant v; it sounds the horn at t1 and hears the echo tau later. Sound covers v t1 out and v(t1 + tau) back: c tau = v (2 t1 + tau), v = c tau/(2 t1 + tau). m/s."""


def solve(start=10, delay=2, sound=340):
    return sound * delay / (2 * start + delay)


def check(start=10, delay=2, sound=340):
    # Bisect on v so the echo arrives exactly `delay` after the horn.
    def echo(v):
        out = v * start / sound
        # back: sound from the cliff at time start + out catches the boat
        t_back = (v * (start + out)) / (sound - v)
        return out + t_back

    lo, hi = 0.0, sound * 0.99
    for _ in range(200):
        mid = (lo + hi) / 2
        if echo(mid) < delay:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"start": 10, "delay": 2, "sound": 340}
VARIANTS = [{"start": 4, "delay": 1}, {"delay": 3}, {"start": 20, "delay": 5, "sound": 330}]
ANSWER = 30.90909090909091
