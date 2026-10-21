"""MC13: H resembles halogens through H2 and a -1 metal hydride state."""


def solve(order=(0, 1, 2, 3)):
    # I H2, II strong electron affinity, III hydride -1, IV +1 with nonmetals.
    halogen_like = {1, 3}
    groups = ({1, 3, 4}, {2, 3, 4}, {1, 3}, {2, 4})
    return order.index(next(i for i, group in enumerate(groups) if group == halogen_like))


def check(order=(0, 1, 2, 3)):
    # H-H shares one pair, NaH contains H-, and H in HCl is +1, unlike Cl-.
    properties = {1: True, 2: False, 3: (-1 == 0 - 1), 4: False}
    groups = ((1, 3, 4), (2, 3, 4), (1, 3), (2, 4))
    valid = [i for i, group in enumerate(groups)
             if all(properties[x] for x in group)]
    assert valid == [2]
    return order.index(valid[0])


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 0, 2)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
