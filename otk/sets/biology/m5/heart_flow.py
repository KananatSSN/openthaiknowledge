"""ทิศทางการไหลของเลือดผ่านหัวใจ

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/11

Sets moved here from: science_wave_f62.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f62 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_ROUTE = "ทิศทางการไหลของเลือดผ่านหัวใจ"


ROUTE = ("เวนาคาวา", "หัวใจห้องบนขวา", "ลิ้นไตรคัสพิด", "หัวใจห้องล่างขวา", "พัลโมนารีอาร์เทอรี", "ปอด",
         "พัลโมนารีเวน", "หัวใจห้องบนซ้าย", "ลิ้นไบคัสพิด", "หัวใจห้องล่างซ้าย", "เอออร์ตา", "เนื้อเยื่อทั่วร่างกาย")


OXYGEN_RICH = {"พัลโมนารีเวน", "หัวใจห้องบนซ้าย", "หัวใจห้องล่างซ้าย", "เอออร์ตา"}


OXYGEN_POOR = {"เวนาคาวา", "หัวใจห้องบนขวา", "หัวใจห้องล่างขวา", "พัลโมนารีอาร์เทอรี"}


ROUTE_HINT = ("เลือดจากร่างกาย → เวนาคาวา → ห้องบนขวา → ห้องล่างขวา → พัลโมนารีอาร์เทอรี → ปอด → พัลโมนารีเวน → ห้องบนซ้าย "
              "→ ห้องล่างซ้าย → เอออร์ตา → ร่างกาย หัวใจซีกขวามีเลือดที่มี O₂ ต่ำ ซีกซ้ายมี O₂ สูง")


@question_type(
    "biology.heart_flow_foundation",
    display_name={"th": "เส้นทางของเลือดผ่านหัวใจ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROUTE,
)
class HeartFlowFoundation(QuestionType):
    """What comes next along the route."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        i = rng.randrange(len(ROUTE) - 1)
        forward = rng.random() < 0.6
        here = ROUTE[i] if forward else ROUTE[i + 1]
        target = ROUTE[i + 1] if forward else ROUTE[i]
        pool = [r for r in ROUTE if r not in (here, target)]
        return _labelled(stem=f"เลือดที่ผ่าน{here}แล้วจะไหลไปยังส่วนใดต่อไป" if forward else f"เลือดที่ไหลเข้าสู่{here}มาจากส่วนใดโดยตรง",
                         correct=target, wrongs=tuple(pool), topic=TOPIC_ROUTE, hint=ROUTE_HINT)


@question_type(
    "biology.heart_flow_fluency",
    display_name={"th": "เลือดที่มีออกซิเจนสูงและต่ำในหัวใจและหลอดเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROUTE,
)
class HeartFlowFluency(QuestionType):
    """Left side oxygen-rich, right side oxygen-poor; the pulmonary vessels break the artery rule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rich = rng.random() < 0.5
        right_pool, wrong_pool = (OXYGEN_RICH, OXYGEN_POOR) if rich else (OXYGEN_POOR, OXYGEN_RICH)
        if rng.random() < 0.3:
            facts = (("พัลโมนารีอาร์เทอรีต่างจากอาร์เทอรีอื่นอย่างไร", "นำเลือดที่มี O₂ ต่ำจากหัวใจไปปอด",
                      ("นำเลือดที่มี O₂ สูงไปทั่วร่างกาย", "นำเลือดกลับเข้าหัวใจ", "ไม่มีเลือดไหลผ่าน")),
                     ("พัลโมนารีเวนต่างจากเวนอื่นอย่างไร", "นำเลือดที่มี O₂ สูงจากปอดกลับเข้าหัวใจ",
                      ("นำเลือดที่มี O₂ ต่ำเข้าหัวใจ", "นำเลือดออกจากหัวใจไปปอด", "มีผนังหนาที่สุดในร่างกาย")),
                     ("วงจรปอด (pulmonary circulation) เริ่มต้นและสิ้นสุดที่ใด", "เริ่มที่หัวใจห้องล่างขวา สิ้นสุดที่หัวใจห้องบนซ้าย",
                      ("เริ่มที่หัวใจห้องล่างซ้าย สิ้นสุดที่หัวใจห้องบนขวา", "เริ่มที่ปอด สิ้นสุดที่ปอด", "เริ่มที่เอออร์ตา สิ้นสุดที่เวนาคาวา")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_ROUTE, hint=ROUTE_HINT)
        return _labelled(stem=f"ข้อใดมีเลือดที่มีออกซิเจน{'สูง' if rich else 'ต่ำ'}",
                         correct=rng.choice(sorted(right_pool)), wrongs=tuple(sorted(wrong_pool)), topic=TOPIC_ROUTE,
                         hint=ROUTE_HINT)


@question_type(
    "biology.heart_flow_application",
    display_name={"th": "ลำดับการไหลเวียนเลือดของมนุษย์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ROUTE,
)
class HeartFlowApplication(QuestionType):
    """Put a stretch of the circuit in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        start = rng.randrange(len(ROUTE) - 3)
        chunk = list(ROUTE[start:start + 4])
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            c = chunk[:]
            rng.shuffle(c)
            if c != chunk:
                wrongs[" → ".join(c)] = None
        return _labelled(stem="ข้อใดเรียงลำดับการไหลของเลือดได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs), topic=TOPIC_ROUTE,
                         hint=ROUTE_HINT)
