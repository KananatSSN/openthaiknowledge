"""Part2,9: equal-volume solid cylinder and sphere of same material, cylinder radius equals sphere radius. Equal heating =>same isotropic length scale. Ratio delta height / delta sphere diameter2/3. radius_ratio generalizes cylinder/sphere radii."""

from fractions import Fraction
from math import pi


def solve(radius_num=1, radius_den=1):
    return Fraction(2 * radius_den**2, 3 * radius_num**2)


def check(radius_num=1, radius_den=1):
    sphere_radius = 3.0
    cylinder_radius = sphere_radius * radius_num / radius_den
    volume = 4 * pi * sphere_radius**3 / 3
    cylinder_height = volume / (pi * cylinder_radius**2)
    scale = 1.01
    dh = cylinder_height * scale - cylinder_height
    dd = 2 * sphere_radius * scale - 2 * sphere_radius
    return dh / dd


PARAMS = {"radius_num": 1, "radius_den": 1}
VARIANTS = [{"radius_num": 2}, {"radius_den": 2}, {"radius_num": 3, "radius_den": 2}]
ANSWER = Fraction(2, 3)
