"""Part2 item 10: v^2 = gamma P / rho with P/rho = R T / M for an ideal gas, T = t + 273: v^2/gamma = R (t + 273)/M. SI units, M in g/mol."""


def solve(celsius=27, molar=29, gas=8.3):
    return gas * (celsius + 273) / (molar / 1000)


def check(celsius=27, molar=29, gas=8.3, pressure=1e5):
    # Density of one cubic metre from the ideal gas law, then P/rho.
    moles = pressure / (gas * (celsius + 273))
    density = moles * molar / 1000
    return pressure / density


PARAMS = {"celsius": 27, "molar": 29, "gas": 8.3}
VARIANTS = [{"celsius": 0}, {"molar": 4, "celsius": 127}, {"molar": 2, "celsius": -73}]
ANSWER = 85862.06896551723
