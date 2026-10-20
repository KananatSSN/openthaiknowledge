"""Theory 1.2 (b): at T0 + Delta T the wire is L0(1 + alpha Delta T) long with modulus Y0 + epsilon Delta T, so Delta L2 = (W/A)(L0 + alpha L0 Delta T)/(Y0 + epsilon Delta T) + alpha L0 Delta T. Adapted: W (N), L0 (m), A (mm^2), Y0 and epsilon (GPa, MPa/K), alpha (1e-6/K) and Delta T vary; returns Delta L2 in mm."""


def solve(weight=100.0, length=2.0, area=1.0, modulus=200.0, slope=50.0, expansion=12.0, warming=20.0):
    W, L0, A = weight, length, area * 1e-6
    Y = modulus * 1e9 + slope * 1e6 * warming
    a = expansion * 1e-6
    return (W / A * (L0 + a * L0 * warming) / Y + a * L0 * warming) * 1e3


def check(weight=100.0, length=2.0, area=1.0, modulus=200.0, slope=50.0, expansion=12.0, warming=20.0):
    # Warm the wire in small steps (length and modulus updated each step),
    # then hang the weight on the warmed wire.
    L, Y = length, modulus * 1e9
    steps = 1000
    dT = warming / steps
    for _ in range(steps):
        L += expansion * 1e-6 * length * dT
        Y += slope * 1e6 * dT
    stretch = weight * L / (area * 1e-6 * Y)
    return (L - length + stretch) * 1e3


PARAMS = {"weight": 100.0, "length": 2.0, "area": 1.0, "modulus": 200.0, "slope": 50.0, "expansion": 12.0, "warming": 20.0}
VARIANTS = [{"warming": 50.0}, {"weight": 300.0, "slope": 80.0}, {"expansion": 20.0}]
ANSWER = 1.47526368159204
TOL = 1e-9
