"""Theory 2 h), j): demagnetising adiabatically keeps the entropy, a function of mu B/(k_B T) alone, so T_f = (B_L/B_H) T_i: 2 mK from 1 K and 1 T with B_L = 2 mT. Adapted: T_i (K), B_H (T) and B_L (mT) vary; returns mK."""


def solve(start=1.0, high=1.0, low=2.0):
    return low * 1e-3 / high * start * 1e3


def check(start=1.0, high=1.0, low=2.0):
    from math import exp, log

    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN, bisect, two_level_entropy

    # the final temperature whose entropy at B_L equals the entropy at B_H and T_i
    target = two_level_entropy(BOHR * high / (BOLTZMANN * start))

    def miss(log_t):
        return two_level_entropy(BOHR * low * 1e-3 / (BOLTZMANN * exp(log_t))) - target

    return exp(bisect(miss, log(1e-9), log(1e3))) * 1e3


PARAMS = {"start": 1.0, "high": 1.0, "low": 2.0}
VARIANTS = [{"start": 0.3}, {"high": 5.0}, {"low": 10.0}]
ANSWER = 2.0
TOL = 1e-6
