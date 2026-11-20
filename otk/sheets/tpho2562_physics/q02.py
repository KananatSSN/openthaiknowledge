"""Theory 1.3: hydrostatic thrusts on the faces of the jump region, F = (1/2) rho g L h^2 each, give a net force of magnitude (1/2) rho g L (h2^2 - h1^2) against the flow. Adapted: the channel width (m) and the depths before and after (cm) vary; returns newtons with g = 9.8."""


def solve(width=0.5, before=2.0, after=6.0, density=1000.0):
    h1, h2 = before * 1e-2, after * 1e-2
    return 0.5 * density * 9.8 * width * (h2**2 - h1**2)


def check(width=0.5, before=2.0, after=6.0, density=1000.0):
    # integrate the pressure rho g y over each face in thin strips
    def thrust(h, n=4000):
        dy = h / n
        return sum(density * 9.8 * (i + 0.5) * dy * width * dy for i in range(n))

    return thrust(after * 1e-2) - thrust(before * 1e-2)


PARAMS = {"width": 0.5, "before": 2.0, "after": 6.0, "density": 1000.0}
VARIANTS = [{"before": 1.0}, {"after": 10.0}, {"width": 1.2}]
ANSWER = 7.839999999999999
TOL = 1e-6
