"""Short7 figure: four parallel plates, gaps d, area A; plates 1 and 4 on the negative terminal, 2 and 3 on the positive one. Only gaps between plates at different potentials count: C = 2 eps0 A / d, Q = 2 eps0 A V / d. Adapted: any +/- pattern; returns C in units of eps0 A / d."""


def solve(pattern="-++-"):
    return sum(1 for a, b in zip(pattern, pattern[1:]) if a != b)


def check(pattern="-++-"):
    # Solve the plate charges from Gauss: each plate's charge is eps0 A/d
    # times (its potential minus each neighbour's); the battery supplies the
    # total on the + plates.
    potential = [1.0 if s == "+" else 0.0 for s in pattern]
    total = 0.0
    for i, v in enumerate(potential):
        if v == 1.0:
            for j in (i - 1, i + 1):
                if 0 <= j < len(potential):
                    total += v - potential[j]
    return total


PARAMS = {"pattern": "-++-"}
VARIANTS = [{"pattern": "+-+-"}, {"pattern": "+--"}, {"pattern": "-+-+-+"}]
ANSWER = 2
