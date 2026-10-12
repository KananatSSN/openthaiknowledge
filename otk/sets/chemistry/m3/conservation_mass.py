"""กฎทรงมวล

เคมี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.3/4

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
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d10 import SECONDARY_THREE

PROVENANCE = Provenance("original")


MASS_TOPIC = "กฎทรงมวล"


class Trial(NamedTuple):
    what: str
    gas: bool


TRIALS = (
    Trial("ผงฟูกับน้ำส้มสายชู ซึ่งเกิดแก๊สคาร์บอนไดออกไซด์", True),
    Trial("ชิ้นแมกนีเซียมกับกรดไฮโดรคลอริก ซึ่งเกิดแก๊สไฮโดรเจน", True),
    Trial("สารละลายเลด(II)ไนเตรตกับสารละลายโพแทสเซียมไอโอไดด์ ซึ่งเกิดตะกอนสีเหลือง", False),
    Trial("สารละลายคอปเปอร์(II)ซัลเฟตกับสารละลายโซเดียมไฮดรอกไซด์ ซึ่งเกิดตะกอนสีฟ้า", False),
)


def _mass(value: float) -> str:
    return f"{value:.1f}"


MASS_SCENARIOS = (
    ("เผาลวดเหล็กฝอยในอากาศบนเครื่องชั่ง พบว่ามวลเพิ่มขึ้น ข้อใดอธิบายได้สอดคล้องกับกฎทรงมวล",
     "เหล็กรวมตัวกับออกซิเจนจากอากาศ มวลของออกซิเจนที่เข้ามารวมทำให้มวลที่ชั่งได้เพิ่มขึ้น",
     ("ความร้อนมีมวลจึงทำให้เหล็กหนักขึ้น",
      "กฎทรงมวลใช้ไม่ได้เมื่อมีการเผา",
      "อะตอมเหล็กเพิ่มจำนวนขึ้นเมื่อร้อน",
      "เหล็กดูดความชื้นจากเปลวไฟจนหนักขึ้น",
      "เครื่องชั่งอ่านค่าผิดเพราะความร้อน มวลจริงไม่เปลี่ยน")),
    ("สารตั้งต้นมีมวลรวม 24 กรัม เกิดปฏิกิริยาในระบบปิดได้ผลิตภัณฑ์ 2 ชนิด ชนิดแรกมีมวล 15 กรัม ผลิตภัณฑ์ชนิดที่สองมีมวลเท่าใด",
     "9 กรัม", ("15 กรัม", "24 กรัม", "39 กรัม", "6 กรัม", "12 กรัม")),
    ("นักเรียนต้องการแสดงกฎทรงมวลด้วยปฏิกิริยาผงฟูกับน้ำส้มสายชู ควรออกแบบการทดลองอย่างไร",
     "ทำปฏิกิริยาในขวดที่ครอบลูกโป่งไว้ที่ปากขวด เพื่อเก็บแก๊สไว้ในระบบ แล้วชั่งมวลก่อนและหลัง",
     ("ทำในบีกเกอร์เปิดเพื่อให้แก๊สออกได้สะดวก",
      "ชั่งเฉพาะผงฟูก่อนและหลังเกิดปฏิกิริยา",
      "ไม่ต้องชั่งมวล ให้สังเกตฟองแก๊สแทน",
      "ชั่งมวลหลังเกิดปฏิกิริยาเพียงครั้งเดียว",
      "เปิดฝาขวดระหว่างเกิดปฏิกิริยาเพื่อให้ความดันลดลง")),
    ("ในขวดปิดสนิทมีสารละลายสองชนิดรวมมวล 150.0 กรัม เมื่อผสมกันเกิดตะกอนขึ้น มวลรวมหลังเกิดปฏิกิริยาเป็นเท่าใด",
     "150.0 กรัม เพราะไม่มีสารใดเข้าหรือออกจากขวด",
     ("มากกว่า 150.0 กรัม เพราะตะกอนเป็นของแข็งที่หนักกว่า",
      "น้อยกว่า 150.0 กรัม เพราะสารละลายบางส่วนกลายเป็นตะกอน",
      "เป็นศูนย์ เพราะสารเดิมหมดไป",
      "มากกว่า 150.0 กรัม เพราะเกิดสารใหม่ขึ้น",
      "น้อยกว่า 150.0 กรัม เพราะอะตอมบางส่วนถูกทำลาย")),
)


def missing_product(rng: Random) -> GeneratedQuestion:
    """Two reactants that react completely in a closed vessel; the second product's mass."""
    a, b = rng.randint(8, 40), rng.randint(5, 30)
    c = rng.randint(3, a + b - 2)
    answer = a + b - c
    pool = [a + b + c, a + b, c, abs(a - b), answer + c, abs(answer - c), 2 * answer, answer + 1]
    wrongs = tuple(dict.fromkeys(f"{w} กรัม" for w in pool if w != answer and w > 0))
    return _labelled(
        stem=(f"สาร A {a} กรัม ทำปฏิกิริยาพอดีกับสาร B {b} กรัม ในระบบปิด ได้ผลิตภัณฑ์ C {c} กรัม "
              "และผลิตภัณฑ์ D อีกชนิดหนึ่ง ผลิตภัณฑ์ D มีมวลกี่กรัม"),
        correct=f"{answer} กรัม",
        wrongs=wrongs,
        hint="มวลรวมของสารตั้งต้นเท่ากับมวลรวมของผลิตภัณฑ์",
        topic=MASS_TOPIC,
    )


@question_type(
    "chem.conservation_mass_foundation",
    display_name={"th": "บอกความหมายของกฎทรงมวล"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MASS_TOPIC,
)
class ConservationMassFoundation(QuestionType):
    """What the law of conservation of mass says, why it holds, and what a closed system is."""

    LAW = "มวลรวมของสารก่อนเกิดปฏิกิริยาเท่ากับมวลรวมของสารหลังเกิดปฏิกิริยา"
    LAW_WRONGS = ("มวลรวมของสารหลังเกิดปฏิกิริยามากกว่าก่อนเกิดปฏิกิริยาเสมอ",
                  "มวลรวมของสารหลังเกิดปฏิกิริยาน้อยกว่าก่อนเกิดปฏิกิริยาเสมอ",
                  "มวลของสารแต่ละชนิดไม่เปลี่ยนแปลงระหว่างเกิดปฏิกิริยา",
                  "มวลรวมของสารหลังเกิดปฏิกิริยาเท่ากับมวลของผลิตภัณฑ์ชนิดที่มากที่สุด",
                  "มวลรวมของสารเปลี่ยนไปตามอุณหภูมิของปฏิกิริยา")
    FACTS = (
        ("ข้อใดเป็นความหมายของกฎทรงมวล", LAW, LAW_WRONGS),
        ("ในระบบปิด มวลรวมของสารก่อนและหลังเกิดปฏิกิริยาเคมีเป็นอย่างไร", LAW, LAW_WRONGS),
        ("เหตุใดมวลรวมของสารจึงคงเดิมเมื่อเกิดปฏิกิริยาเคมีในระบบปิด",
         "อะตอมของสารตั้งต้นไม่หายไปและไม่เกิดขึ้นใหม่ เพียงจัดเรียงตัวใหม่เป็นผลิตภัณฑ์",
         ("อะตอมบางส่วนถูกทำลาย แต่มีอะตอมใหม่เกิดขึ้นแทนพอดี",
          "ปฏิกิริยาเคมีไม่ทำให้เกิดสารใหม่",
          "ผลิตภัณฑ์มีจำนวนอะตอมมากกว่าสารตั้งต้นเสมอ",
          "ความร้อนจากปฏิกิริยาชดเชยมวลที่หายไป",
          "สารทุกชนิดมีมวลเท่ากัน")),
        ("ระบบปิดในการทดลองเรื่องกฎทรงมวลหมายถึงข้อใด",
         "ระบบที่สารเข้าหรือออกจากภาชนะไม่ได้ เช่น ขวดที่ปิดฝาสนิท",
         ("ภาชนะที่ไม่มีฝาปิด เพื่อให้แก๊สออกได้",
          "ระบบที่ไม่มีสารใดทำปฏิกิริยากัน",
          "ภาชนะที่ใส่สารได้เพียงชนิดเดียว",
          "ระบบที่อุณหภูมิไม่เปลี่ยนแปลงเลย",
          "ห้องทดลองที่ปิดประตูหน้าต่างไว้")),
        ("ถ้าทำปฏิกิริยาที่เกิดแก๊สในภาชนะเปิด มวลที่ชั่งได้หลังเกิดปฏิกิริยาจะเป็นอย่างไร",
         "ลดลง เพราะแก๊สที่เกิดขึ้นหนีออกไปจากภาชนะ",
         ("เพิ่มขึ้น เพราะแก๊สมีมวลเพิ่มเข้ามา",
          "เท่าเดิมเสมอ ไม่ว่าแก๊สจะหนีออกไปหรือไม่",
          "ลดลง เพราะอะตอมบางส่วนถูกทำลาย",
          "เพิ่มขึ้น เพราะภาชนะร้อนขึ้น",
          "ลดลงเป็นศูนย์ เพราะสารทั้งหมดกลายเป็นแก๊ส")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(self.FACTS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="อะตอมไม่หายไปและไม่เกิดขึ้นใหม่ เพียงจัดเรียงตัวใหม่",
            topic=MASS_TOPIC,
        )


@question_type(
    "chem.conservation_mass_fluency",
    display_name={"th": "อธิบายกฎทรงมวลจากผลการชั่งมวลก่อนและหลังเกิดปฏิกิริยา"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MASS_TOPIC,
)
class ConservationMassFluency(QuestionType):
    """Masses before and after, closed or open; explain the reading by the law."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trial = rng.choice(TRIALS)
        closed = not trial.gas or rng.random() < 0.5
        before = round(rng.randint(1200, 1800) / 10, 1)
        lost = 0.0 if closed else round(rng.randint(5, 25) / 10, 1)
        after = round(before - lost, 1)
        vessel = "ขวดที่ปิดฝาสนิท" if closed else "บีกเกอร์ที่ไม่ปิดฝา"
        same = f"มวลเท่าเดิม ({_mass(before)} กรัม) เพราะขวดปิดกักสารทั้งหมดไว้"
        down = (f"มวลลดลง {_mass(lost)} กรัม เพราะแก๊สหนีจากภาชนะเปิด "
                "แต่มวลรวมเมื่อรวมแก๊สยังคงเดิม")
        return _labelled(
            stem=(f"นักเรียนทำปฏิกิริยาระหว่าง{trial.what} ใน{vessel} ชั่งมวลทั้งหมดก่อนเกิดปฏิกิริยาได้ {_mass(before)} กรัม "
                  f"และหลังเกิดปฏิกิริยาได้ {_mass(after)} กรัม จากหลักฐานนี้ ข้อใดอธิบายได้ถูกต้อง"),
            correct=same if closed else down,
            wrongs=((f"มวลลดลง {_mass(lost)} กรัม เพราะอะตอมบางส่วนถูกทำลายระหว่างปฏิกิริยา" if not closed
                     else f"มวลเท่าเดิม ({_mass(before)} กรัม) เพราะไม่ได้เกิดปฏิกิริยาเคมี"),
                    (f"มวลลดลง {_mass(lost)} กรัม แสดงว่ากฎทรงมวลใช้ไม่ได้กับปฏิกิริยานี้" if not closed
                     else f"มวลเท่าเดิม ({_mass(before)} กรัม) เพราะกฎทรงมวลใช้ไม่ได้กับปฏิกิริยานี้"),
                    (f"มวลลดลง {_mass(lost)} กรัม เพราะผลิตภัณฑ์เบากว่าสารตั้งต้นเสมอ" if not closed
                     else f"มวลเท่าเดิม ({_mass(before)} กรัม) เพราะตะกอนที่เกิดขึ้นไม่มีมวล")),
            hint="ดูว่าภาชนะปิดหรือเปิด และมีสารใดหนีออกไปได้หรือไม่",
            topic=MASS_TOPIC,
        )


@question_type(
    "chem.conservation_mass_application",
    display_name={"th": "ใช้กฎทรงมวลคำนวณและออกแบบการทดลอง"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MASS_TOPIC,
)
class ConservationMassApplication(QuestionType):
    """Burning steel wool, a missing product mass, and a balloon-capped flask."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return missing_product(rng)
        return _retopic(scenario_question(
            rng, MASS_SCENARIOS,
            hint="นับมวลของสารทุกชนิดที่เข้าและออกจากระบบ รวมทั้งแก๊ส",
        ), MASS_TOPIC)
