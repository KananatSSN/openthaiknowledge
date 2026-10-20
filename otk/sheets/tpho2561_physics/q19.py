"""Theory 3.8-3.9: reflection doubles the pressure amplitude at the plate (P_m = 2 P0), so the mean excess pressure there is (2 P0)^2/(4 rho0 c^2) and the push per area is P0^2/(rho0 c^2); 120 dB (P0 = 20 Pa, from 20 uPa at 0 dB) in air 1.2 kg/m^3 at 340 m/s gives 2.9e-3 N/m^2. Adapted: the level (dB), rho0 and c vary; returns the push in mN/m^2."""


def solve(level=120.0, density=1.2, sound=340.0):
    p0 = 20e-6 * 10 ** (level / 20)
    return p0**2 / (density * sound**2) * 1e3


def check(level=120.0, density=1.2, sound=340.0):
    # Intensity route: I = P0^2/(2 rho0 c) from the reference intensity, and
    # a reflected wave pushes 2I/c.
    i_ref = (20e-6) ** 2 / (2 * density * sound)
    intensity = i_ref * 10 ** (level / 10)
    return 2 * intensity / sound * 1e3


PARAMS = {"level": 120.0, "density": 1.2, "sound": 340.0}
VARIANTS = [{"level": 140.0}, {"level": 110.0}, {"sound": 330.0, "density": 1.29}]
ANSWER = 2.883506343713956
TOL = 1e-9
