"""ชนิด ส่วนประกอบ และการซ้อนทับของคลื่น

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/3

Sets moved here from: science_wave_f7.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f7 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_WAVE = "ชนิด ส่วนประกอบ และการซ้อนทับของคลื่น"


WAVE_FACTS = (
    ("คลื่นที่อนุภาคของตัวกลางสั่นในแนวตั้งฉากกับทิศการเคลื่อนที่ของคลื่นเรียกว่าอะไร", "คลื่นตามขวาง",
     ("คลื่นตามยาว", "คลื่นนิ่ง", "คลื่นกระแทก")),
    ("คลื่นที่อนุภาคของตัวกลางสั่นในแนวเดียวกับทิศการเคลื่อนที่ของคลื่นเรียกว่าอะไร", "คลื่นตามยาว",
     ("คลื่นตามขวาง", "คลื่นแม่เหล็กไฟฟ้า", "คลื่นผิวน้ำ")),
    ("คลื่นกลต่างจากคลื่นแม่เหล็กไฟฟ้าอย่างไร", "คลื่นกลต้องอาศัยตัวกลางในการเคลื่อนที่",
     ("คลื่นกลเคลื่อนที่ในสุญญากาศได้", "คลื่นกลเร็วกว่าเสมอ", "คลื่นกลไม่มีความถี่")),
    ("หลักของฮอยเกนส์กล่าวว่าอย่างไร",
     "ทุกจุดบนหน้าคลื่นเป็นแหล่งกำเนิดคลื่นวงกลมย่อย และแนวสัมผัสของคลื่นย่อยคือหน้าคลื่นใหม่",
     ("คลื่นเคลื่อนที่เป็นเส้นตรงเสมอ", "หน้าคลื่นขนานกับทิศการเคลื่อนที่ของคลื่นเสมอ",
      "คลื่นสองขบวนรวมกันแล้วหายไปเสมอ")),
    ("หลักการซ้อนทับของคลื่นกล่าวว่าอย่างไร", "การกระจัดลัพธ์เท่ากับผลรวมของการกระจัดของคลื่นแต่ละขบวน",
     ("คลื่นที่พบกันจะสะท้อนกลับทั้งหมด", "คลื่นที่มีแอมพลิจูดมากกว่าจะทำลายคลื่นที่เล็กกว่า",
      "คลื่นทั้งสองรวมกันเป็นคลื่นเดียวตลอดไป")),
    ("ความยาวคลื่นคือระยะใด", "ระยะระหว่างสันคลื่นสองสันที่อยู่ถัดกัน",
     ("ระยะจากสันคลื่นถึงท้องคลื่นที่อยู่ถัดกัน", "ความสูงจากท้องคลื่นถึงสันคลื่น", "ระยะที่คลื่นเคลื่อนที่ในหนึ่งวินาที")),
)


@question_type(
    "phys.wave_superposition_foundation",
    display_name={"th": "ชนิดและส่วนประกอบของคลื่น หลักของฮอยเกนส์ และการซ้อนทับ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVE,
)
class WaveSuperpositionFoundation(QuestionType):
    """Kinds and parts of a wave, read off a description."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            stem, correct, wrongs = rng.choice(WAVE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_WAVE,
                             hint="ดูทิศการสั่นของอนุภาคเทียบกับทิศการเคลื่อนที่ของคลื่น")
        if shape == 1:
            crests = rng.randint(3, 8)
            wl = Fraction(rng.randint(1, 20) * 5, 100)
            span = wl * (crests - 1)
            return numeric(
                stem=f"ขบวนคลื่นมีสันคลื่น {crests} สันเรียงกัน สันแรกถึงสันสุดท้ายห่างกัน {show(span)} m ความยาวคลื่นเท่าใด",
                answer=wl, wrongs=[span / crests, span, span / (crests + 1)], unit="m", topic=TOPIC_WAVE,
                hint="สันคลื่น n สันมีช่วงห่างระหว่างกัน n − 1 ช่วง แต่ละช่วงยาวหนึ่งความยาวคลื่น")
        height = rng.randint(2, 40) * 2
        return numeric(
            stem=f"คลื่นในเส้นเชือกมีระยะในแนวดิ่งจากท้องคลื่นถึงสันคลื่น {height} cm แอมพลิจูดของคลื่นเท่าใด",
            answer=Fraction(height, 2), wrongs=[height, height * 2, Fraction(height, 4)], unit="cm", topic=TOPIC_WAVE,
            hint="แอมพลิจูดวัดจากแนวสมดุลถึงสันคลื่น เท่ากับครึ่งหนึ่งของระยะจากท้องถึงสัน")


@question_type(
    "phys.wave_superposition_fluency",
    display_name={"th": "คำนวณอัตราเร็ว ความถี่ ความยาวคลื่น และคาบของคลื่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVE,
)
class WaveSuperpositionFluency(QuestionType):
    """v = fλ each way round, and T = 1/f."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f = rng.choice((2, 4, 5, 8, 10, 20, 25, 40, 50))
        wl = Fraction(rng.randint(1, 40), rng.choice((10, 100)))
        v = f * wl
        what = rng.choice(("คลื่นในเส้นเชือก", "คลื่นผิวน้ำ", "คลื่นในสปริง"))
        shape = rng.randrange(4)
        hint = "v = fλ และ T = 1/f"
        if shape == 0:
            return numeric(stem=f"{what}มีความถี่ {f} Hz ความยาวคลื่น {show(wl)} m มีอัตราเร็วเท่าใด",
                           answer=v, wrongs=[Fraction(f) / wl, wl / f, v * 2], unit="m/s", topic=TOPIC_WAVE, hint=hint)
        if shape == 1:
            return numeric(stem=f"{what}เคลื่อนที่ด้วยอัตราเร็ว {show(v)} m/s ความถี่ {f} Hz มีความยาวคลื่นเท่าใด",
                           answer=wl, wrongs=[v * f, Fraction(f) / v, wl * 2], unit="m", topic=TOPIC_WAVE, hint=hint)
        if shape == 2:
            return numeric(stem=f"{what}เคลื่อนที่ด้วยอัตราเร็ว {show(v)} m/s ความยาวคลื่น {show(wl)} m มีความถี่เท่าใด",
                           answer=f, wrongs=[v * wl, wl / v, f * 2], unit="Hz", topic=TOPIC_WAVE, hint=hint)
        f = rng.choice((2, 4, 5, 10, 20, 25, 50))
        return numeric(stem=f"{what}มีความถี่ {f} Hz มีคาบเท่าใด", answer=Fraction(1, f),
                       wrongs=[f, Fraction(2, f), Fraction(1, 2 * f)], unit="s", topic=TOPIC_WAVE, hint=hint)


@question_type(
    "phys.wave_superposition_application",
    display_name={"th": "การรวมกันของคลื่นตามหลักการซ้อนทับและเฟสของคลื่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVE,
)
class WaveSuperpositionApplication(QuestionType):
    """Two pulses meeting, and whether two points move in or out of step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            a, b = rng.sample(range(1, 16), 2)
            same = rng.random() < 0.5
            return numeric(
                stem=(f"คลื่นดลสองลูกในเส้นเชือกเดียวกันมีแอมพลิจูด {a} cm และ {b} cm "
                      f"{'อยู่ด้านเดียวกันของเชือก' if same else 'อยู่คนละด้านของเชือก'} "
                      "ขณะซ้อนทับกันพอดี การกระจัดลัพธ์มีขนาดเท่าใด"),
                answer=a + b if same else abs(a - b), wrongs=[abs(a - b) if same else a + b, max(a, b), a * b],
                unit="cm", topic=TOPIC_WAVE,
                hint="การกระจัดลัพธ์คือผลรวมของการกระจัดแต่ละลูก ด้านเดียวกันเสริมกัน คนละด้านหักล้างกัน")
        wl = rng.randint(2, 20) * 10
        half = rng.randint(1, 6)
        gap = Fraction(wl * half, 2)
        in_step = half % 2 == 0
        return _labelled(
            stem=f"คลื่นมีความยาวคลื่น {wl} cm จุดสองจุดบนแนวการเคลื่อนที่ของคลื่นห่างกัน {show(gap)} cm สองจุดนี้มีเฟสอย่างไร",
            correct="เฟสตรงกัน" if in_step else "เฟสตรงข้ามกัน",
            wrongs=("เฟสตรงข้ามกัน" if in_step else "เฟสตรงกัน", "เฟสต่างกัน 90 องศา", "เฟสต่างกัน 45 องศา"),
            topic=TOPIC_WAVE,
            hint="จุดที่ห่างกันเป็นจำนวนเต็มเท่าของ λ มีเฟสตรงกัน ห่างกันเป็นจำนวนคี่เท่าของ λ/2 มีเฟสตรงข้าม")
