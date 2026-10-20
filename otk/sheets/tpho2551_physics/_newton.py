"""Shared Newton's-law system for problem 3.3 (string intact, wedge free)."""

from math import sqrt


def intact(wedge, block, pulley, sine, g):
    """Solve the paper's four equations for (a_A, a_rel, T, N):

    m g s - T = m (a_r - a_A c);  m g c - N = m a_A s;
    N s - T c = (m_A + m_C) a_A;  T = (m_C/2) a_r."""
    c = sqrt(1 - sine * sine)
    m, big, k = block, wedge + pulley, pulley / 2
    # unknowns x = [aA, ar, T, N]
    rows = [
        [-m * c, m, 1.0, 0.0, m * g * sine],
        [m * sine, 0.0, 0.0, 1.0, m * g * c],
        [big, 0.0, c, -sine, 0.0],
        [0.0, -k, 1.0, 0.0, 0.0],
    ]
    for col in range(4):
        pivot = max(range(col, 4), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(4):
            if r != col:
                f = rows[r][col] / rows[col][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[col])]
    return tuple(rows[i][4] / rows[i][i] for i in range(4))
