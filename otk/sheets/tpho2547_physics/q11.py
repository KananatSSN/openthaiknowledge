"""Theory 3(c): with the object receding at v < c, the echoes are (c + v) tau/(c - v) apart. Adapted: numbers for c, v, tau; seconds."""


def solve(wave=340, speed=20, gap=0.1):
    return (wave + speed) * gap / (wave - speed)


def check(wave=340, speed=20, gap=0.1, start=100.0):
    # Event simulation, the object moving away from the source at x = 0.
    def echo(n):
        sent = n * gap
        meet = (start + wave * sent) / (wave - speed)
        place = start + speed * meet
        return meet + place / wave

    return echo(1) - echo(0)


PARAMS = {"wave": 340, "speed": 20, "gap": 0.1}
VARIANTS = [{"speed": 0}, {"wave": 3e8, "speed": 3e4, "gap": 1e-6}, {"speed": 300}]
ANSWER = 0.1125
TOL = 1e-9
