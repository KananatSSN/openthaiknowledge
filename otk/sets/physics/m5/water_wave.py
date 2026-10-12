"""การสะท้อน การหักเห การแทรกสอด และการเลี้ยวเบนของคลื่นผิวน้ำ

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/4

Sets moved here from: science_wave_f7.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f7 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_WATER = "การสะท้อน การหักเห การแทรกสอด และการเลี้ยวเบนของคลื่นผิวน้ำ"


WATER_FACTS = (
    ("เมื่อคลื่นผิวน้ำเคลื่อนที่จากน้ำลึกเข้าสู่น้ำตื้น ปริมาณใดไม่เปลี่ยน", "ความถี่",
     ("อัตราเร็ว", "ความยาวคลื่น", "ทิศการเคลื่อนที่เมื่อตกกระทบเป็นมุมเอียง")),
    ("เมื่อคลื่นผิวน้ำเคลื่อนที่จากน้ำลึกเข้าสู่น้ำตื้น อัตราเร็วและความยาวคลื่นเป็นอย่างไร", "ลดลงทั้งสองอย่าง",
     ("เพิ่มขึ้นทั้งสองอย่าง", "อัตราเร็วลดลงแต่ความยาวคลื่นเพิ่มขึ้น", "ไม่เปลี่ยนทั้งสองอย่าง")),
    ("การสะท้อนของคลื่นผิวน้ำที่แผ่นกั้นตรงเป็นไปตามข้อใด", "มุมตกกระทบเท่ากับมุมสะท้อน",
     ("มุมสะท้อนเป็นสองเท่าของมุมตกกระทบ", "มุมสะท้อนเป็นศูนย์เสมอ", "ความยาวคลื่นสะท้อนลดลงครึ่งหนึ่ง")),
    ("การเลี้ยวเบนของคลื่นผิวน้ำผ่านช่องแคบเห็นได้ชัดเมื่อใด", "ความกว้างของช่องแคบใกล้เคียงหรือน้อยกว่าความยาวคลื่น",
     ("ความกว้างของช่องแคบมากกว่าความยาวคลื่นมาก", "คลื่นมีความถี่สูงมาก", "น้ำตื้นมาก")),
    ("ในการแทรกสอดของคลื่นผิวน้ำจากแหล่งกำเนิดอาพันธ์สองแหล่ง แนวบัพคือแนวใด", "แนวที่คลื่นหักล้างกัน ผิวน้ำแทบไม่กระเพื่อม",
     ("แนวที่คลื่นเสริมกัน ผิวน้ำกระเพื่อมมากที่สุด", "แนวที่มีแต่สันคลื่น", "แนวที่คลื่นเคลื่อนที่เร็วที่สุด")),
)


# (sin, label) of the angles the textbook states.
SINES = ((Fraction(1, 2), "30°"), (Fraction(3, 5), "37°"), (Fraction(4, 5), "53°"))


@question_type(
    "phys.water_wave_foundation",
    display_name={"th": "สมบัติของคลื่นผิวน้ำ: การสะท้อน การหักเห การแทรกสอด และการเลี้ยวเบน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterWaveFoundation(QuestionType):
    """What changes across a depth step, and what does not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(WATER_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_WATER,
                             hint="ความถี่ขึ้นกับแหล่งกำเนิด ไม่เปลี่ยนเมื่อเปลี่ยนตัวกลาง น้ำตื้นคลื่นช้าลงและสั้นลง")
        # Speeds in cm/s; the shallow-water wavelength must come out exact in centimetres.
        f, v1, v2 = rng.choice([(f, a, a * r) for f in (2, 4, 5, 8, 10) for a in range(20, 81, 4)
                                for r in (Fraction(1, 2), Fraction(3, 4), Fraction(4, 5))
                                if (a * r).denominator == 1 and _exact(a * r / f)])
        given = (f"คลื่นผิวน้ำความถี่ {f} Hz เคลื่อนที่ในน้ำลึกด้วยอัตราเร็ว {v1} cm/s แล้วเข้าสู่น้ำตื้น"
                 f"ซึ่งอัตราเร็วเหลือ {show(v2)} cm/s")
        if rng.random() < 0.4:
            return numeric(
                stem=f"{given} ความถี่ในน้ำตื้นเท่าใด",
                answer=f, wrongs=[f * v2 / v1, f * v1 / v2, 2 * f], unit="Hz", topic=TOPIC_WATER,
                hint="ความถี่ของคลื่นเท่ากับความถี่ของแหล่งกำเนิด ไม่เปลี่ยนเมื่อเข้าสู่ตัวกลางใหม่")
        return numeric(
            stem=f"{given} ความยาวคลื่นในน้ำตื้นเท่าใด",
            answer=v2 / f, wrongs=[Fraction(v1) / f, v2 * f, v1 * f], unit="cm", topic=TOPIC_WATER,
            hint="ความถี่คงเดิม ความยาวคลื่นในน้ำตื้น = อัตราเร็วในน้ำตื้น ÷ ความถี่")


@question_type(
    "phys.water_wave_fluency",
    display_name={"th": "คำนวณการหักเหของคลื่นผิวน้ำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterWaveFluency(QuestionType):
    """sin θ₁/sin θ₂ = v₁/v₂ = λ₁/λ₂ at the angles the textbook states."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        (s1, a1), (s2, a2) = sorted(rng.sample(SINES, 2), key=lambda p: p[0], reverse=True)
        sines = "sin 30° = 0.5, sin 37° = 0.6, sin 53° = 0.8"
        if rng.random() < 0.5:
            wl1 = rng.choice([x for x in range(2, 41) if _exact(x * s2 / s1)])
            wl2 = wl1 * s2 / s1
            return numeric(
                stem=(f"คลื่นผิวน้ำในน้ำลึกมีความยาวคลื่น {wl1} cm ตกกระทบรอยต่อน้ำตื้นด้วยมุมตกกระทบ {a1} "
                      f"แล้วหักเหเป็นมุม {a2} ความยาวคลื่นในน้ำตื้นเท่าใด ({sines})"),
                answer=wl2, wrongs=[wl1 * s1 / s2, wl1, wl1 * s2], unit="cm",
                topic=TOPIC_WATER, hint="sin θ₁ / sin θ₂ = λ₁ / λ₂ (มุมวัดจากเส้นแนวฉาก)")
        v1 = rng.choice([x for x in range(10, 101, 5) if _exact(x * s2 / s1)])
        v2 = v1 * s2 / s1
        return numeric(
            stem=(f"คลื่นผิวน้ำในน้ำลึกเคลื่อนที่ด้วยอัตราเร็ว {v1} cm/s ตกกระทบรอยต่อน้ำตื้นด้วยมุมตกกระทบ {a1} "
                  f"แล้วหักเหเป็นมุม {a2} อัตราเร็วในน้ำตื้นเท่าใด ({sines})"),
            answer=v2, wrongs=[v1 * s1 / s2, v1, v1 * s2], unit="cm/s",
            topic=TOPIC_WATER, hint="sin θ₁ / sin θ₂ = v₁ / v₂ (มุมวัดจากเส้นแนวฉาก)")


@question_type(
    "phys.water_wave_application",
    display_name={"th": "การแทรกสอดของคลื่นผิวน้ำจากแหล่งกำเนิดอาพันธ์สองแหล่ง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterWaveApplication(QuestionType):
    """Path difference in wavelengths: a whole number is antinodal, a half is nodal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        wl = rng.randint(1, 8)
        s1p = rng.randint(10, 40)
        n = rng.randint(1, 4)
        if rng.random() < 0.5:
            antinode = rng.random() < 0.5
            diff = n * wl if antinode else Fraction(2 * n - 1, 2) * wl
            line, other = ("แนวปฏิบัพ", "แนวบัพ") if antinode else ("แนวบัพ", "แนวปฏิบัพ")
            return _labelled(
                stem=(f"แหล่งกำเนิดอาพันธ์ S₁ และ S₂ ให้คลื่นผิวน้ำความยาวคลื่น {wl} cm จุด P อยู่ห่าง S₁ {s1p} cm "
                      f"และห่าง S₂ {show(s1p + diff)} cm จุด P อยู่บนแนวใด"),
                correct=f"{line}ที่ {n}", wrongs=(f"{other}ที่ {n}", f"{line}ที่ {n + 1}", f"{other}ที่ {n + 1}"),
                topic=TOPIC_WATER,
                hint="ผลต่างระยะทาง = nλ อยู่บนแนวปฏิบัพที่ n และ = (n − ½)λ อยู่บนแนวบัพที่ n")
        diff = n * wl
        return numeric(
            stem=(f"จุด P บนแนวปฏิบัพที่ {n} ของการแทรกสอดของคลื่นผิวน้ำ อยู่ห่างแหล่งกำเนิด S₁ {s1p} cm "
                  f"และห่าง S₂ {s1p + diff} cm ความยาวคลื่นเท่าใด"),
            answer=wl, wrongs=[diff, Fraction(diff, n + 1), Fraction(2 * diff, 2 * n - 1)], unit="cm", topic=TOPIC_WATER,
            hint="บนแนวปฏิบัพที่ n: |S₁P − S₂P| = nλ")
