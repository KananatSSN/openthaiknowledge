"""Theory 1.2 (a) figure: the sound heard when the source is closest left it earlier, at cos(theta) = u/v along the line to the observer, so f = f0 v/(v - u cos theta) = f0 v^2/(v^2 - u^2). Adapted: f0, u and v vary; returns the shift f - f0 in Hz."""


def solve(base=500.0, speed=100.0, sound=340.0):
    return base * sound**2 / (sound**2 - speed**2) - base


def check(base=500.0, speed=100.0, sound=340.0, distance=50.0):
    # A wavefront emitted at time te from x = u te arrives at
    # T(te) = te + sqrt((u te)^2 + L^2)/v. The source is closest at time 0;
    # find the emission heard then (T = 0) and the local rate dT/dte: the
    # heard frequency is f0/(dT/dte).
    from math import hypot

    from otk.sheets.tpho2557_physics._shared import bisect

    def arrival(te):
        return te + hypot(speed * te, distance) / sound

    te = bisect(lambda t: arrival(t), -10 * distance / sound, 0.0)
    h = 1e-6
    rate = (arrival(te + h) - arrival(te - h)) / (2 * h)
    return base / rate - base


PARAMS = {"base": 500.0, "speed": 100.0, "sound": 340.0}
VARIANTS = [{"speed": 60.0}, {"base": 800.0, "speed": 150.0}, {"sound": 330.0}]
ANSWER = 47.34848484848487
TOL = 1e-6
