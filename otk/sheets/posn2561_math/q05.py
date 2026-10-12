"""ข้อ 5 — จำนวนเต็มบวก n ที่ทำให้ n² + 9 หารด้วย 5 ลงตัว

มีจำนวนเต็มบวก n ตั้งแต่ 1 ถึง 200 ทั้งหมดกี่จำนวน ที่ n² + 9 หารด้วย 5 ลงตัว

Only ``n mod 5`` matters. Squaring the five residues gives 0, 1, 4, 4, 1, so

    n² + 9 ≡ 0 (mod 5)  ⟺  n² ≡ −9 ≡ 1 (mod 5)  ⟺  n ≡ 1 or 4 (mod 5)

Two residues out of five qualify, and 200 is a whole number of complete cycles,
so the count is ``200 · 2/5 =`` **80**.

The shortcut worth noticing is that 9 ≡ 4 and −4 ≡ 1, so the condition is just
"n is one away from a multiple of 5" — the squares mod 5 are only ever 0, 1 or 4,
which is why so many shifts give no solutions at all.

``solve`` counts the good residues once and multiplies by the complete cycles,
adding the ragged tail. ``check`` tests every n from 1 to the limit against the
printed condition.
"""

from __future__ import annotations

#: n runs 1..limit, and the condition is (n^power + shift) ≡ 0 mod modulus.
PARAMS = {"limit": 200, "shift": 9, "modulus": 5, "power": 2}
ANSWER = 80
VARIANTS = [
    {"limit": 200, "shift": 1, "modulus": 5, "power": 2},
    {"limit": 100, "shift": 9, "modulus": 5, "power": 2},
    {"limit": 203, "shift": 9, "modulus": 5, "power": 2},   # a ragged tail
    {"limit": 200, "shift": 2, "modulus": 5, "power": 2},   # no residue works
    {"limit": 300, "shift": 4, "modulus": 7, "power": 3},
    {"limit": 200, "shift": 9, "modulus": 1, "power": 2},   # everything divides
]


def solve(limit=200, shift=9, modulus=5, power=2):
    """Count the good residues, then multiply by the complete cycles."""
    if limit < 1 or modulus < 1 or power < 1:
        return None
    good = [r for r in range(modulus) if (pow(r, power, modulus) + shift)
            % modulus == 0]
    whole, tail = divmod(limit, modulus)
    count = whole * len(good)
    for r in good:
        # the tail covers whole·modulus + 1 … limit
        count += sum(1 for extra in range(1, tail + 1)
                     if extra % modulus == r)
    return count


def check(limit=200, shift=9, modulus=5, power=2):
    """Independent: test every n against the printed condition.

    ``n**power + shift`` is formed for each n from 1 to the limit and divided by
    the modulus — no residue argument, no cycle counting, and the ragged tail
    takes care of itself.
    """
    if limit < 1 or modulus < 1 or power < 1:
        return None
    if limit > 2 * 10 ** 6:
        return None
    return sum(1 for n in range(1, limit + 1)
               if (n ** power + shift) % modulus == 0)
