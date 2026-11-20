"""Theory 2.2-2.3 figure 4: moving at u the coil cuts the radial field, V = 2 pi r N B_r u; the data show z = (1.00 mm) sin(2 pi f t) with f = 12.5 Hz and V = (400 mV) cos(2 pi f t), so B_r = 400 mV/(2 pi (0.10 m)(100)(2 pi 12.5 Hz)(1.00 mm)) = 0.081 T. Adapted: the amplitudes (mm, mV), the period (s), r (cm) and N vary; returns B_r in tesla."""

from math import pi


def solve(amplitude=1.0, period=0.08, peak=400.0, radius=10.0, turns=100):
    top_speed = 2 * pi / period * amplitude * 1e-3
    return peak * 1e-3 / (2 * pi * radius * 1e-2 * turns * top_speed)


def check(amplitude=1.0, period=0.08, peak=400.0, radius=10.0, turns=100):
    # Sample the motion, difference z(t) for the speed, and divide the emf
    # by 2 pi r N u at the instant of greatest speed.
    from math import sin

    n = 4000
    best = 0.0
    for i in range(n):
        t = period * i / n
        h = period * 1e-6
        u = (amplitude * 1e-3) * (sin(2 * pi * (t + h) / period) - sin(2 * pi * (t - h) / period)) / (2 * h)
        best = max(best, abs(u))
    return peak * 1e-3 / (2 * pi * radius * 1e-2 * turns * best)


PARAMS = {"amplitude": 1.0, "period": 0.08, "peak": 400.0, "radius": 10.0, "turns": 100}
VARIANTS = [{"peak": 300.0}, {"period": 0.1, "amplitude": 2.0}, {"radius": 15.0, "turns": 50}]
ANSWER = 0.08105694691387022
TOL = 1e-6
