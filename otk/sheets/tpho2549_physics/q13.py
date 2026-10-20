"""Lab 2 figure: a Chinese steelyard balances empty with the sliding weight M at the zero mark x0 from the pivot; an object hung d from the pivot on the other side balances with M at x, so m = M (x - x0)/d. Adapted: synthetic M, d, x0, x; grams."""


def solve(slider=20, hook=4, zero=3, mark=13):
    return slider * (mark - zero) / hook


def check(slider=20, hook=4, zero=3, mark=13, beam=50.0):
    # Torques about the pivot (slider side positive, object at -d). The beam's
    # own weight B acts at some arm b; the empty balance fixes B b.
    beam_torque = -slider * zero          # B b + M x0 = 0
    # Loaded: B b + M x - m d = 0
    return (beam_torque + slider * mark) / hook


PARAMS = {"slider": 20, "hook": 4, "zero": 3, "mark": 13}
VARIANTS = [{"zero": 0}, {"slider": 10, "hook": 5, "mark": 40}, {"hook": 2.5, "mark": 8}]
ANSWER = 50.0
TOL = 1e-12
