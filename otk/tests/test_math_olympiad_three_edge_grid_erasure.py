"""Check the erasure classification with explicit three-edge assignments."""

from functools import lru_cache
from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.three_edge_grid_erasure import (
    count_erasable_sizes,
    erasable_grid_size,
)


def _neighbors(size: int, row: int, col: int):
    for rr, cc in ((row + 1, col), (row, col + 1)):
        if rr < size and cc < size:
            yield rr, cc


def _pair(a, b):
    return tuple(sorted((a, b)))


def _in_core(size: int, row: int, col: int) -> bool:
    return 3 <= row < size - 3 and 3 <= col < size - 3


def _frame_selected(size: int, row: int, col: int) -> bool:
    if row in (0, size - 1):
        return col % 2 == 1
    if row in (1, size - 2):
        return col % 2 == 0
    if row in (2, size - 3):
        return 0 < col < size - 1
    if row % 2:
        return col in (0, 2, size - 3, size - 1)
    return col in (1, 2, size - 3, size - 2)


def _frame_owner(size: int, a, b):
    ar, ac = a
    br, bc = b
    if _in_core(size, ar, ac):
        return b
    if _in_core(size, br, bc):
        return a
    sa = _frame_selected(size, ar, ac)
    sb = _frame_selected(size, br, bc)
    if sa != sb:
        return a if sa else b
    assert sa and sb
    if ar == br:
        if ar == 2:
            return b if ac == 1 else a
        if ar == size - 3:
            return b if ac <= size - 4 else a
        if 3 <= ar <= size - 4 and ar % 2 == 0:
            return b if ac == 1 else a
    else:
        if ar == 1:
            return b
        if ar == size - 3:
            return a
        if 2 <= ar <= size - 4 and ac == 2:
            return b
        if 2 <= ar <= size - 4 and ac == size - 3:
            return a
    raise AssertionError((size, a, b))


def _open_assignment(size: int):
    if size == 1:
        return {}
    if size == 3:
        selected = {(0, 1), (1, 0), (1, 2), (2, 1)}
        result = {}
        for row in range(size):
            for col in range(size):
                a = row, col
                for b in _neighbors(size, row, col):
                    owners = selected.intersection((a, b))
                    assert len(owners) == 1
                    result[_pair(a, b)] = owners.pop()
        return result
    assert size >= 7 and size % 6 in (1, 3)
    core = _open_assignment(size - 6)
    result = {
        _pair((a[0] + 3, a[1] + 3), (b[0] + 3, b[1] + 3)): (owner[0] + 3, owner[1] + 3)
        for (a, b), owner in core.items()
    }
    for row in range(size):
        for col in range(size):
            a = row, col
            for b in _neighbors(size, row, col):
                if not (_in_core(size, *a) and _in_core(size, *b)):
                    result[_pair(a, b)] = _frame_owner(size, a, b)
    return result


def _cell_edges(row: int, col: int):
    return (('H', row, col), ('H', row + 1, col), ('V', row, col), ('V', row, col + 1))


def _shared_edge(a, b):
    if a[0] == b[0]:
        return 'V', a[0], max(a[1], b[1])
    return 'H', max(a[0], b[0]), a[1]


def _boundary_cycle(size: int):
    return (
        [(0, col) for col in range(size)]
        + [(row, size - 1) for row in range(1, size)]
        + [(size - 1, col) for col in range(size - 2, -1, -1)]
        + [(row, 0) for row in range(size - 2, 0, -1)]
    )


def _full_assignment(size: int):
    assert size >= 2
    result = {}

    def assign(edge, owner):
        assert edge not in result
        result[edge] = owner

    ring = _boundary_cycle(size)
    ring_set = set(ring)
    for index, a in enumerate(ring):
        row, col = a
        for edge in _cell_edges(row, col):
            if edge[0] == 'H' and edge[1] in (0, size) or (
                edge[0] == 'V' and edge[2] in (0, size)
            ):
                assign(edge, a)
        for b in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            if 0 <= b[0] < size and 0 <= b[1] < size and b not in ring_set:
                assign(_shared_edge(a, b), a)
        assign(_shared_edge(a, ring[(index + 1) % len(ring)]), a)

    if size >= 3:
        for (a, b), owner in _open_assignment(size - 2).items():
            shifted_a = a[0] + 1, a[1] + 1
            shifted_b = b[0] + 1, b[1] + 1
            assign(_shared_edge(shifted_a, shifted_b), (owner[0] + 1, owner[1] + 1))
    return result


def test_constructed_erasure_for_all_small_valid_sizes():
    for size in range(1, 62):
        if not erasable_grid_size(size):
            assert size == 1 or size % 2 == 0 and size != 2 or (
                2 * size * (size + 1) % 3 != 0
            )
            continue
        assignment = _full_assignment(size)
        expected_edges = {
            edge
            for row in range(size)
            for col in range(size)
            for edge in _cell_edges(row, col)
        }
        assert set(assignment) == expected_edges
        owned = {}
        for edge, cell in assignment.items():
            assert edge in _cell_edges(*cell)
            owned.setdefault(cell, set()).add(edge)
        assert all(len(edges) == 3 for edges in owned.values())
        remaining = set(expected_edges)
        for cell in sorted(owned):
            assert owned[cell] <= remaining
            assert len(set(_cell_edges(*cell)) & remaining) >= 3
            remaining -= owned[cell]
        assert not remaining
    assert count_erasable_sizes(11) == 5  # 2,3,5,9,11


def test_exhaustive_tiny_grids():
    for size in (1, 2, 3):
        edges = sorted({edge for row in range(size) for col in range(size) for edge in _cell_edges(row, col)})
        masks = [sum(1 << edges.index(edge) for edge in _cell_edges(row, col)) for row in range(size) for col in range(size)]

        @lru_cache(None)
        def possible(mask):
            if mask == 0:
                return True
            for cell_mask in masks:
                present = [bit for bit in range(len(edges)) if cell_mask & mask & (1 << bit)]
                for chosen in combinations(present, 3):
                    nxt = mask
                    for bit in chosen:
                        nxt &= ~(1 << bit)
                    if possible(nxt):
                        return True
            return False

        assert possible((1 << len(edges)) - 1) == erasable_grid_size(size)


def test_generated_draws():
    key = "math.three_edge_grid_erasure_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
