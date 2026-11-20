"""Source p10, MC33: cooling does not weaken the fixed-distance force law.

Choice ง is false. The adaptation specifies the same liquid and a fixed
molecular separation for the force statement to avoid conflating force
strength with changing average molecular spacing.
"""

from math import exp

_EXPECTED = {
    "cool": {"vapor_pressure": "decrease", "surface_tension": "increase",
             "kinetic_energy": "decrease", "fixed_distance_attraction": "same"},
    "warm": {"vapor_pressure": "increase", "surface_tension": "decrease",
             "kinetic_energy": "increase", "fixed_distance_attraction": "same"},
}


def solve(direction="cool", claims=(("vapor_pressure", "decrease"),
                                    ("surface_tension", "increase"),
                                    ("kinetic_energy", "decrease"),
                                    ("fixed_distance_attraction", "decrease"))):
    wrong = [i for i, (property_, trend) in enumerate(claims)
             if _EXPECTED[direction][property_] != trend]
    assert len(wrong) == 1
    return wrong[0]


def check(direction="cool", claims=(("vapor_pressure", "decrease"),
                                    ("surface_tension", "increase"),
                                    ("kinetic_energy", "decrease"),
                                    ("fixed_distance_attraction", "decrease"))):
    before, after = 300.0, (280.0 if direction == "cool" else 320.0)

    def properties(temperature):
        return {
            "vapor_pressure": exp(-5000 / temperature),
            "surface_tension": 100 - 0.1 * temperature,
            "kinetic_energy": 1.5 * temperature,
            "fixed_distance_attraction": 1.0,
        }

    initial, final = properties(before), properties(after)
    actual = {name: ("increase" if final[name] > initial[name]
                     else "decrease" if final[name] < initial[name] else "same")
              for name, _ in claims}
    wrong = [i for i, (name, trend) in enumerate(claims) if actual[name] != trend]
    assert len(wrong) == 1
    return wrong[0]


PARAMS = {"direction": "cool", "claims": (
    ("vapor_pressure", "decrease"), ("surface_tension", "increase"),
    ("kinetic_energy", "decrease"), ("fixed_distance_attraction", "decrease"),
)}
VARIANTS = [
    {"direction": "cool", "claims": (
        ("vapor_pressure", "increase"), ("surface_tension", "increase"),
        ("kinetic_energy", "decrease"), ("fixed_distance_attraction", "same"))},
    {"direction": "cool", "claims": (
        ("surface_tension", "decrease"), ("kinetic_energy", "decrease"),
        ("fixed_distance_attraction", "same"), ("vapor_pressure", "decrease"))},
    {"direction": "warm", "claims": (
        ("vapor_pressure", "increase"), ("surface_tension", "decrease"),
        ("kinetic_energy", "decrease"), ("fixed_distance_attraction", "same"))},
]
ANSWER = 3
