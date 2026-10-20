"""Theory 1.2 b): a beam of power P carries P dt of energy in photons of hc/lambda each, so P lambda dt/(hc) photons enter in dt. Adapted: the power (mW), wavelength (nm) and time (ns) vary, with h = 6.63e-34 J s and c = 3.00e8 m/s; returns the count."""


def solve(power=10.0, wavelength=1064.0, time=1.0):
    from otk.sheets.tpho2563_physics._shared import C, H_PLANCK

    return power * 1e-3 * wavelength * 1e-9 * time * 1e-9 / (H_PLANCK * C)


def check(power=10.0, wavelength=1064.0, time=1.0):
    from otk.sheets.tpho2563_physics._shared import C, H_PLANCK

    frequency = C / (wavelength * 1e-9)
    return power * 1e-3 * time * 1e-9 / (H_PLANCK * frequency)


PARAMS = {"power": 10.0, "wavelength": 1064.0, "time": 1.0}
VARIANTS = [{"power": 50.0}, {"wavelength": 532.0}, {"time": 10.0}]
ANSWER = 53494218.20010056
TOL = 1e-9
