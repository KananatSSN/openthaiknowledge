"""การแพร่และออสโมซิส

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/5

Sets moved here from: science_wave_b2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType, widen
from otk.sets._support.science_wave_b2 import DIFFUSION_SCENARIOS, LEVEL, SUBJECT, TOPIC, _labelled

PROVENANCE = Provenance("original")


DIFFUSION = "การแพร่"


OSMOSIS = "ออสโมซิส"


# (เหตุการณ์, กระบวนการที่เกิด). Osmosis is the special case where it is the
# *water* that moves through a membrane; everything else that spreads from high
# to low concentration is plain diffusion. Every example here is one or the
# other without argument.
EVERYDAY_CASES = (
    ("กลิ่นอาหารจากในครัวลอยไปทั่วบ้าน", DIFFUSION),
    ("หยดสีผสมอาหารลงในน้ำนิ่งแล้วสีค่อย ๆ กระจายจนทั่ว", DIFFUSION),
    ("กลิ่นน้ำหอมกระจายออกไปในห้องที่ปิดสนิท", DIFFUSION),
    ("น้ำตาลที่ใส่ลงในน้ำชาค่อย ๆ กระจายจนหวานทั้งแก้ว", DIFFUSION),
    ("แก๊สออกซิเจนแพร่จากถุงลมปอดเข้าสู่หลอดเลือดฝอย", DIFFUSION),
    ("รากพืชดูดน้ำจากดินเข้าสู่เซลล์ขนราก", OSMOSIS),
    ("ผักสดที่แช่น้ำไว้กลับเต่งขึ้นกว่าเดิม", OSMOSIS),
    ("ผักที่โรยเกลือไว้สักครู่แล้วมีน้ำซึมออกมาจนนิ่ม", OSMOSIS),
    ("เซลล์เม็ดเลือดแดงที่หยดลงในน้ำกลั่นแล้วบวมจนแตก", OSMOSIS),
    ("ปลาน้ำจืดที่ถูกนำไปใส่ในน้ำเค็มแล้วเสียน้ำออกจากตัว", OSMOSIS),
)


# (ความเข้มข้นของสารละลายภายนอกเทียบกับภายในเซลล์, ทิศทางที่น้ำเคลื่อน, ผลต่อเซลล์)
TONICITY = (
    ("เข้มข้นน้อยกว่าภายในเซลล์", "น้ำเคลื่อนเข้าสู่เซลล์", "เซลล์เต่งขึ้น"),
    ("เข้มข้นมากกว่าภายในเซลล์", "น้ำเคลื่อนออกจากเซลล์", "เซลล์เหี่ยวลง"),
    ("เข้มข้นเท่ากับภายในเซลล์", "น้ำเคลื่อนเข้าและออกในอัตราเท่ากัน",
     "ขนาดของเซลล์ไม่เปลี่ยนแปลง"),
)


@question_type(
    "cell.diffusion_foundation",
    display_name={"th": "การแพร่และออสโมซิสคืออะไร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class DiffusionFoundation(ConceptBankType):
    """What each process is, and what makes osmosis a special case of the other."""

    ITEMS = widen([
        Concept(
            "การแพร่ของสารเกิดขึ้นในทิศทางใด",
            "จากบริเวณที่มีความเข้มข้นของสารมากไปยังบริเวณที่มีความเข้มข้นน้อยกว่า",
            ("จากบริเวณที่มีความเข้มข้นของสารน้อยไปยังบริเวณที่มีความเข้มข้นมากกว่า",
             "จากบริเวณที่มีอุณหภูมิต่ำไปยังบริเวณที่มีอุณหภูมิสูงกว่าเสมอ",
             "จากบริเวณที่อยู่สูงกว่าลงสู่บริเวณที่อยู่ต่ำกว่าตามแรงโน้มถ่วง"),
        ),
        Concept(
            "ออสโมซิสต่างจากการแพร่ทั่วไปอย่างไร",
            "ออสโมซิสคือการแพร่ของน้ำผ่านเยื่อเลือกผ่าน ส่วนการแพร่เป็นการเคลื่อนที่ของสารใดก็ได้",
            ("ออสโมซิสคือการแพร่ของสารใดก็ได้ผ่านเยื่อเลือกผ่าน ส่วนการแพร่เป็นการเคลื่อนที่ของน้ำโดยเฉพาะ",
             "ออสโมซิสเคลื่อนจากความเข้มข้นน้อยไปมาก ส่วนการแพร่เคลื่อนจากมากไปน้อย",
             "ออสโมซิสต้องใช้พลังงานจากเซลล์ ส่วนการแพร่ไม่ต้องใช้พลังงาน"),
        ),
        Concept(
            "เยื่อเลือกผ่านมีสมบัติอย่างไร",
            "ยอมให้สารบางชนิดผ่านได้และกั้นสารบางชนิดไว้",
            ("ยอมให้สารทุกชนิดผ่านได้อย่างอิสระ",
             "ไม่ยอมให้สารใดผ่านได้เลย",
             "ยอมให้สารผ่านได้เฉพาะเมื่อเซลล์ใช้พลังงานผลักสารนั้น"),
        ),
        Concept(
            "การแพร่จะหยุดสุทธิเมื่อใด",
            "เมื่อความเข้มข้นของสารทั้งสองบริเวณเท่ากัน แม้อนุภาคยังเคลื่อนที่อยู่ตลอดเวลา",
            ("เมื่ออนุภาคของสารหยุดเคลื่อนที่ทั้งหมด เพราะความเข้มข้นสองบริเวณเท่ากัน",
             "เมื่อสารทั้งหมดเคลื่อนไปอยู่ที่บริเวณที่เคยมีความเข้มข้นน้อยกว่า",
             "เมื่ออุณหภูมิของทั้งสองบริเวณลดลงจนเท่ากัน"),
        ),
        Concept(
            "ปัจจัยใดทำให้การแพร่เกิดได้เร็วขึ้น",
            "ความแตกต่างของความเข้มข้นที่มากขึ้น และอุณหภูมิที่สูงขึ้น",
            ("ความแตกต่างของความเข้มข้นที่น้อยลง และอุณหภูมิที่ต่ำลง",
             "ขนาดของภาชนะที่ใหญ่ขึ้น โดยไม่เกี่ยวกับความเข้มข้น",
             "ความหนาแน่นของเยื่อเลือกผ่านที่มากขึ้น และอุณหภูมิที่ต่ำลง"),
        ),
        Concept(
            "การแพร่และออสโมซิสต้องใช้พลังงานจากเซลล์หรือไม่",
            "ไม่ต้องใช้ เพราะเป็นการเคลื่อนที่ไปตามความแตกต่างของความเข้มข้นเอง",
            ("ต้องใช้ทั้งสองกระบวนการ เพราะสารต้องผ่านเยื่อหุ้มเซลล์",
             "ออสโมซิสต้องใช้พลังงาน เพราะน้ำต้องถูกดันผ่านเยื่อเลือกผ่าน",
             "การแพร่ต้องใช้ ส่วนออสโมซิสไม่ต้องใช้"),
        ),
        Concept(
            "เหตุใดปากใบของพืชจึงเกี่ยวข้องกับการแพร่",
            "เพราะแก๊สคาร์บอนไดออกไซด์และออกซิเจนแพร่เข้าออกผ่านปากใบตามความแตกต่าง"
            "ของความเข้มข้น",
            ("เพราะปากใบผลักแก๊สเข้าออกโดยใช้พลังงานจากการสังเคราะห์ด้วยแสง",
             "เพราะปากใบเป็นทางที่น้ำออสโมซิสออกจากรากขึ้นสู่ใบ",
             "เพราะปากใบดูดแก๊สจากอากาศเข้ามาเก็บไว้ในแวคิวโอล"),
        ),
    ], (
        ("ไปในทิศทางใดก็ได้แบบสุ่ม โดยไม่มีทิศทางสุทธิของการเคลื่อนที่เลย",
         "จากบริเวณที่มีความดันอากาศต่ำไปสูงเท่านั้น"),
        ("ออสโมซิสเกิดเฉพาะในพืช ส่วนการแพร่เกิดเฉพาะในสัตว์",
         "ออสโมซิสคือการแพร่ของแก๊สผ่านปากใบเท่านั้น"),
        ("ยอมให้เฉพาะสารที่มีสีผ่านได้",
         "ยอมให้สารผ่านได้เฉพาะทิศทางเข้าเซลล์เท่านั้น"),
        ("เมื่อเยื่อเลือกผ่านถูกทำลาย",
         "เมื่อสารเปลี่ยนสถานะเป็นของแข็งทั้งหมด"),
        ("การลดความแตกต่างของความเข้มข้นให้เป็นศูนย์",
         "การทำให้อนุภาคของสารมีขนาดใหญ่ขึ้น"),
        ("ต้องใช้ทั้งสองกระบวนการ เพราะอนุภาคเคลื่อนที่เองไม่ได้",
         "ไม่ต้องใช้ เพราะเซลล์ดึงสารเข้ามาด้วยแรงแม่เหล็ก"),
        ("เพราะปากใบเป็นที่สร้างแก๊สออกซิเจนโดยตรง",
         "เพราะน้ำตาลแพร่ออกจากใบผ่านปากใบไปเลี้ยงราก"),
    ))


@question_type(
    "cell.diffusion_fluency",
    display_name={"th": "จำแนกการแพร่กับออสโมซิส และทิศทางการเคลื่อนของน้ำ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class DiffusionFluency(QuestionType):
    """Say which process an everyday case is, and which way water moves.

    ``ม.1/5`` asks for examples from everyday life as well as for the mechanism,
    so both are drilled here from one table of cases that are unambiguously one
    process or the other.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            osmosis = [case for case, kind in EVERYDAY_CASES if kind == OSMOSIS]
            diffusion = [case for case, kind in EVERYDAY_CASES
                         if kind == DIFFUSION]
            rng.shuffle(osmosis)
            rng.shuffle(diffusion)
            if rng.random() < 0.5:
                return _labelled(
                    stem="เหตุการณ์ใดต่อไปนี้เป็นออสโมซิส",
                    correct=osmosis[0],
                    wrongs=tuple(diffusion[:3]),
                    hint="ออสโมซิสคือการเคลื่อนที่ของน้ำผ่านเยื่อเลือกผ่าน "
                         "ถ้าสิ่งที่เคลื่อนที่ไม่ใช่น้ำก็เป็นการแพร่ทั่วไป",
                )
            return _labelled(
                stem="เหตุการณ์ใดต่อไปนี้เป็นการแพร่ที่ไม่ใช่ออสโมซิส",
                correct=diffusion[0],
                wrongs=tuple(osmosis[:3]),
                hint="ดูว่าสิ่งที่เคลื่อนที่คือน้ำหรือไม่ ถ้าเป็นน้ำผ่านเยื่อจะเรียกว่าออสโมซิส",
            )
        outside, direction, effect = TONICITY[rng.randrange(len(TONICITY))]
        others = [row for row in TONICITY if row[0] != outside]
        if which == 1:
            return _labelled(
                stem=f"นำเซลล์ไปแช่ในสารละลายที่{outside} น้ำจะเคลื่อนที่อย่างไร",
                correct=direction,
                wrongs=tuple(row[1] for row in others) + (
                    "น้ำจะไม่เคลื่อนที่เลย เพราะเยื่อหุ้มเซลล์กั้นน้ำไว้ทั้งหมด",),
                hint="น้ำเคลื่อนจากบริเวณที่มีน้ำมาก (สารละลายเจือจาง) "
                     "ไปยังบริเวณที่มีน้ำน้อยกว่า",
            )
        return _labelled(
            stem=f"นำเซลล์ไปแช่ในสารละลายที่{outside} เซลล์จะเปลี่ยนแปลงอย่างไร",
            correct=effect,
            wrongs=tuple(row[2] for row in others) + (
                "เซลล์จะแบ่งตัวเพิ่มจำนวนขึ้นทันที",),
            hint="ถ้าน้ำเข้าเซลล์มากกว่าออก เซลล์จะเต่ง ถ้าออกมากกว่าเข้า เซลล์จะเหี่ยว",
        )


@question_type(
    "cell.diffusion_application",
    display_name={"th": "อธิบายสถานการณ์จริงด้วยการแพร่และออสโมซิส"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class DiffusionApplication(QuestionType):
    """Explain a kitchen, garden or clinic result by where the water went.

    ``ม.1/5`` asks for everyday examples explained from evidence. Each item here
    states a result the learner could have seen and asks which way water moved
    and why, with the concentration comparison as the step that decides it.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(DIFFUSION_SCENARIOS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="เทียบความเข้มข้นภายนอกกับภายในเซลล์ก่อน แล้วจึงบอกว่าน้ำเคลื่อนไปทางใด",
        )
