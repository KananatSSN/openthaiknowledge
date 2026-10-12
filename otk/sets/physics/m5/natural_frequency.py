"""ความถี่ธรรมชาติและการสั่นพ้อง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/2

Sets moved here from: science_wave_f7.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f7 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_NATURAL = "ความถี่ธรรมชาติและการสั่นพ้อง"


NATURAL_FACTS = (
    ("ความถี่ธรรมชาติของวัตถุคือความถี่ใด", "ความถี่ที่วัตถุสั่นเองเมื่อถูกทำให้สั่นแล้วปล่อย ขึ้นกับสมบัติของวัตถุ",
     ("ความถี่ของแรงที่มากระทำเสมอ", "ความถี่สูงสุดที่วัตถุสั่นได้", "ความถี่ที่เท่ากันสำหรับวัตถุทุกชนิด")),
    ("การสั่นพ้องเกิดขึ้นเมื่อใด", "เมื่อความถี่ของแรงกระตุ้นเท่ากับความถี่ธรรมชาติของวัตถุ",
     ("เมื่อแรงกระตุ้นมีขนาดมากที่สุด", "เมื่อความถี่ของแรงกระตุ้นเป็นศูนย์", "เมื่อวัตถุมีมวลมากที่สุด")),
    ("ขณะเกิดการสั่นพ้อง วัตถุสั่นอย่างไร", "แอมพลิจูดของการสั่นมากที่สุด",
     ("ความถี่ของการสั่นเป็นศูนย์", "แอมพลิจูดของการสั่นน้อยที่สุด", "วัตถุหยุดสั่นทันที")),
    ("ทหารเดินแถวข้ามสะพานมักถูกสั่งให้เลิกเดินพร้อมเท้า เพราะเหตุใด",
     "ป้องกันไม่ให้จังหวะก้าวตรงกับความถี่ธรรมชาติของสะพานจนเกิดการสั่นพ้อง",
     ("ลดน้ำหนักรวมที่กดสะพาน", "ทำให้เดินข้ามสะพานได้เร็วขึ้น", "ลดแรงเสียดทานระหว่างรองเท้ากับสะพาน")),
    ("การปรับหาสถานีวิทยุอาศัยหลักการใด", "ปรับความถี่ธรรมชาติของวงจรให้เท่ากับความถี่ของสถานีจนเกิดการสั่นพ้อง",
     ("เพิ่มกำลังของเครื่องส่งที่สถานี", "ลดความถี่ของคลื่นวิทยุที่เข้ามา", "เพิ่มความยาวสายอากาศเท่านั้น")),
)


RESONANCE_CASES = (
    ("นักร้องเปล่งเสียงสูงค้างไว้จนแก้วไวน์แตก เกิดจากสาเหตุใด",
     "ความถี่ของเสียงตรงกับความถี่ธรรมชาติของแก้วจนเกิดการสั่นพ้อง"),
    ("วิศวกรติดตั้งตัวหน่วงการสั่นในอาคารสูง มีจุดประสงค์ใด",
     "ลดแอมพลิจูดเมื่อแรงลมหรือแผ่นดินไหวมีความถี่ใกล้ความถี่ธรรมชาติของอาคาร"),
    ("เด็กโยกตัวบนชิงช้าตามจังหวะการแกว่ง ทำให้เกิดผลใด",
     "ชิงช้าแกว่งกว้างขึ้นเพราะแรงกระตุ้นมีความถี่เท่ากับความถี่ธรรมชาติ"),
    ("กระจกหน้าต่างสั่นเสียงดังเฉพาะเมื่อรถบรรทุกเร่งเครื่องถึงช่วงหนึ่ง เกิดจากสาเหตุใด",
     "ความถี่การสั่นของเครื่องยนต์ช่วงนั้นตรงกับความถี่ธรรมชาติของกระจก"),
)


@question_type(
    "phys.natural_frequency_foundation",
    display_name={"th": "ความถี่ธรรมชาติและเงื่อนไขการเกิดการสั่นพ้อง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NATURAL,
)
class NaturalFrequencyFoundation(QuestionType):
    """What natural frequency is, and when resonance happens."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(NATURAL_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_NATURAL,
                             hint="การสั่นพ้องเกิดเมื่อความถี่ของแรงกระตุ้นเท่ากับความถี่ธรรมชาติ แอมพลิจูดจะมากที่สุด")
        n = rng.randint(3, 40)
        t = rng.choice([x for x in (2, 4, 5, 8, 10, 20, 25) if _exact(Fraction(n, x))])
        f = Fraction(n, t)
        drives = [d for d in dict.fromkeys((f * 2, f / 2, f + 1, f * 4)) if d != f and _exact(d)]
        return _labelled(
            stem=(f"ดึงชิงช้าแล้วปล่อย ชิงช้าแกว่งเองครบ {n} รอบในเวลา {t} s ถ้าต้องการผลักชิงช้าให้แกว่งกว้างขึ้นเรื่อย ๆ "
                  "ควรผลักด้วยความถี่เท่าใด"),
            correct=f"{show(f)} Hz", wrongs=tuple(f"{show(d)} Hz" for d in drives)[:3],
            topic=TOPIC_NATURAL, hint="หาความถี่ธรรมชาติ = จำนวนรอบ ÷ เวลา แล้วผลักด้วยความถี่เดียวกันจึงเกิดการสั่นพ้อง")


@question_type(
    "phys.natural_frequency_fluency",
    display_name={"th": "หาความถี่ธรรมชาติจากคาบและลูกตุ้มที่สั่นพ้องกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NATURAL,
)
class NaturalFrequencyFluency(QuestionType):
    """Barton's pendulums: the one of the driver's length swings widest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            lengths = rng.sample(range(20, 101, 10), 4)
            driver = rng.choice(lengths)
            names = ("ก", "ข", "ค", "ง")
            listed = " ".join(f"{n} ยาว {ell} cm" for n, ell in zip(names, lengths))
            right = names[lengths.index(driver)]
            return _labelled(
                stem=(f"แขวนลูกตุ้มสี่ลูกไว้กับเชือกเส้นเดียวกัน: {listed} แล้วแกว่งลูกตุ้มตัวขับที่ยาว {driver} cm "
                      "ลูกตุ้มใดแกว่งด้วยแอมพลิจูดมากที่สุด"),
                correct=f"ลูกตุ้ม {right}", wrongs=tuple(f"ลูกตุ้ม {n}" for n in names if n != right),
                topic=TOPIC_NATURAL,
                hint="ลูกตุ้มที่ยาวเท่ากับตัวขับมีความถี่ธรรมชาติเท่ากับความถี่ของตัวขับ จึงเกิดการสั่นพ้อง")
        period = rng.choice((Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5),
                             Fraction(1, 4), Fraction(1, 2), Fraction(2), Fraction(4, 5)))
        what = rng.choice(("แก้วไวน์", "ส้อมเสียง", "แผ่นเหล็กบาง", "สะพานแขวน", "ชิงช้า"))
        return numeric(
            stem=f"{what}สั่นเองด้วยคาบ {show(period)} s ต้องกระตุ้นด้วยความถี่เท่าใดจึงเกิดการสั่นพ้อง",
            answer=1 / period, wrongs=[period, 2 / period, 1 / (2 * period)], unit="Hz", topic=TOPIC_NATURAL,
            hint="ความถี่ธรรมชาติ f = 1/T การสั่นพ้องเกิดเมื่อกระตุ้นด้วยความถี่นี้")


@question_type(
    "phys.natural_frequency_application",
    display_name={"th": "การสั่นพ้องในเครื่องยนต์ อาคาร และชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NATURAL,
)
class NaturalFrequencyApplication(QuestionType):
    """Engine speed against a part's natural frequency, and resonance used or avoided."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            f = rng.randint(5, 80)
            what = rng.choice(("กระจกมองข้างของรถ", "ฝาครอบเครื่องยนต์", "ที่วางแขนในรถ", "แผงหน้าปัด"))
            if rng.random() < 0.5:
                return numeric(
                    stem=f"{what}มีความถี่ธรรมชาติ {f} Hz เครื่องยนต์ต้องหมุนด้วยอัตรากี่รอบต่อนาที {what}จึงสั่นแรงที่สุด",
                    answer=f * 60, wrongs=[f, f * 30, f * 120], unit="รอบต่อนาที", topic=TOPIC_NATURAL,
                    hint="เครื่องยนต์ที่หมุน n รอบต่อนาทีสั่นด้วยความถี่ n/60 Hz การสั่นพ้องเกิดเมื่อเท่ากับความถี่ธรรมชาติ")
            rpm = f * 60
            return numeric(
                stem=f"เครื่องยนต์หมุนด้วยอัตรา {rpm:,} รอบต่อนาที ทำให้{what}สั่นแรงที่สุด ความถี่ธรรมชาติของ{what}เท่าใด",
                answer=f, wrongs=[rpm, f * 2, Fraction(rpm, 100)], unit="Hz", topic=TOPIC_NATURAL,
                hint="แปลงรอบต่อนาทีเป็นรอบต่อวินาที (หารด้วย 60) ได้ความถี่ของแรงกระตุ้น ซึ่งเท่ากับความถี่ธรรมชาติ")
        pick = rng.randrange(len(RESONANCE_CASES))
        stem, right = RESONANCE_CASES[pick]
        return _labelled(
            stem=stem, correct=right,
            wrongs=("แรงกระตุ้นมีขนาดมาก จึงสั่นแรงโดยไม่เกี่ยวกับความถี่",
                    "ความถี่ธรรมชาติของวัตถุเพิ่มขึ้นเป็นสองเท่า",
                    "วัตถุดูดกลืนพลังงานทั้งหมดจนหยุดสั่น"),
            topic=TOPIC_NATURAL, hint="การสั่นพ้องทำให้แอมพลิจูดมากที่สุด บางกรณีเป็นประโยชน์ บางกรณีต้องป้องกัน")
