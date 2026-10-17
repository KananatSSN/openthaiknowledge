"""ข้อ 2 — ลำดับจำนวนเต็มบวกที่ (n² + 1)aₙ₊₁ − aₙ = n³ + n² + 1

For the family (n² + c)aₙ₊₁ − aₙ = n³ + (s + 1)n² + (c − 1)n + c + s(c − 1), aₙ = n + s
solves it. Modulo n² + c, aₙ ≡ n + s, so aₙ = n + s + (n² + c)bₙ with bₙ ≥ 0, and
the recurrence makes bₙ decrease by a factor larger than 1 unless all bₙ = 0. The
source (c = 1, s = 0) gives aₙ = n. The solver returns a_k.

``check`` tries every start a₁ ≤ 400, runs the recurrence forward 40 steps,
keeps the starts whose terms stay positive integers, and returns a_k from the
one survivor.
"""

from __future__ import annotations

PARAMS = {"constant": 1, "shift": 0, "index": 6}
ANSWER = 6
VARIANTS = [{"constant": 2, "shift": 3, "index": 5}, {"constant": 5, "shift": 1, "index": 9},
            {"constant": 7, "shift": 4, "index": 12}]


def solve(constant=1, shift=0, index=6):
    return index + shift


def _rhs(n, c, s):
    return n**3 + (s + 1) * n * n + (c - 1) * n + c + s * (c - 1)


def check(constant=1, shift=0, index=6):
    survivors = []
    for a1 in range(1, 401):
        seq, ok = [a1], True
        for n in range(1, 41):
            num = _rhs(n, constant, shift) + seq[-1]
            if num % (n * n + constant):
                ok = False
                break
            seq.append(num // (n * n + constant))
        if ok:
            survivors.append(seq)
    assert len(survivors) == 1
    return survivors[0][index - 1]
