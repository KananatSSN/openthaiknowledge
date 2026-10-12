"""การแทรกสอดและการเลี้ยวเบนของแสง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/8

Sets moved here from: science_wave_f9.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f9 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_INTERFERENCE = "การแทรกสอดและการเลี้ยวเบนของแสง"


INTERFERENCE_FACTS = (
    ("การทดลองสลิตคู่ของยังแสดงสมบัติใดของแสง", "แสงมีสมบัติเป็นคลื่น เพราะเกิดการแทรกสอด",
     ("แสงเป็นอนุภาคเท่านั้น", "แสงเคลื่อนที่ช้าลงในอากาศ", "แสงสะท้อนได้เท่านั้น")),
    ("ในการแทรกสอดผ่านสลิตคู่ แถบสว่างเกิดที่ตำแหน่งใด", "ผลต่างระยะทางจากสองสลิตเป็นจำนวนเต็มเท่าของความยาวคลื่น",
     ("ผลต่างระยะทางเป็นครึ่งหนึ่งของความยาวคลื่น", "ระยะจากสลิตทั้งสองต่างกันมากที่สุด", "ตรงกลางระหว่างแถบมืดทุกตำแหน่งเท่านั้น")),
    ("เมื่อใช้สลิตเดี่ยวที่แคบลง แถบสว่างกลางของการเลี้ยวเบนเป็นอย่างไร", "กว้างขึ้น",
     ("แคบลง", "กว้างเท่าเดิม", "หายไป")),
    ("ส่องแสงขาวผ่านเกรตติง แสงสีใดเบนไปจากแนวเดิมมากที่สุดในแถบสเปกตรัมอันดับที่หนึ่ง", "แสงสีแดง",
     ("แสงสีม่วง", "แสงสีเขียว", "ทุกสีเบนเท่ากัน")),
    ("เกรตติงให้แถบสว่างต่างจากสลิตคู่อย่างไร", "แถบสว่างคมชัดและสว่างกว่า เพราะมีช่องจำนวนมาก",
     ("แถบสว่างกว้างและจางกว่า", "ไม่เกิดแถบสว่างเลย", "แถบสว่างอยู่ชิดกันกว่าเสมอ")),
    ("ในการเลี้ยวเบนผ่านสลิตเดี่ยว แถบใดกว้างที่สุด", "แถบสว่างกลาง",
     ("แถบสว่างอันดับที่หนึ่ง", "แถบมืดทุกแถบ", "ทุกแถบกว้างเท่ากัน")),
)


@question_type(
    "phys.light_interference_foundation",
    display_name={"th": "การแทรกสอดของแสงผ่านสลิตคู่ เกรตติง และการเลี้ยวเบนผ่านสลิตเดี่ยว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_INTERFERENCE,
)
class LightInterferenceFoundation(QuestionType):
    """What the fringes show, and whether a point is bright or dark."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(INTERFERENCE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_INTERFERENCE,
                             hint="แถบสว่างเมื่อผลต่างระยะทาง = nλ แถบมืดเมื่อ = (n − ½)λ")
        wl = rng.choice((400, 450, 480, 500, 550, 600, 640, 650, 700))
        n = rng.randint(1, 4)
        bright = rng.random() < 0.5
        # Every wavelength here is even, so a half-wavelength path difference stays whole.
        diff = n * wl if bright else (2 * n - 1) * wl // 2
        line, other = ("แถบสว่าง", "แถบมืด") if bright else ("แถบมืด", "แถบสว่าง")
        return _labelled(
            stem=(f"แสงความยาวคลื่น {wl} nm ผ่านสลิตคู่ จุด P บนฉากมีผลต่างระยะทางจากสลิตทั้งสอง {show(diff)} nm "
                  "จุด P เป็นแถบใด (นับแถบสว่างกลางเป็นอันดับที่ 0)"),
            correct=f"{line}อันดับที่ {n}", wrongs=(f"{other}อันดับที่ {n}", f"{line}อันดับที่ {n + 1}", "แถบสว่างกลาง"),
            topic=TOPIC_INTERFERENCE, hint="ผลต่างระยะทาง ÷ ความยาวคลื่น: จำนวนเต็ม n เป็นแถบสว่างอันดับ n ครึ่ง (n − ½) เป็นแถบมืดอันดับ n")


@question_type(
    "phys.light_interference_fluency",
    display_name={"th": "คำนวณระยะระหว่างแถบสว่างของการแทรกสอดผ่านสลิตคู่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_INTERFERENCE,
)
class LightInterferenceFluency(QuestionType):
    """Δy = λL/d, and λ back from a measured spacing."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        # λ in nm, slit gap d in mm, screen L in m: Δy in mm = λL/d × 10⁻³.
        wl, d, screen = rng.choice([(w, Fraction(dd, 100), s) for w in (400, 450, 500, 550, 600, 640, 700)
                                    for dd in (10, 20, 25, 40, 50, 80, 100) for s in (1, Fraction(3, 2), 2, 3)
                                    if _exact(w * s / Fraction(dd, 100) / 1000)])
        spacing = wl * screen / d / 1000
        if rng.random() < 0.55:
            return numeric(
                stem=(f"ฉายแสงความยาวคลื่น {wl} nm ผ่านสลิตคู่ที่ห่างกัน {show(d)} mm ฉากอยู่ห่างสลิต {show(screen)} m "
                      "แถบสว่างที่อยู่ถัดกันห่างกันเท่าใด"),
                answer=spacing, wrongs=[spacing * 2, spacing / 2, spacing * 10], unit="mm", topic=TOPIC_INTERFERENCE,
                hint="Δy = λL/d ระวังหน่วย: nm = 10⁻⁹ m และ mm = 10⁻³ m")
        return numeric(
            stem=(f"ฉายแสงผ่านสลิตคู่ที่ห่างกัน {show(d)} mm ฉากอยู่ห่างสลิต {show(screen)} m วัดระยะระหว่างแถบสว่าง"
                  f"ที่อยู่ถัดกันได้ {show(spacing)} mm แสงมีความยาวคลื่นเท่าใด"),
            answer=wl, wrongs=[wl * 2, Fraction(wl, 2), wl + 100], unit="nm", topic=TOPIC_INTERFERENCE,
            hint="λ = Δy·d/L แล้วแปลงเป็นนาโนเมตร")


@question_type(
    "phys.light_interference_application",
    display_name={"th": "เกรตติงและการเลี้ยวเบนผ่านสลิตเดี่ยว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_INTERFERENCE,
)
class LightInterferenceApplication(QuestionType):
    """d sin θ = nλ for a grating, and a sin θ = λ for the first dark band."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        sines = ((Fraction(1, 2), 30), (Fraction(3, 5), 37), (Fraction(4, 5), 53))
        stated = "(sin 30° = 0.5, sin 37° = 0.6, sin 53° = 0.8)"
        if rng.random() < 0.6:
            lines, n, (sin, angle) = rng.choice(
                [(ell, n, s) for ell in (200, 250, 300, 400, 500, 600, 750, 800, 1000, 1200, 1250, 1500) for n in (1, 2, 3) for s in sines
                 if (Fraction(10 ** 6, ell) * s[0] / n).denominator == 1 and 380 <= Fraction(10 ** 6, ell) * s[0] / n <= 750])
            d = Fraction(10 ** 6, lines)
            return numeric(
                stem=(f"เกรตติงมี {lines:,} ช่องต่อมิลลิเมตร ฉายแสงสีเดียวตั้งฉากกับเกรตติง เห็นแถบสว่างอันดับที่ {n} "
                      f"ทำมุม {angle}° กับแนวกลาง แสงมีความยาวคลื่นเท่าใด {stated}"),
                answer=d * sin / n, wrongs=[d * sin, d * sin / (n + 1), Fraction(lines) * sin],
                unit="nm", topic=TOPIC_INTERFERENCE,
                hint="ระยะห่างช่อง d = 1/N (1 mm ÷ จำนวนช่อง) แล้ว d sin θ = nλ")
        wl, (sin, angle) = rng.choice([(w, s) for w in (400, 450, 480, 500, 540, 600, 640, 700) for s in sines
                                       if _exact(w / s[0])])
        return numeric(
            stem=(f"แสงความยาวคลื่น {wl} nm ผ่านสลิตเดี่ยว แถบมืดแรกอยู่ที่มุม {angle}° จากแนวกลาง "
                  f"สลิตกว้างเท่าใด {stated}"),
            answer=wl / sin, wrongs=[wl * sin, 2 * wl / sin, Fraction(wl)], unit="nm", topic=TOPIC_INTERFERENCE,
            hint="แถบมืดแรกของสลิตเดี่ยว: a sin θ = λ")
