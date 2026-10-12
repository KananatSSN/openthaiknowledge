"""Wave I slice 1 — the four indicators the task queue found with no set.

Each was earlier set aside as hands-on; each also has a part a multiple-choice
question can assess, which is what these sets practise:

* ``ว 1.2 ม.1/2`` — using a light microscope: its parts, total magnification,
  the order of steps, and what the image does;
* ``เคมีเพิ่มเติม 2 ม.5/4`` — rate experiments: the variables, reading the
  results, and explaining them with collision theory;
* ``เคมีเพิ่มเติม 1 ม.6/9`` — testing esterification, hydrolysis and
  saponification: conditions, observations, and the smell of an ester;
* ``เคมีเพิ่มเติม 1 ม.6/13`` — identifying plastics by burning, floating and
  heating, and choosing a rubber for a job.
"""

from __future__ import annotations

from otk.core.provenance import Provenance

PROVENANCE = Provenance("original")

BIOLOGY, CHEMISTRY = "ชีวะ", "เคมี"
LOWER_ONE, UPPER_FIVE, UPPER_SIX = {"th": "ม.1"}, {"th": "ม.5"}, {"th": "ม.6"}
UNIT_MICROSCOPE = "การใช้กล้องจุลทรรศน์ใช้แสง"


def _others(table: dict, key) -> tuple:
    return tuple(v for k, v in table.items() if k != key)


# ══ ว 1.2 ม.1/2 — การใช้กล้องจุลทรรศน์ใช้แสง ══════════════════════════════════════


CORNERS = {("ด้านบน", "ซ้าย"): ("ด้านล่าง", "ขวา"), ("ด้านบน", "ขวา"): ("ด้านล่าง", "ซ้าย"),
           ("ด้านล่าง", "ซ้าย"): ("ด้านบน", "ขวา"), ("ด้านล่าง", "ขวา"): ("ด้านบน", "ซ้าย")}


# ══ เคมีเพิ่มเติม 2 ม.5/4 — การทดลองเรื่องอัตราการเกิดปฏิกิริยา ═══════════════════════


# ══ เคมีเพิ่มเติม 1 ม.6/9 — ทดสอบเอสเทอริฟิเคชัน ไฮโดรลิซิส และสะปอนนิฟิเคชัน ══════════


# ══ เคมีเพิ่มเติม 1 ม.6/13 — ทดสอบและระบุประเภทของพลาสติกและผลิตภัณฑ์ยาง ═══════════


