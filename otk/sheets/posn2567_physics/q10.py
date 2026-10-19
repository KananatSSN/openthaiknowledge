"""Short10 figure: a boat at constant v toward a cliff sounds its horn at A and hears the echo after t. With (c + v) t = 2L, it reaches the cliff (c + v) t / (2v) after the horn. Seconds."""


def solve(speed=10, echo=7, sound=340):
    return (sound + speed) * echo / (2 * speed)


def check(speed=10, echo=7, sound=340):
    # Bisect on the starting distance L until the echo returns at t, then L/v.
    lo, hi = 0.0, 1e7
    for _ in range(200):
        dist = (lo + hi) / 2
        out = dist / sound
        back = (dist - speed * out) / (sound + speed)
        if out + back < echo:
            lo = dist
        else:
            hi = dist
    return (lo + hi) / 2 / speed


PARAMS = {"speed": 10, "echo": 7, "sound": 340}
VARIANTS = [{"speed": 20, "echo": 4}, {"echo": 12}, {"speed": 5, "sound": 330}]
ANSWER = 122.5
