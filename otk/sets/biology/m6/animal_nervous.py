"""ระบบประสาทของสัตว์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/1

Sets moved here from: science_wave_f65.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f65 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ANIMAL = "ระบบประสาทของสัตว์"


NERVOUS = (
    ("ไฮดรา", "ร่างแหประสาทกระจายทั่วลำตัว ไม่มีศูนย์กลาง"),
    ("พลานาเรีย", "ปมประสาทที่หัว 1 คู่ และเส้นประสาทใหญ่ 2 เส้นทางด้านล่าง มีเส้นประสาทขวางเชื่อมคล้ายขั้นบันได"),
    ("ไส้เดือนดิน", "ปมประสาทสมองเหนือคอหอย และเส้นประสาทใหญ่ด้านท้องที่มีปมประสาททุกปล้อง"),
    ("หอย", "ปมประสาท 3 คู่ ได้แก่ ที่หัว ที่เท้า และที่อวัยวะภายใน เชื่อมกันด้วยเส้นประสาท"),
    ("แมลงและกุ้ง", "ปมประสาทสมองขนาดใหญ่ และเส้นประสาทใหญ่ด้านท้องที่มีปมประสาทเป็นระยะ"),
    ("สัตว์มีกระดูกสันหลัง", "สมองและไขสันหลังที่เป็นหลอดกลวงอยู่ทางด้านหลัง"),
)


NERVE_HINT = ("ไฮดรามีร่างแหประสาท พลานาเรียมีระบบประสาทแบบขั้นบันได ไส้เดือน แมลง และกุ้งมีเส้นประสาทด้านท้องที่มีปมประสาท "
              "สัตว์มีกระดูกสันหลังมีสมองและไขสันหลังด้านหลัง ยิ่งซับซ้อน ระบบประสาทยิ่งรวมศูนย์ที่หัว")


NERVE_FACTS = (
    ("เส้นประสาทใหญ่ของไส้เดือนดินและแมลงอยู่ทางด้านใดของลำตัว", "ด้านท้อง", ("ด้านหลัง", "ด้านข้าง", "กระจายทั่วไปไม่มีทิศทาง")),
    ("ไขสันหลังของสัตว์มีกระดูกสันหลังอยู่ทางด้านใดและมีลักษณะอย่างไร", "ด้านหลัง เป็นหลอดกลวง",
     ("ด้านท้อง เป็นเส้นตัน", "ด้านข้าง เป็นร่างแห", "ด้านท้อง เป็นหลอดกลวง")),
    ("แนวโน้มวิวัฒนาการของระบบประสาทจากไฮดราถึงสัตว์มีกระดูกสันหลังคือข้อใด", "เซลล์ประสาทรวมกลุ่มเป็นศูนย์กลางที่หัวมากขึ้น",
     ("เซลล์ประสาทกระจายตัวมากขึ้น", "ไม่มีการเปลี่ยนแปลง", "สมองมีขนาดเล็กลง")),
    ("การมีปมประสาทรวมอยู่ที่หัวมีประโยชน์อย่างไร", "รับรู้สิ่งเร้าจากทิศทางที่เคลื่อนที่ไปได้ดีและควบคุมการตอบสนองได้รวดเร็ว",
     ("ทำให้สัตว์เคลื่อนที่ไม่ได้", "ลดจำนวนเซลล์ประสาท", "ทำให้ไม่ต้องมีอวัยวะรับความรู้สึก")),
)


@question_type(
    "biology.animal_nervous_foundation",
    display_name={"th": "ระบบประสาทของสัตว์ต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalNervousFoundation(QuestionType):
    """Nerve net to brain and cord, animal by animal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, system = rng.choice(NERVOUS)
        others = rng.sample([n for n in NERVOUS if n[0] != animal], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ระบบประสาทของ{animal}มีลักษณะอย่างไร", correct=system, wrongs=tuple(n[1] for n in others), topic=TOPIC_ANIMAL,
                             hint=NERVE_HINT)
        return _labelled(stem=f"สัตว์ใดมีระบบประสาทแบบ \"{system}\"", correct=animal, wrongs=tuple(n[0] for n in others), topic=TOPIC_ANIMAL,
                         hint=NERVE_HINT)


@question_type(
    "biology.animal_nervous_fluency",
    display_name={"th": "เปรียบเทียบตำแหน่งและแนวโน้มของระบบประสาท"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalNervousFluency(QuestionType):
    """Ventral against dorsal cords, and centralisation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            groups = {"มีเส้นประสาทใหญ่ทางด้านท้อง": ("ไส้เดือนดิน", "แมลง", "กุ้ง", "พลานาเรีย"),
                      "มีไขสันหลังเป็นหลอดกลวงทางด้านหลัง": ("ปลา", "กบ", "นก", "งู", "คน"),
                      "มีร่างแหประสาทโดยไม่มีศูนย์กลาง": ("ไฮดรา", "แมงกะพรุน")}
            label = rng.choice(sorted(groups))
            others = [a for k, v in groups.items() if k != label for a in v]
            return _labelled(stem=f"สัตว์ใด{label}", correct=rng.choice(groups[label]), wrongs=tuple(others), topic=TOPIC_ANIMAL,
                             hint=NERVE_HINT)
        stem, right, wrongs = rng.choice(NERVE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_ANIMAL, hint=NERVE_HINT)


@question_type(
    "biology.animal_nervous_application",
    display_name={"th": "เรียงลำดับความซับซ้อนของระบบประสาท"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ANIMAL,
)
class AnimalNervousApplication(QuestionType):
    """Order animals from least to most centralised."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        order = ["ไฮดรา", "พลานาเรีย", "ไส้เดือนดิน", "แมลง", "สัตว์มีกระดูกสันหลัง"]
        picked = sorted(rng.sample(range(len(order)), 3))
        chunk = [order[i] for i in picked]
        if rng.random() < 0.5:
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                c = chunk[:]
                rng.shuffle(c)
                if c != chunk:
                    wrongs[" → ".join(c)] = None
            return _labelled(stem="ข้อใดเรียงระบบประสาทจากซับซ้อนน้อยไปมากได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                             topic=TOPIC_ANIMAL, hint=NERVE_HINT)
        most = rng.random() < 0.5
        four = sorted(rng.sample(range(len(order)), 4))
        right = order[four[-1]] if most else order[four[0]]
        return _labelled(stem=f"สัตว์ใดมีระบบประสาทที่รวมศูนย์{'มากที่สุด' if most else 'น้อยที่สุด'}", correct=right,
                         wrongs=tuple(order[i] for i in four if order[i] != right), topic=TOPIC_ANIMAL, hint=NERVE_HINT)
