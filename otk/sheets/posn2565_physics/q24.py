"""MC24 figure: wire of cross-section a and conductivity sigma carries I; current density I/a = sigma E, so E = I/(sigma a) (answer 2). Returns V/m for sigma in S/m and a in mm^2."""


def solve(current=2, conductivity=5e7, area=1):
    return current / (conductivity * area * 1e-6)


def check(current=2, conductivity=5e7, area=1, length=3):
    # Resistance of a length, Ohm's law for the voltage, then E = V / length.
    resistance = length / (conductivity * area * 1e-6)
    return current * resistance / length


PARAMS = {"current": 2, "conductivity": 5e7, "area": 1}
VARIANTS = [{"current": 10, "area": 2.5}, {"conductivity": 6e7}, {"area": 0.5}]
ANSWER = 0.04
