"""Lab part 4: the lamp's radiant power differs by wavelength, so the LDR's relative response is E_lambda divided by the lamp's relative power there; at 494 nm and 651 nm (0.0204/56 against 0.0359/166) the response falls to 0.59 of its 494 nm value. Adapted: two illuminances and the lamp's two relative powers vary; returns the ratio of the corrected responses (second over first)."""


def solve(first=0.0204, power1=56.0, second=0.0359, power2=166.0):
    return (second / power2) / (first / power1)


def check(first=0.0204, power1=56.0, second=0.0359, power2=166.0):
    # Scale both readings to a common lamp power of 100 units, then compare.
    return (second * 100 / power2) / (first * 100 / power1)


PARAMS = {"first": 0.0204, "power1": 56.0, "second": 0.0359, "power2": 166.0}
VARIANTS = [{"second": 0.0385, "power2": 147.0}, {"first": 0.0229, "power1": 73.0}, {"second": 0.0266, "power2": 199.0}]
ANSWER = 0.5936687928183322
TOL = 1e-12
