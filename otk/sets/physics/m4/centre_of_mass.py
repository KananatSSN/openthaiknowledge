"""ศูนย์กลางมวล ศูนย์ถ่วง และเสถียรภาพของวัตถุ

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/9

Sets moved here from: science_wave_f5.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f5 import SUBJECT, UPPER_FOUR, _exact

PROVENANCE = Provenance("original")


TOPIC_CENTRE = "ศูนย์กลางมวล ศูนย์ถ่วง และเสถียรภาพของวัตถุ"


CENTRE_FACTS = (
    ("ออกแรงกระทำต่อวัตถุในแนวที่ผ่านศูนย์กลางมวลบนพื้นลื่น วัตถุจะเคลื่อนที่อย่างไร",
     "เลื่อนที่ไปตามแนวแรงโดยไม่หมุน",
     ("หมุนรอบศูนย์กลางมวลโดยไม่เลื่อนที่", "ทั้งเลื่อนที่และหมุน", "อยู่นิ่งเสมอ")),
    ("ออกแรงกระทำต่อวัตถุในแนวที่ไม่ผ่านศูนย์กลางมวลบนพื้นลื่น วัตถุจะเคลื่อนที่อย่างไร",
     "ทั้งเลื่อนที่และหมุน",
     ("เลื่อนที่ตามแนวแรงโดยไม่หมุน", "หมุนอยู่กับที่โดยศูนย์กลางมวลไม่เคลื่อนที่", "อยู่นิ่งเสมอ")),
    ("ศูนย์ถ่วงของวัตถุคือตำแหน่งใด", "ตำแหน่งที่เสมือนว่าน้ำหนักทั้งหมดของวัตถุกระทำผ่าน",
     ("ตำแหน่งที่มีมวลมากที่สุดของวัตถุ", "ตำแหน่งที่อยู่ต่ำที่สุดของวัตถุ", "ตำแหน่งที่วัตถุสัมผัสพื้น")),
    ("ศูนย์กลางมวลของแท่งไม้สม่ำเสมออยู่ที่ใด", "กึ่งกลางความยาวของแท่งไม้",
     ("ปลายข้างใดข้างหนึ่ง", "ห่างจากปลายหนึ่งในสามของความยาว", "ไม่มีตำแหน่งแน่นอน")),
    ("ศูนย์กลางมวลของวงแหวนโลหะบางสม่ำเสมออยู่ที่ใด", "ที่จุดศูนย์กลางของวง ซึ่งไม่มีเนื้อวัตถุ",
     ("บนเนื้อวงแหวนด้านล่างสุด", "บนเนื้อวงแหวนด้านบนสุด", "วงแหวนไม่มีศูนย์กลางมวล")),
    ("วัตถุที่วางบนพื้นจะล้มเมื่อใด", "เมื่อแนวดิ่งที่ผ่านศูนย์ถ่วงตกนอกฐานของวัตถุ",
     ("เมื่อศูนย์ถ่วงอยู่ต่ำกว่าครึ่งหนึ่งของความสูง", "เมื่อวัตถุมีฐานกว้าง", "เมื่อแนวดิ่งผ่านศูนย์ถ่วงอยู่ในฐาน")),
    ("วัตถุแบบใดมีเสถียรภาพมากที่สุด", "ฐานกว้างและศูนย์ถ่วงอยู่ต่ำ",
     ("ฐานแคบและศูนย์ถ่วงอยู่สูง", "ฐานกว้างและศูนย์ถ่วงอยู่สูง", "ฐานแคบและศูนย์ถ่วงอยู่ต่ำ")),
    ("รถบรรทุกที่บรรทุกของสูงบนหลังคาพลิกคว่ำเมื่อเลี้ยวได้ง่ายขึ้น เพราะเหตุใด", "ศูนย์ถ่วงของรถสูงขึ้น เสถียรภาพจึงลดลง",
     ("มวลของรถลดลง", "ฐานของรถกว้างขึ้น", "ศูนย์ถ่วงของรถต่ำลง")),
    ("นักมวยปล้ำย่อตัวและกางขาออกเพื่อไม่ให้ถูกทุ่มล้มง่าย เพราะเหตุใด", "ลดระดับศูนย์ถ่วงและเพิ่มความกว้างของฐาน",
     ("เพิ่มมวลของร่างกาย", "ยกศูนย์ถ่วงให้สูงขึ้น", "ลดแรงเสียดทานกับพื้น")),
)


@question_type(
    "phys.centre_of_mass_foundation",
    display_name={"th": "ศูนย์กลางมวล ศูนย์ถ่วง และการเคลื่อนที่เมื่อแรงผ่านศูนย์กลางมวล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CENTRE,
)
class CentreOfMassFoundation(QuestionType):
    """What the centre of mass does, and where it sits between two masses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(CENTRE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_CENTRE,
                             hint="แรงผ่านศูนย์กลางมวลทำให้เลื่อนที่อย่างเดียว วัตถุล้มเมื่อแนวดิ่งผ่านศูนย์ถ่วงตกนอกฐาน")
        m1, m2, length = rng.choice([(a, b, c) for a in range(1, 11) for b in range(1, 11) if a != b
                                     for c in range(20, 130, 10) if _exact(Fraction(b * c, a + b))])
        return numeric(
            stem=(f"ติดมวล {m1} kg และ {m2} kg ไว้ที่ปลายทั้งสองของแท่งเบายาว {length} cm "
                  f"ศูนย์กลางมวลของระบบอยู่ห่างจากมวล {m1} kg เท่าใด"),
            answer=Fraction(m2 * length, m1 + m2),
            wrongs=[Fraction(m1 * length, m1 + m2), Fraction(length, 2), Fraction(m2 * length, m1)],
            unit="cm", topic=TOPIC_CENTRE,
            hint="ศูนย์กลางมวลอยู่ใกล้มวลที่มากกว่า: x = m₂L ÷ (m₁ + m₂) วัดจาก m₁")


@question_type(
    "phys.centre_of_mass_fluency",
    display_name={"th": "คำนวณตำแหน่งศูนย์กลางมวลของระบบมวลบนแนวเส้นตรง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CENTRE,
)
class CentreOfMassFluency(QuestionType):
    """x = Σmx ÷ Σm for three masses, and a rod carrying a mass at one end."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ตำแหน่งศูนย์กลางมวล = Σmx ÷ Σm (ผลรวมของมวลคูณตำแหน่ง หารด้วยมวลรวม)"
        if rng.random() < 0.6:
            while True:
                masses = [rng.randint(1, 6) for _ in range(3)]
                xs = sorted(rng.sample(range(0, 13), 3))
                moment = sum(m * x for m, x in zip(masses, xs))
                if _exact(Fraction(moment, sum(masses))):
                    break
            listed = " ".join(f"มวล {m} kg ที่ x = {x} m" for m, x in zip(masses, xs))
            return numeric(
                stem=f"บนแกน x มี{listed} ศูนย์กลางมวลของระบบอยู่ที่ x เท่าใด",
                answer=Fraction(moment, sum(masses)),
                wrongs=[Fraction(sum(xs), 3), Fraction(moment, 3), Fraction(xs[0] + xs[2], 2)],
                unit="m", topic=TOPIC_CENTRE, hint=hint)
        rod, mass, length = rng.choice([(a, b, c) for a in range(1, 11) for b in range(1, 11)
                                        for c in (40, 60, 80, 100, 120, 150, 200)
                                        if _exact(Fraction(b * c, 2 * (a + b)))])
        return numeric(
            stem=(f"แท่งไม้สม่ำเสมอมวล {rod} kg ยาว {length} cm มีมวล {mass} kg ติดอยู่ที่ปลายข้างหนึ่ง "
                  "ศูนย์กลางมวลของระบบอยู่ห่างจากกึ่งกลางแท่งไม้เท่าใด"),
            answer=Fraction(mass * length, 2 * (rod + mass)),
            wrongs=[Fraction(mass * length, 2 * rod), Fraction(length, 2), Fraction(mass * length, rod + mass)],
            unit="cm", topic=TOPIC_CENTRE,
            hint="มวลของแท่งไม้เสมือนอยู่ที่กึ่งกลาง ห่างจากมวลที่ปลาย L/2 แล้วหาศูนย์กลางมวลของสองมวลนี้")


@question_type(
    "phys.centre_of_mass_application",
    display_name={"th": "ศูนย์ถ่วงกับเสถียรภาพ: การล้มและการยื่นพ้นขอบโต๊ะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CENTRE,
)
class CentreOfMassApplication(QuestionType):
    """When a body topples: tilted boxes, a plank over an edge, and which stands best."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            angle, (b, h) = rng.choice(((37, (3, 4)), (45, (1, 1)), (53, (4, 3))))
            k = rng.choice((5, 10, 15, 20)) if b != h else rng.choice((20, 30, 40, 50))
            return _labelled(
                stem=(f"กล่องทรงสี่เหลี่ยมมวลสม่ำเสมอ ฐานกว้าง {b * k} cm สูง {h * k} cm วางบนแผ่นไม้ที่มีแรงเสียดทานมาก "
                      "ค่อย ๆ ยกปลายแผ่นไม้ขึ้น กล่องจะเริ่มล้มเมื่อแผ่นไม้ทำมุมกับแนวระดับเท่าใด "
                      "(tan 37° = 0.75, tan 53° ≈ 1.33)"),
                correct=f"{angle}°", wrongs=tuple(f"{a}°" for a in (30, 37, 45, 53, 60) if a != angle)[:3],
                topic=TOPIC_CENTRE,
                hint="กล่องล้มเมื่อแนวดิ่งผ่านศูนย์ถ่วง (กึ่งกลางกล่อง) เลยขอบฐาน คือเมื่อ tan θ = ความกว้างฐาน ÷ ความสูง")
        if shape == 1:
            plank, load, length = rng.choice([(a, b, c) for a in range(5, 31, 5) for b in range(5, 61, 5)
                                              for c in (2, 3, 4, 5, 6)
                                              if _exact(Fraction(a * c, 2 * (a + b)))])
            return numeric(
                stem=(f"วางแผ่นไม้สม่ำเสมอมวล {plank} kg ยาว {length} m บนโต๊ะ แล้ววางกล่องมวล {load} kg "
                      "ที่ปลายด้านหนึ่ง เลื่อนแผ่นไม้ให้ปลายที่มีกล่องยื่นพ้นขอบโต๊ะ "
                      "ยื่นออกไปได้มากที่สุดเท่าใดโดยไม่พลิกคว่ำ"),
                answer=Fraction(plank * length, 2 * (plank + load)),
                wrongs=[Fraction(length, 2), Fraction(load * length, 2 * (plank + load)),
                        Fraction(plank * length, 2 * load)],
                unit="m", topic=TOPIC_CENTRE,
                hint="แผ่นไม้เริ่มพลิกเมื่อศูนย์ถ่วงของระบบอยู่ตรงขอบโต๊ะพอดี: Mg(L/2 − x) = mgx")
        # Four objects; the one with the widest half-base per unit height tips last.
        while True:
            objects = [(rng.randint(2, 12) * 5, rng.randint(2, 12) * 5) for _ in range(4)]
            ratios = [Fraction(w, 2 * h) for w, h in objects]
            if len(set(ratios)) == 4:
                break
        names = ("ก", "ข", "ค", "ง")
        best = names[ratios.index(max(ratios))]
        listed = " ".join(f"{n} ฐานกว้าง {w} cm ศูนย์ถ่วงสูงจากพื้น {h} cm" for n, (w, h) in zip(names, objects))
        return _labelled(
            stem=f"วัตถุสี่ชิ้นมีศูนย์ถ่วงอยู่เหนือกึ่งกลางฐานพอดี: {listed} ชิ้นใดมีเสถียรภาพมากที่สุด",
            correct=f"ชิ้น {best}", wrongs=tuple(f"ชิ้น {n}" for n in names if n != best),
            topic=TOPIC_CENTRE,
            hint="เสถียรภาพสูงเมื่อฐานกว้างเทียบกับความสูงของศูนย์ถ่วง ต้องเอียงมากก่อนแนวดิ่งผ่านศูนย์ถ่วงจะพ้นฐาน")
