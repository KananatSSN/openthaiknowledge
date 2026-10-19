"""MC3 figure: siphon crest height h above open reservoir. Necessary bound h<Pa/(rho g), answer3. Positive crest kinetic head and vapor pressure make actual limit stricter; source does NOT give enough data for exact operating maximum. Return the necessary upper bound in meters."""


def solve(atmosphere=100000, density=1000, g=10):
    return atmosphere / (density * g)


def check(atmosphere=100000, density=1000, g=10):
    # Integrate hydrostatic pressure gradient; moving flow has a further loss.
    lo, hi = 0.0, 1000.0
    for _ in range(100):
        height = (lo + hi) / 2
        dz = height / 100
        pressure = atmosphere
        for _ in range(100):
            pressure -= density * g * dz
        if pressure > 0:
            lo = height
        else:
            hi = height
    return (lo + hi) / 2


PARAMS = {"atmosphere": 100000, "density": 1000, "g": 10}
VARIANTS = [{"atmosphere": 90000}, {"density": 800}, {"g": 9.8}]
ANSWER = 10.0
