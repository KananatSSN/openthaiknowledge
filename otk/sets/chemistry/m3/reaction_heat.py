"""ปฏิกิริยาดูดความร้อนและคายความร้อน

เคมี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.3/5

Sets moved here from: science_wave_d12.
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
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d10 import SECONDARY_THREE

PROVENANCE = Provenance("original")


HEAT_TOPIC = "ปฏิกิริยาดูดความร้อนและคายความร้อน"


class Heat(NamedTuple):
    what: str
    gives_out: bool


HEATS = (
    Heat("ใส่แคลเซียมคลอไรด์ลงในน้ำ", True),
    Heat("เติมสารละลายโซเดียมไฮดรอกไซด์ลงในกรดไฮโดรคลอริก", True),
    Heat("ใส่ชิ้นแมกนีเซียมลงในกรดไฮโดรคลอริก", True),
    Heat("ใส่แอมโมเนียมคลอไรด์ลงในน้ำ", False),
    Heat("ผสมผงฟูกับน้ำส้มสายชู", False),
    Heat("ผสมผงฟูกับกรดซิตริกในน้ำ", False),
    Heat("ละลายโซเดียมไฮดรอกไซด์ในน้ำ", True),
    Heat("ใส่โพแทสเซียมไนเตรตลงในน้ำ", False),
)


def heat_parts(heat: Heat, start: int, end: int) -> tuple[Part, ...]:
    change = abs(end - start)
    if heat.gives_out:
        kind = Part("ประเภท", "ปฏิกิริยาคายความร้อน", "ปฏิกิริยาดูดความร้อน")
        evidence = Part("หลักฐาน", f"อุณหภูมิเพิ่มขึ้น {change} องศาเซลเซียส", f"อุณหภูมิลดลง {change} องศาเซลเซียส")
        energy = Part("พลังงาน", "ระบบถ่ายโอนความร้อนออกสู่สิ่งแวดล้อม สารละลายจึงร้อนขึ้น",
                      "ระบบรับความร้อนจากสิ่งแวดล้อม สารละลายจึงร้อนขึ้น")
    else:
        kind = Part("ประเภท", "ปฏิกิริยาดูดความร้อน", "ปฏิกิริยาคายความร้อน")
        evidence = Part("หลักฐาน", f"อุณหภูมิลดลง {change} องศาเซลเซียส", f"อุณหภูมิเพิ่มขึ้น {change} องศาเซลเซียส")
        energy = Part("พลังงาน", "ระบบรับความร้อนจากสิ่งแวดล้อม สารละลายจึงเย็นลง",
                      "ระบบถ่ายโอนความร้อนออกสู่สิ่งแวดล้อม สารละลายจึงเย็นลง")
    return (kind, evidence, energy)


HEAT_SCENARIOS = (
    ("แผ่นประคบเย็นแบบใช้ครั้งเดียวทำงานเมื่อบีบให้ถุงน้ำด้านในแตกผสมกับผงสารเคมี ผงสารเคมีนั้นควรทำปฏิกิริยาแบบใดกับน้ำ",
     "ปฏิกิริยาดูดความร้อน เพื่อดึงความร้อนจากบริเวณที่ประคบให้เย็นลง",
     ("ปฏิกิริยาคายความร้อน เพื่อให้ถุงเย็นลง",
      "ไม่เกิดปฏิกิริยา เพราะความเย็นมาจากน้ำอย่างเดียว",
      "ปฏิกิริยาคายความร้อน เพราะแผ่นประคบต้องร้อนก่อนจึงเย็น",
      "ปฏิกิริยาดูดความร้อน เพื่อปล่อยความร้อนให้ผิวหนัง",
      "ปฏิกิริยาคายความร้อน เพื่อดึงความร้อนออกจากผิวหนัง")),
    ("อาหารกระป๋องแบบอุ่นร้อนได้เองมีช่องใส่ปูนขาวกับน้ำแยกไว้ เมื่อกดให้ผสมกันอาหารจะร้อนขึ้น ข้อใดอธิบายได้ถูกต้อง",
     "ปูนขาวทำปฏิกิริยากับน้ำแบบคายความร้อน ความร้อนที่ปล่อยออกมาถ่ายโอนไปยังอาหาร",
     ("ปูนขาวทำปฏิกิริยาดูดความร้อนจากอาหาร",
      "น้ำร้อนอยู่แล้วตั้งแต่ก่อนผสม",
      "อาหารคายความร้อนให้ปูนขาว",
      "ปูนขาวละลายน้ำโดยไม่มีการถ่ายโอนพลังงาน",
      "กระป๋องดูดความร้อนจากมือผู้ถือมาอุ่นอาหาร")),
    ("การทดลองหนึ่งอุณหภูมิลดลงจาก 28 เป็น 19 องศาเซลเซียส อีกการทดลองหนึ่งเพิ่มขึ้นจาก 28 เป็น 34 องศาเซลเซียส ข้อใดถูกต้อง",
     "การทดลองแรกเป็นปฏิกิริยาดูดความร้อนที่อุณหภูมิเปลี่ยน 9 องศาเซลเซียส การทดลองที่สองเป็นปฏิกิริยาคายความร้อนที่อุณหภูมิเปลี่ยน 6 องศาเซลเซียส",
     ("การทดลองแรกเป็นปฏิกิริยาคายความร้อน การทดลองที่สองเป็นปฏิกิริยาดูดความร้อน",
      "ทั้งสองเป็นปฏิกิริยาคายความร้อน",
      "การทดลองแรกเป็นปฏิกิริยาดูดความร้อนที่อุณหภูมิเปลี่ยน 19 องศาเซลเซียส",
      "ทั้งสองเป็นปฏิกิริยาดูดความร้อน",
      "การทดลองที่สองเป็นปฏิกิริยาคายความร้อนที่อุณหภูมิเปลี่ยน 34 องศาเซลเซียส")),
    ("ถุงอุ่นมือแบบผงเหล็กร้อนขึ้นเมื่อแกะซองให้สัมผัสอากาศ ข้อใดอธิบายได้ถูกต้อง",
     "ผงเหล็กทำปฏิกิริยากับออกซิเจนแบบคายความร้อน จึงปล่อยความร้อนออกมาให้มือ",
     ("ผงเหล็กดูดความร้อนจากอากาศมาเก็บไว้",
      "ถุงร้อนเพราะแรงเสียดทานจากการเขย่าเท่านั้น",
      "ผงเหล็กทำปฏิกิริยาดูดความร้อนจึงอุ่นขึ้น",
      "อากาศที่เข้าไปในถุงมีอุณหภูมิสูงอยู่แล้ว",
      "ผงเหล็กหลอมเหลวกลายเป็นของเหลวร้อน")),
)


def two_records(rng: Random) -> GeneratedQuestion:
    """One experiment warms and one cools from the same start; classify both with their changes."""
    start = rng.randint(25, 30)
    first_cools = rng.random() < 0.5
    a, b = rng.sample(range(3, 13), 2)
    end1, end2 = (start - a, start + b) if first_cools else (start + a, start - b)
    k1, k2 = ("ดูดความร้อน", "คายความร้อน") if first_cools else ("คายความร้อน", "ดูดความร้อน")

    def line(x: str, dx: int, y: str, dy: int) -> str:
        return (f"การทดลองแรกเป็นปฏิกิริยา{x}ที่อุณหภูมิเปลี่ยน {dx} องศาเซลเซียส "
                f"การทดลองที่สองเป็นปฏิกิริยา{y}ที่อุณหภูมิเปลี่ยน {dy} องศาเซลเซียส")

    correct = line(k1, a, k2, b)
    wrongs = (line(k2, a, k1, b), line(k1, a, k1, b), line(k2, a, k2, b),
              line(k1, end1, k2, end2), line(k1, b, k2, a))
    return _labelled(
        stem=(f"การทดลองหนึ่งอุณหภูมิเปลี่ยนจาก {start} เป็น {end1} องศาเซลเซียส "
              f"อีกการทดลองหนึ่งเปลี่ยนจาก {start} เป็น {end2} องศาเซลเซียส ข้อใดถูกต้อง"),
        correct=correct,
        wrongs=tuple(w for w in dict.fromkeys(wrongs) if w != correct),
        hint="อุณหภูมิลดลงคือดูดความร้อน เพิ่มขึ้นคือคายความร้อน และขนาดการเปลี่ยนคือผลต่างของอุณหภูมิ",
        topic=HEAT_TOPIC,
    )


@question_type(
    "chem.reaction_heat_foundation",
    display_name={"th": "จำแนกปฏิกิริยาดูดความร้อนและคายความร้อนจากการสัมผัส"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class ReactionHeatFoundation(QuestionType):
    """Warm or cold to the touch; which kind of reaction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        heat = rng.choice(HEATS)
        feel = "ร้อนขึ้น" if heat.gives_out else "เย็นลง"
        right = ("ปฏิกิริยาคายความร้อน เพราะระบบถ่ายโอนความร้อนออกมาสู่สิ่งแวดล้อม" if heat.gives_out
                 else "ปฏิกิริยาดูดความร้อน เพราะระบบรับความร้อนจากสิ่งแวดล้อม")
        return _labelled(
            stem=f"เมื่อ{heat.what} แล้วจับภาชนะรู้สึกว่า{feel} ปฏิกิริยานี้เป็นแบบใด",
            correct=right,
            wrongs=("ปฏิกิริยาดูดความร้อน เพราะระบบรับความร้อนจากสิ่งแวดล้อม" if heat.gives_out
                    else "ปฏิกิริยาคายความร้อน เพราะระบบถ่ายโอนความร้อนออกมาสู่สิ่งแวดล้อม",
                    "ไม่เกี่ยวกับความร้อน เพราะอุณหภูมิไม่ใช่หลักฐานของปฏิกิริยา",
                    "ปฏิกิริยาคายความร้อน เพราะระบบรับความร้อนจากสิ่งแวดล้อม" if heat.gives_out
                    else "ปฏิกิริยาดูดความร้อน เพราะระบบถ่ายโอนความร้อนออกมาสู่สิ่งแวดล้อม",
                    "ไม่เกิดปฏิกิริยาเคมี เพราะอุณหภูมิที่เปลี่ยนมาจากมือของผู้จับ",
                    "เป็นได้ทั้งสองแบบ เพราะอุณหภูมิไม่ได้บอกทิศทางของความร้อน"),
            hint="ภาชนะร้อนขึ้นแปลว่าความร้อนออกมาจากระบบ เย็นลงแปลว่าระบบดึงความร้อนไป",
            topic=HEAT_TOPIC,
        )


@question_type(
    "chem.reaction_heat_fluency",
    display_name={"th": "วิเคราะห์ปฏิกิริยาดูดความร้อนและคายความร้อนจากการเปลี่ยนแปลงอุณหภูมิ"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class ReactionHeatFluency(QuestionType):
    """Temperatures before and after; the kind, the evidence and the energy together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        heat = rng.choice(HEATS)
        start = rng.randint(25, 30)
        change = rng.randint(4, 15)
        end = start + change if heat.gives_out else start - change
        return parts_item(
            rng, heat_parts(heat, start, end),
            stem=(f"นักเรียน{heat.what} วัดอุณหภูมิก่อนเกิดปฏิกิริยาได้ {start} องศาเซลเซียส "
                  f"และหลังเกิดปฏิกิริยาได้ {end} องศาเซลเซียส จากข้อมูลนี้ ข้อใดวิเคราะห์ได้ถูกต้องทั้งหมด"),
            hint="เทียบอุณหภูมิก่อนและหลัง แล้วถามว่าความร้อนไหลออกจากระบบหรือเข้าสู่ระบบ",
            topic=HEAT_TOPIC,
        )


@question_type(
    "chem.reaction_heat_application",
    display_name={"th": "ใช้ปฏิกิริยาดูดความร้อนและคายความร้อนในชีวิตประจำวัน"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class ReactionHeatApplication(QuestionType):
    """Instant cold packs, self-heating cans, and comparing two records."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return two_records(rng)
        return _retopic(scenario_question(
            rng, HEAT_SCENARIOS,
            hint="ถ้าต้องการให้เย็นใช้ปฏิกิริยาดูดความร้อน ถ้าต้องการให้ร้อนใช้ปฏิกิริยาคายความร้อน",
        ), HEAT_TOPIC)
