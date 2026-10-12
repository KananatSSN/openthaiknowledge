"""Wave E slice 15 — sound at work, colour, electromagnetic waves and
communication. Closes ``ว 2.3 ม.5`` and with it Wave E's core content.

* ``ว 2.3 ม.5/8`` สืบค้นข้อมูล และยกตัวอย่างการนำความรู้เกี่ยวกับเสียงไปใช้ประโยชน์
  ในชีวิตประจำวัน — สืบค้นข้อมูล is not assessable, so ยกตัวอย่าง carries the
  record: default filing.
* ``ว 2.3 ม.5/9`` สังเกต และอธิบายการมองเห็นสีของวัตถุ และความผิดปกติในการมองเห็นสี —
  one verb pair, two objects: default filing, and the ``exact`` set reaches both.
* ``ว 2.3 ม.5/10`` สังเกต และอธิบายการทำงานของแผ่นกรองแสงสี การผสมแสงสี การผสมสารสี
  และการนำไปใช้ประโยชน์ในชีวิตประจำวัน — default filing; the ``exact`` set reaches
  filters, mixing light and mixing pigment.
* ``ว 2.3 ม.5/11`` สืบค้นข้อมูลและอธิบายคลื่นแม่เหล็กไฟฟ้า ส่วนประกอบคลื่นแม่เหล็ก
  ไฟฟ้า และหลักการทำงานของอุปกรณ์บางชนิดที่อาศัยคลื่นแม่เหล็กไฟฟ้า — default filing.
  The ม.3 sets (``phys.em_spectrum``) already order the bands; these go on to
  the wave's make-up, c = fλ, and how devices work.
* ``ว 2.3 ม.5/12`` สืบค้นข้อมูลและอธิบายการสื่อสารโดยอาศัยคลื่นแม่เหล็กไฟฟ้า ... และ
  เปรียบเทียบการสื่อสารด้วยสัญญาณแอนะล็อกกับสัญญาณดิจิทัล — two free verbs, each
  with its own object: Foundation (how EM waves carry information) and Fluency
  (analogue against digital) are both ``exact``.

Colour is computed, not labelled: a colour is the set of primary lights it
contains, an object's seen colour is what it reflects of the light falling on
it, and a filter passes only its own primaries.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_e13 import show

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _labelled(*, stem, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)] if isinstance(stem, str) else stem,
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def _numeric(*, stem: str, answer, wrongs, unit: str, topic: str, hint: str) -> GeneratedQuestion:
    seen = [Fraction(answer)]
    # Slips on both sides; the registry's rank balancing picks among them.
    for w in [*wrongs, answer / 2, answer * 2, answer - 1, answer + 1, answer / 10, answer * 10, answer - 2, answer + 2, answer * 3]:
        w = Fraction(w)
        if w > 0 and w not in seen and show(w) not in {show(s) for s in seen}:
            seen.append(w)
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(f"{show(seen[0])} {unit}")],
        distractors=fixed(*[[text(f"{show(w)} {unit}")] for w in seen[1:]]),
        topic=topic, hint=[text(hint)],
    )


# ══ ว 2.3 ม.5/8 — การใช้ประโยชน์จากเสียง ═════════════════════════════════════════


# ══ ว 2.3 ม.5/9 and ม.5/10 — colour ══════════════════════════════════════════════

R, G, B = "R", "G", "B"
COLOUR_NAME = {
    frozenset(): "สีดำ",
    frozenset({R}): "สีแดง",
    frozenset({G}): "สีเขียว",
    frozenset({B}): "สีน้ำเงิน",
    frozenset({R, G}): "สีเหลือง",
    frozenset({G, B}): "สีฟ้า (ไซแอน)",
    frozenset({R, B}): "สีแดงม่วง (มาเจนตา)",
    frozenset({R, G, B}): "สีขาว",
}
NAME_COLOUR = {name: c for c, name in COLOUR_NAME.items()}
# "แสงสีแดง", never "แสงแดง", which is sunlight.
LIGHT_NAME = {c: ("แสงขาว" if c == frozenset({R, G, B}) else f"แสง{name}")
              for c, name in COLOUR_NAME.items() if c}
PRIMARY_LIGHTS = (frozenset({R}), frozenset({G}), frozenset({B}))
PIGMENTS = {"สีเหลือง": frozenset({R, G}), "สีฟ้า (ไซแอน)": frozenset({G, B}),
            "สีแดงม่วง (มาเจนตา)": frozenset({R, B})}


def _colour_choices(correct: str, rng: Random) -> tuple[str, ...]:
    return tuple(rng.sample([n for n in COLOUR_NAME.values() if n != correct], 3))


OBJECTS = (("เสื้อ", "ตัว"), ("ลูกบอล", "ลูก"), ("กระดาษ", "แผ่น"), ("แอปเปิล", "ผล"), ("ใบไม้", "ใบ"))


# ══ ว 2.3 ม.5/11 — คลื่นแม่เหล็กไฟฟ้า ════════════════════════════════════════════


# ══ ว 2.3 ม.5/12 — การสื่อสาร ═════════════════════════════════════════════════════


