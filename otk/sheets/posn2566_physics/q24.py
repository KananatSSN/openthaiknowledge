"""Short24: 1 cm^3 of liquid water (1 g, 1/18 mol) boiled to vapour at 267 C and 1e5 Pa occupies nRT/P = 2.49e-3 m^3 = 2490 cm^3 with R = 8.3. Returns cm^3."""


def solve(volume=1, celsius=267, pressure=1e5, gas=8.3):
    moles = volume / 18
    return moles * gas * (celsius + 273) / pressure * 1e6


def check(volume=1, celsius=267, pressure=1e5, gas=8.3):
    # Molecule count and kT: N = moles * N_A, V = N k T / P.
    avogadro = 6.02e23
    boltzmann = gas / avogadro
    molecules = volume / 18 * avogadro
    return molecules * boltzmann * (celsius + 273) / pressure * 1e6


PARAMS = {"volume": 1, "celsius": 267, "pressure": 1e5, "gas": 8.3}
VARIANTS = [{"volume": 2, "celsius": 87}, {"pressure": 2e5}, {"celsius": 627, "volume": 3}]
ANSWER = 2490.0000000000005
