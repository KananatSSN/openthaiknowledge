"""Wave F slice 54 — plant tissues, roots and stems.

Three ``additional_outcome`` indicators, each filed whole:

* ``ชีววิทยาเพิ่มเติม 3 ม.5/1`` — meristems and permanent tissues;
* ``ชีววิทยาเพิ่มเติม 3 ม.5/2`` — the cross-section of monocot and dicot roots;
* ``ชีววิทยาเพิ่มเติม 3 ม.5/3`` — the cross-section of monocot and dicot stems.

Cutting and staining sections is hands-on, so the sets quiz what a section
shows: each slide description is generated from the features that tell the
four kinds apart, and the answer follows from them.
"""

from __future__ import annotations

from random import Random

SUBJECT = "ชีวะ"
UPPER_FIVE = {"th": "ม.5"}

# ══ ชีววิทยาเพิ่มเติม 3 ม.5/1 — เนื้อเยื่อพืช ═══════════════════════════════════════════


# ══ ชีววิทยาเพิ่มเติม 3 ม.5/2-3 — รากและลำต้น ═════════════════════════════════════════


SECTIONS = ("รากพืชใบเลี้ยงคู่", "รากพืชใบเลี้ยงเดี่ยว", "ลำต้นพืชใบเลี้ยงคู่", "ลำต้นพืชใบเลี้ยงเดี่ยว")


def slide(rng: Random, kind: str) -> str:
    if kind.startswith("ราก"):
        core = (f"ไซเลมอยู่ตรงกลางเรียงเป็นแฉก {rng.randint(2, 5)} แฉก โฟลเอ็มอยู่ระหว่างแฉก และไม่มีพิธ"
                if kind == "รากพืชใบเลี้ยงคู่" else
                f"ไซเลมและโฟลเอ็มเรียงสลับกันเป็นวง {rng.randint(8, 20)} กลุ่ม ล้อมรอบพิธขนาดใหญ่")
        extras = [e for e in ("เซลล์เอพิเดอร์มิสบางเซลล์ยื่นเป็นขนราก", "คอร์เทกซ์กว้าง", "มีเอนโดเดอร์มิสเห็นชัดเจน",
                              "มีเพริไซเคิลอยู่ถัดจากเอนโดเดอร์มิส") if rng.random() < 0.5]
        return " ".join([*extras, core])
    if kind == "ลำต้นพืชใบเลี้ยงคู่":
        return (f"มีมัดท่อลำเลียง {rng.randint(8, 20)} มัดเรียงเป็นวงเดียว มีแคมเบียมคั่นระหว่างไซเลมและโฟลเอ็ม "
                f"แบ่งคอร์เทกซ์และพิธได้ชัดเจน")
    return (f"มีมัดท่อลำเลียงประมาณ {rng.randrange(30, 121, 10)} มัดกระจายทั่วลำต้น แต่ละมัดมีบันเดิลชีทล้อมรอบ "
            f"ไม่มีแคมเบียม และแยกคอร์เทกซ์กับพิธไม่ชัดเจน")


