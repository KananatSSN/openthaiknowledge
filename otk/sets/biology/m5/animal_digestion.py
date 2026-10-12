"""การย่อยอาหารของสัตว์

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/1

Sets moved here from: science_wave_f59.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f59 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_GUT = "การย่อยอาหารของสัตว์"


GUTS = {
    "ไม่มีทางเดินอาหาร": ("ฟองน้ำ",),
    "ทางเดินอาหารแบบไม่สมบูรณ์ (มีช่องเปิดทางเดียว)": ("ไฮดรา", "พลานาเรีย", "แมงกะพรุน"),
    "ทางเดินอาหารแบบสมบูรณ์ (มีปากและทวารหนัก)": ("ไส้เดือนดิน", "ตั๊กแตน", "ไก่", "วัว", "ปลา"),
}


GUT_PARTS = (
    ("กระเพาะพักอาหาร (ครอป) ของไส้เดือนดินและนก", "เก็บอาหารไว้ชั่วคราวและทำให้อาหารอ่อนนุ่ม"),
    ("กึ๋น (กิซซาร์ด) ของไส้เดือนดินและนก", "มีผนังกล้ามเนื้อหนาบดอาหารให้ละเอียด"),
    ("รูเมนของวัว", "มีจุลินทรีย์ช่วยย่อยเซลลูโลส"),
    ("แอบโอมาซัมของวัว", "เป็นกระเพาะจริงที่หลั่งเอนไซม์และกรดย่อยอาหาร"),
    ("ไทโฟลโซลในลำไส้ของไส้เดือนดิน", "เป็นรอยพับของผนังลำไส้ช่วยเพิ่มพื้นที่ดูดซึม"),
    ("เซลล์ปลอกคอ (โคอาโนไซต์) ของฟองน้ำ", "จับอาหารแล้วย่อยภายในเซลล์ด้วยฟูดแวคิวโอล"),
)


GUT_HINT = ("ฟองน้ำไม่มีทางเดินอาหาร ย่อยภายในเซลล์ ไฮดราและพลานาเรียมีช่องเปิดทางเดียว สัตว์ที่มีปากและทวารหนักมีทางเดินอาหารสมบูรณ์ "
            "ครอปพักอาหาร กึ๋นบด รูเมนมีจุลินทรีย์ย่อยเซลลูโลส")


PATHS = {
    "ไส้เดือนดิน": ("ปาก", "คอหอย", "หลอดอาหาร", "กระเพาะพักอาหาร", "กึ๋น", "ลำไส้", "ทวารหนัก"),
    "ไก่": ("ปาก", "หลอดอาหาร", "กระเพาะพักอาหาร", "กระเพาะแท้", "กึ๋น", "ลำไส้", "ทวารร่วม"),
    "วัว": ("ปาก", "หลอดอาหาร", "รูเมน", "เรติคิวลัม", "โอมาซัม", "แอบโอมาซัม", "ลำไส้เล็ก"),
}


@question_type(
    "biology.animal_digestion_foundation",
    display_name={"th": "ประเภทของทางเดินอาหารในสัตว์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GUT,
)
class AnimalDigestionFoundation(QuestionType):
    """No gut, one opening, or two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(GUTS))
        animal = rng.choice(GUTS[kind])
        others = [k for k in GUTS if k != kind]
        if rng.random() < 0.55:
            return _labelled(stem=f"{animal}มีทางเดินอาหารแบบใด", correct=kind, wrongs=(*others, "มีทางเดินอาหารสองท่อแยกกัน"),
                             topic=TOPIC_GUT, hint=GUT_HINT)
        pool = [a for k in others for a in GUTS[k]]
        return _labelled(stem=f"สัตว์ใดมี{kind}", correct=animal, wrongs=tuple(pool), topic=TOPIC_GUT, hint=GUT_HINT)


@question_type(
    "biology.animal_digestion_fluency",
    display_name={"th": "โครงสร้างพิเศษในทางเดินอาหารของสัตว์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GUT,
)
class AnimalDigestionFluency(QuestionType):
    """Crop, gizzard, rumen, abomasum, typhlosole and collar cells."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, role = rng.choice(GUT_PARTS)
        others = rng.sample([p for p in GUT_PARTS if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ทำหน้าที่อะไร", correct=role, wrongs=tuple(p[1] for p in others), topic=TOPIC_GUT, hint=GUT_HINT)
        return _labelled(stem=f"โครงสร้างใด{role}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_GUT, hint=GUT_HINT)


@question_type(
    "biology.animal_digestion_application",
    display_name={"th": "ลำดับการเคลื่อนที่ของอาหารในทางเดินอาหารของสัตว์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GUT,
)
class AnimalDigestionApplication(QuestionType):
    """Put the stretch of gut in order, or say what comes next."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal = rng.choice(sorted(PATHS))
        path = PATHS[animal]
        if rng.random() < 0.5:
            i = rng.randrange(len(path) - 1)
            nxt = path[i + 1]
            pool = sorted({p for ps in PATHS.values() for p in ps} - {nxt, path[i]})
            return _labelled(stem=f"ในทางเดินอาหารของ{animal} อาหารที่ผ่าน{path[i]}แล้วจะเข้าสู่ส่วนใดต่อไป", correct=nxt,
                             wrongs=tuple(pool), topic=TOPIC_GUT, hint=GUT_HINT + " วัวเคี้ยวเอื้องย้อนอาหารจากรูเมนและเรติคิวลัมมาเคี้ยวใหม่")
        start = rng.randrange(len(path) - 3)
        chunk = list(path[start:start + 4])
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            c = chunk[:]
            rng.shuffle(c)
            if c != chunk:
                wrongs[" → ".join(c)] = None
        return _labelled(stem=f"ข้อใดเรียงลำดับการเคลื่อนที่ของอาหารใน{animal}ได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                         topic=TOPIC_GUT, hint=GUT_HINT)
