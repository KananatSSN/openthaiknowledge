"""ข้อ 25 — ค่าของ (1·2·3·4) ⊕ (2·3·4·5) ⊕ ⋯ ⊕ (18·19·20·21)

สำหรับจำนวนจริงบวก x, y ใด ๆ กำหนดให้ x ⊕ y = xy/(x+y) ซึ่งตัวดำเนินการ ⊕ มี
สมบัติการเปลี่ยนกลุ่ม นั่นคือ x ⊕ y ⊕ z = (x ⊕ y) ⊕ z = x ⊕ (y ⊕ z)
จงหาค่าของ (1·2·3·4) ⊕ (2·3·4·5) ⊕ (3·4·5·6) ⊕ ⋯ ⊕ (18·19·20·21)
(ตอบเป็นเศษส่วนของจำนวนเต็ม โดยไม่จำเป็นต้องเป็นเศษส่วนอย่างต่ำ)

⊕ is the **parallel-resistance** operation, and its whole point is that
reciprocals add:

    1/(x ⊕ y) = 1/x + 1/y

so the associativity the stem hands you is really just the associativity of
addition, and the answer is the reciprocal of Σ 1/tₖ with tₖ = k(k+1)(k+2)(k+3).

Those reciprocals telescope, because

    1/(k(k+1)(k+2)(k+3)) = ⅓·[ 1/(k(k+1)(k+2)) − 1/((k+1)(k+2)(k+3)) ]

leaving Σ = ⅓·(1/6 − 1/(19·20·21)) = 1329/23940, so the value is
23940/1329 = **7980/443** (443 is prime). The stem's "ไม่จำเป็นต้องเป็นเศษส่วน
อย่างต่ำ" is there because 23940/1329 is the form the telescoping hands you.

``solve`` uses the telescoped closed form — two terms, no loop. ``check`` adds
the reciprocals one at a time in exact arithmetic and inverts, which is the
definition rather than the identity.
"""

from __future__ import annotations

from fractions import Fraction

#: terms tₖ = k(k+1)⋯(k+width−1) for k = 1 … terms.
PARAMS = {"terms": 18, "width": 4}
ANSWER = Fraction(7980, 443)
VARIANTS = [
    {"terms": 5, "width": 4},
    {"terms": 18, "width": 3},
    {"terms": 10, "width": 2},
    {"terms": 30, "width": 4},
    {"terms": 1, "width": 4},
    {"terms": 7, "width": 5},
]


def solve(terms=18, width=4):
    """Telescoping: Σ 1/tₖ = (1/(width−1))·[1/t'(1) − 1/t'(terms+1)].

    Here t'(k) is the product of the first width−1 factors starting at k, and the
    sum of the reciprocals collapses to its two endpoints.
    """
    if terms < 1 or width < 2:
        return None

    def partial(k):
        value = 1
        for i in range(width - 1):
            value *= k + i
        return value

    total = Fraction(1, width - 1) * (Fraction(1, partial(1))
                                      - Fraction(1, partial(terms + 1)))
    if total == 0:
        return None
    return 1 / total


def check(terms=18, width=4):
    """Independent: fold ⊕ over the list, using its definition each time.

    Nothing telescopes and no reciprocal identity is invoked — the operation
    xy/(x+y) is applied left to right in exact fractions, exactly as the stem
    writes it, so associativity is exercised rather than assumed.
    """
    if terms < 1 or width < 2:
        return None
    if terms > 400:
        return None

    def term(k):
        value = 1
        for i in range(width):
            value *= k + i
        return Fraction(value)

    acc = term(1)
    for k in range(2, terms + 1):
        t = term(k)
        if acc + t == 0:
            return None
        acc = acc * t / (acc + t)
    return acc
