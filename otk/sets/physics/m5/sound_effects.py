"""เสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้องของเสียง

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/7

Sets moved here from: science_wave_e14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import show
from otk.sets._support.science_wave_e14 import (
    SUBJECT,
    UPPER_FIVE,
    V_AIR,
    V_WATER,
    _labelled,
    _numeric,
)

PROVENANCE = Provenance("original")


TOPIC_SOUND_EFFECTS = "เสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้องของเสียง"


ECHO, BEAT, DOPPLER, SOUND_RESONANCE = ("เสียงสะท้อนกลับ", "บีต", "ปรากฏการณ์ดอปเพลอร์",
                                         "การสั่นพ้องของเสียง")


SOUND_EFFECTS = (ECHO, BEAT, DOPPLER, SOUND_RESONANCE)


EFFECT_EXAMPLES = (
    ("ตะโกนหน้าหน้าผาแล้วได้ยินเสียงตัวเองกลับมาหลังจากนั้นครู่หนึ่ง", ECHO),
    ("เรือประมงใช้เครื่องหาฝูงปลาที่ส่งเสียงลงไปแล้วจับเวลาเสียงที่กลับมา", ECHO),
    ("ค้างคาวบินหลบสิ่งกีดขวางในที่มืดได้", ECHO),
    ("เคาะส้อมเสียง 440 เฮิรตซ์ และ 444 เฮิรตซ์พร้อมกัน ได้ยินเสียงดังค่อยสลับ 4 ครั้งต่อวินาที", BEAT),
    ("นักดนตรีฟังเสียงดังค่อยเป็นจังหวะขณะตั้งสายกีตาร์เทียบกับอีกสาย", BEAT),
    ("เครื่องบินใบพัดสองเครื่องยนต์ที่หมุนเร็วไม่เท่ากันทำให้ได้ยินเสียงหึ่งดังค่อยเป็นจังหวะ", BEAT),
    ("เสียงไซเรนรถพยาบาลแหลมขึ้นเมื่อรถวิ่งเข้าหา และทุ้มลงเมื่อรถวิ่งผ่านไป", DOPPLER),
    ("เสียงรถแข่งที่วิ่งผ่านหน้าอัฒจันทร์เปลี่ยนจากแหลมเป็นทุ้มทันที", DOPPLER),
    ("เครื่องตรวจจับความเร็วรถใช้การเปลี่ยนความถี่ของคลื่นที่สะท้อนจากรถที่เคลื่อนที่", DOPPLER),
    ("เป่าลมผ่านปากขวดแล้วเกิดเสียงดังหวีด", SOUND_RESONANCE),
    ("เติมน้ำในขวดแก้วมากขึ้นแล้วเป่าปากขวด เสียงที่ได้แหลมขึ้น", SOUND_RESONANCE),
    ("ตัวกีตาร์ที่เป็นกล่องกลวงทำให้เสียงสายกีตาร์ดังขึ้น", SOUND_RESONANCE),
)


EFFECT_TRUE = (
    ("เสียงสะท้อนกลับเกิดจากเสียงสะท้อนจากสิ่งกีดขวางที่อยู่ไกลพอ จนแยกได้จากเสียงเดิม", ECHO),
    ("บีตเกิดจากเสียงสองเสียงที่มีความถี่ต่างกันเล็กน้อยมารวมกัน", BEAT),
    ("ความถี่บีตเท่ากับผลต่างของความถี่ของเสียงทั้งสอง", BEAT),
    ("เมื่อแหล่งกำเนิดเสียงเคลื่อนที่เข้าหาผู้ฟัง ผู้ฟังได้ยินเสียงความถี่สูงกว่าความถี่จริง", DOPPLER),
    ("เมื่อแหล่งกำเนิดเสียงเคลื่อนที่ออกห่างผู้ฟัง ผู้ฟังได้ยินเสียงความถี่ต่ำกว่าความถี่จริง", DOPPLER),
    ("การสั่นพ้องของเสียงเกิดเมื่อความถี่ของเสียงเท่ากับความถี่ธรรมชาติของอากาศในท่อหรือภาชนะ", SOUND_RESONANCE),
)


EFFECT_FALSE = (
    "เสียงสะท้อนกลับมีความถี่สูงกว่าเสียงเดิมเสมอ",
    "บีตเกิดจากเสียงสองเสียงที่มีความถี่เท่ากันพอดี",
    "ความถี่บีตเท่ากับผลบวกของความถี่ของเสียงทั้งสอง",
    "เมื่อแหล่งกำเนิดเสียงเคลื่อนที่เข้าหาผู้ฟัง ผู้ฟังได้ยินเสียงทุ้มลง",
    "ปรากฏการณ์ดอปเพลอร์ทำให้ความถี่ที่แหล่งกำเนิดส่งออกมาเปลี่ยนไปจริง",
    "การสั่นพ้องของเสียงทำให้เสียงค่อยลง",
)


@question_type(
    "phys.sound_effects_foundation",
    display_name={"th": "จำแนกเสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้องของเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_EFFECTS,
)
class SoundEffectsFoundation(QuestionType):
    """Name the effect from what is heard."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        example, effect = rng.choice(EFFECT_EXAMPLES)
        if rng.random() < 0.5:
            others = [e for e, x in EFFECT_EXAMPLES if x != effect]
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของ{effect}",
                correct=example, wrongs=tuple(others),
                topic=TOPIC_SOUND_EFFECTS,
                hint="เสียงย้อนกลับมาคือเสียงสะท้อนกลับ ดังค่อยเป็นจังหวะคือบีต แหลม-ทุ้มตามการเคลื่อนที่คือดอปเพลอร์ ดังขึ้นเพราะความถี่ตรงกันคือการสั่นพ้อง")
        return _labelled(
            stem=f"\"{example}\" เป็นปรากฏการณ์ใดของเสียง",
            correct=effect, wrongs=tuple(e for e in SOUND_EFFECTS if e != effect),
            topic=TOPIC_SOUND_EFFECTS,
            hint="เสียงย้อนกลับมาคือเสียงสะท้อนกลับ ดังค่อยเป็นจังหวะคือบีต แหลม-ทุ้มตามการเคลื่อนที่คือดอปเพลอร์ ดังขึ้นเพราะความถี่ตรงกันคือการสั่นพ้อง")


@question_type(
    "phys.sound_effects_fluency",
    display_name={"th": "อธิบายการเกิดเสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้องของเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_EFFECTS,
)
class SoundEffectsFluency(QuestionType):
    """The indicator across all four effects: why each happens."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            moving = rng.choice(("รถพยาบาล", "รถไฟ", "รถตำรวจ", "รถดับเพลิง"))
            towards = rng.random() < 0.5
            correct = ("ได้ยินเสียงแหลมกว่าความถี่จริง" if towards else "ได้ยินเสียงทุ้มกว่าความถี่จริง")
            return _labelled(
                stem=(f"{moving}เปิดเสียงสัญญาณความถี่คงตัวและกำลัง"
                      f"{'เคลื่อนที่เข้าหา' if towards else 'เคลื่อนที่ออกห่างจาก'}ผู้ฟังที่ยืนนิ่ง ผู้ฟังจะได้ยินเสียงอย่างไร"),
                correct=correct,
                wrongs=(("ได้ยินเสียงทุ้มกว่าความถี่จริง" if towards else "ได้ยินเสียงแหลมกว่าความถี่จริง"),
                        "ได้ยินเสียงความถี่เท่ากับความถี่จริงเสมอ",
                        "ได้ยินเสียงดังค่อยเป็นจังหวะ"),
                topic=TOPIC_SOUND_EFFECTS,
                hint="แหล่งกำเนิดเข้าหาผู้ฟัง หน้าคลื่นอัดชิดกัน ความถี่ที่ได้ยินสูงขึ้น ออกห่างจะต่ำลง")
        statement, _ = rng.choice(EFFECT_TRUE)
        return _labelled(
            stem="ข้อใดอธิบายปรากฏการณ์ของเสียงได้ถูกต้อง",
            correct=statement, wrongs=tuple(EFFECT_FALSE),
            topic=TOPIC_SOUND_EFFECTS,
            hint="บีตคือผลต่างของความถี่ ดอปเพลอร์คือความถี่ที่ได้ยินเปลี่ยนเพราะการเคลื่อนที่ ส่วนความถี่ที่ปล่อยออกมาไม่เปลี่ยน")


@question_type(
    "phys.sound_effects_application",
    display_name={"th": "คำนวณระยะจากเสียงสะท้อนกลับ ความถี่บีต และการสั่นพ้องในท่อ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_EFFECTS,
)
class SoundEffectsApplication(QuestionType):
    """Echo ranging in air and water, beat frequency both ways, and a closed tube."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            in_water = rng.random() < 0.4
            v = V_WATER if in_water else V_AIR
            t = rng.choice((Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(4)))
            d = v * t / 2
            stem = (f"เรือส่งคลื่นเสียงลงไปในน้ำ (อัตราเร็วเสียงในน้ำ 1,500 m/s) ได้รับเสียงสะท้อนจากพื้นทะเล"
                    f"หลังส่ง {show(t)} วินาที ทะเลบริเวณนั้นลึกเท่าใด" if in_water else
                    f"ตะโกนหน้าหน้าผา (อัตราเร็วเสียง 340 m/s) ได้ยินเสียงสะท้อนกลับหลังตะโกน {show(t)} วินาที "
                    "หน้าผาอยู่ห่างเท่าใด")
            return _numeric(stem=stem, answer=d, wrongs=[v * t, v / t, d / 2], unit="เมตร",
                            topic=TOPIC_SOUND_EFFECTS,
                            hint="เสียงเดินทางไปและกลับ ระยะห่าง = อัตราเร็ว × เวลา ÷ 2")
        if shape == 1:
            f1 = rng.choice((256, 320, 384, 440, 512))
            df = rng.randint(1, 8)
            f2 = f1 + df * rng.choice((1, -1))
            return _numeric(
                stem=f"เคาะส้อมเสียงความถี่ {f1} เฮิรตซ์ และ {f2} เฮิรตซ์พร้อมกัน จะได้ยินบีตกี่ครั้งต่อวินาที",
                answer=df, wrongs=[f1 + f2, Fraction(f1 + f2, 2), df * 2], unit="ครั้งต่อวินาที",
                topic=TOPIC_SOUND_EFFECTS, hint="ความถี่บีต = ผลต่างของความถี่ของเสียงทั้งสอง")
        if shape == 2:
            f1 = rng.choice((256, 320, 384, 440, 512))
            df = rng.randint(2, 6)
            return _labelled(
                stem=(f"เคาะส้อมเสียงความถี่ {f1} เฮิรตซ์พร้อมกับดีดสายกีตาร์ ได้ยินบีต {df} ครั้งต่อวินาที "
                      "เมื่อขันสายให้ตึงขึ้นเล็กน้อย บีตค่อย ๆ ลดลง ความถี่เดิมของสายกีตาร์เป็นเท่าใด"),
                correct=f"{f1 - df} เฮิรตซ์",
                wrongs=(f"{f1 + df} เฮิรตซ์", f"{f1} เฮิรตซ์", f"{df} เฮิรตซ์"),
                topic=TOPIC_SOUND_EFFECTS,
                hint="ขันสายให้ตึงขึ้นทำให้ความถี่สูงขึ้น ถ้าบีตลดลงแปลว่าความถี่เข้าใกล้ส้อมเสียง สายเดิมจึงต่ำกว่าส้อมเสียง")
        f = rng.choice((170, 340, 425, 850))
        length = Fraction(V_AIR, 4 * f)
        return _numeric(
            stem=(f"ท่อปลายปิดด้านหนึ่งเกิดการสั่นพ้องครั้งแรก (เสียงดังที่สุดครั้งแรก) กับเสียงความถี่ {f} เฮิรตซ์ "
                  "ถ้าอัตราเร็วเสียง 340 m/s ลำอากาศในท่อยาวเท่าใด"),
            answer=length * 100, wrongs=[Fraction(V_AIR, f) * 100, Fraction(V_AIR, 2 * f) * 100, length * 1000],
            unit="เซนติเมตร", topic=TOPIC_SOUND_EFFECTS,
            hint="ท่อปลายปิดสั่นพ้องครั้งแรกเมื่อความยาวลำอากาศเท่ากับหนึ่งในสี่ของความยาวคลื่น (L = λ/4 และ λ = v/f)")
