"""Theory 3(b): raising v to v + dv changes the echo interval by -2c tau dv/(c + v)^2 to first order. Adapted: numbers for c, v, tau, dv; seconds."""


def solve(wave=340, speed=20, gap=0.1, step=0.5):
    return -2 * wave * gap * step / (wave + speed) ** 2


def check(wave=340, speed=20, gap=0.1, step=0.5):
    # Slope of the exact interval in v, by a central difference, times dv.
    def interval(v):
        return (wave - v) * gap / (wave + v)

    h = 1e-4
    return (interval(speed + h) - interval(speed - h)) / (2 * h) * step


PARAMS = {"wave": 340, "speed": 20, "gap": 0.1, "step": 0.5}
VARIANTS = [{"speed": 0}, {"wave": 1500, "speed": 10, "step": 1}, {"gap": 2}]
ANSWER = -0.0002623456790123457
TOL = 1e-6
