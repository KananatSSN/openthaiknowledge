"""Source p11, MC39: 25 to 50 Celsius does not double absolute T (ค)."""


def solve(factor=2, initial_celsius=25, final_celsius=50):
    # The first, second and fourth ideal-gas claims use linear dependence.
    ratios = (factor, factor, (final_celsius + 273.15) /
              (initial_celsius + 273.15), factor)
    stated = (factor, factor, factor, factor)
    false = [i for i, (actual, claim) in enumerate(zip(ratios, stated))
             if abs(actual - claim) > 1e-9]
    assert len(false) == 1
    return false[0]


def check(factor=2, initial_celsius=25, final_celsius=50):
    # PV=nRT and rho=PM/(RT), independently evaluated at two states.
    initial_k = initial_celsius + 273.15
    final_k = final_celsius + 273.15
    base_p = base_n = 1.0
    base_t = initial_k
    base_v = base_n * base_t / base_p
    ratios = (
        (factor * base_n * base_t / base_p) / base_v,
        (factor * base_p / base_t) / (base_p / base_t),
        (base_n * final_k / base_v) / (base_n * base_t / base_v),
        (factor * base_n * base_t / base_v) / (base_n * base_t / base_v),
    )
    return next(i for i, actual in enumerate(ratios)
                if abs(actual - factor) > 1e-9)


PARAMS = {"factor": 2, "initial_celsius": 25, "final_celsius": 50}
VARIANTS = [
    {"factor": 2, "initial_celsius": 20, "final_celsius": 40},
    {"factor": 3, "initial_celsius": 30, "final_celsius": 90},
    {"factor": 4, "initial_celsius": 10, "final_celsius": 40},
]
ANSWER = 2
