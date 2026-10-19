"""Written9: insulated container initially300ml water and200g ice at0C, add metal1000g c2J/gK, equilibrium10C all ice melted. Water c4.2, ice latent335J/g. Metal initial54C."""

from fractions import Fraction


def solve(water_g=300, ice_g=200, metal_g=1000, metal_c=2, final=10, water_c=4.2, latent=335):
    absorbed = ice_g * latent + (water_g + ice_g) * Fraction(str(water_c)) * final
    return final + absorbed / (metal_g * Fraction(str(metal_c)))


def check(water_g=300, ice_g=200, metal_g=1000, metal_c=2, final=10, water_c=4.2, latent=335):
    # Zero enthalpy: liquid water at0C; ice initial enthalpy -mL.
    final_enthalpy = (water_g + ice_g) * water_c * final + metal_g * metal_c * final
    lo, hi = final, 10000.0
    for _ in range(100):
        initial_metal = (lo + hi) / 2
        initial_enthalpy = -ice_g * latent + metal_g * metal_c * initial_metal
        if initial_enthalpy < final_enthalpy:
            lo = initial_metal
        else:
            hi = initial_metal
    return (lo + hi) / 2


PARAMS = {
    "water_g": 300,
    "ice_g": 200,
    "metal_g": 1000,
    "metal_c": 2,
    "final": 10,
    "water_c": 4.2,
    "latent": 335,
}
VARIANTS = [{"final": 20}, {"ice_g": 100}, {"metal_g": 2000}]
ANSWER = Fraction(54, 1)
