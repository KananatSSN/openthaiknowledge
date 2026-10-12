"""การทำลายป่าไม้และการอนุรักษ์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/12

Sets moved here from: science_wave_f74.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f74 import BIOLOGY, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_FOREST = "การทำลายป่าไม้และการอนุรักษ์"


CAUSES = ("การบุกรุกป่าเพื่อทำไร่และที่อยู่อาศัย", "การลักลอบตัดไม้", "ไฟป่าที่เกิดจากการเผาเตรียมพื้นที่", "การสร้างเขื่อนและถนนผ่านพื้นที่ป่า",
          "การทำไร่เลื่อนลอย")


EFFECTS = ("น้ำท่วมฉับพลันและดินถล่มในฤดูฝน", "แหล่งต้นน้ำลำธารเสื่อมโทรม ฤดูแล้งขาดน้ำ", "ความหลากหลายทางชีวภาพลดลง",
           "หน้าดินถูกชะล้าง", "คาร์บอนไดออกไซด์ในบรรยากาศเพิ่มขึ้น")


REMEDIES = ("ปลูกป่าทดแทนด้วยพืชพื้นเมือง", "จัดตั้งป่าชุมชนให้ชุมชนร่วมดูแล", "ประกาศเขตอุทยานแห่งชาติและเขตรักษาพันธุ์สัตว์ป่า",
            "ใช้วัสดุทดแทนไม้และรีไซเคิลกระดาษ", "ทำแนวกันไฟป่า")


FOREST_HINT = ("ป่าถูกทำลายจากการบุกรุก ตัดไม้ ไฟป่า และโครงการพัฒนา ผลคือน้ำท่วม ดินถล่ม ขาดน้ำ และสูญเสียความหลากหลาย "
               "แก้ไขด้วยการปลูกป่า ป่าชุมชน พื้นที่คุ้มครอง และใช้ทรัพยากรอย่างประหยัด")


FOREST_FACTS = (
    ("ป่าชายเลนมีความสำคัญอย่างไร", "เป็นแหล่งอนุบาลสัตว์น้ำ และช่วยลดการกัดเซาะชายฝั่ง",
     ("ช่วยให้น้ำทะเลจืดลง และทำให้ปลาน้ำจืดขยายพันธุ์ได้ดี", "เป็นแหล่งทำนาเกลือ และช่วยเพิ่มพื้นที่ชายฝั่งให้กว้างขึ้น", "เป็นแหล่งทำนาเกลือเท่านั้น", "ไม่มีประโยชน์ทางระบบนิเวศ")),
    ("ป่าต้นน้ำช่วยให้มีน้ำไหลในลำธารตลอดปีได้อย่างไร", "รากไม้และซากใบไม้ช่วยให้น้ำฝนซึมลงดินและค่อย ๆ ไหลออกมา",
     ("ต้นไม้สร้างน้ำขึ้นเองจากรากแล้วปล่อยลงลำธารตลอดเวลา", "ต้นไม้ดูดน้ำจากลำธารไปเก็บไว้ ทำให้น้ำในลำธารลดลงตลอดปี", "ต้นไม้ดูดน้ำจากลำธารจนหมด", "ป่าทำให้น้ำระเหยเร็วขึ้นเท่านั้น")),
    ("เหตุใดการปลูกป่าด้วยพืชพื้นเมืองหลายชนิดจึงดีกว่าปลูกพืชชนิดเดียว", "ฟื้นฟูความหลากหลายและแหล่งอาหารของสัตว์ป่าได้ใกล้เคียงธรรมชาติ",
     ("ปลูกได้เร็วกว่าและได้เนื้อไม้ชนิดเดียวที่ขายได้ราคาดี", "ไม่ต้องดูแลเลย เพราะไม้ชนิดเดียวทนโรคและแมลงได้ทั้งหมด", "ใช้พื้นที่น้อยกว่า", "ป้องกันไฟป่าได้ทั้งหมด")),
)


@question_type(
    "biology.forest_conservation_foundation",
    display_name={"th": "สาเหตุและผลกระทบของการทำลายป่าไม้"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_FOREST,
)
class ForestConservationFoundation(QuestionType):
    """Causes against effects against remedies."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        groups = {"สาเหตุของการทำลายป่าไม้": CAUSES, "ผลกระทบจากการทำลายป่าไม้": EFFECTS, "แนวทางอนุรักษ์ป่าไม้": REMEDIES}
        label = rng.choice(sorted(groups))
        pool = [x for k, v in groups.items() if k != label for x in v]
        return _labelled(stem=f"ข้อใดเป็น{label}", correct=rng.choice(groups[label]), wrongs=tuple(pool), topic=TOPIC_FOREST,
                         hint=FOREST_HINT)


@question_type(
    "biology.forest_conservation_fluency",
    display_name={"th": "ความสำคัญของป่าไม้และการฟื้นฟู"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_FOREST,
)
class ForestConservationFluency(QuestionType):
    """Why mangroves and watershed forests matter, and how to restore."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            cause, effect = rng.choice((("ตัดไม้บนภูเขาจนหมด", "ดินถล่มและน้ำป่าไหลหลากในฤดูฝน"),
                                        ("ถางป่าชายเลนทำนากุ้ง", "ชายฝั่งถูกกัดเซาะและสัตว์น้ำวัยอ่อนลดลง"),
                                        ("เผาป่าเพื่อเตรียมพื้นที่เพาะปลูก", "หมอกควันและฝุ่น PM2.5 เพิ่มขึ้น"),
                                        ("บุกรุกป่าต้นน้ำ", "ลำธารแห้งในฤดูแล้ง")))
            pool = [e for e in EFFECTS if e != effect] + ["ปริมาณน้ำฝนเพิ่มขึ้นทุกปี"]
            return _labelled(stem=f"ผลกระทบโดยตรงที่สุดจากการ{cause}คือข้อใด", correct=effect, wrongs=tuple(pool),
                             topic=TOPIC_FOREST, hint=FOREST_HINT)
        stem, right, wrongs = rng.choice(FOREST_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FOREST, hint=FOREST_HINT)


@question_type(
    "biology.forest_conservation_application",
    display_name={"th": "คำนวณการเปลี่ยนแปลงพื้นที่ป่าและการดูดซับคาร์บอน"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_FOREST,
)
class ForestConservationApplication(QuestionType):
    """Share of forest lost, and CO₂ taken up by planted trees."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            before = rng.randrange(1000, 20001, 500)
            lost_share = rng.choice((5, 10, 12, 15, 20, 25, 30, 40))
            after = Fraction(before * (100 - lost_share), 100)
            return numeric(stem=f"จังหวัดหนึ่งมีพื้นที่ป่า {before:,} ไร่ ต่อมาเหลือ {show(after)} ไร่ พื้นที่ป่าลดลงร้อยละเท่าใด", answer=lost_share,
                           wrongs=[100 - lost_share, before - after, Fraction(after * 100, before)], unit="%", topic=TOPIC_FOREST,
                           hint="ร้อยละที่ลด = (พื้นที่เดิม − พื้นที่ใหม่) × 100 ÷ พื้นที่เดิม")
        per_tree = rng.choice((10, 15, 20, 22, 25))
        trees = rng.randrange(100, 5001, 100)
        years = rng.randint(1, 10)
        tonnes = Fraction(per_tree * trees * years, 1000)
        return numeric(stem=f"ต้นไม้ 1 ต้นดูดซับ CO₂ ได้ประมาณ {per_tree} kg ต่อปี ปลูกต้นไม้ {trees:,} ต้น ใน {years} ปีจะดูดซับ CO₂ ได้กี่ตัน",
                       answer=tonnes, wrongs=[per_tree * trees * years, Fraction(per_tree * trees, 1000), tonnes * 10], unit="ตัน",
                       topic=TOPIC_FOREST, hint="CO₂ รวม = ต่อต้นต่อปี × จำนวนต้น × จำนวนปี แล้วแปลง kg เป็นตัน (÷ 1,000)")
