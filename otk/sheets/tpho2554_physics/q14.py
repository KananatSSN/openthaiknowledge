"""Theory 3.3-3.5: with the surface-tension pressure, (R0^4/R^4) v0^2 + 2 gamma/(rho R) - 2gh = v0^2 + 2 gamma/(rho R0); to first order about R1 = R0 (1 + 2gh/v0^2)^(-1/4), dR = (2 gamma/rho)(1/R1 - 1/R0)/(4 R0^4 v0^2/R1^5 + 2 gamma/(rho R1^2)). The bound solution's 3.5 value 1.34e-5 m comes from its simplified gamma(1 - R1/R0)/(2 rho (v0^2 + 2gh)); the full first-order form gives 1.32e-5 m. Adapted: h, R0 (cm) and v0 vary; returns dR in micrometres."""


def solve(radius0=0.5, speed0=0.10, height=0.10, tension=0.072, density=1000.0, g=9.8):
    R0 = radius0 * 1e-2
    R1 = R0 * (1 + 2 * g * height / speed0**2) ** -0.25
    k = 2 * tension / density
    return k * (1 / R1 - 1 / R0) / (4 * R0**4 * speed0**2 / R1**5 + k / R1**2) * 1e6


def check(radius0=0.5, speed0=0.10, height=0.10, tension=0.072, density=1000.0, g=9.8):
    # Linearising about R1 is one Newton step on the 3.3 relation: take it
    # with a numerical derivative.
    R0 = radius0 * 1e-2
    k = 2 * tension / density
    R1 = R0 * (1 + 2 * g * height / speed0**2) ** -0.25

    def residual(R):
        return R0**4 / R**4 * speed0**2 + k / R - 2 * g * height - speed0**2 - k / R0

    h = R1 * 1e-6
    slope = (residual(R1 + h) - residual(R1 - h)) / (2 * h)
    return -residual(R1) / slope * 1e6


PARAMS = {"radius0": 0.5, "speed0": 0.10, "height": 0.10, "tension": 0.072, "density": 1000.0, "g": 9.8}
VARIANTS = [{"height": 0.05}, {"radius0": 0.3, "speed0": 0.2}, {"height": 0.2}]
ANSWER = 13.215407646785307
TOL = 1e-6
