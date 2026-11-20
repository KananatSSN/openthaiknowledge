"""Shared model for problem 2.2: the trapped air column (cross-section A) is compressed adiabatically from L0 at P_a until it pushes the first pellet past its static friction F, then expands adiabatically while driving the pellet a distance D against kinetic friction f and the atmosphere."""


def start_gap(rest, grip, area, gamma=1.4, air=1.0e5):
    """Column length L (m) at which P A = F + P_a A."""
    return rest * (air * area / (grip + air * area)) ** (1 / gamma)


def push(x, gap, grip, area, slide, gamma=1.4, air=1.0e5):
    """Net force on the pellet after it has moved x."""
    return (grip + air * area) * (gap / (gap + x)) ** gamma - air * area - slide
