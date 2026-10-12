"""การผุพัง การกร่อน และการสะสมตัว

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/5

Sets moved here from: science_wave_c20.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import LETTERS, SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c20 import PROCESS_SCENARIOS

PROVENANCE = Provenance("original")


PROCESS_TOPIC = "การผุพัง การกร่อน และการสะสมตัว"


class Process(NamedTuple):
    """A surface process, what it is, the model that shows it, and landforms it makes."""
    name: str
    means: str
    model: str
    examples: tuple[str, ...]


PROCESSES = (
    Process("การผุพังอยู่กับที่",
            "หินแตกหรือเปลี่ยนแปลงทางเคมีอยู่ ณ ที่เดิม โดยยังไม่ถูกพาไปที่อื่น",
            "แช่ก้อนหินปูนในน้ำส้มสายชูหลายวัน ผิวหินกร่อนเป็นหลุมและมีฟองแก๊สเกิดขึ้น",
            ("หินบนยอดเขาแตกเป็นแผ่นกาบเพราะร้อนและเย็นสลับกันทุกวัน",
             "รากไม้ชอนไชเข้าไปในรอยแตกจนก้อนหินปริออก")),
    Process("การกร่อน",
            "ตัวกลาง เช่น น้ำ ลม หรือคลื่น พาตะกอนและเศษหินออกไปจากที่เดิม",
            "รดน้ำจากบัวรดน้ำลงบนกองทรายที่ลาดเอียง ทรายถูกน้ำพาไหลลงไปเป็นร่อง",
            ("หุบเขารูปตัววีที่แม่น้ำกัดเซาะลึกลงไปในหิน",
             "ผาหินริมทะเลที่ถูกคลื่นกัดเซาะจนเว้าเข้าไป")),
    Process("การสะสมตัวของตะกอน",
            "ตะกอนตกทับถมเมื่อตัวกลางที่พาตะกอนมาเคลื่อนที่ช้าลง",
            "ที่ปลายร่องน้ำบนกองทรายซึ่งน้ำไหลช้าลง ทรายตกกองรวมกันเป็นรูปพัด",
            ("สามเหลี่ยมปากแม่น้ำที่ตะกอนทับถมจนเกิดแผ่นดินใหม่",
             "หาดทรายที่เกิดจากคลื่นพาทรายมาทับถม")),
)


# More models of each process. Each shows its own process only: rock changing in
# place, material carried away, or material settling where the carrier slows.
MORE_MODELS = {
    "การผุพังอยู่กับที่": (
        "ชุบก้อนดินเหนียวแห้งในน้ำแล้วตากแดดสลับกันหลายรอบ ก้อนดินปริแตกเป็นเสี่ยงอยู่ที่เดิม",
        "หยอดน้ำลงในรอยแตกของก้อนปูนปลาสเตอร์แล้วแช่แข็งสลับกับละลายหลายรอบ ก้อนปูนแตกออกอยู่ที่เดิม",
    ),
    "การกร่อน": (
        "ใช้ไดร์เป่าผมเป่าลมผ่านกองทรายแห้ง ทรายถูกลมพาปลิวออกไปจากกอง",
        "เทน้ำจากขวดลงบนกองดินซ้ำหลายครั้ง ดินถูกน้ำพาไหลออกจากกองเป็นร่อง",
    ),
    "การสะสมตัวของตะกอน": (
        "เทน้ำขุ่นที่มีดินปนลงในแก้วแล้วตั้งทิ้งไว้ ตะกอนค่อย ๆ ตกทับถมเป็นชั้นที่ก้นแก้ว",
        "เป่าลมพาทรายไปกระทบแผ่นไม้ที่ขวางไว้ ทรายหยุดและกองสะสมอยู่หน้าแผ่นไม้",
    ),
}


def _match_models(order: list[str]) -> str:
    return " / ".join(f"แบบจำลอง {letter} → {name}" for letter, name in zip(LETTERS, order))


@question_type(
    "geo.surface_processes_foundation",
    display_name={"th": "ยกตัวอย่างผลของการผุพัง การกร่อน และการสะสมตัวต่อผิวโลก"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=PROCESS_TOPIC,
)
class SurfaceProcessesFoundation(QuestionType):
    """Give an example of each process changing the land — the free verb ยกตัวอย่าง."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        process = rng.choice(PROCESSES)
        example = rng.choice(process.examples)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{example}” เป็นตัวอย่างผลของกระบวนการใดที่ทำให้ผิวโลกเปลี่ยนแปลง",
                correct=process.name,
                wrongs=tuple(other.name for other in PROCESSES if other.name != process.name)
                       + ("การแปรสภาพของหินภายใต้ความร้อนและความดันสูง",),
                hint="ถามว่าหินยังอยู่ที่เดิม ถูกพาออกไป หรือถูกพามาทับถม",
                topic=PROCESS_TOPIC,
            )
        others = [other for other in PROCESSES if other.name != process.name]
        wrongs = [rng.choice(other.examples) for other in others]
        wrongs.append("หินหนืดดันตัวขึ้นมาเย็นตัวเป็นหินอัคนี")
        return _labelled(
            stem=f"ข้อใดเป็นตัวอย่างผลของ{process.name}ที่ทำให้ผิวโลกเปลี่ยนแปลง",
            correct=example,
            wrongs=tuple(wrongs),
            hint="ถามว่าหินยังอยู่ที่เดิม ถูกพาออกไป หรือถูกพามาทับถม",
            topic=PROCESS_TOPIC,
        )


@question_type(
    "geo.surface_processes_fluency",
    display_name={"th": "อธิบายการผุพัง การกร่อน และการสะสมตัวจากแบบจำลอง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=PROCESS_TOPIC,
)
class SurfaceProcessesFluency(QuestionType):
    """Place all three processes against the models; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shown = list(PROCESSES)
        rng.shuffle(shown)
        record = " / ".join(f"แบบจำลอง {letter}: {rng.choice((process.model, *MORE_MODELS[process.name]))}"
                            for letter, process in zip(LETTERS, shown))
        names = [process.name for process in shown]
        return _labelled(
            stem=f"นักเรียนทำแบบจำลอง 3 แบบ — {record} "
                 "ข้อใดอธิบายว่าแต่ละแบบจำลองแสดงกระบวนการใดได้ถูกต้องทั้งหมด",
            correct=_match_models(names),
            # Each swap of two, then both rotations: every model misplaced.
            wrongs=tuple(_match_models(_swapped(names, i, j)) for i, j in _swaps(rng, 3, 3))
                   + (_match_models(names[1:] + names[:1]), _match_models(names[2:] + names[:2])),
            hint="ดูว่าในแบบจำลอง หินเปลี่ยนแปลงอยู่ที่เดิม ถูกพาไป หรือตกทับถม",
            topic=PROCESS_TOPIC,
        )


@question_type(
    "geo.surface_processes_application",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงของผิวโลก"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=PROCESS_TOPIC,
)
class SurfaceProcessesApplication(QuestionType):
    """Sediment sorting down a river, cleared slopes, and a Thai rock pillar."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PROCESS_SCENARIOS,
            hint="ถามว่าหินผุพังที่ใด ถูกพาไปอย่างไร และตกทับถมเมื่อใด",
        ), PROCESS_TOPIC)
