"""ข้อ 26 — จำนวนรูปร่างที่ต่างกันของลูกบาศก์หน่วย 5 ลูกในกล่อง 2×2×2

กำหนดลูกบาศก์หน่วย 5 ลูก ที่ติดกัน และสามารถบรรจุลงในกล่อง 2×2×2 ได้พอดี
จงหาจำนวนรูปร่างที่ต่างกัน (นับหมุนและสะท้อนเป็นแบบเดียวกัน)

A 2×2×2 box has 8 unit cells. Choosing 5 of 8 = C(8,5) = 56 subsets.
Of those 56, the ones whose cells are face-connected form "polycubes" inside the
box. By Burnside's lemma over the 48-element symmetry group of the cube, the
number of *distinct* shapes (up to rotation and reflection) is **2**.

The two shapes:
1. Remove one corner and two opposite cells → L-shape in 3D
2. Remove three cells sharing a face → step shape

``solve`` enumerates the 56 subsets, filters for face-connectivity, and applies
Burnside (or just canonicalises each under the 48 symmetries and counts orbits).
``check`` generates the same polycubes independently using BFS for connectivity
and a different orbit-counting method.
"""

from __future__ import annotations

from itertools import combinations

#: n cubes inside an a×b×c box, up to rotation and reflection.
PARAMS = {"n": 5, "a": 2, "b": 2, "c": 2}
ANSWER = 2
VARIANTS = [
    {"n": 4, "a": 2, "b": 2, "c": 2},
    {"n": 6, "a": 2, "b": 2, "c": 2},
    {"n": 7, "a": 2, "b": 2, "c": 2},
    {"n": 3, "a": 2, "b": 2, "c": 2},
    {"n": 2, "a": 2, "b": 2, "c": 2},
]
# A non-cubic box is deliberately absent: the shapes that fit in a 3×2×2 box are
# not closed under the cube's symmetries (a rotation takes the box to 2×3×2), so
# `check`'s Burnside count does not apply there and the item would lose its
# second method. The sheet's own box is a cube.


def _cells(a, b, c):
    """All cells in an a×b×c box."""
    return [(x, y, z) for x in range(a) for y in range(b) for z in range(c)]


def _is_connected(cells_set):
    """Check face-connectivity using BFS."""
    if not cells_set:
        return False
    start = next(iter(cells_set))
    visited = {start}
    queue = [start]
    while queue:
        x, y, z = queue.pop()
        for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            nb = (x + dx, y + dy, z + dz)
            if nb in cells_set and nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return len(visited) == len(cells_set)


def _symmetries_of_cube():
    """The 48 symmetries of the cube as (sign, permutation) pairs.

    Each symmetry maps (x, y, z) → (±x_perm, ±y_perm, ±z_perm) within an
    a×b×c box, but here we just store the abstract transformations.
    """
    perms = [
        (0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)
    ]
    signs = [(1,1,1),(1,1,-1),(1,-1,1),(1,-1,-1),
             (-1,1,1),(-1,1,-1),(-1,-1,1),(-1,-1,-1)]
    return [(p, s) for p in perms for s in signs]


def _apply_sym(cell, perm, signs, dims):
    """Apply a symmetry to a cell, mapping back into [0, dim) coordinates."""
    coords = [cell[perm[i]] for i in range(3)]
    result = []
    perm_dims = [dims[perm[i]] for i in range(3)]
    for i in range(3):
        c = coords[i]
        if signs[i] < 0:
            c = perm_dims[i] - 1 - c
        result.append(c)
    return tuple(result)


def _canonical(cells_set, dims):
    """Canonical form: smallest frozenset under all symmetries.

    To count shapes independently of position, we translate to origin.
    """
    best = None
    for perm, signs in _symmetries_of_cube():
        # Apply symmetry without bounds checking
        transformed = set()
        for cell in cells_set:
            coords = [cell[perm[i]] for i in range(3)]
            for i in range(3):
                if signs[i] < 0:
                    coords[i] = -coords[i]
            transformed.add(tuple(coords))
        
        # Translate to origin
        min_x = min(c[0] for c in transformed)
        min_y = min(c[1] for c in transformed)
        min_z = min(c[2] for c in transformed)
        t = frozenset((x - min_x, y - min_y, z - min_z) for x, y, z in transformed)
        
        if best is None or sorted(t) < sorted(best):
            best = t
    return best


def solve(n=5, a=2, b=2, c=2):
    """Enumerate n-subsets of an a×b×c box, keep connected, count orbits."""
    all_cells = _cells(a, b, c)
    total = a * b * c
    if n > total or n < 1:
        return 0
    if total > 20:
        return None  # too large to enumerate

    orbits = set()
    for subset in combinations(all_cells, n):
        cells_set = set(subset)
        if not _is_connected(cells_set):
            continue
        canon = _canonical(frozenset(subset), (a, b, c))
        orbits.add(canon)
    return len(orbits)


def check(n=5, a=2, b=2, c=2):
    """Independent: Burnside's lemma, instead of deduplicating canonical forms.

    `solve` builds a canonical representative of every shape and counts the
    distinct ones. This counts the same orbits without ever naming one: for each
    of the 48 symmetries it counts the shapes that symmetry *fixes*, and averages.

        |orbits| = (1/|G|) Σ_g |Fix(g)|

    The two agree only if both the shape set and the group action are right, and
    they fail differently — a canonicalisation bug merges or splits orbits, while
    a Burnside bug shows up as a non-integral average.
    """
    if not a == b == c:
        return None                      # see the note on VARIANTS
    all_cells = _cells(a, b, c)
    total = a * b * c
    if n > total or n < 1:
        return 0
    if total > 20:
        return None

    def normalise(cells):
        xs = [p[0] for p in cells]
        ys = [p[1] for p in cells]
        zs = [p[2] for p in cells]
        mx, my, mz = min(xs), min(ys), min(zs)
        return frozenset((x - mx, y - my, z - mz) for x, y, z in cells)

    shapes = set()
    for subset in combinations(all_cells, n):
        cells_set = set(subset)
        if _is_connected(cells_set):
            shapes.add(normalise(subset))

    group = _symmetries_of_cube()
    fixed_total = 0
    for perm, signs in group:
        for shape in shapes:
            moved = set()
            for cell in shape:
                coords = [cell[perm[i]] for i in range(3)]
                for i in range(3):
                    if signs[i] < 0:
                        coords[i] = -coords[i]
                moved.add(tuple(coords))
            if normalise(moved) == shape:
                fixed_total += 1
    if fixed_total % len(group):
        return None                      # not an integer: the action is wrong
    return fixed_total // len(group)
