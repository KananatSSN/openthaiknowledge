"""ความสำคัญของความหลากหลายทางชีวภาพ

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/10

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
from otk.sets._support.science_wave_b28 import BIODIVERSITY_TOPIC, VALUE_SCENARIOS

PROVENANCE = Provenance("original")


class Value(NamedTuple):
    """One thing biodiversity does, and which of the two it does it for."""
    statement: str
    beneficiary: str


VALUES = (
    Value("เมื่อผู้ล่าชนิดหนึ่งลดลง ผู้ล่าชนิดอื่นยังควบคุมจำนวนเหยื่อไว้ได้ "
          "ประชากรในระบบนิเวศจึงไม่แกว่งจนเสียสมดุล", "ระบบนิเวศ"),
    Value("ผู้ย่อยสลายหลายชนิดช่วยกันย่อยซากที่ต่างกัน "
          "ธาตุอาหารจึงหมุนเวียนกลับสู่ดินได้อย่างต่อเนื่อง", "ระบบนิเวศ"),
    Value("สายใยอาหารที่มีหลายเส้นทางทำให้ระบบนิเวศทนต่อการสูญเสีย"
          "สิ่งมีชีวิตชนิดใดชนิดหนึ่งได้ดีกว่าโซ่อาหารเส้นเดียว", "ระบบนิเวศ"),
    Value("พืชและจุลินทรีย์หลายชนิดเป็นแหล่งของสารออกฤทธิ์ที่นำมาพัฒนาเป็นยา "
          "การสูญพันธุ์จึงเท่ากับสูญเสียโอกาสในการค้นพบยาใหม่", "มนุษย์"),
    Value("ความหลากหลายของพันธุ์พืชที่ปลูกทำให้เมื่อโรคระบาดทำลายพันธุ์หนึ่ง "
          "ยังมีพันธุ์อื่นให้ปลูกทดแทน ความมั่นคงทางอาหารจึงสูงขึ้น", "มนุษย์"),
    Value("แมลงผสมเรณูหลายชนิดช่วยให้พืชอาหารของมนุษย์ติดผล "
          "ผลผลิตทางการเกษตรจึงขึ้นกับความหลากหลายของแมลงเหล่านั้น", "มนุษย์"),
)


VALUE_FACTS = (
    Fact("เหตุใดระบบนิเวศที่มีความหลากหลายสูงจึงรักษาสมดุลไว้ได้ดีกว่า",
         "เพราะมีหลายชนิดที่ทำหน้าที่ทดแทนกันได้ เมื่อชนิดหนึ่งลดลง "
         "หน้าที่นั้นยังมีผู้อื่นทำต่อ ระบบจึงไม่ล้มทั้งระบบ"),
    Fact("ความหลากหลายทางชีวภาพเกี่ยวข้องกับการหมุนเวียนสารอย่างไร",
         "ผู้ย่อยสลายหลายชนิดย่อยซากที่ต่างกันคนละแบบ "
         "ธาตุอาหารจึงกลับคืนสู่ดินและน้ำได้อย่างต่อเนื่อง"),
    Fact("บริการจากระบบนิเวศที่มนุษย์ได้รับมีอะไรบ้าง",
         "อาหาร ยา ไม้และเส้นใย รวมทั้งการผสมเรณู การควบคุมน้ำท่วม "
         "และการรักษาคุณภาพน้ำและดิน"),
    Fact("เหตุใดการสูญพันธุ์ของสิ่งมีชีวิตชนิดหนึ่งจึงกระทบชนิดอื่นด้วย",
         "เพราะสิ่งมีชีวิตในระบบนิเวศเชื่อมโยงกันผ่านสายใยอาหารและการพึ่งพา "
         "การหายไปของชนิดหนึ่งจึงตัดความสัมพันธ์เหล่านั้นลง"),
    Fact("ความหลากหลายทางพันธุกรรมภายในชนิดเดียวกันสำคัญอย่างไร",
         "ทำให้ประชากรมีโอกาสมีสมาชิกที่ทนต่อโรคหรือสภาพแวดล้อมใหม่ "
         "ประชากรจึงไม่สูญสิ้นไปพร้อมกันเมื่อเกิดการเปลี่ยนแปลง"),
    Fact("เหตุใดการปลูกพืชชนิดเดียวเป็นบริเวณกว้างจึงเสี่ยงต่อความมั่นคงทางอาหาร",
         "เพราะถ้าเกิดโรคที่พันธุ์นั้นอ่อนแอ ผลผลิตจะเสียหายพร้อมกันทั้งพื้นที่ "
         "โดยไม่มีพันธุ์อื่นเหลือไว้ทดแทน"),
)


class Loss(NamedTuple):
    """A loss of diversity, and the consequence that follows from it."""
    event: str
    consequence: str


LOSSES = (
    Loss("แมลงผสมเรณูในพื้นที่เกษตรลดจำนวนลงอย่างมาก",
         "พืชอาหารหลายชนิดติดผลน้อยลง ผลผลิตและรายได้ของเกษตรกรจึงลดลงตามไปด้วย"),
    Loss("ผู้ล่าสูงสุดในระบบนิเวศหนึ่งถูกล่าจนหมดไป",
         "ประชากรของเหยื่อเพิ่มขึ้นอย่างรวดเร็วจนกินพืชหมด "
         "ระบบนิเวศจึงเสียสมดุลไปทั้งระบบ"),
    Loss("เกษตรกรทั้งประเทศเปลี่ยนไปปลูกข้าวพันธุ์เดียวกันทั้งหมด",
         "เมื่อเกิดโรคระบาดที่พันธุ์นั้นอ่อนแอ ผลผลิตจะเสียหายพร้อมกันทั้งประเทศ "
         "เพราะไม่มีพันธุ์อื่นทดแทน"),
    Loss("ป่าต้นน้ำถูกเปลี่ยนเป็นพื้นที่เกษตรชนิดเดียว",
         "รากไม้ที่เคยยึดดินและชะลอน้ำหายไป จึงเกิดดินถล่มและน้ำหลากง่ายขึ้น "
         "กระทบทั้งระบบนิเวศและชุมชนท้ายน้ำ"),
    Loss("จุลินทรีย์ผู้ย่อยสลายในดินลดความหลากหลายลงจากการใช้สารเคมี",
         "ซากพืชซากสัตว์ย่อยสลายช้าลง ธาตุอาหารจึงหมุนเวียนกลับสู่ดินได้น้อยลง "
         "และดินเสื่อมโทรมในระยะยาว"),
    Loss("พืชสมุนไพรพื้นถิ่นบางชนิดสูญพันธุ์ไปก่อนที่จะมีใครศึกษา",
         "สารออกฤทธิ์ที่อาจนำไปพัฒนาเป็นยาได้สูญหายไปพร้อมกับพืชนั้นอย่างถาวร"),
)


LOSSES += (
    Loss('ป่าชายเลนตามชายฝั่งถูกถางเพื่อทำนากุ้ง',
          'สัตว์น้ำวัยอ่อนขาดแหล่งอนุบาล และชายฝั่งขาดแนวกันคลื่น จึงถูกกัดเซาะได้ง่ายขึ้น'),
    Loss('ปะการังในแนวปะการังตายจากการฟอกขาวเป็นบริเวณกว้าง',
          'สัตว์ทะเลจำนวนมากเสียที่อยู่และแหล่งอาหาร การประมงและการท่องเที่ยวของชุมชนชายฝั่งจึงได้รับผลกระทบ'),
    Loss('ผักป่าและเห็ดป่าหลายชนิดที่ชุมชนเคยเก็บกินหายไปจากป่าใกล้หมู่บ้าน',
          'ชุมชนขาดแหล่งอาหารและรายได้จากของป่า และภูมิปัญญาการใช้ประโยชน์จากพืชเหล่านั้นก็ค่อย ๆ หายไป'),
)


@question_type(
    "ecology.biodiversity_value_foundation",
    display_name={"th": "ความสำคัญของความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityValueFoundation(QuestionType):
    """Say what diversity does, for the ecosystem and for people alike."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _fact_question(
                rng, VALUE_FACTS, topic=BIODIVERSITY_TOPIC,
                hint="แยกให้ออกว่าผลตกอยู่กับระบบนิเวศเอง หรือตกอยู่กับมนุษย์",
            )
        item = rng.choice(VALUES)
        # Distractors must belong to the *other* beneficiary. A statement about
        # the same one would be true as well, and the item would have two
        # defensible answers.
        others = [other.statement for other in VALUES
                  if other.beneficiary != item.beneficiary]
        rng.shuffle(others)
        return _labelled(
            stem=f"ข้อใดแสดงความสำคัญของความหลากหลายทางชีวภาพต่อ"
                 f"“{item.beneficiary}” ได้ถูกต้อง",
            correct=item.statement, wrongs=tuple(others[:3]),
            hint="อ่านให้จบว่าผลที่เกิดขึ้นตกอยู่กับระบบนิเวศเอง "
                 "หรือตกอยู่กับมนุษย์",
            topic=BIODIVERSITY_TOPIC,
        )


@question_type(
    "ecology.biodiversity_value_fluency",
    display_name={"th": "ผลของการสูญเสียความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityValueFluency(QuestionType):
    """Follow a loss of diversity through to what it costs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(LOSSES)
        others = [other.consequence for other in LOSSES
                  if other.consequence != item.consequence]
        rng.shuffle(others)
        return _labelled(
            stem=f"ถ้า{item.event} จะเกิดผลอย่างไร",
            correct=item.consequence, wrongs=tuple(others[:3]),
            hint="ตามผลไปทีละขั้นจากสิ่งมีชีวิตที่หายไป "
                 "ว่าใครเคยพึ่งพาสิ่งนั้นอยู่บ้าง",
            topic=BIODIVERSITY_TOPIC,
        )


@question_type(
    "ecology.biodiversity_value_application",
    display_name={"th": "วิเคราะห์ความสำคัญของความหลากหลายทางชีวภาพ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=BIODIVERSITY_TOPIC,
)
class BiodiversityValueApplication(QuestionType):
    """Trace a real loss through the ecosystem and back to people."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, VALUE_SCENARIOS,
            hint="ถามว่าสิ่งมีชีวิตที่หายไปเคยทำหน้าที่ใด "
                 "แล้วใครหรือสิ่งใดเคยพึ่งพาหน้าที่นั้นอยู่",
        ), BIODIVERSITY_TOPIC)
