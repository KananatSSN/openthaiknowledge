"""Shared model for problem 1: a superconducting ring of radius R and inductance L released from rest at A, where it carried no current, in the field B_z = B0(1 + alpha z), B_r = B0 beta r (z downward from A). Its flux stays B0 pi R^2."""

from math import pi


def current(z, B0, alpha, radius, inductance):
    """Signed ring current at depth z from flux conservation (negative is clockwise seen from above)."""
    area = pi * radius**2
    return (area * B0 - area * B0 * (1 + alpha * z)) / inductance


def lift(z, B0, alpha, beta, radius, inductance):
    """Upward force |I| 2 pi R B_r of the radial field on the ring current."""
    return abs(current(z, B0, alpha, radius, inductance)) * 2 * pi * radius * B0 * beta * radius


def fall(mass, B0, alpha, beta, radius, inductance, g=9.8, dt=2e-5, duration=2.0):
    """RK4 from rest at z = 0; yields (t, z, v) with v downward."""
    def accel(z):
        return g - lift(z, B0, alpha, beta, radius, inductance) / mass

    t, z, v = 0.0, 0.0, 0.0
    yield t, z, v
    while t < duration:
        k1z, k1v = v, accel(z)
        k2z, k2v = v + dt / 2 * k1v, accel(z + dt / 2 * k1z)
        k3z, k3v = v + dt / 2 * k2v, accel(z + dt / 2 * k2z)
        k4z, k4v = v + dt * k3v, accel(z + dt * k3z)
        z += dt / 6 * (k1z + 2 * k2z + 2 * k3z + k4z)
        v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += dt
        yield t, z, v
