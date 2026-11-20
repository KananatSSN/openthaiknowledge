"""Theory 2.7: the Hall resistance R = B/(e n) of a sheet with n electrons per area becomes quantised when the electrons fill nu flux quanta, n = nu e B/h, so R = h/(nu e^2), proportional to h/e^2 with a dimensionless constant: 25.8 kOhm for nu = 1. Adapted: the integer nu varies; returns R in kOhm."""

H, E = 6.626069e-34, 1.602177e-19


def solve(filling=1):
    return H / (filling * E * E) / 1e3


def check(filling=1):
    # Build a sheet: choose B, fill nu quanta of flux h/e per electron pair
    # count, then compute the classical Hall resistance B/(e n).
    field = 10.0
    n_area = filling * E * field / H
    return field / (E * n_area) / 1e3


PARAMS = {"filling": 1}
VARIANTS = [{"filling": 2}, {"filling": 3}, {"filling": 4}]
ANSWER = 25.812791186004677
TOL = 1e-12
