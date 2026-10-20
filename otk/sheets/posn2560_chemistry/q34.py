"""Source p10, MC34: evaporation is a surface phenomenon (choice ข)."""

_TRUTH = {
    "boil_pressure_up": False, "boil_pressure_down": True,
    "evap_surface": True, "evap_bulk_only": False,
    "iodine_melts_below_room": False, "iodine_melts_above_room": True,
    "salt_vapor_higher": False, "salt_vapor_lower": True,
}


def solve(claims=("boil_pressure_up", "evap_surface", "iodine_melts_below_room",
                  "salt_vapor_higher")):
    matches = [i for i, claim in enumerate(claims) if _TRUTH[claim]]
    assert len(matches) == 1
    return matches[0]


def check(claims=("boil_pressure_up", "evap_surface", "iodine_melts_below_room",
                  "salt_vapor_higher")):
    # Independent physical criteria: boiling when vapor pressure reaches external
    # pressure; evaporation at a free surface; iodine mp 113.7 C; NaCl has a
    # much lower vapor pressure than molecular iodine near room temperature.
    room_celsius = 25.0
    iodine_melting_celsius = 113.7
    # Relative vapor-pressure scale is sufficient for this comparison.
    iodine_vapor = 1.0
    sodium_chloride_vapor = 0.0001
    facts = {
        "boil_pressure_up": 90.0 > 100.0,
        "boil_pressure_down": 90.0 < 100.0,
        "evap_surface": True,
        "evap_bulk_only": False,
        "iodine_melts_below_room": iodine_melting_celsius < room_celsius,
        "iodine_melts_above_room": iodine_melting_celsius > room_celsius,
        "salt_vapor_higher": sodium_chloride_vapor > iodine_vapor,
        "salt_vapor_lower": sodium_chloride_vapor < iodine_vapor,
    }
    matches = [i for i, claim in enumerate(claims) if facts[claim]]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"claims": ("boil_pressure_up", "evap_surface", "iodine_melts_below_room",
                     "salt_vapor_higher")}
VARIANTS = [
    {"claims": ("boil_pressure_down", "evap_bulk_only", "iodine_melts_below_room",
                "salt_vapor_higher")},
    {"claims": ("boil_pressure_up", "evap_bulk_only", "iodine_melts_above_room",
                "salt_vapor_higher")},
    {"claims": ("boil_pressure_up", "evap_bulk_only", "iodine_melts_below_room",
                "salt_vapor_lower")},
]
ANSWER = 1
