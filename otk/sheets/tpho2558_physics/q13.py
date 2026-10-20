"""Theory 3 (d)-(e): a ring of radius r and width dr has resistance rho 2 pi r/(z dr) and dissipates (pi r^2 B0 omega sin omega t)^2 z dr/(2 pi rho r); summing rings gives z pi a^4 B0^2 omega^2 sin^2(omega t)/(8 rho), averaging to z pi a^4 B0^2 omega^2/(16 rho). Adapted: z (mm), a (cm), B0 and omega vary for copper (rho = 1.7e-8 ohm m); returns the mean power in watts."""

from math import pi


def solve(thickness=1.0, radius=5.0, field=0.1, omega=100.0, resistivity=1.7e-8):
    return thickness * 1e-3 * pi * (radius * 1e-2) ** 4 * field**2 * omega**2 / (16 * resistivity)


def check(thickness=1.0, radius=5.0, field=0.1, omega=100.0, resistivity=1.7e-8):
    # Sum the rings' instantaneous power (midpoint in r) and average over a
    # period (midpoint in t).
    from math import sin

    z, a = thickness * 1e-3, radius * 1e-2
    nr, nt = 400, 400
    total = 0.0
    for j in range(nt):
        s = sin(2 * pi * (j + 0.5) / nt)
        for i in range(nr):
            r = (i + 0.5) * a / nr
            emf = pi * r * r * field * omega * s
            total += emf * emf * z * (a / nr) / (2 * pi * resistivity * r)
    return total / nt


PARAMS = {"thickness": 1.0, "radius": 5.0, "field": 0.1, "omega": 100.0, "resistivity": 1.7e-8}
VARIANTS = [{"radius": 3.0}, {"field": 0.05, "omega": 300.0}, {"thickness": 0.5}]
ANSWER = 7.218733119461843
TOL = 1e-4
