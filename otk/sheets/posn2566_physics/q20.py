"""MC20: each fusion chain 4 H -> He + 2 e+ + 2 gamma + 2 nu releases 26 MeV ~ 42e-13 J; the Sun gives 3.8e26 W, so it emits 2 x 3.8e26 / 42e-13 ~ 1.8e38 ~ 2 x 10^38 neutrinos per second (answer 4). Returns the count per second."""


def solve(power=3.8e26, energy=42e-13, per_reaction=2):
    return per_reaction * power / energy


def check(power=3.8e26, energy=42e-13, per_reaction=2):
    # Count reactions over one hour, then neutrinos, then divide by the hour.
    reactions = power * 3600 / energy
    return reactions * per_reaction / 3600


PARAMS = {"power": 3.8e26, "energy": 42e-13, "per_reaction": 2}
VARIANTS = [{"power": 1e26}, {"energy": 4e-12, "power": 8e26}, {"per_reaction": 1}]
ANSWER = 1.8095238095238098e+38
