"""Theory 2.2(a) figure: a solid ball struck through its centre slides with deceleration mu g while friction spins it up at 5 mu g/(2R); rolling starts at t = 2V0/(7 mu g) after S = 12 V0^2/(49 mu g). Adapted: numbers for V0 and mu; metres with g = 10."""


def solve(speed=7, friction=0.2, radius=0.05, g=10):
    return 12 * speed**2 / (49 * friction * g)


def check(speed=7, friction=0.2, radius=0.05, g=10):
    # Step the sliding motion until the contact point stops slipping.
    v, w, x, dt = float(speed), 0.0, 0.0, 1e-6
    while v - w * radius > 0:
        v -= friction * g * dt
        w += 5 * friction * g / (2 * radius) * dt
        x += v * dt
    return x


PARAMS = {"speed": 7, "friction": 0.2, "radius": 0.05, "g": 10}
VARIANTS = [{"speed": 2}, {"friction": 0.5, "radius": 0.1}, {"speed": 3.5, "friction": 0.1}]
ANSWER = 6.0
TOL = 1e-4
