"""ข้อ 4 — มีทางเดินประดับไฟอย่างน้อย 11 เส้นที่เป็นวัสดุเดียวกัน  (พิสูจน์)

With 2r + 1 gates, the chord from gate i to gate i + r has r − 1 gates on one
side and r on the other, so r(r − 1) crossings (90 for 21 gates): pigeonhole on
the two pot kinds gives at least r(r − 1)/2 = 45 of one kind, so all 2r + 1 such
chords are lit, and r + 1 of them share a material. The solver returns r + 1.

``check`` counts, for every chord, how many chords cross it; collects the chords
certain to be lit (crossings ≥ 2T − 1 with T = r(r − 1)/2); and confirms on
random materials, by placing the pots, that at least ⌈lit/2⌉ lit chords of one
material appear. It returns ⌈lit/2⌉.
"""

from __future__ import annotations

from itertools import combinations
from random import Random

PARAMS = {"gates": 21}
ANSWER = 11
VARIANTS = [{"gates": 5}, {"gates": 9}, {"gates": 13}]


def solve(gates=21):
    return (gates + 1) // 2


def _cross(c1, c2):
    a, b = c1
    x, y = c2
    if len({a, b, x, y}) < 4:
        return False
    return (a < x < b) != (a < y < b)


def check(gates=21):
    r = (gates - 1) // 2
    threshold = r * (r - 1) // 2
    chords = list(combinations(range(gates), 2))
    crossing = {c: [d for d in chords if _cross(c, d)] for c in chords}
    certain = [c for c in chords if len(crossing[c]) >= 2 * threshold - 1]
    guarantee = -(-len(certain) // 2)
    rng = Random(2564)
    for _ in range(30):
        material = {c: rng.randrange(2) for c in chords}
        lit = [c for c in chords
               if max(sum(material[c] == material[d] for d in crossing[c]),
                      sum(material[c] != material[d] for d in crossing[c])) >= threshold]
        per = [sum(1 for c in lit if material[c] == m) for m in (0, 1)]
        assert max(per) >= guarantee
    return guarantee
