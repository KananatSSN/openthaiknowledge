"""ข้อ 28 — ผลรวมค่า a ที่ทำให้คำตอบของสมการกำลังสองเป็นจำนวนเต็ม

กำหนดให้ a เป็นจำนวนเต็ม ที่ทำให้สมการ ax² − (3a − 4)x + 2(a − 2) = 0
มีคำตอบทั้งหมดเป็นจำนวนเต็ม จงหาผลรวมของค่า a ที่เป็นไปได้ทั้งหมด

(The original problem asks for the *sum* of possible a values? The DERIVATIONS.md says:
Answer: −4, −2, −1, 0, 1, 2, 4  (set of 7 integers)
Wait, the table says:
"integer a with every root of ... an integer" -> "-4, -2, -1, 0, 1, 2, 4"
The question might ask for the set or the count or the sum.
The table in DERIVATIONS.md says the answer is the set of 7 integers.
Let's return a sorted tuple of the values, as sets are unordered.

The quadratic is ax² − (3a − 4)x + 2(a − 2) = 0.
Notice that x = 1 is a root: a(1) − (3a − 4)(1) + 2(a − 2) = a − 3a + 4 + 2a − 4 = 0.
So it factors: (x − 1)(ax − (2a − 4)) = 0.
The other root is x = (2a − 4)/a = 2 − 4/a.
For this to be an integer, 4/a must be an integer, so a | 4.
The divisors of 4 are ±1, ±2, ±4.
This gives a ∈ {−4, −2, −1, 1, 2, 4}.
What about a = 0?
If a = 0, the equation is −(−4)x + 2(−2) = 0  ⟹  4x − 4 = 0  ⟹  x = 1, which is an integer.
So a = 0 works too!
The set of valid a is {−4, −2, −1, 0, 1, 2, 4}.

``solve`` finds divisors of the constant term of the numerator.
``check`` tests a over a large range by evaluating the discriminant and roots.
"""

from __future__ import annotations

import math

#: a·x² − (3a − c)x + 2(a − c/2) = 0  has integer roots. Find all integer a.
# In general: ax² - (p a + q)x + p_a_q_term = 0
# Let's keep it simple. x=1 is a root: a - (3a - c) + k(a - c/2) = 0
# To generalize, ax² - (k+1)ax + ckx + k a - ck = 0?
# x=1 is a root: a - ((k+1)a - c) + k a - c = a - ka - a + c + ka - c = 0.
# So ax² - ((k+1)a - c)x + k a - c = 0
# Roots are 1 and (ka - c)/a = k - c/a.
# So we need a | c. And a=0 gives cx - c = 0 -> x=1.
PARAMS = {"k": 2, "c": 4}
ANSWER = (-4, -2, -1, 0, 1, 2, 4)
VARIANTS = [
    {"k": 5, "c": 6},
    {"k": 2, "c": 12},
    {"k": 0, "c": 10},
    {"k": -3, "c": 5},
    {"k": 1, "c": 7},
    {"k": 4, "c": 8},
]


def solve(k=2, c=4):
    """x = 1 is a root. The other is k - c/a, so a | c. Also check a=0."""
    if c == 0:
        return None # degenerate, infinitely many a
    
    valid_a = set()
    # a divides c
    for i in range(1, abs(c) + 1):
        if c % i == 0:
            valid_a.add(i)
            valid_a.add(-i)
    # Check a = 0
    # Equation: c * x - c = 0 -> x = 1 (integer)
    valid_a.add(0)
    
    return tuple(sorted(valid_a))


def check(k=2, c=4):
    """Independent: test a range of a and find roots directly."""
    if c == 0:
        return None
    
    valid_a = set()
    for a in range(-abs(c) - 100, abs(c) + 101):
        # Equation: ax² - ((k+1)a - c)x + (ka - c) = 0
        A = a
        B = -((k + 1) * a - c)
        C = k * a - c
        
        if A == 0:
            if B != 0:
                x = -C / B
                if x == int(x):
                    valid_a.add(a)
            elif C == 0:
                pass # infinitely many roots, maybe valid?
            continue
            
        disc = B * B - 4 * A * C
        if disc < 0:
            continue
        
        root_disc = math.isqrt(disc)
        if root_disc * root_disc != disc:
            continue
            
        x1 = (-B + root_disc) / (2 * A)
        x2 = (-B - root_disc) / (2 * A)
        
        if x1 == int(x1) and x2 == int(x2):
            valid_a.add(a)
            
    return tuple(sorted(valid_a))
