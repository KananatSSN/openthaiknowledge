"""Block programs on a 5 × 5 grid — the drawn pictures of Phase 7 wave T3.

A primary ``ว 4.2`` outcome asks a learner to write and debug a simple program
"โดยใช้ซอฟต์แวร์หรือสื่อ". Writing one needs a block editor, which the product
does not have (``docs/for_admin/technology_ipst_interaction.csv``); *reading*
one does not. Each picture shows a grid, the square a character starts on
(``S``), sometimes a star to reach, and a column of numbered blocks, each an
arrow that moves the character one square. The drawing carries no Thai glyphs
— columns are ``A``-``E``, rows ``1``-``5`` — so it renders on a server with no
Thai font.

Every family is a fixed tuple built from a seeded generator, so the set of
drawable pictures is finite and known (``otk/pictures/registry.py``
draws only registered ids). Moves are absolute — ``R`` is always to the right
— so a program's result never depends on which way the character faces.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

SIZE = 5
MOVES = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
OPPOSITE = {"R": "L", "L": "R", "U": "D", "D": "U"}
SAY = {"R": "ไปทางขวา", "L": "ไปทางซ้าย", "U": "ขึ้นข้างบน", "D": "ลงข้างล่าง"}
COLUMNS = "ABCDE"


def cell(pos: tuple[int, int]) -> str:
    """(column, row) from the bottom-left, as the drawn label: (1, 2) -> "B3"."""
    return f"{COLUMNS[pos[0]]}{pos[1] + 1}"


def inside(pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE


def expand(blocks) -> list[str]:
    """Plain moves, with each repeat block ``"x3RU"`` written out (RU RU RU)."""
    moves: list[str] = []
    for block in blocks:
        if block.startswith("x"):
            moves.extend(list(block[2:]) * int(block[1]))
        else:
            moves.append(block)
    return moves


def walk(start: tuple[int, int], blocks) -> list[tuple[int, int]]:
    """Every square the character stands on, start first. Repeat blocks expand."""
    path = [start]
    for move in expand(blocks):
        dx, dy = MOVES[move]
        path.append((path[-1][0] + dx, path[-1][1] + dy))
    return path


class BlockProgram(NamedTuple):
    """``blocks`` are ``"R"``, ``"L"``, ``"U"``, ``"D"`` or a repeat block
    ``"x<k><moves>"`` — ``"x3RU"`` runs R then U three times."""
    start: tuple[int, int]
    blocks: tuple[str, ...] = ()
    target: tuple[int, int] | None = None
    coins: tuple[tuple[int, int], ...] = ()

    @property
    def asset_id(self) -> str:
        star = cell(self.target) if self.target else "x"
        joined = "-".join(self.blocks) if any(b.startswith("x") for b in self.blocks) else "".join(self.blocks)
        coins = ("_c" + "".join(cell(c) for c in self.coins)) if self.coins else ""
        return f"blockprog_{cell(self.start)}_{joined or 'none'}_{star}{coins}"

    @property
    def end(self) -> tuple[int, int]:
        return walk(self.start, self.blocks)[-1]


def alt(spec: BlockProgram) -> str:
    """Everything the picture shows, in words, for a reader who cannot see it."""
    parts = [f"ภาพตาราง 5 × 5 ช่อง คอลัมน์ A ถึง E จากซ้ายไปขวา แถว 1 ถึง 5 จากล่างขึ้นบน "
             f"ตัวละครเริ่มที่ช่อง {cell(spec.start)}"]
    if spec.target:
        parts.append(f"มีดาวอยู่ที่ช่อง {cell(spec.target)}")
    if spec.coins:
        parts.append("มีเหรียญอยู่ที่ช่อง " + " ".join(cell(c) for c in spec.coins))
    if spec.blocks:
        listed = " ".join(f"บล็อกที่ {i} {say_block(b)}" for i, b in enumerate(spec.blocks, 1))
        parts.append(f"บล็อกคำสั่งเรียงจากบนลงล่าง {listed}")
    return " ".join(parts)


def say_block(block: str) -> str:
    if block.startswith("x"):
        inner = " แล้ว".join(SAY[m] for m in block[2:])
        return f"ทำซ้ำ {block[1]} รอบ: เดิน{inner}"
    return SAY[block]


def _monotone(rng: Random, start, across: int, updown: int) -> tuple[str, ...]:
    """A path using one horizontal and one vertical direction, shuffled."""
    h = "R" if across > 0 else "L"
    v = "U" if updown > 0 else "D"
    moves = [h] * abs(across) + [v] * abs(updown)
    rng.shuffle(moves)
    return tuple(moves)


def _random_start(rng: Random):
    return (rng.randrange(SIZE), rng.randrange(SIZE))


def _build(seed: int, count: int, make) -> tuple[BlockProgram, ...]:
    rng = Random(seed)
    found: dict[str, BlockProgram] = {}
    while len(found) < count:
        spec = make(rng)
        if spec is not None and all(inside(p) for p in walk(spec.start, spec.blocks)):
            found.setdefault(spec.asset_id, spec)
    return tuple(found.values())


def _simple(rng: Random):
    start = _random_start(rng)
    blocks = tuple(rng.choice("RLUD") for _ in range(rng.randint(2, 3)))
    return BlockProgram(start, blocks)


def _goal(rng: Random):
    start = _random_start(rng)
    target = _random_start(rng)
    if start[0] == target[0] or start[1] == target[1]:
        return None
    return BlockProgram(start, (), target)


def _debug(rng: Random):
    """A monotone path to the star; half the time one block points the wrong way."""
    start = _random_start(rng)
    target = _random_start(rng)
    across, updown = target[0] - start[0], target[1] - start[1]
    if not across or not updown or abs(across) + abs(updown) not in (3, 4):
        return None
    blocks = list(_monotone(rng, start, across, updown))
    if rng.random() < 0.6:
        i = rng.randrange(len(blocks))
        blocks[i] = OPPOSITE[blocks[i]]
    return BlockProgram(start, tuple(blocks), target)


def _long(rng: Random):
    start = _random_start(rng)
    blocks = tuple(rng.choice("RLUD") for _ in range(rng.randint(5, 6)))
    return BlockProgram(start, blocks)


def _missing(rng: Random):
    """A monotone path with one block taken out; the star marks where it should end."""
    start = _random_start(rng)
    target = _random_start(rng)
    across, updown = target[0] - start[0], target[1] - start[1]
    if not across or not updown or abs(across) + abs(updown) not in (4, 5):
        return None
    blocks = list(_monotone(rng, start, across, updown))
    blocks.pop(rng.randrange(len(blocks)))
    return BlockProgram(start, tuple(blocks), target)


def _loop(rng: Random):
    """One repeat block, with up to two plain blocks around it."""
    start = _random_start(rng)
    inner = rng.choice(("R", "L", "U", "D", "RU", "RD", "LU", "LD", "UR", "DR"))
    repeat = f"x{rng.randint(2, 4)}{inner}"
    before = tuple(rng.choice("RLUD") for _ in range(rng.randint(0, 1)))
    after = tuple(rng.choice("RLUD") for _ in range(rng.randint(0, 1)))
    return BlockProgram(start, before + (repeat,) + after)


def _loop_goal(rng: Random):
    """A repeat block with the wrong count; the star sits where the right count ends."""
    start = _random_start(rng)
    move = rng.choice("RLUD")
    turn = rng.choice(("U", "D") if move in "RL" else ("R", "L"))
    right = rng.randint(2, 4)
    wrong = right + rng.choice((-1, 1))
    if wrong < 1:
        return None
    target = walk(start, (f"x{right}{move}", turn))[-1]
    spec = BlockProgram(start, (f"x{wrong}{move}", turn), target)
    if not all(inside(p) for p in walk(start, (f"x{right}{move}", turn))):
        return None
    return spec


def _coin_run(rng: Random):
    """Four coins: one to three on squares the program lands on, the rest off its path."""
    start = _random_start(rng)
    blocks = tuple(rng.choice("RLUD") for _ in range(rng.randint(4, 5)))
    path = walk(start, blocks)
    if not all(inside(p) for p in path):
        return None
    landed = [p for p in dict.fromkeys(path[1:]) if p != start]
    missed = [(c, r) for c in range(SIZE) for r in range(SIZE) if (c, r) not in path]
    hits = rng.randint(1, 3)
    if len(landed) < hits or len(missed) < 4 - hits:
        return None
    coins = tuple(sorted(rng.sample(landed, hits) + rng.sample(missed, 4 - hits)))
    return BlockProgram(start, blocks, None, coins)


def _diagonal_goal(rng: Random):
    """A star as far across as it is up or down: a staircase repeat reaches it."""
    start = _random_start(rng)
    target = _random_start(rng)
    dx, dy = target[0] - start[0], target[1] - start[1]
    if abs(dx) != abs(dy) or abs(dx) < 2:
        return None
    return BlockProgram(start, (), target)


SIMPLE = _build(4201, 36, _simple)          # ป.1: two or three blocks
GOALS = _build(4202, 30, _goal)             # ป.1: a start and a star, no program
DEBUG = _build(4203, 40, _debug)            # ป.2: three or four blocks to a star
LONG = _build(4204, 36, _long)              # ป.3: five or six blocks
MISSING = _build(4205, 36, _missing)        # ป.3: one block short of the star
LOOPS = _build(4206, 40, _loop)             # ป.4, ป.6: one repeat block
LOOP_GOALS = _build(4207, 36, _loop_goal)   # ป.4: a repeat count to fix
COIN_RUNS = _build(4208, 60, _coin_run)     # ป.5: coins picked up by a rule
DIAGONALS = _build(4209, 30, _diagonal_goal)  # ป.6: a star a staircase reaches
# Two families can hold the same picture (a diagonal star is also an ordinary
# goal); the drawable set lists each picture once.
BLOCK_PROGRAM_SPECS = tuple({spec.asset_id: spec for spec in (
    SIMPLE + GOALS + DEBUG + LONG + MISSING + LOOPS + LOOP_GOALS + COIN_RUNS + DIAGONALS)}.values())


def wrong_block(spec: BlockProgram) -> int | None:
    """1-based number of the block pointing away from the star, if any.

    A ``DEBUG`` program is monotone except for at most one flipped block, and a
    flipped block is the only one whose direction the path to the star never uses.
    """
    assert spec.target is not None
    dx, dy = spec.target[0] - spec.start[0], spec.target[1] - spec.start[1]
    wanted = {"R" if dx > 0 else "L", "U" if dy > 0 else "D"}
    bad = [i for i, move in enumerate(spec.blocks, 1) if move not in wanted]
    return bad[0] if bad else None
