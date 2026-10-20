"""Theory 3.1 figures 3.1-3.2: a voltage doubler (C - D1 - C with D2 to ground) driven by V0 sin(2 pi t/T) from rest; the table of V_b, V_d, q, Q at quarter periods continues (in units V0 and C V0) with position 4: V_b 0, V_d 1/2, q 1, Q 1/2; position 5: V_b 3/4, V_d 3/4, q 3/4, Q 3/4; position 6: V_b 5/4, V_d 5/4, q 1/4, Q 5/4. Adapted: returns one entry; quantity is 'Vb', 'Vd', 'q' or 'Q' and position 2-6."""


def _table(position):
    # Step model at each quarter period (C = V0 = 1, q = C (V_b - V_a)):
    # D2 clamps b to 0 when it would go negative; when b rises above d, D1
    # joins them and the charge q + Q on the b-d node is shared.
    q = big_q = 0.0
    vb = vd = 0.0
    sources = {1: 0.0, 2: 1.0, 3: 0.0, 4: -1.0, 5: 0.0, 6: 1.0}
    for k in range(2, position + 1):
        va = sources[k]
        if va + q < 0:        # D2 conducts: b held at 0
            vb, q = 0.0, -va
        elif va + q > vd:     # D1 conducts: b and d share charge
            v = (q + big_q + va) / 2
            vb = vd = v
            q, big_q = v - va, v
        else:                 # both off
            vb = va + q
    return {"Vb": vb, "Vd": vd, "q": q, "Q": big_q}


def solve(position=6, quantity="Q"):
    return _table(position)[quantity]


def check(position=6, quantity="Q", steps=200000):
    # Time-step the circuit with stiff ideal-diode resistances (C = V0 = 1,
    # T = 1) and read the state at the quarter periods.
    from math import pi, sin

    r_on, r_off = 1e-4, 1e9
    vc1 = 0.0   # voltage across C1, b minus a (q = C (V_b - V_a))
    vd = 0.0
    dt = 1.0 / steps
    for i in range(int(steps * position / 4 - steps / 4) + 1):
        t = i * dt
        va = sin(2 * pi * t)
        vb = va + vc1
        i2 = (0 - vb) / (r_on if vb < 0 else r_off)          # through D2 into b
        i1 = (vb - vd) / (r_on if vb > vd else r_off)        # through D1 out of b
        vc1 += (i2 - i1) * dt
        vd += i1 * dt
    va = sin(2 * pi * (position - 1) / 4)
    state = {"Vb": va + vc1, "Vd": vd, "q": vc1 if position > 1 else 0.0, "Q": vd}
    return state[quantity]


PARAMS = {"position": 6, "quantity": "Q"}
VARIANTS = [{"position": 4, "quantity": "q"}, {"position": 5, "quantity": "Vb"}, {"position": 6, "quantity": "q"}]
ANSWER = 1.25
TOL = 1e-2
