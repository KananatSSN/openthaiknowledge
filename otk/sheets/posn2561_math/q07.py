"""ข้อ 7 — เศษจากการหาร N ด้วย 37

กำหนดให้ N = 737373…73 เป็นจำนวนเต็มที่มี 2560 หลัก ประกอบไปด้วยเลขโดด 7 และ 3
สลับกันอย่างละ 1280 ตัว จงหาเศษจากการหาร N ด้วย 37

N is the block "73" repeated 1280 times, so

    N = 73 · (1 + 100 + 100² + … + 100¹²⁷⁹)

and the whole question is that geometric sum modulo 37. The key fact is
``1000 = 27·37 + 1``, so **10³ ≡ 1 (mod 37)** and the powers of ten cycle with
period three: 1, 10, 26, 1, 10, 26, …

Since ``100^k = 10^{2k}``, the terms cycle 1, 26, 10, 1, 26, 10, … — and one full
period sums to ``1 + 26 + 10 = 37 ≡ 0``. So only the leftover terms matter:
1280 = 3·426 + 2, leaving two terms worth 1 + 26 = 27. Then, since
``73 ≡ 36 ≡ −1 (mod 37)``,

    N ≡ (−1)·27 = −27 ≡ **10 (mod 37)**

Neither 2560 nor 1280 has to be handled as a number — only 1280 mod 3.

``solve`` uses that cycle. ``check`` builds the 2560-digit integer and takes the
remainder directly; Python's big integers make the brute-force route genuinely
available here, which is what makes it worth doing.
"""

from __future__ import annotations

#: the repeated block, how many times, and the divisor.
PARAMS = {"block": "73", "repeats": 1280, "divisor": 37}
ANSWER = 10
VARIANTS = [
    {"block": "73", "repeats": 1279, "divisor": 37},
    {"block": "73", "repeats": 1281, "divisor": 37},
    {"block": "142857", "repeats": 200, "divisor": 37},
    {"block": "73", "repeats": 1280, "divisor": 101},
    {"block": "9", "repeats": 500, "divisor": 7},
    {"block": "73", "repeats": 0, "divisor": 37},        # nothing to divide
]


def solve(block="73", repeats=1280, divisor=37):
    """The remainder, from the cycle of the block's shift modulo the divisor."""
    if repeats < 1 or divisor < 2 or not block.isdigit():
        return None
    value = int(block)
    shift = pow(10, len(block), divisor)          # multiplier per extra block

    # 1 + shift + shift² + … + shift^(repeats−1), found by walking the cycle of
    # powers of ``shift`` rather than by repeated addition.
    seen, powers = {}, []
    current = 1 % divisor
    while current not in seen:
        seen[current] = len(powers)
        powers.append(current)
        current = current * shift % divisor
    offset = seen[current]
    period = len(powers) - offset

    total = sum(powers[:min(offset, repeats)]) % divisor
    if repeats > offset:
        left = repeats - offset
        cycle = powers[offset:]
        whole, tail = divmod(left, period)
        total = (total + whole * sum(cycle) + sum(cycle[:tail])) % divisor
    return value % divisor * total % divisor


def check(block="73", repeats=1280, divisor=37):
    """Independent: build the whole number and divide it.

    The digits are concatenated into one big integer — 2560 of them for the
    sheet's own case — and ``%`` does the work. No modular arithmetic, no cycle,
    no geometric series.
    """
    if repeats < 1 or divisor < 2 or not block.isdigit():
        return None
    if len(block) * repeats > 20000:
        return None
    return int(block * repeats) % divisor
