"""Theory III.a figure: current I passes through the liquid between the metal plates in field B; the force I a x B pushes the liquid sideways along the tube, raising one arm. As drawn (current up, B into the page) the force is toward the left: the left arm rises, the right arm falls. Adapted: current up/down and B into/out of the page; returns 'left' or 'right' for the arm that rises."""


def solve(current_up=True, field_in=True):
    # (up x in) points left; each flip reverses it.
    left = current_up == field_in
    return "left" if left else "right"


def check(current_up=True, field_in=True):
    # Explicit cross product with x right, y up, z out of the page.
    i = (0, 1 if current_up else -1, 0)
    b = (0, 0, -1 if field_in else 1)
    fx = i[1] * b[2] - i[2] * b[1]
    return "left" if fx < 0 else "right"


PARAMS = {"current_up": True, "field_in": True}
VARIANTS = [{"current_up": False}, {"field_in": False}, {"current_up": False, "field_in": False}]
ANSWER = 'left'
