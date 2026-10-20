"""Theory 1.1 a), c): a thin tube (I = m'R^2) rolling without slipping down an incline of angle theta along a line at phi to the steepest slope has a = g sin(theta) cos(phi)/(1 + I/(m'R^2)) = g sin(theta) cos(phi)/2 (phi = 0 gives g sin(theta)/2). Adapted: theta and phi (degrees) vary; returns m/s^2 with g = 9.81."""

from math import cos, radians, sin


def solve(incline=30.0, slant=40.0):
    return 9.81 * sin(radians(incline)) * cos(radians(slant)) / 2


def check(incline=30.0, slant=40.0, mass=1.0, radius=0.1):
    # m a = m g sin(t) cos(p) - f1 and f1 R = I a/R, solved by Cramer's rule
    drive = mass * 9.81 * sin(radians(incline)) * cos(radians(slant))
    inertia = mass * radius * radius
    rows = ((mass, 1.0), (-inertia / radius, radius))
    det = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
    return (drive * rows[1][1] - rows[0][1] * 0.0) / det


PARAMS = {"incline": 30.0, "slant": 40.0}
VARIANTS = [{"slant": 0.0}, {"incline": 15.0}, {"slant": 70.0}]
ANSWER = 1.8787239967492932
TOL = 1e-9
