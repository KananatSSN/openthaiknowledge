"""แรงเสียดทานกับการเคลื่อนที่

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.5/4

Sets moved here from: science_wave_d16.
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
from otk.sets._support.science_wave_d16 import FIFTH

PROVENANCE = Provenance("original")


FRICTION_TOPIC = "แรงเสียดทานกับการเคลื่อนที่"


SURFACES = ("พื้นกระจก", "พื้นกระเบื้อง", "พื้นไม้", "พื้นพรม", "พื้นหญ้า", "พื้นทราย")  # smoothest first


FRICTION_CHANGES = (
    ("ติดล้อที่ขาโต๊ะ", False), ("หยอดน้ำมันที่บานพับประตู", False), ("ขัดพื้นไม้ให้เรียบแล้วลงแว็กซ์", False),
    ("ใช้ลูกปืนในล้อจักรยาน", False), ("โรยแป้งบนกระดานเล่นเกม", False), ("สวมถุงเท้าเดินบนพื้นขัดมัน", False),
    ("ใส่รองเท้าพื้นยางมีดอก", True), ("ปูแผ่นยางกันลื่นในห้องน้ำ", True), ("โรยทรายบนทางลาดที่เปียก", True),
    ("พันผ้าที่ด้ามไม้แบดมินตัน", True), ("ทาผงชอล์กที่มือก่อนปีนเชือก", True), ("ทำร่องดอกยางที่ล้อรถ", True),
    ("ถูเทียนไขที่รางลิ้นชัก", False), ("ทาสบู่ที่นิ้วเพื่อถอดแหวนที่คับ", False), ("ใช้รางเลื่อนแบบมีล้อที่ประตูตู้", False),
    ("วางท่อนไม้กลมใต้ของหนักแล้วกลิ้งไป", False), ("หยอดน้ำมันที่โซ่จักรยาน", False), ("ลงแว็กซ์ใต้แผ่นสกี", False),
    ("ติดแผ่นยางใต้ขาเก้าอี้", True), ("สวมถุงมือยางขณะเปิดฝาขวด", True), ("ใส่รองเท้าสตั๊ดเล่นฟุตบอลบนสนามหญ้า", True),
    ("ติดแถบกันลื่นที่ขั้นบันได", True), ("ใช้ผ้าเบรกใหม่ที่ล้อจักรยาน", True), ("รองแผ่นยางใต้พรมเช็ดเท้า", True),
)


FRICTION_SCENARIOS = (
    ("เหตุใดจึงโรยทรายบนถนนที่มีน้ำมันหก",
     "ทรายเพิ่มแรงเสียดทานระหว่างล้อรถกับถนน รถจึงไม่ลื่นไถล",
     ("ทรายลดแรงเสียดทานให้รถแล่นเร็วขึ้น", "ทรายดูดน้ำมันจนถนนหายไป", "ทรายทำให้ถนนมีน้ำหนักมากขึ้น")),
    ("ข้อใดเป็นการลดแรงเสียดทานที่เป็นประโยชน์",
     "หยอดน้ำมันที่โซ่จักรยาน เพื่อให้โซ่หมุนได้คล่อง",
     ("ใส่รองเท้าพื้นยางมีดอกเพื่อไม่ให้ลื่น", "ทำดอกยางที่ล้อรถ", "ปูพรมกันลื่นในห้องน้ำ")),
    ("ถ้าลากกล่องบนพื้นพรมต้องใช้แรงมากกว่าบนพื้นกระเบื้อง ข้อใดอธิบายได้ถูกต้อง",
     "พื้นพรมมีผิวขรุขระกว่า แรงเสียดทานจึงมากกว่า ต้องใช้แรงลากมากกว่า",
     ("พื้นกระเบื้องมีแรงเสียดทานมากกว่า เพราะผิวเรียบจึงยึดติดกับกล่องได้ดี", "กล่องหนักขึ้นเมื่ออยู่บนพรม", "แรงเสียดทานไม่ขึ้นกับผิวสัมผัส")),
)


@question_type(
    "phys.friction_effect_foundation",
    display_name={"th": "บอกผลของแรงเสียดทานต่อวัตถุที่กำลังเคลื่อนที่"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_TOPIC,
)
class FrictionEffectFoundation(QuestionType):
    """What friction does to a moving object, and which of two surfaces stops it sooner."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            i, j = sorted(rng.sample(range(len(SURFACES)), 2))
            smooth, rough = SURFACES[i], SURFACES[j]
            first, second = rng.sample((smooth, rough), 2)
            thing = rng.choice(("ลูกบอล", "รถของเล่น", "ลูกแก้ว", "กล่องเล็ก", "ลูกเทนนิส"))
            near = rng.random() < 0.5
            pick = rough if near else smooth
            other = smooth if near else rough
            return _labelled(
                stem=(f"ผลัก{thing}ด้วยแรงเท่ากันบน{first}และบน{second} {thing}บนพื้นแบบใดน่าจะเคลื่อนที่ได้"
                      f"{'ระยะสั้นกว่า' if near else 'ไกลกว่า'}"),
                correct=f"บน{pick} เพราะมีแรงเสียดทาน{'มาก' if near else 'น้อย'}กว่า",
                wrongs=(f"บน{other} เพราะมีแรงเสียดทาน{'มาก' if near else 'น้อย'}กว่า", "เท่ากัน เพราะผลักด้วยแรงเท่ากัน",
                        f"บน{pick} เพราะมีแรงเสียดทาน{'น้อย' if near else 'มาก'}กว่า"),
                hint="พื้นขรุขระมีแรงเสียดทานมาก ต้านการเคลื่อนที่มาก วัตถุจึงหยุดเร็ว",
                topic=FRICTION_TOPIC,
            )
        return _labelled(
            stem=rng.choice(("แรงเสียดทานมีผลต่อวัตถุที่กำลังเคลื่อนที่บนพื้นอย่างไร",
                             "ลูกบอลที่กลิ้งบนพื้นค่อย ๆ ช้าลงจนหยุด เพราะแรงใด")),
            correct="แรงเสียดทานต้านการเคลื่อนที่ ทำให้วัตถุเคลื่อนที่ช้าลงจนหยุด",
            wrongs=("แรงเสียดทานเสริมการเคลื่อนที่ ทำให้วัตถุเร็วขึ้นเรื่อย ๆ",
                    "แรงเสียดทานไม่มีผลต่อวัตถุที่กำลังเคลื่อนที่",
                    "แรงเสียดทานทำให้วัตถุลอยขึ้นจากพื้น"),
            hint="แรงเสียดทานเกิดระหว่างผิวที่สัมผัสกัน และมีทิศตรงข้ามกับการเคลื่อนที่",
            topic=FRICTION_TOPIC,
        )


@question_type(
    "phys.friction_effect_fluency",
    display_name={"th": "ระบุผลของแรงเสียดทานต่อการเคลื่อนที่จากผลการทดลอง"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_TOPIC,
)
class FrictionEffectFluency(QuestionType):
    """A block pushed alike on three surfaces; where friction was greatest, and its effect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        surfaces = rng.sample(SURFACES, 3)
        distances = rng.sample(range(20, 201, 15), 3)
        rows = list(zip(surfaces, distances))
        record = " / ".join(f"{s}: ไถลได้ {d} เซนติเมตรแล้วหยุด" for s, d in rows)
        most = min(rows, key=lambda r: r[1])[0]
        least = max(rows, key=lambda r: r[1])[0]
        return _labelled(
            stem=(f"นักเรียนผลักกล่องใบเดียวกันด้วยแรงเท่ากันบนพื้น 3 แบบ ได้ผลดังนี้ — {record} "
                  "จากหลักฐานนี้ ข้อใดระบุผลของแรงเสียดทานได้ถูกต้อง"),
            correct=f"{most}มีแรงเสียดทานมากที่สุด จึงทำให้กล่องช้าลงและหยุดเร็วที่สุด",
            wrongs=(f"{least}มีแรงเสียดทานมากที่สุด จึงทำให้กล่องช้าลงและหยุดเร็วที่สุด",
                    f"{most}มีแรงเสียดทานมากที่สุด จึงทำให้กล่องเคลื่อนที่ได้ไกลที่สุด",
                    "แรงเสียดทานบนพื้นทั้งสามเท่ากัน เพราะใช้กล่องใบเดียวกัน",
                    # Wrong surface and wrong effect; a true reading, a false effect.
                    f"{least}มีแรงเสียดทานมากที่สุด จึงทำให้กล่องเคลื่อนที่ได้ไกลที่สุด",
                    f"{least}มีแรงเสียดทานน้อยที่สุด จึงทำให้กล่องช้าลงและหยุดเร็วที่สุด"),
            hint="พื้นที่กล่องไถลได้ระยะสั้นที่สุด แรงเสียดทานต้านการเคลื่อนที่มากที่สุด",
            topic=FRICTION_TOPIC,
        )


@question_type(
    "phys.friction_effect_application",
    display_name={"th": "ใช้ผลของแรงเสียดทานแก้ปัญหาในชีวิตประจำวัน"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_TOPIC,
)
class FrictionEffectApplication(QuestionType):
    """Authored cases, and whether a change increases or reduces friction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            change, more = rng.choice(FRICTION_CHANGES)
            return _labelled(
                stem=f"\"{change}\" ทำให้แรงเสียดทานเปลี่ยนไปอย่างไร และส่งผลต่อการเคลื่อนที่อย่างไร",
                correct=("แรงเสียดทานเพิ่มขึ้น วัตถุจึงลื่นไถลหรือเคลื่อนที่ได้ยากขึ้น" if more
                         else "แรงเสียดทานลดลง วัตถุจึงเคลื่อนที่ได้ง่ายและลื่นขึ้น"),
                wrongs=(("แรงเสียดทานลดลง วัตถุจึงเคลื่อนที่ได้ง่ายและลื่นขึ้น" if more
                         else "แรงเสียดทานเพิ่มขึ้น วัตถุจึงลื่นไถลหรือเคลื่อนที่ได้ยากขึ้น"),
                        "แรงเสียดทานไม่เปลี่ยน เพราะวัตถุเป็นชิ้นเดิม", "แรงเสียดทานหายไปทั้งหมด วัตถุจึงลอยได้"),
                hint="ผิวขรุขระหรือมียางยึดเกาะเพิ่มแรงเสียดทาน ผิวเรียบ ล้อ และน้ำมันหล่อลื่นลดแรงเสียดทาน",
                topic=FRICTION_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FRICTION_SCENARIOS,
            hint="ผิวขรุขระเพิ่มแรงเสียดทาน ผิวเรียบหรือมีน้ำมันหล่อลื่นลดแรงเสียดทาน",
        ), FRICTION_TOPIC)
