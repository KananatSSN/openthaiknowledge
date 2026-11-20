"""Lab 1 part 1 figures 1-2: the frequency falls in proportion to the load on the tube springs, so the nut's mass is the battery's mass times the frequency drop per nut (slope of frequency against number of nuts, least squares) over the drop the battery causes (from the fitted empty reading). Adapted with synthetic readings (kHz); returns the nut's mass in grams."""


def solve(battery=46.0, counts=(2, 4, 6, 8, 10), freqs=(9.62, 9.25, 8.87, 8.50, 8.12), loaded=7.20):
    n = len(counts)
    mx, my = sum(counts) / n, sum(freqs) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(counts, freqs)) / sum((x - mx) ** 2 for x in counts)
    empty = my - slope * mx
    return battery * -slope / (empty - loaded)


def check(battery=46.0, counts=(2, 4, 6, 8, 10), freqs=(9.62, 9.25, 8.87, 8.50, 8.12), loaded=7.20):
    from otk.sheets.tpho2555_physics._fit import line

    slope, empty = line(list(counts), list(freqs))
    # Count how many nuts would match the battery's drop, then share its mass.
    nuts = (empty - loaded) / -slope
    return battery / nuts


PARAMS = {"battery": 46.0, "counts": (2, 4, 6, 8, 10), "freqs": (9.62, 9.25, 8.87, 8.50, 8.12), "loaded": 7.20}
VARIANTS = [{"battery": 40.0}, {"loaded": 6.5}, {"counts": (4, 8, 12, 16), "freqs": (9.2, 8.5, 7.7, 7.0)}]
ANSWER = 3.083661065427244
TOL = 1e-12
