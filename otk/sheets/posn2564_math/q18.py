"""ข้อ 18 — มีคนพูดจริงในห้องนี้อยู่กี่คน

ในห้องเรียนแห่งหนึ่งมีนักเรียนทั้งหมด 24 คน นักเรียนแต่ละคนจะพูดข้อความต่อกัน
ทีละคน ดังนี้
    คนที่ 1 "ไม่มีใครในห้องนี้พูดจริงเลย"
    คนที่ 2 "ในห้องนี้มีคนพูดจริงอย่างมาก 1 คน"
    คนที่ 3 "ในห้องนี้มีคนพูดจริงอย่างมาก 2 คน"   ⋮
    คนที่ 24 "ในห้องนี้มีคนพูดจริงอย่างมาก 23 คน"
จงหาว่า มีคนที่พูดจริงในห้องนี้อยู่กี่คน

Person k asserts "at most k − 1 tell the truth". If exactly t do, that assertion
is true precisely when t ≤ k − 1, i.e. for k = t+1, …, n — which is **n − t**
true statements. But the truth-tellers *are* the speakers of the true
statements, so

    t = n − t   ⟹   t = n/2 = **12**

and the answer exists only when n is even: with an odd roll call the room is
inconsistent, nobody can be speaking. That is a real feature of the item rather
than an edge case to paper over.

``solve`` uses that fixed point. ``check`` assumes nothing: for each candidate t
it labels every one of the n statements true or false by evaluating it against t,
counts the true ones, and keeps t only if the count comes back to t.
"""

from __future__ import annotations

#: n students; person k claims "at most k − 1 tell the truth".
PARAMS = {"n": 24}
ANSWER = 12
VARIANTS = [
    {"n": 10},
    {"n": 100},
    {"n": 2},
    {"n": 7},          # odd: no consistent assignment
    {"n": 40},
    {"n": 1},
]


def solve(n=24):
    """t = n/2, when that is a whole number."""
    if n < 1:
        return None
    if n % 2:
        return None            # an odd room has no consistent count
    return n // 2


def check(n=24):
    """Independent: test every candidate count against all n statements."""
    if n < 1:
        return None
    consistent = []
    for t in range(n + 1):
        # statement k (1-indexed) is "at most k − 1 tell the truth"
        truths = sum(1 for k in range(1, n + 1) if t <= k - 1)
        if truths == t:
            consistent.append(t)
    if len(consistent) != 1:
        return None
    return consistent[0]
