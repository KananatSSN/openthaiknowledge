"""วันที่สอง ข้อ 6 — (f(xy))² = f(x²)f(y²) เมื่อ x²y³ > 2008 ⇒ จริงทุก x, y  (พิสูจน์ร่าง)

Along powers of b the relation reads f(b^(2^j)) = f(b^(2^(j−1)))²/f(1), so
f(b^(2^j)) = f(b)^(2^j)/f(1)^(2^j − 1). The solver returns that value
(f(1) = 2, f(b) = 3, j = 3: 6561/128). Extending from x²y³ > 2008 to all x, y
is sketched in the bank note.

``check`` iterates the squaring relation step by step.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"f1": 2, "fb": 3, "steps": 3}
ANSWER = Fraction(6561, 128)
VARIANTS = [{"f1": 1, "fb": 2, "steps": 4}, {"f1": 3, "fb": 2, "steps": 2}, {"steps": 1}]


def solve(f1=2, fb=3, steps=3):
    return Fraction(fb ** (2**steps), f1 ** (2**steps - 1))


def check(f1=2, fb=3, steps=3):
    value = Fraction(fb)
    for _ in range(steps):
        value = value * value / f1
    return value
