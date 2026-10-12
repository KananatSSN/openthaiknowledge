"""ข้อ 30 — ค่าความจริงของ f²³ เมื่อรู้ว่า f¹⁶ เป็นเท็จทั้งสาม

สำหรับประพจน์ P, Q และ R ใด ๆ กำหนดรูปแบบของประพจน์
    Q ⊛ R ≡ (Q ∧ ~R) ∨ (R ∧ ~Q)
และให้
    f(P, Q, R) = (P → (Q ⊛ R),  P ∧ (Q ⊛ R),  P ∧ (Q ∨ R))
    fⁿ(P, Q, R) = f(fⁿ⁻¹(P, Q, R))
สมมุติว่า f¹⁶(P, Q, R) = (P₁, Q₁, R₁) และ f²³(P, Q, R) = (P₂, Q₂, R₂)
เมื่อ P₁, Q₁, R₁ มีค่าความจริงเป็นเท็จทั้งหมด  จงหาค่าความจริงของ P₂, Q₂ และ R₂

``Q ⊛ R`` is exclusive or, and the rest is a map of the eight truth-triples into
itself. Nothing about the *original* P, Q, R is needed or knowable: the sheet
hands over the state at step 16, and

    f²³ = f⁷ ∘ f¹⁶

so the answer is seven steps on from (F, F, F).

Those seven steps are two steps repeated, because (F, F, F) sits on a 2-cycle:

    f(F, F, F) = (F → F, F ∧ F, F ∧ F) = (**T**, F, F)
    f(T, F, F) = (T → F, T ∧ F, T ∧ F) = (**F**, F, F)

`P → (Q ⊛ R)` is what flips: with Q and R both false the XOR is false, so the
implication is exactly ¬P, while the two conjunctions stay false forever once Q
and R are. Seven is odd, so

    **f²³ = (T, F, F)** — P₂ true, Q₂ false, R₂ false

``solve`` applies the printed formula step by step. ``check`` never iterates: it
tabulates f over all eight triples, follows that map to decompose the state's
orbit into its tail and cycle, and indexes into the cycle with one modulo — a
different mechanism, and one that also proves the orbit really is periodic
rather than assuming it.
"""

from __future__ import annotations

#: the state at ``known_step``, and the step whose state is wanted.
PARAMS = {"known_step": 16, "target_step": 23,
          "known_state": (False, False, False)}
ANSWER = (True, False, False)
VARIANTS = [
    {"target_step": 24},
    {"target_step": 30},
    {"known_step": 3, "target_step": 10},
    {"known_state": (True, True, False)},
    {"known_state": (True, False, True), "target_step": 25},
    {"known_state": (False, True, True), "known_step": 1, "target_step": 9},
]

STATES = [(p, q, r) for p in (False, True) for q in (False, True)
          for r in (False, True)]


def step(state):
    """One application of the printed f."""
    p, q, r = state
    xor = (q and not r) or (r and not q)
    return ((not p) or xor, p and xor, p and (q or r))


def solve(known_step=16, target_step=23, known_state=(False, False, False)):
    """Apply f the remaining number of times, as printed."""
    if target_step < known_step:
        return None
    state = tuple(bool(v) for v in known_state)
    if len(state) != 3:
        return None
    for _ in range(target_step - known_step):
        state = step(state)
    return state


def check(known_step=16, target_step=23, known_state=(False, False, False)):
    """Independent: tabulate f, then read the answer off the orbit's cycle.

    f is a map on eight points, so every orbit is a tail into a cycle. This
    builds the whole table once, walks the orbit until a state repeats — which
    *establishes* the period instead of assuming one — and then lands on the
    right member with a single modulo. No repeated application of the formula.
    """
    if target_step < known_step:
        return None
    state = tuple(bool(v) for v in known_state)
    if len(state) != 3:
        return None
    table = {s: step(s) for s in STATES}

    orbit = [state]
    seen = {state: 0}
    while True:
        nxt = table[orbit[-1]]
        if nxt in seen:
            tail = seen[nxt]                      # where the cycle starts
            break
        seen[nxt] = len(orbit)
        orbit.append(nxt)

    n = target_step - known_step
    if n < tail:
        return orbit[n]
    period = len(orbit) - tail
    return orbit[tail + (n - tail) % period]
