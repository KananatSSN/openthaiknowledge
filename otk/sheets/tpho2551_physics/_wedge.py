"""Shared Lagrangian check for problem 3: wedge (with pulley) of mass M free on a smooth floor, block m on its smooth face, string inertia I/R^2 = k (0 when cut)."""

from math import sqrt


def lagrange(wedge, block, pulley_inertia, sine, g):
    """(a_A, a_rel) from the Lagrangian of X (wedge, +x) and s (block down the face).

    KE = (1/2) M X'^2 + (1/2) m [(X' - s' c)^2 + (s' s_)^2] + (1/2) k s'^2,
    PE = -m g s sin(theta). Solved as a 2x2 linear system."""
    c = sqrt(1 - sine * sine)
    a11, a12 = wedge + block, -block * c
    a21, a22 = -block * c, block + pulley_inertia
    b1, b2 = 0.0, block * g * sine
    det = a11 * a22 - a12 * a21
    return (b1 * a22 - a12 * b2) / det, (a11 * b2 - a21 * b1) / det
