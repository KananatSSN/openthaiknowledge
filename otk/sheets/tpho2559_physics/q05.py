"""Theory 1.3 (a) figure: in steady state the filament radiates sigma A T^4 while absorbing sigma A T0^4 from the room, so the electrical power is P = sigma A (T^4 - T0^4). Adapted: A (mm^2), T and T0 vary; returns P in watts."""


def solve(area=50.0, hot=2500.0, room=300.0, sigma=5.67e-8):
    return sigma * area * 1e-6 * (hot**4 - room**4)


def check(area=50.0, hot=2500.0, room=300.0, sigma=5.67e-8):
    # Heat the filament from room temperature in small steps with the net
    # radiative loss; the input that holds it at T is the loss there,
    # found as the integral of d(loss)/dT from T0 to T (Simpson).
    n = 2000
    h = (hot - room) / n
    total = 0.0
    for i in range(n + 1):
        T = room + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        total += w * 4 * sigma * area * 1e-6 * T**3
    return total * h / 3


PARAMS = {"area": 50.0, "hot": 2500.0, "room": 300.0, "sigma": 5.67e-8}
VARIANTS = [{"hot": 3000.0}, {"area": 20.0}, {"room": 290.0, "hot": 1800.0}]
ANSWER = 110.719224
TOL = 1e-9
