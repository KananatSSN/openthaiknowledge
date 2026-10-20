"""Theory 3.7: the Einstein ring MG1654+1346 of angular radius 1.05 arcsec, with the quasar 3300 Mpc and the galaxy 940 Mpc away (so d1 = 2360 Mpc), gives M = beta^2 c^2 d2(d1 + d2)/(4G d1) = 3.55e41 kg. Adapted: the ring radius (arcsec) and both distances from Earth (Mpc) vary; returns 1e41 kg."""

from math import pi


def solve(ring=1.05, quasar=3300.0, galaxy=940.0):
    from otk.sheets.tpho2563_physics._shared import C, G, PARSEC

    beta = ring / 3600 * pi / 180
    d2, d1 = galaxy * 1e6 * PARSEC, (quasar - galaxy) * 1e6 * PARSEC
    return beta**2 * C**2 * d2 * (d1 + d2) / (4 * G * d1) / 1e41


def check(ring=1.05, quasar=3300.0, galaxy=940.0):
    from math import exp, log

    from otk.sheets.tpho2563_physics import q14
    from otk.sheets.tpho2563_physics._shared import bisect

    # the mass whose Fermat image sits at the measured ring
    def miss(log_m):
        return q14.check(mass=exp(log_m), source=quasar - galaxy, observer=galaxy) - ring

    return exp(bisect(miss, log(1e-3), log(1e3), n=60))


PARAMS = {"ring": 1.05, "quasar": 3300.0, "galaxy": 940.0}
VARIANTS = [{"ring": 0.8}, {"galaxy": 1500.0}, {"quasar": 5000.0}]
ANSWER = 3.545771363411483
TOL = 1e-6
