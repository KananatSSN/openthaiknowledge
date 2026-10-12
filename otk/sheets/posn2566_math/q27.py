"""ข้อ 27 — จำนวนส่วนของเส้นตรงที่มีความยาวเป็นจำนวนเต็มระหว่างจุดแลตทิซ

กำหนดจุดแลตทิซ (x, y) ที่ 0 ≤ x ≤ 5 และ 0 ≤ y ≤ 5
จงหาจำนวนส่วนของเส้นตรงที่เชื่อมจุดสองจุดที่มีความยาวเป็นจำนวนเต็ม

The grid is 6×6 = 36 points. For every pair of points (x₁,y₁), (x₂,y₂),
the squared distance is (x₂−x₁)² + (y₂−y₁)² = dx² + dy². We need this to be
a perfect square.

Possible (|dx|, |dy|) with dx² + dy² a perfect square and 0 ≤ |dx|, |dy| ≤ 5:
    (0,k): distance k, for k = 0…5 — k ≥ 1: horizontal/vertical
    (3,4) and (4,3): distance 5
    (0,5), (5,0): distance 5 (already counted)
    (1,0)…(5,0): distances 1–5
    No other Pythagorean pair fits within 5×5.

Count by displacement:
- Horizontal (dy = 0, dx = 1…5): for each dx, 6 rows × (6 − dx) positions each.
  dx=1: 6×5=30, dx=2: 6×4=24, dx=3: 6×3=18, dx=4: 6×2=12, dx=5: 6×1=6 → 90
- Vertical (dx = 0, dy = 1…5): same → 90
- Diagonal (3,4): positions = (6−3)×(6−4) = 3×2 = 6, ×4 orientations = 24
  Wait: (dx,dy) can be (±3,±4) — 4 sign combos, each with (6−3)(6−4) placements.
  Actually: for displacement (3,4): # positions = (6−3)×(6−4) = 3×2 = 6
  For (3,−4): same 6. For (−3,4): same 6. For (−3,−4): same 6.
  But each segment is counted twice (once from each endpoint), so 6×4/2 = 12.
  Hmm, no — let's be more careful. Each *unordered* pair: I should count ordered
  then halve.
  
  Actually, simpler: for (|dx|,|dy|) = (3,4), the number of ordered pairs is
  (6−3)×(6−4) × 4 sign combos = 6 × 4 = 24. Each unordered pair is counted
  twice (swapping endpoints reverses the displacement). So 24/2 = 12.
  Similarly (4,3): 12.

Total: 90 + 90 + 12 + 12 = **204**.

``solve`` computes by displacement type.  ``check`` enumerates all C(36,2) pairs.
"""

from __future__ import annotations

from math import isqrt

#: grid of (0..grid_x) × (0..grid_y), count integer-length segments.
PARAMS = {"grid_x": 5, "grid_y": 5}
ANSWER = 204
VARIANTS = [
    {"grid_x": 3, "grid_y": 3},
    {"grid_x": 4, "grid_y": 4},
    {"grid_x": 2, "grid_y": 2},
    {"grid_x": 5, "grid_y": 3},
    {"grid_x": 4, "grid_y": 6},
    {"grid_x": 7, "grid_y": 7},
]


def solve(grid_x=5, grid_y=5):
    """Count by displacement type: for each (|dx|, |dy|) with integer distance."""
    nx = grid_x + 1    # number of points in x-direction
    ny = grid_y + 1    # number of points in y-direction
    count = 0
    # For each possible displacement (dx, dy) with dx ≥ 0, dy ≥ 0, not both 0
    for dx in range(0, nx):
        for dy in range(0, ny):
            if dx == 0 and dy == 0:
                continue
            d2 = dx * dx + dy * dy
            d = isqrt(d2)
            if d * d != d2:
                continue
            # How many ordered pairs have this displacement?
            # For displacement exactly (dx, dy): (nx − dx) × (ny − dy)
            # But we need to count all sign combinations and avoid double-counting
            positions = (nx - dx) * (ny - dy)
            if dx == 0:
                # only (0, +dy) and (0, -dy) — but ordered, so each is one direction
                # unordered pairs: positions (from + direction only)
                count += positions
            elif dy == 0:
                count += positions
            else:
                # four sign combos: (+dx,+dy), (+dx,-dy), (-dx,+dy), (-dx,-dy)
                # each gives 'positions' ordered pairs
                # unordered: 4 * positions / 2 = 2 * positions
                count += 2 * positions
    return count


def check(grid_x=5, grid_y=5):
    """Independent: enumerate all pairs of lattice points."""
    nx = grid_x + 1
    ny = grid_y + 1
    if nx * ny > 2000:
        return None
    points = [(x, y) for x in range(nx) for y in range(ny)]
    count = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            d2 = dx * dx + dy * dy
            d = isqrt(d2)
            if d * d == d2:
                count += 1
    return count
