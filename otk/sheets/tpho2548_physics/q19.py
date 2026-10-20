"""Lab 2: laser light at grazing angle theta on a steel ruler whose lines are d apart; bright spots satisfy d cos theta - d cos phi = n lambda. Adapted: the screen is L from the spot; the specular spot is h0 and the order-n spot hn above the ruler's plane, so cos = L/sqrt(L^2 + h^2); nm."""

from math import atan, cos, sqrt


def solve(pitch=1e-3, distance=2.0, mirror=0.2, spot=0.2128, order=1):
    c0 = distance / sqrt(distance**2 + mirror**2)
    cn = distance / sqrt(distance**2 + spot**2)
    return pitch * (c0 - cn) / order * 1e9


def check(pitch=1e-3, distance=2.0, mirror=0.2, spot=0.2128, order=1):
    # Angles from the arctangent, path difference of two neighbouring rays.
    theta, phi = atan(mirror / distance), atan(spot / distance)
    return (pitch * cos(theta) - pitch * cos(phi)) / order * 1e9


PARAMS = {"pitch": 1e-3, "distance": 2.0, "mirror": 0.2, "spot": 0.2128, "order": 1}
VARIANTS = [{"order": 2, "spot": 0.225}, {"distance": 3.0, "mirror": 0.3, "spot": 0.3192}, {"pitch": 0.5e-3}]
ANSWER = 650.0576321180063
TOL = 1e-9
