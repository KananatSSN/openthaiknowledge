"""Source p14, written 1: ground-state sublevel configuration of Zr."""


ELEMENTS = {
    "Zr": (40, "Kr", 36, "4d", "5s"),
    "Ti": (22, "Ar", 18, "3d", "4s"),
    "V": (23, "Ar", 18, "3d", "4s"),
    "Fe": (26, "Ar", 18, "3d", "4s"),
}
SUPERSCRIPTS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def format_config(core, d_orbital, d_count, s_orbital, s_count):
    return (f"[{core}] {d_orbital}{str(d_count).translate(SUPERSCRIPTS)} "
            f"{s_orbital}{str(s_count).translate(SUPERSCRIPTS)}")


def solve(element="Zr"):
    atomic_number, core, core_electrons, d_orbital, s_orbital = ELEMENTS[element]
    d_count = atomic_number - core_electrons - 2
    assert 0 < d_count <= 10
    return format_config(core, d_orbital, d_count, s_orbital, 2)


def check(element="Zr"):
    # Independently transcribed neutral ground states from NIST Atomic Data.
    observed = {
        "Zr": "[Kr] 4d² 5s²",
        "Ti": "[Ar] 3d² 4s²",
        "V": "[Ar] 3d³ 4s²",
        "Fe": "[Ar] 3d⁶ 4s²",
    }
    return observed[element]


PARAMS = {"element": "Zr"}
VARIANTS = [{"element": "Ti"}, {"element": "V"}, {"element": "Fe"}]
ANSWER = "[Kr] 4d² 5s²"
