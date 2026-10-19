"""Short28 figure: a boat runs at constant speed u toward a cliff. Echo times t1 (horn at position 1) and t2 (horn tau later). Each echo: c t + u t = 2 L, so t1 - t2 = 2 u tau/(c + u) and u = c (t1 - t2)/(2 tau - t1 + t2). Seconds, c in m/s."""


def solve(t1=10, t2=9, tau=9, sound=340):
    return sound * (t1 - t2) / (2 * tau - t1 + t2)


def check(t1=10, t2=9, tau=9, sound=340):
    # Bisect on u: from the first echo, L1 = (c + u) t1 / 2; predict the
    # second echo after moving u tau, and match t2.
    def predicted_t2(u):
        start = (sound + u) * t1 / 2
        return 2 * (start - u * tau) / (sound + u)

    lo, hi = 0.0, sound * 0.99
    for _ in range(200):
        u = (lo + hi) / 2
        if predicted_t2(u) > t2:
            lo = u
        else:
            hi = u
    return (lo + hi) / 2


PARAMS = {"t1": 10, "t2": 9, "tau": 9, "sound": 340}
VARIANTS = [{"t1": 6, "t2": 5, "tau": 10}, {"t1": 4, "t2": 3.5, "tau": 5}, {"sound": 330, "tau": 12}]
ANSWER = 20.0
