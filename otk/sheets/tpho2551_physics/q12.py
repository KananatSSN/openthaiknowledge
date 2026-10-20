"""Theory 3.3.1 figure: string intact and wedge free; solving the block, wedge-and-pulley and pulley equations gives a_A = 1.08 m/s^2 for the paper's masses. Adapted: masses vary; g = 9.80."""


def solve(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    from otk.sheets.tpho2551_physics._newton import intact

    return intact(wedge, block, pulley, sine, g)[0]


def check(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    from otk.sheets.tpho2551_physics._wedge import lagrange

    return lagrange(wedge + pulley, block, pulley / 2, sine, g)[0]


PARAMS = {"wedge": 10.0, "block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"wedge": 4.0}, {"block": 8.0, "pulley": 1.0}, {"sine": 0.8}]
ANSWER = 1.0788990825688078
TOL = 1e-9
