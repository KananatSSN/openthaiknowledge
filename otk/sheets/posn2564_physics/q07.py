"""MC7: liquids A and B mix without reaction; with m_A S_A = m_B S_B the final temperature is (theta_A + theta_B)/2 (answer 3). Adapted: heat-capacity ratio r = m_A S_A / (m_B S_B); final (r theta_A + theta_B)/(r + 1)."""


def solve(hot=80, cold=20, ratio=1):
    return (ratio * hot + cold) / (ratio + 1)


def check(hot=80, cold=20, ratio=1):
    # Bisect on the final temperature where heat lost by A equals heat gained by B.
    lo, hi = min(hot, cold), max(hot, cold)
    for _ in range(200):
        t = (lo + hi) / 2
        lost = ratio * (hot - t)
        gained = t - cold
        if (lost > gained) == (hot > cold):
            lo = t
        else:
            hi = t
    return (lo + hi) / 2


PARAMS = {"hot": 80, "cold": 20, "ratio": 1}
VARIANTS = [{"ratio": 2}, {"ratio": 0.5, "hot": 90}, {"ratio": 3, "cold": 10}]
ANSWER = 50.0
