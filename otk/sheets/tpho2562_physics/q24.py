"""Lab part 3.2 B: below V_OC/2 the I-V curve has slope dI/dV = -1/(R_SH + R_S), so two readings there and R_S from the slope near V_OC give R_SH = -(V2 - V1)/(I2 - I1) - R_S. Synthetic readings (0.10 V, 0.418 mA) and (0.60 V, 0.405 mA) with R_S = 0.50 kilohm give 38.0 kilohm. Adapted: the readings and R_S vary; returns kilohms."""


def solve(first=(0.10, 0.418), second=(0.60, 0.405), series=0.50):
    (v1, i1), (v2, i2) = first, second
    return -(v2 - v1) / (i2 - i1) - series


def check(first=(0.10, 0.418), second=(0.60, 0.405), series=0.50):
    from otk.sheets.tpho2562_physics._shared import bisect

    # the shunt for which the straight-line model meets both readings
    (v1, i1), (v2, i2) = first, second
    short = i1 + (i1 - i2) / (v2 - v1) * v1

    def miss(shunt):
        return short - v2 / (shunt + series) - i2

    return bisect(miss, 1e-3, 1e4)


PARAMS = {"first": (0.10, 0.418), "second": (0.60, 0.405), "series": 0.50}
VARIANTS = [{"series": 1.2}, {"second": (0.70, 0.400)}, {"first": (0.05, 0.420)}]
ANSWER = 37.961538461538595
TOL = 1e-6
