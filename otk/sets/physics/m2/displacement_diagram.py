"""แผนภาพแสดงการกระจัดและความเร็ว

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/15

Sets moved here from: science_wave_d21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


DISPLACEMENT_DIAGRAM_TOPIC = "แผนภาพแสดงการกระจัดและความเร็ว"


DISPLACEMENT_DIAGRAM_SCENARIOS = (
    ("เพื่อนวาดลูกศรการกระจัดของคนที่เดินวนรอบสวนหนึ่งรอบแล้วกลับมาจุดเดิม โดยลากลูกศรยาวเท่าเส้นรอบวงสวน ข้อใดแก้ไขได้ถูกต้อง",
     "ไม่ควรมีลูกศรการกระจัดเลย เพราะจุดเริ่มต้นและจุดสุดท้ายเป็นจุดเดียวกัน การกระจัดจึงเป็นศูนย์",
     ("ถูกต้องแล้ว เพราะลูกศรควรยาวเท่าระยะทางที่เดินจริง", "ลูกศรควรสั้นลงครึ่งหนึ่ง เพราะการกระจัดคือครึ่งหนึ่งของระยะทางที่เดินไปและกลับ", "ลูกศรควรชี้ย้อนกลับทิศที่เดิน และยาวเท่ากับระยะทางขากลับที่เดินมาถึงจุดเริ่มต้น")),
    ("รถเคลื่อนที่จากบ้านไปทางเหนือ 300 เมตร แล้วเลี้ยวไปทางตะวันออกอีก 400 เมตรถึงโรงเรียน ควรวาดลูกศรการกระจัดอย่างไร",
     "ลากเส้นตรงจากบ้านไปยังโรงเรียนโดยตรง มีขนาด 500 เมตร ตามทฤษฎีพีทาโกรัส",
     ("ลากตามเส้นทางจริงทั้งสองช่วงต่อกัน ความยาวรวม 700 เมตร เท่ากับระยะทางที่เดินจริง", "ลากเฉพาะช่วงไปทางเหนือ 300 เมตรเท่านั้น", "ลากเส้นตรงจากบ้านไปโรงเรียน มีขนาด 700 เมตร เพราะการกระจัดเท่ากับระยะทางเสมอ")),
    ("แผนภาพแสดงลูกศรความเร็ว 5 ช่องชี้ไปทางเหนือ ถ้าใช้ 1 ช่องแทน 2 เมตรต่อวินาที วัตถุมีความเร็วเท่าใด",
     "10 เมตรต่อวินาที ไปทางเหนือ", ("5 เมตรต่อวินาที ไปทางเหนือ", "10 เมตรต่อวินาที ไปทางใต้", "2.5 เมตรต่อวินาที ไปทางเหนือ")),
)


@question_type(
    "phys.displacement_diagram_foundation",
    display_name={"th": "บอกวิธีลากลูกศรแสดงการกระจัด"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DISPLACEMENT_DIAGRAM_TOPIC,
)
class DisplacementDiagramFoundation(QuestionType):
    """How the displacement arrow is drawn, in words or for a two-leg straight-line trip."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.75:
            a, b = rng.randint(2, 15), rng.randint(1, 15)
            first = rng.choice(("ตะวันออก", "ตะวันตก", "เหนือ", "ใต้"))
            back = {"ตะวันออก": "ตะวันตก", "ตะวันตก": "ตะวันออก", "เหนือ": "ใต้", "ใต้": "เหนือ"}[first]
            net = a - b
            answer = ("ไม่มีลูกศร เพราะการกระจัดเป็นศูนย์" if net == 0 else
                      f"ลูกศรยาว {abs(net)} ช่อง ชี้ไปทางทิศ{first if net > 0 else back}")
            options = [f"ลูกศรยาว {a + b} ช่อง ชี้ไปทางทิศ{first}", f"ลูกศรยาว {abs(net) or a} ช่อง ชี้ไปทางทิศ{back if net >= 0 else first}",
                       "ไม่มีลูกศร เพราะการกระจัดเป็นศูนย์", f"ลูกศรยาว {a + b} ช่อง ชี้ไปทางทิศ{back}"]
            return _labelled(
                stem=(f"เดินไปทางทิศ{first} {a} เมตร แล้วเดินย้อนไปทางทิศ{back} {b} เมตร "
                      "ถ้าใช้ 1 ช่องแทน 1 เมตร ควรวาดลูกศรการกระจัดอย่างไร"),
                correct=answer,
                wrongs=tuple(o for o in dict.fromkeys(options) if o != answer)[:3],
                hint="ลูกศรการกระจัดลากจากจุดเริ่มต้นตรงไปยังจุดสุดท้าย ยาวเท่าผลต่างของระยะที่ไปและย้อนกลับ",
                topic=DISPLACEMENT_DIAGRAM_TOPIC,
            )
        return _labelled(
            stem="ลูกศรที่แสดงการกระจัดของวัตถุที่เคลื่อนที่จากจุดเริ่มต้นไปจุดสุดท้ายควรลากอย่างไร",
            correct="ลากเป็นเส้นตรงจากจุดเริ่มต้นไปยังจุดสุดท้าย โดยไม่ต้องตามเส้นทางที่เคลื่อนที่จริง",
            wrongs=("ลากตามเส้นทางที่เคลื่อนที่จริงทั้งหมด แม้จะคดโค้ง",
                    "ลากจากจุดสุดท้ายย้อนกลับไปยังจุดเริ่มต้น",
                    "ลากเส้นตรงจากจุดเริ่มต้นไปจุดสุดท้ายโดยไม่ต้องมีหัวลูกศรระบุทิศทาง"),
            hint="การกระจัดคือเส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย พร้อมหัวลูกศรบอกทิศทาง",
            topic=DISPLACEMENT_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.displacement_diagram_fluency",
    display_name={"th": "เลือกแผนภาพลูกศรแสดงการกระจัดบนเส้นตรง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DISPLACEMENT_DIAGRAM_TOPIC,
)
class DisplacementDiagramFluency(QuestionType):
    """A move along a straight east-west road, scaled by squares."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        start = rng.randint(0, 10)
        end = rng.choice([p for p in range(0, 21) if p != start])
        magnitude = abs(end - start)
        direction = "ตะวันออก" if end > start else "ตะวันตก"
        other = "ตะวันตก" if direction == "ตะวันออก" else "ตะวันออก"

        def diagram(m: int, d: str) -> str:
            return f"ลูกศรยาว {m} ช่อง ชี้ไปทาง{d}"

        return _labelled(
            stem=(f"วัตถุเคลื่อนที่จากตำแหน่ง {start} เมตร ไปยังตำแหน่ง {end} เมตร บนถนนตรงแนวตะวันออก-ตะวันตก "
                  f"ถ้าใช้ 1 ช่องแทนระยะทาง 1 เมตร แผนภาพลูกศรแสดงการกระจัดข้อใดถูกต้อง"),
            correct=diagram(magnitude, direction),
            wrongs=(diagram(magnitude, other),
                    diagram(magnitude + 3, direction),
                    diagram(magnitude + 6, direction),
                    # The wrong length and the wrong direction.
                    diagram(magnitude + 3, other),
                    diagram(magnitude + 6, other)),
            hint="ขนาดของการกระจัดคือผลต่างของตำแหน่งปลายทางกับตำแหน่งเริ่มต้น ทิศทางคือทิศที่ตำแหน่งเพิ่มขึ้นหรือลดลง",
            topic=DISPLACEMENT_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.displacement_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพการกระจัดและความเร็ว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DISPLACEMENT_DIAGRAM_TOPIC,
)
class DisplacementDiagramApplication(QuestionType):
    """Authored cases, a scaled velocity arrow, and a right-angled two-leg trip."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            scale, boxes = rng.choice((2, 5, 10)), rng.randint(2, 9)
            way = rng.choice(("เหนือ", "ใต้", "ตะวันออก", "ตะวันตก"))
            other = {"ตะวันออก": "ตะวันตก", "ตะวันตก": "ตะวันออก", "เหนือ": "ใต้", "ใต้": "เหนือ"}[way]
            v = scale * boxes
            return _labelled(
                stem=f"แผนภาพแสดงลูกศรความเร็ว {boxes} ช่องชี้ไปทางทิศ{way} ถ้าใช้ 1 ช่องแทน {scale} เมตรต่อวินาที วัตถุมีความเร็วเท่าใด",
                correct=f"{v} เมตรต่อวินาที ไปทางทิศ{way}",
                wrongs=(f"{boxes} เมตรต่อวินาที ไปทางทิศ{way}", f"{v} เมตรต่อวินาที ไปทางทิศ{other}", f"{v * 2} เมตรต่อวินาที ไปทางทิศ{way}"),
                hint="ความเร็ว = จำนวนช่อง × ค่าที่ 1 ช่องแทน ทิศตามหัวลูกศร",
                topic=DISPLACEMENT_DIAGRAM_TOPIC,
            )
        if roll < 0.7:
            k = rng.choice((10, 20, 30, 50, 100))
            a, b, c = rng.choice(((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)))
            north, east = (a * k, b * k) if rng.random() < 0.5 else (b * k, a * k)
            return _labelled(
                stem=(f"เดินจากบ้านไปทางทิศเหนือ {north} เมตร แล้วเลี้ยวไปทางทิศตะวันออก {east} เมตร "
                      "ลูกศรการกระจัดจากบ้านถึงจุดสุดท้ายยาวเท่าใด"),
                correct=f"{c * k} เมตร ชี้จากบ้านตรงไปยังจุดสุดท้าย",
                wrongs=(f"{north + east} เมตร ตามเส้นทางที่เดินจริง", f"{abs(north - east)} เมตร ชี้จากบ้านตรงไปยังจุดสุดท้าย",
                        f"{max(north, east)} เมตร ตามช่วงที่ยาวที่สุด"),
                hint="การกระจัดเป็นด้านตรงข้ามมุมฉากของสามเหลี่ยมที่เกิดจากสองช่วงทาง ใช้ทฤษฎีบทพีทาโกรัส",
                topic=DISPLACEMENT_DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, DISPLACEMENT_DIAGRAM_SCENARIOS,
            hint="การกระจัดเป็นเส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย ความเร็วอ่านจากความยาวลูกศรคูณมาตราส่วน",
        ), DISPLACEMENT_DIAGRAM_TOPIC)
