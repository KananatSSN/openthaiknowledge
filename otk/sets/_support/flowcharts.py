"""Flowcharts that turn an input number into an output — Phase 7 wave T3 pictures.

Lower-secondary ``ว 4.2 ม.1/1`` and ``ม.2/1`` ask a learner to design an
algorithm and show it as a flowchart. Drawing one needs a diagram editor the
product does not have (``docs/for_admin/technology_ipst_interaction.csv``);
*reading* one does not. Every picture here is a small flowchart with the
standard shapes: rounded ``Start``/``End``, a slanted box for ``Input x`` and
``Output y``, rectangles for statements and a diamond for a test with ``Yes``
and ``No`` exits. All drawn text is ASCII (``y = x * 2``, ``x > 5``), so it
renders on a server with no Thai font; the question stem, in Thai, supplies the
input value.

A chart is one of three shapes:

* a straight sequence (``test`` empty),
* one decision whose ``yes`` and ``no`` statements meet again before the output,
* a loop (``loop=True``): while ``test`` holds, run ``yes``, then output.

Each statement has at most one operator, so no question turns on operator
precedence. Every family is a fixed tuple built from a seeded generator, and an
asset id is spelled from the chart's own text, so a changed chart never reuses
a cached picture.
"""

from __future__ import annotations

import operator
from random import Random
from typing import NamedTuple

OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul}
TESTS = {"<": operator.lt, ">": operator.gt, "<=": operator.le, ">=": operator.ge}
_SPELL = (("<=", "le"), (">=", "ge"), ("<", "lt"), (">", "gt"), ("+", "p"), ("-", "m"),
          ("*", "t"), ("=", "e"), (" ", ""))
LOOP_LIMIT = 50


class Flowchart(NamedTuple):
    setup: tuple[str, ...]          # statements after ``Input x``
    test: str = ""                  # a decision such as ``x > 5``; "" for a straight chart
    yes: tuple[str, ...] = ()       # the Yes path (the loop body when ``loop``)
    no: tuple[str, ...] = ()        # the No path of a one-off decision
    loop: bool = False
    out: str = "y"
    hole: int = -1                  # index into ``setup`` drawn as "?"

    @property
    def asset_id(self) -> str:
        def spell(parts) -> str:
            joined = "_".join(parts)
            for sign, word in _SPELL:
                joined = joined.replace(sign, word)
            return joined or "0"
        kind = "loop" if self.loop else ("if" if self.test else "seq")
        hole = f"_h{self.hole}" if self.hole >= 0 else ""
        return (f"flow_{kind}_{spell(self.setup)}__{spell([self.test])}__{spell(self.yes)}"
                f"__{spell(self.no)}__o{self.out}{hole}")

    def shown(self, index: int) -> str:
        return "?" if index == self.hole else self.setup[index]


def _value(token: str, env: dict[str, int]) -> int:
    return int(token) if token.lstrip("-").isdigit() else env[token]


def do(statement: str, env: dict[str, int]) -> None:
    """Run ``v = a`` or ``v = a op b`` in place."""
    var, expr = statement.split(" = ")
    parts = expr.split()
    value = _value(parts[0], env)
    if len(parts) == 3:
        value = OPS[parts[1]](value, _value(parts[2], env))
    env[var] = value


def holds(test: str, env: dict[str, int]) -> bool:
    left, sign, right = test.split()
    return TESTS[sign](_value(left, env), _value(right, env))


class Run(NamedTuple):
    output: int
    passes: int         # times the Yes path ran (0 or 1 outside a loop)
    env: dict


def run(spec: Flowchart, x: int, setup: tuple[str, ...] | None = None) -> Run:
    """Follow the chart for input ``x``; ``setup`` overrides the statements (to try a fill for "?")."""
    env = {"x": x}
    for statement in setup if setup is not None else spec.setup:
        do(statement, env)
    passes = 0
    if spec.loop:
        while holds(spec.test, env):
            for statement in spec.yes:
                do(statement, env)
            passes += 1
            if passes > LOOP_LIMIT:
                raise ValueError(f"{spec.asset_id} does not stop for x = {x}")
    elif spec.test:
        taken = holds(spec.test, env)
        for statement in spec.yes if taken else spec.no:
            do(statement, env)
        passes = int(taken)
    return Run(env[spec.out], passes, env)


def alt(spec: Flowchart) -> str:
    """Every box of the chart in reading order, for a reader who cannot see it."""
    def box(text: str) -> str:
        return "ช่องว่างที่มีเครื่องหมาย ?" if text == "?" else f"คำสั่ง {text}"
    head = ["ภาพผังงาน เริ่มที่ Start", "รับค่า x (Input x)"]
    head += [box(spec.shown(i)) for i in range(len(spec.setup))]
    if spec.loop:
        body = " แล้ว ".join(box(s) for s in spec.yes)
        head.append(f"ตรวจเงื่อนไข {spec.test} ถ้าเป็นจริง (Yes) ทำ {body} แล้วย้อนกลับไปตรวจเงื่อนไขอีกครั้ง "
                    f"ถ้าเป็นเท็จ (No) ไปแสดงผล")
    elif spec.test:
        head.append(f"ตรวจเงื่อนไข {spec.test} ถ้าเป็นจริง (Yes) ทำ {' แล้ว '.join(box(s) for s in spec.yes)} "
                    f"ถ้าเป็นเท็จ (No) ทำ {' แล้ว '.join(box(s) for s in spec.no)} แล้วทั้งสองทางมาบรรจบกัน")
    head += [f"แสดงผล {spec.out} (Output {spec.out})", "จบที่ End"]
    return " → ".join(head)


# ── families ──────────────────────────────────────────────────────────────────

def _build(seed: int, count: int, make) -> tuple[Flowchart, ...]:
    rng = Random(seed)
    found: dict[str, Flowchart] = {}
    while len(found) < count:
        spec = make(rng)
        if spec is not None:
            found.setdefault(spec.asset_id, spec)
    return tuple(found.values())


def _step(rng: Random, var: str, source: str) -> str:
    op = rng.choice("+*-") if source == "y" else rng.choice("+*")
    number = rng.randint(2, 3) if op == "*" else rng.randint(1, 9)
    return f"{var} = {source} {op} {number}"


def _sequence(rng: Random):
    """Input x, two statements, Output y: y = x op a, y = y op b."""
    return Flowchart((_step(rng, "y", "x"), _step(rng, "y", "y")))


SEQ_INPUTS = range(2, 11)


def _sequence_ok(spec: Flowchart) -> bool:
    return all(run(spec, x).output >= 0 for x in SEQ_INPUTS)


def _branch(rng: Random):
    """One decision on x; each side sets y from x."""
    k = rng.randint(4, 9)
    test = f"x {rng.choice(('>', '<', '>=', '<='))} {k}"
    yes, no = _step(rng, "y", "x"), _step(rng, "y", "x")
    if yes == no:
        return None
    return Flowchart((), test, (yes,), (no,))


def _loop(rng: Random):
    """Count the steps from x to a limit: n = 0; while x < L: x = x + s; n = n + 1."""
    step = rng.randint(2, 5)
    if rng.random() < 0.5:
        limit = rng.randint(12, 30)
        test, move = f"x {rng.choice(('<', '<='))} {limit}", f"x = x + {step}"
    else:
        limit = rng.randint(0, 8)
        test, move = f"x {rng.choice(('>', '>='))} {limit}", f"x = x - {step}"
    out = rng.choice(("n", "x"))
    return Flowchart(("n = 0",), test, (move, "n = n + 1"), (), True, out)


def _sum(rng: Random):
    """Build a total over i = 1 .. x: a pattern to spot from a few passes."""
    start = rng.choice((0, 0, 1))
    add = rng.choice(("s = s + i", "s = s + 2", "s = s + 3", "s = s * 2", "s = s + i", "s = s + x"))
    if add == "s = s * 2" and start == 0:
        start = 1
    test = rng.choice(("i <= x", "i < x"))
    return Flowchart((f"s = {start}", "i = 1"), test, (add, "i = i + 1"), (), True, "s")


SEQUENCES = tuple(s for s in _build(5101, 40, _sequence) if _sequence_ok(s))[:30]   # ม.1: trace
HOLES = tuple(s._replace(hole=h) for s in SEQUENCES for h in (0, 1))                 # ม.1: fill the "?"
BRANCHES = _build(5102, 30, _branch)                                                  # ม.1: one decision
LOOPS = _build(5103, 40, _loop)                                                       # ม.2: count and trace
SUMS = _build(5104, 12, _sum)                                                         # ม.2: a total's pattern
FLOWCHART_SPECS = SEQUENCES + HOLES + BRANCHES + LOOPS + SUMS
