"""MC14: 1 g of water boiled to steam at 100 C and pressure P; volume ratio to 1 g of cold water (1 cm^3) is (373/18)(R/P) x 10^6 (answer 2). Adapted: steam at t C; returns the ratio for R = 8.314, P = 1.01325e5 Pa."""

GAS = 8.314
ATM = 1.01325e5


def solve(celsius=100):
    return (celsius + 273) / 18 * GAS / ATM * 1e6


def check(celsius=100):
    # Molar volume at STP (22.414 L) scaled by Charles's law, in litres per
    # mole, for 1/18 mol, against 1 mL of liquid water.
    stp_litres = GAS * 273.15 / ATM * 1000
    litres = stp_litres * (celsius + 273) / 273.15 / 18
    return litres * 1000


PARAMS = {"celsius": 100}
VARIANTS = [{"celsius": 120}, {"celsius": 150}, {"celsius": 200}]
ANSWER = 1700.3163637360528
