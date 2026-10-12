"""Wave F slice 1 — friction coefficient, mechanical equilibrium, fluid pressure and buoyancy.

Built from ``sheet_database/Faii/ข้อสอบแรง.pdf``, a five-part Thai force paper
(แรงลัพธ์ / แรงเสียดทาน / ความดันและแรงพยุง / โมเมนต์ / สนามและแรงในสนาม).

The sheet's *conceptual* half already has coverage: resultant force, the
static-vs-kinetic distinction, the factors behind friction and liquid pressure,
sink-and-float, ``M = Fl`` on a central pivot, and the three fields are all
filed under ``ว 2.2 ม.2`` by Wave D. What had no coverage at all is the sheet's
*calculating* half, and those computations sit above the ``ม.2`` indicators —
they are named by four ``ฟิสิกส์เพิ่มเติม`` outcomes, all of which stood at zero
sets:

* ``ฟิสิกส์เพิ่มเติม 1 ม.4/7`` วิเคราะห์ อธิบาย และคำนวณแรงเสียดทาน … รวมทั้ง
  ทดลองหาสัมประสิทธิ์ความเสียดทาน — the sheet's μ = f/N block (ข้อ 15-25 of
  the friction part).
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/8`` อธิบายสมดุลกลของวัตถุ โมเมนต์ และผลรวมของโมเมนต์ …
  และคำนวณปริมาณต่าง ๆ ที่เกี่ยวข้อง — the sheet's moment part, whose multi-load
  and end-pivot levers go past ``ว 2.2 ม.2/10``'s single load either side.
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/3`` อธิบาย และคำนวณความดันเกจ ความดันสัมบูรณ์ … — the
  sheet's P = ρgh block.
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/4`` ทดลอง อธิบาย และคำนวณขนาดแรงพยุงจากของไหล — the
  sheet's แรงพยุง block, both the two-weighings form and F_B = ρVg.

All four are ``additional_outcome``: an additional-course outcome is filed as a
whole, so the stage split is ours, not the indicator's.

**Two of the sheet's own answers are wrong and are deliberately not reproduced.**
Both were caught by working the physics independently of the printed key:

* friction ข้อ 20 — a 1 kg box with μ = 0.5 pulled by 100 N. The key computes
  ``f = 0.5 × 100 = 50 N``, using the *applied pull* as the normal force. The
  normal force is the weight, ``1 × 10 = 10 N``, so ``f = 5 N``. Nothing here
  ever multiplies μ by a horizontal force.
* pressure ข้อ 5 — force on the *side* wall of a full 2×2×4 m tank. The key
  computes ``P_bottom × A_side = 40000 × 8 = 3.2 × 10⁵ N``. Pressure on a
  vertical wall grows with depth, so the force is the *average* pressure over
  the wall, ``20000 × 8 = 1.6 × 10⁵ N``. Only horizontal surfaces, where
  ``F = PA`` holds with a single pressure, are generated.

``g`` is 10 m/s² throughout, as the sheet states, and every stem says so.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "ฟิสิกส์"
UPPER_FOUR = {"th": "ม.4"}
UPPER_SIX = {"th": "ม.6"}


G = 10                                   # m/s², the value the sheet uses


def _num(x) -> str:
    """Format a computed value: 2.0 → '2', 0.375 → '0.375'."""
    x = round(float(x), 3)
    return str(int(x)) if x == int(x) else f"{x:g}"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def _numeric(*, stem: str, answer, unit: str, slips: tuple, fillers: tuple,
             topic: str, hint: str) -> GeneratedQuestion:
    """A computed answer plus three distinct wrong values, all carrying the unit.

    ``slips`` are the diagnostic miscalculations for this draw, in the order
    they are worth offering; ``fillers`` top the list up whenever a slip
    collided with the answer or with another slip, so a draw always has four
    distinct choices.
    """
    correct = f"{_num(answer)} {unit}".strip()
    wrongs: list[str] = []
    for value in (*slips, *fillers):
        if value is None or value <= 0:
            continue
        label = f"{_num(value)} {unit}".strip()
        if label != correct and label not in wrongs:
            wrongs.append(label)
        if len(wrongs) == 3:
            break
    return _labelled(stem=stem, correct=correct, wrongs=tuple(wrongs),
                     topic=topic, hint=hint)


# ══ ฟิสิกส์เพิ่มเติม 1 ม.4/7 — แรงเสียดทานและสัมประสิทธิ์ความเสียดทาน ═══════════════


# ══ ฟิสิกส์เพิ่มเติม 1 ม.4/8 — สมดุลกลและผลรวมของโมเมนต์ ═══════════════════════════


# ══ ฟิสิกส์เพิ่มเติม 4 ม.6/3 — ความดันเกจและความดันสัมบูรณ์ ════════════════════════

# (ชื่อ, ความหนาแน่น kg/m³) — the liquids the sheet itself uses.
FLUIDS = (("น้ำ", 1000), ("น้ำมัน", 800), ("น้ำทะเล", 1030), ("แอลกอฮอล์", 800))


# ══ ฟิสิกส์เพิ่มเติม 4 ม.6/4 — แรงพยุงจากของไหล ════════════════════════════════════


