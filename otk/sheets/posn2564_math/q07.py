"""ข้อ 7 — ทีม G แข่งไปแล้วกี่นัด

ในการแข่งขันฟุตบอลแบบพบกันหมด มีทีมเข้าร่วมแข่งขันทั้งหมด 7 ทีม ได้แก่ทีม
A B C D E F และ G เมื่อการแข่งขันดำเนินไปได้ระยะหนึ่งพบว่า ทีม A แข่งไปแล้ว
6 นัด ทีม B แข่งไปแล้ว 5 นัด ทีม C แข่งไปแล้ว 4 นัด ทีม D แข่งไปแล้ว 3 นัด
ทีม E แข่งไปแล้ว 2 นัด และทีม F แข่งไปแล้ว 1 นัด จงหาว่าทีม G แข่งไปแล้วกี่นัด

The played-matches counts are the degrees of a graph on 7 vertices, so the
question is which value of deg(G) makes the sequence **realisable**. Parity
alone is not enough: 6+5+4+3+2+1 = 21 is odd, so deg(G) must be odd, but that
leaves 1, 3 and 5 as candidates.

The peeling argument settles it. A has played everyone, so A is a neighbour of
all six others; F has played once, and that once must be A. Removing the pair
leaves 4, 3, 2, 1 and deg(G) − 1 on five teams, and repeating the argument twice
more forces **deg(G) = 3**.

``solve`` tests each candidate with the Erdős–Gallai inequalities — a criterion,
not a construction. ``check`` uses Havel–Hakimi instead, which repeatedly
*builds* the graph by connecting the highest-degree vertex to the next ones and
fails if it ever runs out. Two different theorems, and they must agree on which
single value survives.
"""

from __future__ import annotations

#: the printed degrees, in team order, with the last team's degree unknown.
PARAMS = {"degrees": (6, 5, 4, 3, 2, 1), "teams": 7}
ANSWER = 3
VARIANTS = [
    {"degrees": (4, 3, 2, 1), "teams": 5},
    {"degrees": (5, 4, 3, 2, 1), "teams": 6},
    {"degrees": (8, 7, 6, 5, 4, 3, 2, 1), "teams": 9},
    {"degrees": (2, 2, 2), "teams": 4},
    {"degrees": (6, 6, 4, 3, 2, 1), "teams": 7},     # nothing works
    {"degrees": (3, 2, 2, 1), "teams": 5},
]


def _erdos_gallai(seq):
    """True when the (non-increasing) sequence is graphical."""
    seq = sorted(seq, reverse=True)
    n = len(seq)
    if any(d < 0 or d > n - 1 for d in seq):
        return False
    if sum(seq) % 2:
        return False
    for k in range(1, n + 1):
        left = sum(seq[:k])
        right = k * (k - 1) + sum(min(d, k) for d in seq[k:])
        if left > right:
            return False
    return True


def solve(degrees=(6, 5, 4, 3, 2, 1), teams=7):
    """The one unknown degree that makes the whole sequence graphical."""
    degrees = tuple(degrees)
    if teams != len(degrees) + 1 or teams < 2:
        return None
    good = [g for g in range(teams) if _erdos_gallai(degrees + (g,))]
    if len(good) != 1:
        return None                # ambiguous or impossible: not a question
    return good[0]


def _havel_hakimi(seq):
    """True when the sequence can actually be built, by repeated construction."""
    seq = list(seq)
    while True:
        seq = sorted((d for d in seq if d), reverse=True)
        if not seq:
            return True
        head, rest = seq[0], seq[1:]
        if head > len(rest):
            return False
        for i in range(head):
            rest[i] -= 1
            if rest[i] < 0:
                return False
        seq = rest


def check(degrees=(6, 5, 4, 3, 2, 1), teams=7):
    """Independent: Havel–Hakimi builds the graph instead of testing a bound."""
    degrees = tuple(degrees)
    if teams != len(degrees) + 1 or teams < 2:
        return None
    good = [g for g in range(teams)
            if sum(degrees) + g == 2 * ((sum(degrees) + g) // 2)
            and max(degrees + (g,)) <= teams - 1
            and _havel_hakimi(degrees + (g,))]
    if len(good) != 1:
        return None
    return good[0]
