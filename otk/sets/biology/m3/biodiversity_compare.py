"""ความหลากหลายในระดับชนิดของระบบนิเวศ

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/9

Sets moved here from: science_wave_b28.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b28 import BIODIVERSITY_TOPIC, COMPARE_SCENARIOS

PROVENANCE = Provenance("original")


DIVERSITY_FACTS = (
    Fact("ความหลากหลายทางชีวภาพในระดับชนิดหมายถึงอะไร",
         "จำนวนชนิดของสิ่งมีชีวิตที่พบในบริเวณหนึ่ง "
         "ร่วมกับความสม่ำเสมอของจำนวนสมาชิกในแต่ละชนิด"),
    Fact("การนับเฉพาะจำนวนชนิดเพียงอย่างเดียวมีข้อจำกัดอย่างไร",
         "ไม่ได้บอกว่าแต่ละชนิดมีจำนวนมากน้อยเพียงใด บริเวณที่มีชนิดหนึ่งมากจน"
         "ท่วมท้นและชนิดอื่นเหลือน้อยมาก จึงอาจนับได้หลายชนิดแต่ไม่สมดุล"),
    Fact("เหตุใดระบบนิเวศในเขตร้อนชื้นจึงมีความหลากหลายสูงกว่าเขตหนาว",
         "เพราะมีแสง อุณหภูมิ และน้ำเพียงพอตลอดปี "
         "สิ่งมีชีวิตจึงเจริญเติบโตและแบ่งพื้นที่หากินได้หลากหลายรูปแบบกว่า"),
    Fact("โครงสร้างที่ซับซ้อนของถิ่นอาศัยมีผลต่อความหลากหลายอย่างไร",
         "ยิ่งมีชั้นและซอกหลืบมาก ยิ่งมีที่อยู่และแหล่งอาหารย่อย ๆ หลายแบบ "
         "สิ่งมีชีวิตหลายชนิดจึงอยู่ร่วมกันได้โดยไม่แย่งกันจนสูญพันธุ์"),
    Fact("เหตุใดพื้นที่เกษตรที่ปลูกพืชชนิดเดียวจึงมีความหลากหลายต่ำ",
         "เพราะพืชที่ปลูกถูกคัดให้เหลือชนิดเดียว และวัชพืชกับแมลงชนิดอื่น"
         "ถูกกำจัดออกไป โครงสร้างของถิ่นอาศัยจึงเรียบและซ้ำกันทั้งแปลง"),
    Fact("การสำรวจความหลากหลายในระดับชนิดควรทำอย่างไรจึงจะเปรียบเทียบกันได้",
         "ต้องสำรวจด้วยวิธีเดียวกัน ขนาดพื้นที่เท่ากัน และช่วงเวลาใกล้เคียงกัน "
         "จึงจะนำผลของสองบริเวณมาเทียบกันได้"),
)


DIVERSITY_FACTS += (
    Fact('ความหลากหลายทางพันธุกรรมหมายถึงอะไร',
         'ความแตกต่างของยีนระหว่างสิ่งมีชีวิตชนิดเดียวกัน ทำให้แต่ละตัวมีลักษณะต่างกัน'),
    Fact('ความหลากหลายของระบบนิเวศหมายถึงอะไร',
         'การมีระบบนิเวศหลายแบบอยู่ในพื้นที่หนึ่ง เช่น ป่า ทุ่งหญ้า และแหล่งน้ำ'),
    Fact('การนำชนิดพันธุ์ต่างถิ่นเข้ามาในพื้นที่มีผลต่อความหลากหลายอย่างไร',
         'อาจแย่งอาหารและที่อยู่จนชนิดพื้นเมืองลดลง ความหลากหลายจึงลดลง'),
    Fact('การสูญเสียถิ่นที่อยู่มีผลต่อความหลากหลายอย่างไร',
         'สิ่งมีชีวิตที่ต้องอาศัยถิ่นนั้นไม่มีที่อยู่และแหล่งอาหาร จำนวนชนิดในพื้นที่จึงลดลง'),
)


class Ecosystem(NamedTuple):
    """An ecosystem, why its diversity ranks where it does, and that rank."""
    name: str
    because: str
    rank: int


ECOSYSTEMS = (
    Ecosystem("ป่าดิบชื้น",
              "มีแสง น้ำ และอุณหภูมิเหมาะสมตลอดปี และมีเรือนยอดหลายชั้น "
              "จึงมีที่อยู่และแหล่งอาหารย่อย ๆ จำนวนมาก", 6),
    Ecosystem("แนวปะการัง",
              "โครงสร้างของปะการังสร้างซอกหลืบจำนวนมากให้สัตว์น้ำหลายชนิด"
              "อยู่อาศัยและหลบภัยได้พร้อมกัน", 5),
    Ecosystem("ป่าชายเลน",
              "เป็นรอยต่อระหว่างน้ำจืดกับน้ำเค็ม จึงมีทั้งชนิดที่ทนเค็มและ"
              "ชนิดที่อาศัยรากค้ำจุนเป็นที่อนุบาลตัวอ่อน", 4),
    Ecosystem("ทุ่งหญ้า",
              "มีพืชล้มลุกเป็นหลักและโครงสร้างเป็นชั้นเดียว "
              "ชนิดของสิ่งมีชีวิตจึงน้อยกว่าป่าที่มีหลายชั้น", 3),
    Ecosystem("นาข้าวที่ปลูกพันธุ์เดียวทั้งแปลง",
              "พืชถูกคัดให้เหลือชนิดเดียวและสิ่งมีชีวิตอื่นถูกกำจัดออกไป "
              "โครงสร้างของถิ่นอาศัยจึงซ้ำกันทั้งแปลง", 2),
    Ecosystem("ทะเลทราย",
              "น้ำเป็นปัจจัยจำกัดอย่างรุนแรงและอุณหภูมิเปลี่ยนแปลงมาก "
              "จึงมีเฉพาะชนิดที่ทนสภาพเช่นนี้ได้", 1),
)


@question_type(
    "ecology.biodiversity_compare_foundation",
    display_name={"th": "ความหลากหลายทางชีวภาพในระดับชนิด"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCompareFoundation(QuestionType):
    """What species diversity is, before two places are compared."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, DIVERSITY_FACTS, topic=BIODIVERSITY_TOPIC,
            hint="ความหลากหลายในระดับชนิดดูสองอย่าง คือมีกี่ชนิด "
                 "และแต่ละชนิดมีจำนวนสม่ำเสมอกันเพียงใด",
        )


@question_type(
    "ecology.biodiversity_compare_fluency",
    display_name={"th": "เปรียบเทียบความหลากหลายระหว่างระบบนิเวศ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCompareFluency(QuestionType):
    """Compare two ecosystems — the ``เปรียบเทียบ`` the indicator asks for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        first, second = rng.sample(ECOSYSTEMS, 2)
        higher, lower = ((first, second) if first.rank > second.rank
                         else (second, first))
        return _labelled(
            stem=f"เมื่อสำรวจด้วยวิธีเดียวกันและพื้นที่เท่ากัน ระหว่าง"
                 f"“{first.name}” กับ “{second.name}” "
                 f"ข้อใดเปรียบเทียบความหลากหลายในระดับชนิดได้ถูกต้อง",
            correct=f"{higher.name}มีความหลากหลายในระดับชนิดสูงกว่า "
                    f"เพราะ{higher.because}",
            wrongs=(f"{lower.name}มีความหลากหลายในระดับชนิดสูงกว่า "
                    f"เพราะ{lower.because}",
                    f"{higher.name}มีความหลากหลายในระดับชนิดสูงกว่า "
                    f"เพราะมีพื้นที่กว้างกว่า",
                    "ทั้งสองระบบนิเวศมีความหลากหลายในระดับชนิดเท่ากัน "
                    "เพราะต่างก็เป็นระบบนิเวศตามธรรมชาติเหมือนกัน"),
            hint="ดูว่าถิ่นอาศัยมีชั้นและซอกหลืบมากเพียงใด "
                 "และมีปัจจัยใดจำกัดการอยู่รอดอย่างรุนแรงหรือไม่",
            topic=BIODIVERSITY_TOPIC,
        )


@question_type(
    "ecology.biodiversity_compare_application",
    display_name={"th": "วิเคราะห์การเปรียบเทียบความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityCompareApplication(QuestionType):
    """Judge a comparison, or the survey that produced the numbers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, COMPARE_SCENARIOS,
            hint="ตรวจว่าสองบริเวณถูกสำรวจด้วยวิธีเดียวกันหรือไม่ "
                 "และอย่าลืมดูความสม่ำเสมอของจำนวนในแต่ละชนิด",
        ), BIODIVERSITY_TOPIC)
