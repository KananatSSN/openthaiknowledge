"""Short15 figure: a slab (conductivity K, thickness l) has one face held at T1 and a black outer face at T2 radiating into vacuum. Steady state: K (T1 - T2)/l = sigma T2^4. With K = 0.57, l = 0.1, sigma = 5.7e-8 and T1 = 1000 K this is 10x^4 + x = 1, x = T2/1000 = 0.478. Returns T2 in kelvin."""

SIGMA = 5.7e-8


def solve(hot=1000, conductivity=0.57, thickness=0.1):
    # Newton's method on sigma T^4 + (K/l) T - (K/l) T1 = 0.
    g = conductivity / thickness
    t = hot / 2
    for _ in range(100):
        t -= (SIGMA * t**4 + g * t - g * hot) / (4 * SIGMA * t**3 + g)
    return t


def check(hot=1000, conductivity=0.57, thickness=0.1):
    # Bisection on the energy balance instead.
    g = conductivity / thickness
    lo, hi = 0.0, float(hot)
    for _ in range(200):
        mid = (lo + hi) / 2
        if SIGMA * mid**4 < g * (hot - mid):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"hot": 1000, "conductivity": 0.57, "thickness": 0.1}
VARIANTS = [{"hot": 600}, {"conductivity": 2.28}, {"hot": 1500, "thickness": 0.05}]
ANSWER = 477.9908014025168
