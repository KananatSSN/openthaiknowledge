"""Lab 1 part 2: the frequency is proportional to the plate gap, so plastic spacers give the frequency per metre of gap (least squares) and part 1 gives the frequency drop per kilogram of load; the two tubes in parallel then have k_total = g (per metre)/(per kilogram) and one tube k = k_total/2. Adapted with synthetic spacer readings (mm, kHz) and the part-1 drop per 100 g; returns k of one tube in N/m."""


def solve(thickness=(0.0, 1.0, 2.0, 3.0, 4.0), freqs=(9.95, 11.03, 12.08, 13.14, 14.21), drop=0.95, g=9.81):
    n = len(thickness)
    mx, my = sum(thickness) / n, sum(freqs) / n
    per_mm = sum((x - mx) * (y - my) for x, y in zip(thickness, freqs)) / sum((x - mx) ** 2 for x in thickness)
    per_kg = drop / 0.1
    return per_mm * 1e3 * g / per_kg / 2


def check(thickness=(0.0, 1.0, 2.0, 3.0, 4.0), freqs=(9.95, 11.03, 12.08, 13.14, 14.21), drop=0.95, g=9.81):
    from otk.sheets.tpho2555_physics._fit import line

    per_mm, _ = line(list(thickness), list(freqs))
    squeeze = drop / per_mm * 1e-3          # metres the gap closes under 100 g
    return 0.1 * g / squeeze / 2


PARAMS = {"thickness": (0.0, 1.0, 2.0, 3.0, 4.0), "freqs": (9.95, 11.03, 12.08, 13.14, 14.21), "drop": 0.95, "g": 9.81}
VARIANTS = [{"drop": 0.5}, {"freqs": (8.0, 9.0, 10.0, 11.0, 12.0)}, {"thickness": (0.0, 2.0, 4.0, 6.0, 8.0)}]
ANSWER = 548.8436842105266
TOL = 1e-9
