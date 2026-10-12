"""การดูดซับน้ำของวัสดุ

เคมี · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.2/1

Sets moved here from: science_wave_d1.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_d1 import SECOND, SUBJECT

PROVENANCE = Provenance("original")


ABSORPTION_TOPIC = "การดูดซับน้ำของวัสดุ"


# Four bands of absorption, so a record always ranks four materials unambiguously.
BANDS = (
    ("ฟองน้ำ", "ผ้าขนหนู"),
    ("กระดาษทิชชู", "ผ้าฝ้าย"),
    ("กระดาษแข็ง", "ไม้"),
    ("แผ่นพลาสติก", "แผ่นโลหะ"),
)


BAND_RANGES = ((8, 10), (5, 7), (1, 3), (0, 0))


class Use(NamedTuple):
    thing: str
    material: str
    because: str


USES = (
    Use("ผ้าเช็ดตัว", "ผ้าขนหนู", "ดูดซับน้ำได้ดี จึงซับน้ำออกจากตัวได้มาก"),
    Use("ฟองน้ำล้างจาน", "ฟองน้ำ", "ดูดซับน้ำและน้ำยาไว้ได้มาก"),
    Use("เสื้อกันฝน", "พลาสติก", "ไม่ดูดซับน้ำ น้ำฝนจึงไหลออกไม่เปียกตัว"),
    Use("กระดาษเช็ดมือ", "กระดาษทิชชู", "ดูดซับน้ำได้ดีและใช้ครั้งเดียวทิ้งได้"),
    Use("แก้วน้ำดื่ม", "แก้ว", "ไม่ดูดซับน้ำ จึงใส่น้ำไว้ได้โดยน้ำไม่ซึมออก"),
    Use("ถาดทำน้ำแข็ง", "โลหะ", "ไม่ดูดซับน้ำ จึงใส่น้ำไปแช่แข็งได้โดยน้ำไม่ซึมหายไป"),
    Use("ผ้าถูพื้น", "ผ้าฝ้าย", "ดูดซับน้ำได้ดี จึงเช็ดน้ำที่พื้นออกได้มาก"),
)


def absorption_record(rng: Random) -> list[tuple[str, int]]:
    """One material from each band, with the water it held, in shuffled order."""
    rows = [(rng.choice(band), rng.randint(low, high)) for band, (low, high) in zip(BANDS, BAND_RANGES)]
    rng.shuffle(rows)
    return rows


ABSORPTION_SCENARIOS = (
    ("นักเรียนทำน้ำหกบนโต๊ะ ควรเลือกใช้สิ่งใดเช็ดจึงเหมาะสมที่สุด",
     "ผ้าขนหนู เพราะดูดซับน้ำได้ดี",
     ("ถุงพลาสติก เพราะน้ำไม่ซึมผ่าน",
      "แผ่นอะลูมิเนียมฟอยล์ เพราะผิวมันวาว",
      "ไม้บรรทัดพลาสติก เพราะแข็งแรง",
      "กระดาษแข็ง เพราะแข็งแรง",
      "แผ่นโลหะ เพราะเย็น")),
    ("นักเรียนสองคนทดสอบการดูดซับน้ำของผ้าสองชนิด คนแรกใช้ผ้าชิ้นใหญ่ คนที่สองใช้ผ้าชิ้นเล็ก แล้วสรุปว่าผ้าชิ้นใหญ่ดูดซับน้ำได้ดีกว่า ข้อสรุปนี้มีปัญหาอย่างไร",
     "ผ้ามีขนาดไม่เท่ากัน จึงไม่รู้ว่าผลต่างมาจากชนิดของผ้าหรือจากขนาด",
     ("ไม่มีปัญหา เพราะผ้าชิ้นใหญ่ดูดซับน้ำได้ดีกว่าเสมอ",
      "ควรใช้น้ำร้อนแทนน้ำเย็น",
      "ควรทดสอบกับพลาสติกแทนผ้า",
      "ผ้าชิ้นเล็กดูดซับน้ำไม่ได้เลย",
      "ควรวัดด้วยไม้บรรทัดแทนการวัดน้ำ")),
    ("กล่องใส่ขนมที่ต้องวางไว้ในที่ชื้นควรทำจากวัสดุใด",
     "พลาสติก เพราะไม่ดูดซับน้ำ ขนมข้างในจึงไม่ชื้น",
     ("กระดาษทิชชู เพราะดูดซับความชื้นไว้ในกล่อง",
      "ผ้าฝ้าย เพราะนุ่มและดูดซับน้ำได้ดี",
      "ฟองน้ำ เพราะดูดซับน้ำได้มาก",
      "กระดาษแข็ง เพราะแข็งแรงและดูดซับความชื้น",
      "ผ้าขนหนู เพราะหนาและนุ่ม")),
)


# (job, whether it needs a material that soaks water up)
JOBS = (("ซับน้ำที่หกบนพื้น", True), ("ทำผ้าเช็ดตัว", True), ("ทำหลังคาเล้าไก่ให้กันฝน", False),
        ("ทำถุงใส่ของเปียก", False))


def absorb_choice(rng: Random) -> GeneratedQuestion:
    """Two materials' measured absorption; the one a job needs."""
    upper, lower = sorted(rng.sample(range(len(BANDS)), 2))
    hi, lo = rng.choice(BANDS[upper]), rng.choice(BANDS[lower])
    hi_ml = rng.randint(*BAND_RANGES[upper])
    lo_ml = rng.randint(*BAND_RANGES[lower])
    job, soak = rng.choice(JOBS)
    options = [f"{hi} เพราะดูดซับน้ำได้มากกว่า", f"{lo} เพราะดูดซับน้ำได้น้อยกว่า",
               f"{hi} เพราะดูดซับน้ำได้น้อยกว่า", f"{lo} เพราะดูดซับน้ำได้มากกว่า",
               "ใช้ได้ทั้งสองชนิดเท่ากัน เพราะดูดซับน้ำได้เท่ากัน"]
    correct = options[0] if soak else options[1]
    first, second = rng.sample([(hi, hi_ml), (lo, lo_ml)], 2)
    return _labelled(
        stem=(f"นักเรียนเทน้ำ 10 มิลลิลิตรลงบนวัสดุขนาดเท่ากัน {first[0]}ดูดซับน้ำไว้ {first[1]} มิลลิลิตร "
              f"{second[0]}ดูดซับน้ำไว้ {second[1]} มิลลิลิตร ถ้าต้องการ{job} ควรเลือกวัสดุใด"),
        correct=correct,
        wrongs=tuple(o for o in options if o != correct),
        hint="งานที่ต้องซับน้ำใช้วัสดุที่ดูดซับน้ำได้มาก งานที่ต้องกันน้ำใช้วัสดุที่ดูดซับน้ำได้น้อย",
        topic=ABSORPTION_TOPIC,
    )


@question_type(
    "chem.water_absorption_foundation",
    display_name={"th": "ระบุการนำสมบัติการดูดซับน้ำของวัสดุไปใช้"},
    level=SECOND, subject=SUBJECT, topic=ABSORPTION_TOPIC,
)
class WaterAbsorptionFoundation(QuestionType):
    """An everyday object; the material it uses and why its absorption suits it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(USES))
        use = USES[index]
        others = [other for i, other in enumerate(USES) if i != index]
        return _labelled(
            stem=f"{use.thing}ควรทำจากวัสดุใด เพราะเหตุใด",
            correct=f"{use.material} เพราะ{use.because}",
            wrongs=tuple(f"{other.material} เพราะ{other.because}" for other in rng.sample(others, 3)),
            hint="ถามว่าสิ่งของนี้ต้องการให้น้ำซึมเข้าไป หรือต้องการกันน้ำ",
            topic=ABSORPTION_TOPIC,
        )


@question_type(
    "chem.water_absorption_fluency",
    display_name={"th": "เปรียบเทียบการดูดซับน้ำของวัสดุจากผลการทดลอง"},
    level=SECOND, subject=SUBJECT, topic=ABSORPTION_TOPIC,
)
class WaterAbsorptionFluency(QuestionType):
    """An experiment's record; rank the four materials by the water they absorbed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = absorption_record(rng)
        record = " / ".join(f"{name} {amount} มิลลิลิตร" for name, amount in rows)
        ranked = [name for name, _ in sorted(rows, key=lambda row: -row[1])]
        return _labelled(
            stem=(f"นักเรียนเทน้ำ 10 มิลลิลิตรลงบนวัสดุขนาดเท่ากัน 4 ชนิด แล้ววัดปริมาณน้ำที่วัสดุดูดซับไว้ ได้ผลดังนี้ — "
                  f"{record} จากหลักฐานนี้ ข้อใดเรียงวัสดุจากดูดซับน้ำได้มากที่สุดไปน้อยที่สุดได้ถูกต้อง"),
            correct=" → ".join(ranked),
            wrongs=tuple(" → ".join(_swapped(ranked, i, j)) for i, j in _swaps(rng, 3, len(ranked))),
            hint="วัสดุที่ดูดซับน้ำไว้ได้มิลลิลิตรมากกว่า ดูดซับน้ำได้ดีกว่า",
            topic=ABSORPTION_TOPIC,
        )


@question_type(
    "chem.water_absorption_application",
    display_name={"th": "ใช้สมบัติการดูดซับน้ำเลือกวัสดุและตรวจการทดลอง"},
    level=SECOND, subject=SUBJECT, topic=ABSORPTION_TOPIC,
)
class WaterAbsorptionApplication(QuestionType):
    """Wiping a spill, a fair absorption test, and a box for a damp place."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return absorb_choice(rng)
        return _retopic(scenario_question(
            rng, ABSORPTION_SCENARIOS,
            hint="ถามว่างานนี้ต้องการให้วัสดุดูดซับน้ำหรือกันน้ำ และการเปรียบเทียบนั้นยุติธรรมหรือไม่",
        ), ABSORPTION_TOPIC)
