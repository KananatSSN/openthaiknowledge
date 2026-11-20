"""Short24 figure: water (density rho, viscosity eta) drains from a large tank of depth h through a horizontal tube of length l and radius r to the air. Poiseuille flow driven by rho g h: mean speed v = rho g h r^2/(8 eta l), outlet kinetic head neglected. m/s; r in mm, eta in mPa s."""


def solve(depth=0.4, radius=0.5, viscosity=1, length=1, density=1000, g=10):
    r, eta = radius / 1000, viscosity / 1000
    return density * g * depth * r * r / (8 * eta * length)


def check(depth=0.4, radius=0.5, viscosity=1, length=1, density=1000, g=10):
    # Integrate the parabolic velocity profile over the cross-section, then
    # divide the flow by the area.
    r, eta = radius / 1000, viscosity / 1000
    gradient = density * g * depth / length
    n = 20000
    flow = 0.0
    for k in range(n):
        s = r * (k + 0.5) / n
        u = gradient / (4 * eta) * (r * r - s * s)
        flow += u * 2 * 3.141592653589793 * s * (r / n)
    return flow / (3.141592653589793 * r * r)


PARAMS = {"depth": 0.4, "radius": 0.5, "viscosity": 1, "length": 1, "density": 1000, "g": 10}
VARIANTS = [{"depth": 1}, {"radius": 0.2, "length": 0.5}, {"viscosity": 2}]
TOL = 1e-6
ANSWER = 0.125
