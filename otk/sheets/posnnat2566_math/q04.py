"""ข้อ 4 — มีผู้เล่น A, B, C ที่ผลสองนัดเท่ากันแต่นัดที่สามไม่เท่า  (พิสูจน์)

Colour each match by the loser's score (11 colours, at least two used: 0 and
10). If no three players had exactly two equal colours, every triangle would be
monochromatic or rainbow; fixing a player, each colour class of its neighbours
is a clique of that colour, and a counting argument bounds the players by
(q − 1)² = 100 < 101. The bound is sharp when q − 1 is prime (directions in the
affine plane of order q − 1). The solver returns (q − 1)²; PARAMS uses q = 4 so
that ``check`` can prove the bound by search (the source has q = 11).

``check`` colours the affine plane of order q − 1 by line direction and confirms
every triangle is monochromatic or rainbow; for q ≤ 4 it also searches all
colourings of one more player and confirms none works.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"colors": 4}
ANSWER = 9
VARIANTS = [{"colors": 3}, {"colors": 6}, {"colors": 8}]


def solve(colors=4):
    return (colors - 1) ** 2


def _good(a, b, c):
    return a == b == c or len({a, b, c}) == 3


def _affine(m):
    pts = [(x, y) for x in range(m) for y in range(m)]
    colour = {}
    for p, q in combinations(pts, 2):
        dx, dy = (q[0] - p[0]) % m, (q[1] - p[1]) % m
        colour[(p, q)] = m if dx == 0 else dy * pow(dx, -1, m) % m  # slope, or vertical
    for p, q, r in combinations(pts, 3):
        assert _good(colour[(p, q)], colour[(p, r)], colour[(q, r)])
    return len(pts)


def _extendable(n, colors):
    """A colouring of K_n with every triangle mono or rainbow and two colours used."""
    edges = sorted(combinations(range(n), 2), key=lambda e: (e[1], e[0]))  # close triangles early
    col = {}

    def ok(e):
        i, j = e
        for k in range(n):
            if k in (i, j):
                continue
            e1, e2 = tuple(sorted((i, k))), tuple(sorted((j, k)))
            if e1 in col and e2 in col and not _good(col[e], col[e1], col[e2]):
                return False
        return True

    def go(idx, used):
        if idx == len(edges):
            return used >= 2
        e = edges[idx]
        for c in range(min(used + 1, colors)):  # colours introduced in order
            col[e] = c
            if ok(e) and go(idx + 1, max(used, c + 1)):
                return True
            del col[e]
        return False

    return go(0, 0)


def check(colors=4):
    size = _affine(colors - 1)
    if colors <= 4:
        assert _extendable(size, colors)
        assert not _extendable(size + 1, colors)
    return size
