"""MC7 figure: metal bar of length L, section A, conductivity K between T1 and T2 < T1; steady heat flow A K (T1 - T2)/L (answer 7). Watts; A in cm^2."""


def solve(conductivity=400, area=2, hot=100, cold=20, length=0.5):
    return area * 1e-4 * conductivity * (hot - cold) / length


def check(conductivity=400, area=2, hot=100, cold=20, length=0.5):
    # Series thermal resistances of thin slices.
    n = 1000
    total = n * (length / n) / (conductivity * area * 1e-4)
    return (hot - cold) / total


PARAMS = {"conductivity": 400, "area": 2, "hot": 100, "cold": 20, "length": 0.5}
VARIANTS = [{"conductivity": 50, "length": 0.2}, {"area": 5, "cold": 0}, {"hot": 300, "length": 2}]
ANSWER = 12.8
