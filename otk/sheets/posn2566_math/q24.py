"""ข้อ 24 — จำนวนคนมากที่สุดที่ไม่ได้คะแนน 3 คะแนน

ครูออกสอบเติมคำ คะแนนเต็ม 3 คะแนน จากผู้สอบทั้งหมด ค่าเฉลี่ยคือ a คะแนน
ฐานนิยมคือ a คะแนน และ b คะแนน (a ≠ b) คะแนนรวมทั้งหมด 23 คะแนน
จงหาจำนวนคนมากที่สุดที่ไม่ได้คะแนน 3 คะแนน

Since the total is 23 = n·a, and a ∈ {0,1,2,3} is both the mean and a mode,
23 prime forces **a = 1, n = 23**.

Let c₀, c₁, c₂, c₃ be the counts of scores 0, 1, 2, 3.

    c₀ + c₁ + c₂ + c₃ = 23
    c₁ + 2c₂ + 3c₃ = 23  (total = 23·1)
    → c₀ = c₂ + 2c₃     (subtract)

Mode a = 1 and mode b: score 1 is a mode, one other score b is also a mode,
and no other score ties them. So c₁ = c_b > c_j for all j ∉ {1, b}.

Maximise n − c₃ = 23 − c₃, i.e., minimise c₃.

c₃ = 0 ⟹ c₀ = c₂, and then modes are 0, 1, 2 (three-way tie unless c₁ > c₀),
but then c₁ is the unique mode (single mode) unless c₁ = c₀ = c₂. If c₁ = c₀ = c₂
then there are three modes, not two. If c₁ > c₀ = c₂, mode is only {1}, not two
modes. So c₃ = 0 fails to produce exactly two modes.

c₃ = 1 ⟹ c₀ = c₂ + 2, c₁ + 2c₂ = 20, c₀ + c₁ + c₂ = 22.
With c₂ + 2 + c₁ + c₂ = 22 → c₁ = 20 − 2c₂, combined: c₁ = 20 − 2c₂.
For two modes {1, b}: c₁ = c_b > others.
Try b = 0: c₀ = c₁ → c₂ + 2 = 20 − 2c₂ → 3c₂ = 18 → c₂ = 6, c₁ = 8, c₀ = 8, c₃ = 1.
Check: c₁ = c₀ = 8 > c₂ = 6 > c₃ = 1. Modes = {0, 1}. ✓
Answer: 23 − 1 = **22**.

``solve`` finds the minimum c₃.  ``check`` enumerates all count vectors.
"""

from __future__ import annotations

#: quiz out of max_score, mean and mode a, other mode b ≠ a, total score total_score
PARAMS = {"max_score": 3, "total_score": 23}
ANSWER = 22
VARIANTS = [
    {"max_score": 3, "total_score": 7},
    {"max_score": 3, "total_score": 11},
    {"max_score": 3, "total_score": 29},
    {"max_score": 3, "total_score": 37},
    {"max_score": 3, "total_score": 13},
    {"max_score": 3, "total_score": 17},
]


def solve(max_score=3, total_score=23):
    """Find n that maximises (n − c_{max_score}), equivalently minimises c_{max_score}.

    Since n·a = total_score and a ∈ 0..max_score, we need total_score divisible
    by some a in 1..max_score (a = 0 would mean total = 0).
    """
    if total_score <= 0 or max_score < 2:
        return None

    best = None
    # Try each possible mean a (which is also a mode)
    for a in range(1, max_score + 1):
        if total_score % a != 0:
            continue
        n = total_score // a
        # c₀ + c₁ + … + c_m = n
        # Σ i·cᵢ = total_score = n·a
        # a is a mode, and exactly one other value b is also a mode
        # c_a = c_b > c_j for j ∉ {a, b}
        # Maximise n − c_{max_score}

        result = _best_for_mean(n, a, max_score, total_score)
        if result is not None:
            if best is None or result > best:
                best = result
    return best


def _best_for_mean(n, a, max_score, total_score):
    """Given mean = a and n students, find max n − c_{max_score}."""
    best = None
    # brute force over possible c vectors
    # c₀ + c₁ + … + c_m = n, Σ i·cᵢ = total_score
    # For max_score = 3: 4 variables, manageable
    if max_score > 5 or n > 500:
        return None

    # generate all partitions — for small max_score this is fine
    if max_score == 3:
        for c3 in range(n + 1):
            for c2 in range(n - c3 + 1):
                for c1 in range(n - c3 - c2 + 1):
                    c0 = n - c3 - c2 - c1
                    if c1 + 2 * c2 + 3 * c3 != total_score:
                        continue
                    counts = [c0, c1, c2, c3]
                    # Check two modes: a is a mode, exactly one other b is also a mode
                    if not _has_exactly_two_modes_including(counts, a):
                        continue
                    val = n - c3
                    if best is None or val > best:
                        best = val
    return best


def _has_exactly_two_modes_including(counts, a):
    """Check that counts has exactly two modes and one of them is a."""
    max_c = max(counts)
    if counts[a] != max_c:
        return False
    modes = [i for i, c in enumerate(counts) if c == max_c]
    return len(modes) == 2


def check(max_score=3, total_score=23):
    """Independent: enumerate all (n, count-vector) and find the best."""
    if total_score <= 0 or max_score < 2:
        return None

    best = None
    for a in range(1, max_score + 1):
        if total_score % a != 0:
            continue
        n = total_score // a
        if n > 500 or max_score > 5:
            continue

        if max_score == 3:
            for c3 in range(n + 1):
                rem = total_score - 3 * c3
                if rem < 0:
                    break
                for c2 in range(min(n - c3, rem // 2) + 1):
                    c1 = rem - 2 * c2
                    if c1 < 0:
                        continue
                    c0 = n - c3 - c2 - c1
                    if c0 < 0:
                        continue
                    counts = [c0, c1, c2, c3]
                    max_c = max(counts)
                    if counts[a] != max_c:
                        continue
                    modes = [i for i, c in enumerate(counts) if c == max_c]
                    if len(modes) != 2:
                        continue
                    val = n - c3
                    if best is None or val > best:
                        best = val
    return best
