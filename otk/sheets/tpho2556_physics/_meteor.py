"""Shared numerical descent for problem 1.2: d(ln v)/dz = k e^(-alpha z) with k = C_d rho0 pi r^2/(2 m sin theta), integrated down from 200 km by Simpson's rule."""

from math import exp, pi, sin


def rate(drag, radius, mass, angle, rho0=1.2, alpha=1.25e-4):
    """The ODE's coefficient k (per metre) and alpha."""
    return drag * rho0 * pi * radius**2 / (2 * mass * sin(angle)), alpha


def speed_at(z, drag, radius, mass, angle, speed, rho0=1.2, alpha=1.25e-4, top=200e3, steps=200000):
    """v at height z by integrating d(ln v)/dz downward from the top."""
    k, _ = rate(drag, radius, mass, angle, rho0, alpha)
    h = (top - z) / steps
    lnv = 0.0
    for i in range(steps):
        a = top - i * h
        lnv -= h * k * (exp(-alpha * a) + 4 * exp(-alpha * (a - h / 2)) + exp(-alpha * (a - h))) / 6
    return speed * exp(lnv)


def brightest(drag, radius, mass, angle, speed, rho0=1.2, alpha=1.25e-4):
    """(z, rho, v) where rho v^3 is stationary: d ln(rho v^3)/dz = -alpha + 3 d(ln v)/dz = 0,
    found by bisection on the ODE's own rate."""
    k, _ = rate(drag, radius, mass, angle, rho0, alpha)
    lo, hi = -1e5, 1e6
    for _ in range(200):
        mid = (lo + hi) / 2
        if 3 * k * exp(-alpha * mid) > alpha:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2
    return z, rho0 * exp(-alpha * z), speed_at(z, drag, radius, mass, angle, speed, rho0, alpha)
