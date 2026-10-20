"""Lab part 4: the drag b v = sigma Lambda v, so sigma = b/Lambda; b = 0.466 kg/s and Lambda = 1.5e-8 give 3.1e7 S/m. Adapted: b and Lambda (units of 1e-8) vary; returns sigma in units of 1e7 S/m."""


def solve(damping=0.466, shape=1.5):
    return damping / (shape * 1e-8) / 1e7


def check(damping=0.466, shape=1.5, mass=0.0174):
    # Through the time constant: tau = m/b, and the drag per unit speed
    # m/tau equals sigma Lambda.
    tau = mass / damping
    return mass / tau / (shape * 1e-8) / 1e7


PARAMS = {"damping": 0.466, "shape": 1.5}
VARIANTS = [{"damping": 0.30}, {"shape": 2.0}, {"damping": 0.55, "shape": 1.2}]
ANSWER = 3.1066666666666665
TOL = 1e-9
