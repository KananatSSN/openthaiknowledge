"""MC11: ice (0.92 g/cm^3, 200 cm^3) floats in water in a cup of section 100 cm^2; melting leaves the level unchanged (answer 1). Adapted: the liquid may be denser (brine of density rho); the level rises by m (1/rho_water - 1/rho) / A. cm."""


def solve(ice_density=0.92, volume=200, area=100, liquid=1.0, water=1.0):
    mass = ice_density * volume
    return mass * (1 / water - 1 / liquid) / area


def check(ice_density=0.92, volume=200, area=100, liquid=1.0, water=1.0):
    # Before: submerged volume from flotation. After: the melt water mixes in
    # as its own volume (no change in mixing volume assumed). Level change is
    # the change in occupied volume over the area.
    mass = ice_density * volume
    before = mass / liquid
    after = mass / water
    return (after - before) / area


PARAMS = {"ice_density": 0.92, "volume": 200, "area": 100, "liquid": 1.0}
VARIANTS = [{"liquid": 1.15}, {"liquid": 1.25, "volume": 500, "area": 50}, {"liquid": 1.2, "ice_density": 0.9}]
ANSWER = 0.0
