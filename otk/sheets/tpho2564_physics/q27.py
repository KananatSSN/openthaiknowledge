"""Lab part 2 a): the mean slope at N washers is t_N = (dy_{N+1} - dy_{N-1})/(m_{N+1} - m_{N-1}) and e_N = (t_N - t_1)/t_1 x 100%; the solution's 90 cm readings give t_1 = 0.313 cm/g and e_4 = -12.3%, so the linear range ends at N = 3. Adapted: the readings and N vary; returns percent."""

MASSES = (0.0, 15.2, 25.6, 36.0, 46.4, 56.8, 67.2)
SAGS = (13.5, 18.4, 21.5, 24.6, 27.5, 30.3, 32.9)


def solve(masses=MASSES, sags=SAGS, washers=4):
    def slope(n):
        return (sags[n + 1] - sags[n - 1]) / (masses[n + 1] - masses[n - 1])

    return (slope(washers) - slope(1)) / slope(1) * 100


def check(masses=MASSES, sags=SAGS, washers=4):
    # the ratio of the two chord slopes, as a fractional change
    rise = (sags[washers + 1] - sags[washers - 1]) * (masses[2] - masses[0])
    run = (sags[2] - sags[0]) * (masses[washers + 1] - masses[washers - 1])
    return (rise / run - 1) * 100


PARAMS = {"masses": MASSES, "sags": SAGS, "washers": 4}
VARIANTS = [{"washers": 3}, {"washers": 5}, {"sags": (13.0, 17.6, 20.5, 23.3, 26.0, 28.6, 31.0)}]
ANSWER = -12.3076923076923
TOL = 1e-9
