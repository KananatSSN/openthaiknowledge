"""วิธีการและผลของการต่อเซลล์ไฟฟ้าแบบอนุกรม

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/3

Sets moved here from: science_wave_d26.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d26 import SIXTH

PROVENANCE = Provenance("original")


SERIES_CELLS_TOPIC = "วิธีการและผลของการต่อเซลล์ไฟฟ้าแบบอนุกรม"


CELL_FACTS = (
    ("การต่อเซลล์ไฟฟ้าแบบอนุกรมทำอย่างไร", "นำขั้วบวกของเซลล์หนึ่งต่อกับขั้วลบของอีกเซลล์หนึ่ง เรียงต่อกันไปเรื่อย ๆ",
     ("นำขั้วบวกต่อกับขั้วบวก และขั้วลบต่อกับขั้วลบของแต่ละเซลล์", "ต่อเซลล์ไฟฟ้าเพียงเซลล์เดียวในวงจร",
      "นำเซลล์ไฟฟ้าหลายเซลล์วางขนานกันโดยไม่เชื่อมขั้วต่อกัน", "ต่อขั้วลบของทุกเซลล์เข้าด้วยกันเพียงจุดเดียว", "นำเซลล์มาวางเรียงกันโดยไม่ต้องให้ขั้วสัมผัสกัน")),
    ("ถ่านไฟฉายหนึ่งก้อนมีความต่างศักย์ประมาณเท่าใด", "1.5 โวลต์", ("15 โวลต์", "220 โวลต์", "0.15 โวลต์", "12 โวลต์", "150 โวลต์")),
    ("เมื่อต่อเซลล์ไฟฟ้าแบบอนุกรมเพิ่มขึ้น ความต่างศักย์รวมเป็นอย่างไร", "เพิ่มขึ้นเท่ากับผลรวมของความต่างศักย์ของแต่ละเซลล์",
     ("ลดลง เท่ากับผลต่างของความต่างศักย์แต่ละเซลล์", "เท่าเดิม เท่ากับความต่างศักย์ของเซลล์เดียว",
      "เท่ากับเซลล์ที่มีค่ามากที่สุด", "เป็นศูนย์ เพราะเซลล์หักล้างกันหมด", "ลดลงครึ่งหนึ่ง")),
    ("ถ้าใส่ถ่านก้อนหนึ่งกลับขั้วในวงจรที่ต่อถ่านแบบอนุกรม จะเกิดอะไรขึ้น", "ถ่านก้อนนั้นหักล้างกับก้อนอื่น ความต่างศักย์รวมจึงลดลง",
     ("ความต่างศักย์รวมเพิ่มขึ้น", "ไม่มีผลใด ๆ", "ถ่านทุกก้อนหมดทันที และหลอดไฟดับถาวร", "หลอดไฟสว่างจ้าขึ้น เพราะความต่างศักย์รวมเพิ่มเป็นสองเท่า", "กระแสไฟฟ้าไหลเร็วขึ้นสองเท่า")),
)


ARRANGEMENTS = (
    ("ขั้วบวกของก้อนที่ 1 แตะขั้วลบของก้อนที่ 2 และขั้วบวกของก้อนที่ 2 แตะขั้วลบของก้อนที่ 3", True),
    ("ขั้วบวกของก้อนที่ 1 แตะขั้วลบของก้อนที่ 2", True),
    ("ขั้วบวกของก้อนที่ 1 แตะขั้วบวกของก้อนที่ 2", False),
    ("ขั้วลบของก้อนที่ 1 แตะขั้วลบของก้อนที่ 2", False),
    ("ขั้วบวกของก้อนที่ 1 แตะขั้วลบของก้อนที่ 2 แต่ขั้วบวกของก้อนที่ 2 แตะขั้วบวกของก้อนที่ 3", False),
)


CELL_HINT = "ต่อแบบอนุกรมคือขั้วบวกของก้อนหนึ่งต่อกับขั้วลบของก้อนถัดไป ความต่างศักย์รวมเท่ากับผลบวกของแต่ละก้อน (ก้อนละ 1.5 โวลต์)"


SERIES_CELLS_STEM = ("นักเรียนต่อวงจรโดยใช้เซลล์ไฟฟ้า 1 เซลล์ หลอดไฟสว่างเล็กน้อย เมื่อเปลี่ยนเป็นต่อเซลล์ไฟฟ้า 2 เซลล์แบบอนุกรม "
                     "(ขั้วบวกของเซลล์หนึ่งต่อกับขั้วลบของอีกเซลล์หนึ่ง) หลอดไฟสว่างมากขึ้นชัดเจน "
                     "จากผลการทดลองนี้ ข้อใดอธิบายวิธีการและผลของการต่อเซลล์ไฟฟ้าแบบอนุกรมได้ถูกต้อง")


SERIES_CELLS_SCENARIOS = (
    ("ไฟฉายที่ใช้ถ่านไฟฉาย 2 ก้อนต่อแบบอนุกรมให้แสงสว่างจ้ากว่าไฟฉายรุ่นเดียวกันที่ใช้ถ่านเพียง 1 ก้อน เพราะเหตุใด",
     "ถ่านไฟฉาย 2 ก้อนที่ต่อแบบอนุกรมให้พลังงานไฟฟ้ารวมมากกว่า 1 ก้อน หลอดไฟจึงสว่างจ้ากว่า",
     ("ถ่านไฟฉาย 2 ก้อนให้พลังงานไฟฟ้ารวมเท่ากับ 1 ก้อนเสมอ", "จำนวนถ่านไฟฉายไม่มีผลต่อความสว่างของหลอดไฟฉาย", "ถ่านไฟฉาย 2 ก้อนต่อแบบอนุกรมให้พลังงานไฟฟ้าน้อยกว่า 1 ก้อน")),
    ("ของเล่นชนิดหนึ่งใส่ถ่านไฟฉายสลับขั้วผิดด้านหนึ่งก้อนในช่องใส่ถ่านแบบอนุกรม ของเล่นจะทำงานอย่างไร",
     "ของเล่นอาจไม่ทำงานเลย เพราะขั้วที่สลับผิดทำให้พลังงานไฟฟ้าหักล้างกันแทนที่จะรวมกัน",
     ("ของเล่นจะทำงานแรงขึ้นกว่าเดิมเพราะมีถ่านครบทุกก้อน", "การใส่ขั้วถ่านไม่มีผลต่อการทำงานของของเล่นเลย", "ของเล่นจะทำงานได้ปกติทุกประการเหมือนใส่ถ่านถูกขั้ว")),
    ("รีโมทควบคุมทีวีที่ใช้ถ่าน 2 ก้อนแบบอนุกรม เมื่อถ่านก้อนหนึ่งเสื่อมสภาพจนให้พลังงานได้น้อยลงมาก รีโมทจะเป็นอย่างไร",
     "รีโมทอาจทำงานได้ไม่เต็มประสิทธิภาพหรือหยุดทำงาน เพราะพลังงานไฟฟ้ารวมของวงจรลดลงตามถ่านก้อนที่เสื่อม",
     ("รีโมทยังทำงานได้ปกติเพราะถ่านอีกก้อนยังดีอยู่", "ถ่านก้อนที่เสื่อมสภาพไม่มีผลต่อวงจรที่ต่อแบบอนุกรม", "รีโมทจะทำงานแรงขึ้นเพราะถ่านก้อนที่เสื่อมสภาพให้พลังงานมากขึ้น")),
)


CELL_DEVICES = ("ไฟฉาย", "รถของเล่น", "นาฬิกาปลุก", "วิทยุพกพา", "หุ่นยนต์ของเล่น", "พัดลมมือถือ")


@question_type(
    "phys.series_cells_foundation",
    display_name={"th": "บอกวิธีการต่อเซลล์ไฟฟ้าแบบอนุกรม"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_TOPIC,
)
class SeriesCellsFoundation(QuestionType):
    """How to join cells in series, and whether a described join is series."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            arrangement, series = rng.choice(ARRANGEMENTS)
            good = "เป็นการต่อแบบอนุกรมที่ถูกต้อง เพราะขั้วบวกแตะขั้วลบของก้อนถัดไป"
            bad = "ไม่ใช่การต่อแบบอนุกรมที่ถูกต้อง เพราะมีขั้วชนิดเดียวกันแตะกัน"
            right, other = (good, bad) if series else (bad, good)
            return _labelled(stem=f"นักเรียนวางถ่านไฟฉายโดย{arrangement} ข้อใดถูกต้อง", correct=right,
                             wrongs=(other, "เป็นการต่อแบบขนาน เพราะถ่านวางเรียงกันเป็นแถวเดียว", "ถ่านจะไม่ให้พลังงานเลยไม่ว่าจะวางขั้วอย่างไร"),
                             hint=CELL_HINT, topic=SERIES_CELLS_TOPIC)
        stem, right, wrongs = rng.choice(CELL_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=CELL_HINT, topic=SERIES_CELLS_TOPIC)


@question_type(
    "phys.series_cells_fluency",
    display_name={"th": "ทดลองอธิบายวิธีการและผลของการต่อเซลล์ไฟฟ้าแบบอนุกรม"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_TOPIC,
)
class SeriesCellsFluency(QuestionType):
    """The one-and-two-cell experiment, or a drawn cell count and its total voltage."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _labelled(
                stem=SERIES_CELLS_STEM,
                correct="การต่อเซลล์ไฟฟ้าแบบอนุกรมทำให้พลังงานไฟฟ้ารวมในวงจรมากขึ้น หลอดไฟจึงสว่างขึ้น",
                wrongs=("การต่อเซลล์ไฟฟ้าแบบอนุกรมทำให้พลังงานไฟฟ้ารวมในวงจรลดลง หลอดไฟจึงสว่างน้อยลง",
                        "จำนวนเซลล์ไฟฟ้าที่ต่อในวงจรไม่มีผลต่อความสว่างของหลอดไฟเลย",
                        "การต่อแบบอนุกรมทำให้เซลล์ไฟฟ้าหมดเร็วขึ้นเท่านั้น โดยไม่ส่งผลต่อความสว่างของหลอดไฟ"),
                hint="เปรียบเทียบความสว่างของหลอดไฟก่อนและหลังเพิ่มเซลล์ไฟฟ้าแบบอนุกรม",
                topic=SERIES_CELLS_TOPIC,
            )
        if rng.random() < 0.5:
            a, b = rng.sample(range(1, 9), 2)
            brighter = "วงจร ก" if a > b else "วงจร ข"
            return _labelled(stem=f"วงจร ก ใช้ถ่านไฟฉาย {a} ก้อน วงจร ข ใช้ถ่านไฟฉาย {b} ก้อน ต่อแบบอนุกรมถูกขั้วกับหลอดไฟชนิดเดียวกัน "
                                  f"หลอดไฟของวงจรใดสว่างกว่า และเพราะเหตุใด",
                             correct=f"{brighter} เพราะมีถ่านต่ออนุกรมมากกว่า ความต่างศักย์รวมจึงมากกว่า",
                             wrongs=(f"{'วงจร ข' if brighter == 'วงจร ก' else 'วงจร ก'} เพราะมีถ่านน้อยกว่า ไฟฟ้าจึงไหลสะดวกกว่า",
                                     "สว่างเท่ากัน เพราะใช้หลอดไฟชนิดเดียวกัน", "ไม่สว่างทั้งสองวงจร เพราะต่อถ่านหลายก้อนไม่ได้"),
                             hint=CELL_HINT, topic=SERIES_CELLS_TOPIC)
        count = rng.randint(2, 8)
        total = Fraction(3, 2) * count
        return numeric(stem=f"นำถ่านไฟฉายก้อนละ 1.5 โวลต์ จำนวน {count} ก้อน มาต่อกันแบบอนุกรมอย่างถูกขั้ว ความต่างศักย์รวมเป็นกี่โวลต์",
                       answer=total, wrongs=[Fraction(3, 2), count, total + Fraction(3, 2)], unit="โวลต์", topic=SERIES_CELLS_TOPIC,
                       hint="ความต่างศักย์รวม = 1.5 × จำนวนก้อนที่ต่อแบบอนุกรมถูกขั้ว")


@question_type(
    "phys.series_cells_application",
    display_name={"th": "ใช้ความรู้เรื่องเซลล์ไฟฟ้าแบบอนุกรมอธิบายอุปกรณ์ในชีวิตประจำวัน"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_TOPIC,
)
class SeriesCellsApplication(QuestionType):
    """Authored cases, cells needed for a device, and a pack with one cell reversed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.25:
            return _retopic(scenario_question(
                rng, SERIES_CELLS_SCENARIOS,
                hint="เซลล์ไฟฟ้าที่ต่ออนุกรมถูกขั้วรวมพลังงานกัน ต่อผิดขั้วจะหักล้างกันแทน",
            ), SERIES_CELLS_TOPIC)
        device = rng.choice(CELL_DEVICES)
        if roll < 0.6:
            count = rng.randint(2, 8)
            need = Fraction(3, 2) * count
            return numeric(stem=f"{device}ต้องใช้ความต่างศักย์ {show(need)} โวลต์ ถ้าใช้ถ่านไฟฉายก้อนละ 1.5 โวลต์ต่อแบบอนุกรม ต้องใช้ถ่านกี่ก้อน",
                           answer=count, wrongs=[count * 2, count + 1, need], unit="ก้อน", topic=SERIES_CELLS_TOPIC,
                           hint="จำนวนก้อน = ความต่างศักย์ที่ต้องการ ÷ 1.5")
        count = rng.randint(3, 8)
        total = Fraction(3, 2) * (count - 2)
        return numeric(stem=f"{device}ใส่ถ่านไฟฉายก้อนละ 1.5 โวลต์ {count} ก้อนแบบอนุกรม แต่ใส่กลับขั้วผิดไป 1 ก้อน ความต่างศักย์รวมเหลือกี่โวลต์",
                       answer=total, wrongs=[Fraction(3, 2) * count, Fraction(3, 2) * (count - 1), total + 3 if total else 3], unit="โวลต์",
                       topic=SERIES_CELLS_TOPIC, hint="ก้อนที่กลับขั้วหักล้างกับก้อนที่ถูกขั้วหนึ่งก้อน จึงหายไปสองก้อน: 1.5 × (จำนวนก้อน − 2)")
