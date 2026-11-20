"""Short9 figure: a bar of length L, section A, conductivity K passes heat Q = (T1 - T2)/R_th with R_th = L/(K A). Kelvin per watt; L in m, A in cm^2."""


def solve(length=0.5, area=2, conductivity=400):
    return length / (conductivity * area * 1e-4)


def check(length=0.5, area=2, conductivity=400):
    # Fourier's law over slices in series: their resistances add.
    n = 1000
    slice_resistance = (length / n) / (conductivity * area * 1e-4)
    return sum(slice_resistance for _ in range(n))


PARAMS = {"length": 0.5, "area": 2, "conductivity": 400}
VARIANTS = [{"length": 2, "area": 5}, {"conductivity": 50}, {"length": 0.1, "area": 1, "conductivity": 200}]
ANSWER = 6.25
