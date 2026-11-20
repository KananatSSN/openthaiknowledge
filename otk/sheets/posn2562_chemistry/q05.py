"""Source MC5: V has [Ar] 3d³4s²; its first two ions lose 4s electrons."""

D_COUNT = {22: 2, 23: 3, 26: 6, 27: 7}
GROUP = {22: 4, 23: 5, 26: 8, 27: 9, 43: 7}


def solve(z=23, comparison_z=43):
    d = D_COUNT[z]
    claims = (GROUP[z] == GROUP[comparison_z], d == z - 20,
              False, d - 2 == d)
    # For these non-anomalous 3d metals, 3d occupancy is Z-20.
    assert claims.count(True) == 1
    return claims.index(True)


def check(z=23, comparison_z=43):
    assert z in D_COUNT and comparison_z == 43
    # Remove the 4s pair first: neutral (3d^d,4s²) -> 2+ (3d^d,4s⁰).
    neutral = {"3d": D_COUNT[z], "4s": 2}
    ion = {"3d": neutral["3d"], "4s": 0}
    statements = (GROUP[z] == 7, neutral["3d"] == z - 20,
                  neutral["4s"] == 0, ion["3d"] < neutral["3d"])
    return statements.index(True) if statements.count(True) == 1 else None


PARAMS = {"z": 23, "comparison_z": 43}
VARIANTS = [
    {"z": 22, "comparison_z": 43},
    {"z": 26, "comparison_z": 43},
    {"z": 27, "comparison_z": 43},
]
ANSWER = solve(**PARAMS)
