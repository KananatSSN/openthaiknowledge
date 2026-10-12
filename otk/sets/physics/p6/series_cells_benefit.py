"""ประโยชน์ของการต่อเซลล์ไฟฟ้าแบบอนุกรม

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/4

Sets moved here from: science_wave_d26.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d26 import SIXTH

PROVENANCE = Provenance("original")


SERIES_CELLS_BENEFIT_TOPIC = "ประโยชน์ของการต่อเซลล์ไฟฟ้าแบบอนุกรม"


BENEFIT_FACTS = (
    ("การต่อเซลล์ไฟฟ้าแบบอนุกรมมีประโยชน์อย่างไร", "เพิ่มพลังงานไฟฟ้ารวม ทำให้อุปกรณ์ที่ต้องการพลังงานมากทำงานได้ตามต้องการ",
     ("ลดพลังงานไฟฟ้ารวมในวงจรเพื่อยืดอายุการใช้งานของอุปกรณ์ แต่อุปกรณ์ทำงานเหมือนเดิม", "ทำให้เซลล์ไฟฟ้าแต่ละเซลล์ไม่มีวันหมดพลังงาน แม้ใช้งานต่อเนื่องเป็นเวลานาน",
      "ไม่มีประโยชน์ใด ๆ เมื่อเทียบกับการใช้เซลล์ไฟฟ้าเพียงเซลล์เดียวในวงจร", "ทำให้ถ่านไฟฉายแต่ละก้อนเบาลงและพกพาได้สะดวกขึ้นกว่าเดิม", "ทำให้ต่อขั้วผิดได้โดยไม่มีผลต่อการทำงานของอุปกรณ์ไฟฟ้าในวงจร")),
    ("ข้อใดเป็นข้อควรระวังเมื่อใช้ถ่านหลายก้อนต่อแบบอนุกรม", "ใส่ขั้วให้ถูกทุกก้อน และใช้ถ่านชนิดเดียวกันที่ใหม่พอ ๆ กัน",
     ("ใส่ถ่านเก่าปนกับถ่านใหม่ได้เสมอ โดยไม่มีผลต่ออุปกรณ์", "ใส่ขั้วอย่างไรก็ได้ เพราะถ่านทุกก้อนให้พลังงานเท่ากัน", "ใช้ถ่านต่างขนาดปนกันจะดีกว่า เพราะได้พลังงานหลายระดับ", "ควรทิ้งถ่านที่ใช้แล้วลงถังขยะทั่วไปรวมกับขยะเปียก", "ควรใส่ถ่านเกินจำนวนที่อุปกรณ์กำหนด เพื่อให้ทำงานแรงขึ้น")),
    ("ถ้าใช้ถ่านจำนวนมากเกินกว่าที่อุปกรณ์ต้องการ อาจเกิดผลอย่างไร", "หลอดไฟหรืออุปกรณ์อาจเสียหาย เพราะได้รับพลังงานไฟฟ้ามากเกินไป",
     ("อุปกรณ์ทำงานได้นานขึ้นเสมอ เพราะถ่านแต่ละก้อนใช้พลังงานน้อยลง", "ไม่มีผลใด ๆ เพราะอุปกรณ์ใช้พลังงานเท่าที่ต้องการเสมอ", "ถ่านที่เกินจะชาร์จไฟกลับเข้าตัวเองจนเต็ม ใช้ได้นานขึ้น", "หลอดไฟจะดับเพราะพลังงานน้อยลงเมื่อใส่ถ่านมากเกินไป", "อุปกรณ์จะเบาลงเพราะพลังงานไฟฟ้ามีน้ำหนัก")),
)


class SeriesDevice(NamedTuple):
    device: str
    reason: str


SERIES_DEVICES = (
    SeriesDevice("ไฟฉายขนาดใหญ่ที่ให้แสงสว่างจ้า", "ต้องการพลังงานไฟฟ้ามากเพื่อให้หลอดไฟสว่างจ้า จึงต่อเซลล์ไฟฟ้าหลายเซลล์แบบอนุกรม"),
    SeriesDevice("ของเล่นที่มีมอเตอร์แรงบิดสูงต้องใช้ถ่านหลายก้อน", "มอเตอร์ต้องการพลังงานไฟฟ้ามากในการหมุนแรง จึงต่อเซลล์ไฟฟ้าแบบอนุกรมเพื่อเพิ่มพลังงานรวม"),
    SeriesDevice("รีโมทควบคุมระยะไกลที่ใช้ถ่าน 2 ก้อน", "ต้องการพลังงานไฟฟ้าเพียงพอส่งสัญญาณได้ไกลและใช้งานได้นาน จึงต่อเซลล์ไฟฟ้าแบบอนุกรม"),
    SeriesDevice("เครื่องวัดอุณหภูมิดิจิทัลที่ใช้ถ่าน 2 ก้อน", "วงจรอิเล็กทรอนิกส์ภายในต้องการแรงดันไฟฟ้ารวมตามที่กำหนด จึงต่อเซลล์ไฟฟ้าแบบอนุกรมให้ได้แรงดันที่ต้องการ"),
    SeriesDevice("วิทยุพกพาที่ใช้ถ่าน 4 ก้อน", "ลำโพงและวงจรขยายเสียงต้องการแรงดันไฟฟ้ามาก จึงต่อถ่าน 4 ก้อนแบบอนุกรมให้ได้ 6 โวลต์"),
    SeriesDevice("เครื่องคิดเลขที่ใช้ถ่านกระดุม 2 ก้อน", "จอแสดงผลต้องการแรงดันไฟฟ้ามากกว่าถ่านกระดุมก้อนเดียว จึงวางซ้อนกันแบบอนุกรม"),
    SeriesDevice("ไฟจักรยานแบบ LED ที่ใช้ถ่าน 3 ก้อน", "หลอด LED สีขาวต้องการแรงดันไฟฟ้าสูงกว่าถ่านก้อนเดียว จึงต่อถ่าน 3 ก้อนแบบอนุกรม"),
    SeriesDevice("แบตเตอรี่รถยนต์ที่ประกอบด้วยเซลล์ย่อย 6 เซลล์", "มอเตอร์สตาร์ทเครื่องยนต์ต้องการแรงดันไฟฟ้าสูง จึงต่อเซลล์ย่อยแบบอนุกรมให้ได้ประมาณ 12 โวลต์"),
)


SERIES_CELLS_BENEFIT_SCENARIOS = (
    ("เหตุใดผู้ผลิตของเล่นบางชนิดจึงออกแบบให้ใช้ถ่านไฟฉาย 4 ก้อนต่อแบบอนุกรมแทนที่จะใช้เพียง 1 ก้อน",
     "ของเล่นที่มีมอเตอร์หรือไฟ LED หลายดวงต้องการพลังงานไฟฟ้ามาก การต่อถ่านหลายก้อนแบบอนุกรมจึงให้พลังงานเพียงพอ",
     ("การใช้ถ่านหลายก้อนไม่มีผลต่อพลังงานที่ของเล่นได้รับ", "ถ่าน 1 ก้อนให้พลังงานมากกว่าถ่าน 4 ก้อนต่ออนุกรมเสมอ", "ผู้ผลิตใช้ถ่านหลายก้อนเพียงเพื่อเพิ่มน้ำหนักของเล่นเท่านั้น")),
    ("นักเรียนต้องเลือกจำนวนเซลล์ไฟฟ้าที่จะต่อแบบอนุกรมให้เหมาะกับหลอดไฟที่ใช้ ข้อใดพิจารณาได้เหมาะสมที่สุด",
     "เลือกจำนวนเซลล์ไฟฟ้าให้พลังงานไฟฟ้ารวมเพียงพอกับที่หลอดไฟต้องการ ไม่มากหรือน้อยเกินไป",
     ("ต่อเซลล์ไฟฟ้าให้มากที่สุดเท่าที่จะหาได้เสมอ", "จำนวนเซลล์ไฟฟ้าไม่มีผลต่อการเลือกใช้กับหลอดไฟชนิดใด", "ใช้เซลล์ไฟฟ้าเพียงเซลล์เดียวเสมอไม่ว่าหลอดไฟจะต้องการพลังงานเท่าใด")),
    ("อุปกรณ์แพทย์พกพาบางชนิดต้องต่อเซลล์ไฟฟ้าหลายเซลล์แบบอนุกรมอย่างระมัดระวัง เหตุใดจึงต้องระวังเป็นพิเศษ",
     "ต้องต่อขั้วให้ถูกต้องและพลังงานไฟฟ้ารวมต้องพอดี เพราะพลังงานที่มากหรือน้อยเกินไปอาจทำให้อุปกรณ์ทำงานผิดพลาดหรือเสียหาย",
     ("ไม่จำเป็นต้องระวังเพราะเซลล์ไฟฟ้าต่อผิดขั้วอย่างไรก็ให้พลังงานเท่าเดิม", "ยิ่งต่อพลังงานมากเท่าใดยิ่งดีต่ออุปกรณ์แพทย์เสมอ", "การต่อขั้วเซลล์ไฟฟ้าไม่มีผลต่อการทำงานของอุปกรณ์แพทย์")),
)


@question_type(
    "phys.series_cells_benefit_foundation",
    display_name={"th": "บอกประโยชน์ของการต่อเซลล์ไฟฟ้าแบบอนุกรม"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_BENEFIT_TOPIC,
)
class SeriesCellsBenefitFoundation(QuestionType):
    """Why join cells in series, and the care it needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(BENEFIT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                         hint="อุปกรณ์ไฟฟ้าบางชนิดต้องการพลังงานมากกว่าที่เซลล์ไฟฟ้าเซลล์เดียวจะให้ได้", topic=SERIES_CELLS_BENEFIT_TOPIC)


@question_type(
    "phys.series_cells_benefit_fluency",
    display_name={"th": "บอกประโยชน์และการประยุกต์ใช้เซลล์ไฟฟ้าแบบอนุกรมในชีวิตประจำวัน"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_BENEFIT_TOPIC,
)
class SeriesCellsBenefitFluency(QuestionType):
    """A device that uses several cells in series; the reason it needs them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(SERIES_DEVICES))
        device = SERIES_DEVICES[index]
        others = [d.reason for i, d in enumerate(SERIES_DEVICES) if i != index]
        return _labelled(
            stem=f"เหตุใด{device.device}จึงมักต่อเซลล์ไฟฟ้าหลายเซลล์แบบอนุกรม",
            correct=device.reason,
            wrongs=tuple(others),
            hint="อุปกรณ์ที่ต้องการพลังงานไฟฟ้ามากขึ้นมักต้องการเซลล์ไฟฟ้าหลายเซลล์ต่อแบบอนุกรม",
            topic=SERIES_CELLS_BENEFIT_TOPIC,
        )


@question_type(
    "phys.series_cells_benefit_application",
    display_name={"th": "ประเมินการเลือกใช้เซลล์ไฟฟ้าแบบอนุกรมในอุปกรณ์จริง"},
    level=SIXTH, subject=SUBJECT, topic=SERIES_CELLS_BENEFIT_TOPIC,
)
class SeriesCellsBenefitApplication(QuestionType):
    """Authored cases, and whether a pack of cells meets a device's need."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, SERIES_CELLS_BENEFIT_SCENARIOS,
                hint="เลือกจำนวนเซลล์ไฟฟ้าให้พลังงานรวมพอดีกับความต้องการของอุปกรณ์ ไม่ใช่ยิ่งมากยิ่งดีเสมอไป",
            ), SERIES_CELLS_BENEFIT_TOPIC)
        need_cells = rng.randint(2, 6)
        need = Fraction(3, 2) * need_cells
        have = rng.choice([n for n in range(1, 9) if n != need_cells])
        device = rng.choice(("ของเล่นหุ่นยนต์", "ไฟฉายเดินป่า", "พัดลมพกพา", "วิทยุพกพา", "ไฟจักรยาน"))
        right = (f"ไม่พอ ต้องเพิ่มถ่านอีก {need_cells - have} ก้อน" if have < need_cells
                 else f"มากเกินไป ควรใช้เพียง {need_cells} ก้อนเพื่อไม่ให้อุปกรณ์เสียหาย")
        wrongs = ("พอดี ใช้ได้ทันที", f"ไม่พอ ต้องเพิ่มถ่านอีก {need_cells - have + 1} ก้อน" if have < need_cells else "ไม่พอ ต้องเพิ่มถ่านอีก 1 ก้อน",
                  f"มากเกินไป ควรใช้เพียง {max(1, need_cells - 1)} ก้อนเพื่อไม่ให้อุปกรณ์เสียหาย" if have > need_cells else "มากเกินไป ควรใช้เพียง 1 ก้อน")
        return _labelled(stem=f"{device}ต้องใช้ความต่างศักย์ {show(need)} โวลต์ นักเรียนมีถ่านไฟฉายก้อนละ 1.5 โวลต์ต่อแบบอนุกรม {have} ก้อน ถูกต้องหรือไม่",
                         correct=right, wrongs=wrongs,
                         hint="ความต่างศักย์รวม = 1.5 × จำนวนก้อน แล้วเทียบกับที่อุปกรณ์ต้องการ", topic=SERIES_CELLS_BENEFIT_TOPIC)
