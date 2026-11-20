"""MC13 figure: E in series with R and C to a node; the lower R and the starred C* sit in parallel from that node to the bottom wire; switch SW closes at t = 0 with no charge anywhere. No current flows at steady state, so C* charges then empties: rise to a peak, decay to zero (answer 2). Returns the curve's shape for the named capacitor."""

SHAPES = {"starred": "rise_then_decay", "series": "rise_to_constant"}


def solve(capacitor="starred", emf=1.0, resistance=1.0, capacitance=1.0):
    return SHAPES[capacitor]


def check(capacitor="starred", emf=1.0, resistance=1.0, capacitance=1.0):
    # Simulate: q1 on the series C, q2 on C*. Node voltage v = q2/C.
    # Series branch current i1 = (E - q1/C - v)/R; lower R takes v/R; C* gets
    # i1 - v/R.
    dt, q1, q2 = 2e-4 * resistance * capacitance, 0.0, 0.0
    trace = []
    for _ in range(200000):
        v = q2 / capacitance
        i1 = (emf - q1 / capacitance - v) / resistance
        q1 += i1 * dt
        q2 += (i1 - v / resistance) * dt
        trace.append(q2 if capacitor == "starred" else q1)
    peak = max(trace)
    final = trace[-1]
    negative = min(trace) < -1e-9
    if negative:
        return "oscillating"
    if final < 1e-3 * peak:
        return "rise_then_decay"
    return "rise_to_constant"


PARAMS = {"capacitor": "starred", "emf": 1.0, "resistance": 1.0, "capacitance": 1.0}
VARIANTS = [{"capacitor": "series"}, {"capacitor": "starred", "resistance": 2.0}, {"capacitor": "series", "capacitance": 0.5}]
ANSWER = 'rise_then_decay'
