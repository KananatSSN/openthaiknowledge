"""Wave E slice 2 — the periodic-table classification and elements-in-use cluster.

Three more core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/5`` หมู่และคาบของธาตุ และโลหะ/อโลหะ/กึ่งโลหะ/เรพรีเซนเททีฟ/แทรนซิชัน
  จากตารางธาตุ — verb ระบุ repeated over two joined objects, so the default
  filing applies: only Fluency (the combined classification) is exact.
* ``ว 2.1 ม.5/6`` เปรียบเทียบสมบัติการนำไฟฟ้า การให้และรับอิเล็กตรอนระหว่าง
  โลหะกับอโลหะ — single verb เปรียบเทียบ, same default filing.
* ``ว 2.1 ม.5/7`` ตัวอย่างประโยชน์และอันตรายจากธาตุเรพรีเซนเททีฟและแทรนซิชัน —
  สืบค้นข้อมูลและนำเสนอตัวอย่าง: the research half is not itself assessable by
  an MCQ item, so this files under the default single-verb pattern too, the
  same precedent already set for ``chem.element_use_effect`` (``ว 2.1 ม.1/2``)
  in Wave D.

The periodic-table helpers are the ones already drilled for the *additional*-
course indicator เคมีเพิ่มเติม 1 ม.4/4 in :mod:`otk.sets._support.science_wave_a5`;
reusing them keeps both courses' element data in step with one periodic table.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "เคมี"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ══ ว 2.1 ม.5/5 — หมู่และคาบของธาตุ และการจัดกลุ่มธาตุ ═══════════════════════


# ══ ว 2.1 ม.5/6 — การนำไฟฟ้า การให้และรับอิเล็กตรอน: โลหะกับอโลหะ ═══════════


# ══ ว 2.1 ม.5/7 — ประโยชน์และอันตรายจากธาตุเรพรีเซนเททีฟและแทรนซิชัน ═══════


