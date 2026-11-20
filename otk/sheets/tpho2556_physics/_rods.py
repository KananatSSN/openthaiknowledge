"""Impulse equations for problem 1.1: rod CD (mass m, length l) hinged at C to rod BC, which the jerk sets moving at u along Y; CD starts at angle theta (radians) to BC. Unknowns: CD's centre velocity (vx, vy), its spin w and the hinge impulse (Jx, Jy); solved by Gaussian elimination."""

from math import cos, sin


def solve_linear(rows, rhs):
    n = len(rows)
    a = [row[:] + [b] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        a[col], a[pivot] = a[pivot], a[col]
        for r in range(n):
            if r != col:
                f = a[r][col] / a[col][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def hinged_rod(mass, length, theta, speed):
    """(vx, vy, w, Jx, Jy) for CD just after the jerk."""
    cx, cy = -length / 2 * cos(theta), -length / 2 * sin(theta)   # C relative to CD's centre
    inertia = mass * length**2 / 12
    # unknowns x = (vx, vy, w, Jx, Jy)
    rows = [
        [mass, 0, 0, -1, 0],                 # m vx = Jx
        [0, mass, 0, 0, -1],                 # m vy = Jy
        [0, 0, inertia, cy, -cx],            # I w = cx Jy - cy Jx
        [1, 0, -cy, 0, 0],                   # point C moves with BC: vx - w cy = 0
        [0, 1, cx, 0, 0],                    # vy + w cx = u
    ]
    return solve_linear(rows, [0, 0, 0, 0, speed])
