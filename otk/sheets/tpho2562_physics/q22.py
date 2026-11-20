"""Lab part 2.2: eV_t = hc/lambda - E0 with E0 the same for every LED, so V_t against 1/lambda is a straight line of slope hc/e; the infrared LED's threshold then gives lambda = slope/(V_t - intercept). Synthetic thresholds (E0 = 0.30 eV) for violet, blue, green, orange and red LEDs and 1.16 V for the infrared one give about 850 nm. Adapted: the readings vary; returns nanometres."""

LAMBDAS = (405.0, 455.0, 525.0, 600.0, 630.0)
THRESHOLDS = (2.77, 2.43, 2.07, 1.77, 1.67)


def solve(lambdas=LAMBDAS, thresholds=THRESHOLDS, infrared=1.16):
    from otk.sheets.tpho2562_physics._shared import line

    slope, intercept = line([1 / x for x in lambdas], thresholds)
    return slope / (infrared - intercept)


def check(lambdas=LAMBDAS, thresholds=THRESHOLDS, infrared=1.16):
    from otk.sheets.tpho2562_physics._shared import centred_line

    slope, intercept = centred_line([1 / x for x in lambdas], thresholds)
    return 1 / ((infrared - intercept) / slope)


PARAMS = {"lambdas": LAMBDAS, "thresholds": THRESHOLDS, "infrared": 1.16}
VARIANTS = [{"infrared": 1.30}, {"thresholds": (2.67, 2.33, 1.97, 1.67, 1.57)}, {"infrared": 1.05}]
ANSWER = 849.7242111063281
TOL = 1e-9
