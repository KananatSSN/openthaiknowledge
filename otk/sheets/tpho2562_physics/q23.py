"""Lab part 3.2 A: the fill factor is FF = P_max/(V_OC I_SC) with P_max = V_mp I_mp at the knee of the I-V curve. Synthetic readings for a green LED lit by a violet one: V_OC = 1.85 V, I_SC = 0.420 mA, and the maximum power at 1.52 V and 0.350 mA, give FF = 0.685. Adapted: the four readings vary."""


def solve(open_volts=1.85, short_ma=0.420, volts=1.52, ma=0.350):
    return volts * ma / (open_volts * short_ma)


def check(open_volts=1.85, short_ma=0.420, volts=1.52, ma=0.350):
    # the fraction of the V_OC x I_SC rectangle filled, as two side ratios
    return (volts / open_volts) * (ma / short_ma)


PARAMS = {"open_volts": 1.85, "short_ma": 0.420, "volts": 1.52, "ma": 0.350}
VARIANTS = [{"volts": 1.40}, {"ma": 0.300}, {"open_volts": 1.95}]
ANSWER = 0.6846846846846846
TOL = 1e-9
