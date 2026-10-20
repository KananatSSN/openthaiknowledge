"""Theory 2 (a) figure: with the wheel behind, friction mu N1 on the front leg is the only horizontal force; torque about the centre of mass gives N1 (w/2 - mu h) = N2 w/2, so a = w g mu/(2(w - mu h)) and the table stops after s1 = u^2 (w - mu h)/(w g mu). Adapted: u, w, h and mu vary; returns s1 in metres with g = 9.8."""


def solve(speed=2.0, width=1.0, height=0.6, mu=0.3, g=9.8):
    return speed**2 * (width - mu * height) / (width * g * mu)


def check(speed=2.0, width=1.0, height=0.6, mu=0.3, g=9.8):
    # Solve the three force and torque equations, then integrate the
    # constant deceleration in small time steps.
    from otk.sheets.tpho2557_physics._shared import table

    a = table(width, height, mu, True, g)[0]
    n = 100000
    dt = speed / a / n
    v, x = speed, 0.0
    for _ in range(n):
        x += (v + (v - a * dt)) / 2 * dt
        v -= a * dt
    return x


PARAMS = {"speed": 2.0, "width": 1.0, "height": 0.6, "mu": 0.3, "g": 9.8}
VARIANTS = [{"mu": 0.5}, {"width": 0.8, "height": 0.5}, {"speed": 3.0}]
ANSWER = 1.1156462585034015
TOL = 1e-9
