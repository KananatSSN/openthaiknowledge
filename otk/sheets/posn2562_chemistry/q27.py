"""MC27: XeF4 changes from AX4E2 square planar to AX4E seesaw."""


def solve(order=(0, 1, 2, 3)):
    before, after = "square planar", "seesaw"
    transitions = (("tetrahedral", "seesaw"), ("square planar", "seesaw"),
                   ("square planar", "square pyramidal"),
                   ("seesaw", "square planar"))
    return order.index(transitions.index((before, after)))


def check(order=(0, 1, 2, 3)):
    # Four bonded pairs and two lone pairs give octahedral electron geometry;
    # remove one lone pair and five domains give trigonal-bipyramidal geometry.
    domains_before, domains_after = 4 + 2, 4 + 1
    shapes = {6: "square planar", 5: "seesaw"}
    pair = (shapes[domains_before], shapes[domains_after])
    choices = (("tetrahedral", "seesaw"), ("square planar", "seesaw"),
               ("square planar", "square pyramidal"),
               ("seesaw", "square planar"))
    return order.index(choices.index(pair))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 1, 0)},
            {"order": (3, 1, 0, 2)}]
ANSWER = solve(**PARAMS)
