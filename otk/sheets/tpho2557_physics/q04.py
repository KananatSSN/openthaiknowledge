"""Theory 1.2 (b): the unshifted sound was emitted at the closest point x = 0 and arrives L/v later, when the source has moved uL/v on, so it is L sqrt(u^2 + v^2)/v from the observer. Adapted: L, u and v vary; returns the distance in metres."""

from math import sqrt


def solve(distance=50.0, speed=100.0, sound=340.0):
    return distance * sqrt(speed**2 + sound**2) / sound


def check(distance=50.0, speed=100.0, sound=340.0):
    # Bisect the observer time at which the heard frequency equals f0,
    # then measure where the source is at that time.
    from math import hypot

    from otk.sheets.tpho2557_physics._shared import bisect

    def arrival(te):
        return te + hypot(speed * te, distance) / sound

    def heard_shift(T):
        te = bisect(lambda t: arrival(t) - T, T - 100.0, T)
        h = 1e-6
        return (arrival(te + h) - arrival(te - h)) / (2 * h) - 1

    T = bisect(heard_shift, -5.0, 5.0)
    return hypot(speed * T, distance)


PARAMS = {"distance": 50.0, "speed": 100.0, "sound": 340.0}
VARIANTS = [{"speed": 60.0}, {"distance": 120.0}, {"speed": 150.0, "sound": 330.0}]
ANSWER = 52.117779843145144
TOL = 1e-6
