"""การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นของคลื่นเสียง

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/5

Sets moved here from: science_wave_e14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import (
    BEHAVIOURS,
    DIFFRACT,
    REFLECT,
    REFRACT,
    SUPERPOSE,
    show,
)
from otk.sets._support.science_wave_e14 import (
    SUBJECT,
    UPPER_FIVE,
    V_AIR,
    V_WATER,
    _labelled,
    _numeric,
)

PROVENANCE = Provenance("original")


TOPIC_SOUND_WAVES = "การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นของคลื่นเสียง"


SOUND_EXAMPLES = (
    ("ตะโกนในหุบเขาแล้วได้ยินเสียงตัวเองย้อนกลับมา", REFLECT),
    ("เรือใช้โซนาร์ส่งเสียงลงไปแล้วรับเสียงที่กลับมาจากพื้นทะเล", REFLECT),
    ("ค้างคาวส่งเสียงความถี่สูงแล้วฟังเสียงที่กลับมาเพื่อหาตำแหน่งแมลง", REFLECT),
    ("ห้องประชุมบุผนังด้วยวัสดุนุ่มเพื่อลดเสียงก้อง", REFLECT),
    ("เวลากลางคืนได้ยินเสียงจากที่ไกล ๆ ชัดกว่าเวลากลางวัน เพราะอากาศใกล้พื้นเย็นกว่าอากาศด้านบน", REFRACT),
    ("เสียงเดินทางจากอากาศลงไปในน้ำแล้วอัตราเร็วเปลี่ยนไป", REFRACT),
    ("เสียงฟ้าร้องที่อยู่ไกลเบนขึ้นด้านบนในวันที่อากาศใกล้พื้นร้อนจัด", REFRACT),
    ("ได้ยินเสียงคนคุยกันในห้องข้าง ๆ ผ่านประตูที่เปิดแง้มไว้ แม้มองไม่เห็นตัว", DIFFRACT),
    ("ได้ยินเสียงรถที่อยู่หลังตึกโดยไม่เห็นรถ", DIFFRACT),
    ("ได้ยินเสียงดนตรีจากงานเลี้ยงที่อยู่อีกฟากของกำแพงสูง", DIFFRACT),
    ("เดินผ่านหน้าลำโพงสองตัวที่เล่นเสียงเดียวกัน แล้วได้ยินเสียงดังและค่อยสลับกัน", SUPERPOSE),
    ("หูฟังตัดเสียงรบกวนสร้างเสียงที่มีเฟสตรงข้ามกับเสียงรบกวน", SUPERPOSE),
    ("ส้อมเสียงสองอันความถี่ต่างกันเล็กน้อย เคาะพร้อมกันแล้วได้ยินเสียงดังค่อยเป็นจังหวะ", SUPERPOSE),
)


SOUND_TRUE = (
    ("เสียงสะท้อนได้ดีจากผิวแข็งและเรียบ และถูกดูดกลืนมากโดยผิวนุ่มหรือพรุน", REFLECT),
    ("เสียงสะท้อนที่แยกได้ต้องมาถึงหูช้ากว่าเสียงเดิมอย่างน้อยประมาณ 0.1 วินาที", REFLECT),
    ("เสียงเคลื่อนที่ในอากาศร้อนเร็วกว่าอากาศเย็น จึงหักเหเมื่อผ่านอากาศต่างอุณหภูมิ", REFRACT),
    ("เมื่อเสียงหักเห ความถี่ไม่เปลี่ยน แต่อัตราเร็วและความยาวคลื่นเปลี่ยน", REFRACT),
    ("เสียงเลี้ยวเบนผ่านประตูได้ดี เพราะความยาวคลื่นใกล้เคียงความกว้างประตู", DIFFRACT),
    ("เสียงความถี่ต่ำเลี้ยวเบนอ้อมสิ่งกีดขวางได้ดีกว่าเสียงความถี่สูง", DIFFRACT),
    ("เสียงจากสองแหล่งที่มาเสริมกันทำให้ดังขึ้น และที่มาหักล้างกันทำให้ค่อยลง", SUPERPOSE),
)


SOUND_FALSE = (
    "เสียงสะท้อนได้ดีที่สุดจากผ้าม่านหนาและพรมนุ่มในห้อง",
    "เสียงเคลื่อนที่ในอากาศเย็นได้เร็วกว่าในอากาศร้อน",
    "เมื่อเสียงเข้าสู่ตัวกลางใหม่ ความถี่ของเสียงเปลี่ยนไปด้วยตามอุณหภูมิ",
    "เสียงความถี่สูงเลี้ยวเบนได้ดีกว่าเสียงความถี่ต่ำ",
    "เสียงเลี้ยวเบนไม่ได้ เราจึงได้ยินเฉพาะเสียงที่มองเห็นแหล่งกำเนิด",
    "เสียงจากสองแหล่งรวมกันแล้วมีความถี่เท่ากับผลบวกของความถี่ทั้งสอง",
    "เสียงเดินทางในสุญญากาศได้เร็วที่สุดเพราะไม่มีอากาศขวาง",
)


@question_type(
    "phys.sound_wave_behaviour_foundation",
    display_name={"th": "พฤติกรรมของคลื่นเสียงในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_WAVES,
)
class SoundWaveBehaviourFoundation(QuestionType):
    """Name the behaviour behind an everyday sound."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        example, behaviour = rng.choice(SOUND_EXAMPLES)
        if rng.random() < 0.5:
            others = [e for e, b in SOUND_EXAMPLES if b != behaviour]
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของ{behaviour}ของคลื่นเสียง",
                correct=example, wrongs=tuple(others),
                topic=TOPIC_SOUND_WAVES,
                hint="เสียงกลับมาหาผู้ฟังคือสะท้อน เปลี่ยนอัตราเร็วเพราะตัวกลางคือหักเห อ้อมสิ่งกีดขวางคือเลี้ยวเบน สองเสียงซ้อนกันคือการรวมคลื่น")
        return _labelled(
            stem=f"\"{example}\" เป็นผลของพฤติกรรมใดของคลื่นเสียง",
            correct=behaviour, wrongs=tuple(b for b in BEHAVIOURS if b != behaviour),
            topic=TOPIC_SOUND_WAVES,
            hint="เสียงกลับมาหาผู้ฟังคือสะท้อน เปลี่ยนอัตราเร็วเพราะตัวกลางคือหักเห อ้อมสิ่งกีดขวางคือเลี้ยวเบน สองเสียงซ้อนกันคือการรวมคลื่น")


@question_type(
    "phys.sound_wave_behaviour_fluency",
    display_name={"th": "อธิบายการสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นของเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_WAVES,
)
class SoundWaveBehaviourFluency(QuestionType):
    """The indicator across all four behaviours, as one true account among wrong ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        statement, _ = rng.choice(SOUND_TRUE)
        return _labelled(
            stem="ข้อใดอธิบายพฤติกรรมของคลื่นเสียงได้ถูกต้อง",
            correct=statement, wrongs=tuple(SOUND_FALSE),
            topic=TOPIC_SOUND_WAVES,
            hint="เสียงเป็นคลื่นกล จึงสะท้อน หักเห เลี้ยวเบน และรวมกันได้เหมือนคลื่นอื่น ความถี่ขึ้นกับแหล่งกำเนิดเท่านั้น")


@question_type(
    "phys.sound_wave_behaviour_application",
    display_name={"th": "คำนวณความยาวคลื่นเสียงในตัวกลางต่าง ๆ และจุดดังค่อยจากลำโพงสองตัว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_WAVES,
)
class SoundWaveBehaviourApplication(QuestionType):
    """v = fλ across a boundary, and loud or quiet from a path difference."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            # Frequencies that divide 1,500, so the wavelength in water is exact.
            f = rng.choice((150, 250, 300, 500, 750, 1000, 1500))
            return _numeric(
                stem=(f"เสียงความถี่ {f:,} เฮิรตซ์ เคลื่อนที่จากอากาศ (อัตราเร็ว 340 m/s) ลงไปในน้ำ "
                      "(อัตราเร็ว 1,500 m/s) ความยาวคลื่นเสียงในน้ำเท่าใด"),
                answer=Fraction(V_WATER, f),
                wrongs=[Fraction(V_AIR, f), Fraction(f * V_AIR, V_WATER), Fraction(V_WATER - V_AIR, f)],
                unit="เมตร", topic=TOPIC_SOUND_WAVES,
                hint="ความถี่ไม่เปลี่ยนเมื่อหักเห ความยาวคลื่นในตัวกลางใหม่ = อัตราเร็วในตัวกลางใหม่ ÷ ความถี่")
        if shape == 1:
            temp = rng.choice((0, 10, 15, 20, 25, 30, 35, 40))
            v = Fraction(331) + Fraction(6, 10) * temp
            return _numeric(
                stem=(f"อัตราเร็วเสียงในอากาศประมาณ v = 331 + 0.6T เมตรต่อวินาที เมื่อ T เป็นอุณหภูมิ"
                      f"องศาเซลเซียส ที่อุณหภูมิ {temp} องศาเซลเซียส เสียงมีอัตราเร็วเท่าใด"),
                answer=v, wrongs=[331 + 6 * temp, 331 - Fraction(6, 10) * temp, Fraction(331)],
                unit="m/s", topic=TOPIC_SOUND_WAVES,
                hint="แทนค่าอุณหภูมิในสูตร อากาศยิ่งร้อน เสียงยิ่งเดินทางเร็ว")
        wavelength = rng.choice((Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3, 2)))
        halves = rng.randint(0, 6)
        diff = wavelength * halves / 2
        loud = halves % 2 == 0
        return _labelled(
            stem=(f"ลำโพงสองตัวเล่นเสียงเดียวกันพร้อมกัน ความยาวคลื่น {show(wavelength)} เมตร "
                  f"ผู้ฟังยืนอยู่ห่างจากลำโพงทั้งสองต่างกัน {show(diff)} เมตร ผู้ฟังจะได้ยินเสียงอย่างไร"),
            correct=("ดังมาก เพราะคลื่นเสียงมาเสริมกัน" if loud else "ค่อยมาก เพราะคลื่นเสียงมาหักล้างกัน"),
            wrongs=(("ค่อยมาก เพราะคลื่นเสียงมาหักล้างกัน" if loud else "ดังมาก เพราะคลื่นเสียงมาเสริมกัน"),
                    "ดังเท่ากับได้ยินจากลำโพงตัวเดียวเสมอ",
                    "ไม่ได้ยินเสียงเลย เพราะเสียงสะท้อนกลับไปที่ลำโพง"),
            topic=TOPIC_SOUND_WAVES,
            hint="ระยะต่างเป็นจำนวนเต็มเท่าของความยาวคลื่นจะเสริมกัน เป็นครึ่งหนึ่ง หนึ่งเท่าครึ่ง ... จะหักล้างกัน")
