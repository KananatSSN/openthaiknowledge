"""Shared exact simulation for problem 1: M slides at V0 into a resting m that bounces between M and a wall l0 away; all collisions elastic, smooth floor."""


def collisions(big, small, speed, gap, count=None):
    """Yield (distance of the meeting from the wall, V of M, v of m) after
    each M-m collision; velocities toward the wall positive."""
    V, v = speed, 0.0
    x_big = x_small = 0.0          # positions from the start, wall at gap
    n = 0
    while count is None or n < count:
        # M-m collision (M behind m)
        V, v = ((big - small) * V + 2 * small * v) / (big + small), ((small - big) * v + 2 * big * V) / (big + small)
        n += 1
        yield gap - x_small, V, v
        # m flies to the wall and back
        t_wall = (gap - x_small) / v
        x_big += V * t_wall
        x_small = gap
        v = -v
        # meet again
        t_meet = (x_small - x_big) / (V - v)
        x_big += V * t_meet
        x_small += v * t_meet
