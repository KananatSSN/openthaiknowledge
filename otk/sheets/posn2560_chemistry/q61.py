"""Source p16, written 1: X=Ni and Y=Cu; X is [Ar]3d8 4s2, Y+ is [Ar]3d10."""


def _ground(atomic):
    # Ground-state occupancies past argon for Ni, Cu, Zn and Ga.
    if atomic == 29:  # copper's filled 3d subshell
        return 10, 1, 0
    if 28 <= atomic <= 30:
        return atomic - 20, 2, 0
    if atomic == 31:
        return 10, 2, 1
    raise ValueError(atomic)


def _remove(orbitals, count):
    shells = list(orbitals)
    for _ in range(count):
        for index in (2, 1, 0):  # 4p, then 4s, then 3d
            if shells[index]:
                shells[index] -= 1
                break
    return tuple(shells)


def _format(orbitals):
    d, s, p = orbitals
    return "[Ar]" + f"3d{d}" + (f" 4s{s}" if s else "") + (f" 4p{p}" if p else "")


def solve(x2_d=8, y_offset=1):
    # The 2+ ion has 18 argon-core electrons and x2_d electrons in 3d.
    x_atomic = 18 + x2_d + 2
    y_atomic = x_atomic + y_offset
    assert x_atomic in (28, 29, 30) and y_atomic in (29, 30, 31)
    assert _remove(_ground(x_atomic), 2) == (x2_d, 0, 0)
    return _format(_ground(x_atomic)), _format(_remove(_ground(y_atomic), 1))


def check(x2_d=8, y_offset=1):
    # Independently read the established configurations for these three
    # source-neighbour pairs and verify both atomic numbers by electron count.
    known_neutral = {
        28: "[Ar]3d8 4s2", 29: "[Ar]3d10 4s1", 30: "[Ar]3d10 4s2",
    }
    known_y_plus = {
        29: "[Ar]3d10", 30: "[Ar]3d10 4s1", 31: "[Ar]3d10 4s2",
    }
    x_atomic = 20 + x2_d
    y_atomic = x_atomic + y_offset
    return known_neutral[x_atomic], known_y_plus[y_atomic]


PARAMS = {"x2_d": 8, "y_offset": 1}
VARIANTS = [
    {"x2_d": 8, "y_offset": 2},
    {"x2_d": 9, "y_offset": 1},
    {"x2_d": 10, "y_offset": 1},
]
ANSWER = ("[Ar]3d8 4s2", "[Ar]3d10")
