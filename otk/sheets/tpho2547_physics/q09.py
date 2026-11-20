"""Theory 3(a) figure: pulses at speed c, tau apart, reflect from an object approaching the source at v < c; the reflected pulses are (c - v) tau/(c + v) apart. Adapted: numbers for c, v, tau; seconds."""


def solve(wave=340, speed=20, gap=0.1):
    return (wave - speed) * gap / (wave + speed)


def check(wave=340, speed=20, gap=0.1, start=100.0):
    # Event simulation: find where each pulse meets the object, then when its
    # echo returns to the source at x = 0.
    def echo(n):
        sent = n * gap
        # pulse x = c (t - sent), object x = start - v t
        meet = (start + wave * sent) / (wave + speed)
        place = start - speed * meet
        return meet + place / wave

    return echo(1) - echo(0)


PARAMS = {"wave": 340, "speed": 20, "gap": 0.1}
VARIANTS = [{"speed": 0}, {"wave": 3e8, "speed": 3e4, "gap": 1e-6}, {"speed": 300}]
ANSWER = 0.08888888888888889
TOL = 1e-9
