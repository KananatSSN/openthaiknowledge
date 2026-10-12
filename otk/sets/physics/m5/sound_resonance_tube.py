"""การสั่นพ้องของอากาศในท่อ บีต คลื่นนิ่ง ปรากฏการณ์ดอปเพลอร์ และคลื่นกระแทก

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/7

Sets moved here from: science_wave_f8.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f8 import SUBJECT, UPPER_FIVE, _exact, speed_at

PROVENANCE = Provenance("original")


TOPIC_PIPE = "การสั่นพ้องของอากาศในท่อ บีต คลื่นนิ่ง ปรากฏการณ์ดอปเพลอร์ และคลื่นกระแทก"


PIPE_FACTS = (
    ("บีตของเสียงเกิดขึ้นเมื่อใด", "เมื่อเสียงสองเสียงที่มีความถี่ต่างกันเล็กน้อยมารวมกัน",
     ("เมื่อเสียงสะท้อนจากผนังห้อง", "เมื่อแหล่งกำเนิดเคลื่อนที่เร็วกว่าเสียง", "เมื่อเสียงผ่านช่องแคบ")),
    ("ปรากฏการณ์ดอปเพลอร์ของเสียงคือข้อใด", "ผู้ฟังได้ยินความถี่เปลี่ยนไปเมื่อแหล่งกำเนิดกับผู้ฟังเคลื่อนที่สัมพัทธ์กัน",
     ("เสียงดังขึ้นเมื่อความเข้มเพิ่มขึ้น", "เสียงเลี้ยวเบนผ่านสิ่งกีดขวาง", "เสียงสะท้อนกลับจากหน้าผา")),
    ("รถพยาบาลเปิดไซเรนวิ่งเข้าหาผู้ฟังที่ยืนนิ่ง ผู้ฟังได้ยินเสียงอย่างไร", "ความถี่สูงกว่าความถี่จริงของไซเรน",
     ("ความถี่ต่ำกว่าความถี่จริงของไซเรน", "ความถี่เท่ากับความถี่จริงของไซเรน", "ไม่ได้ยินเสียงเลย")),
    ("คลื่นกระแทกของเสียง (ซอนิกบูม) เกิดขึ้นเมื่อใด", "เมื่อแหล่งกำเนิดเสียงเคลื่อนที่เร็วกว่าเสียง",
     ("เมื่อแหล่งกำเนิดหยุดนิ่ง", "เมื่อเสียงสองเสียงความถี่ใกล้กันมารวมกัน", "เมื่อเสียงผ่านน้ำ")),
    ("คลื่นนิ่งในเส้นเชือก บัพที่อยู่ติดกันห่างกันเท่าใด", "ครึ่งหนึ่งของความยาวคลื่น",
     ("หนึ่งความยาวคลื่น", "หนึ่งในสี่ของความยาวคลื่น", "สองเท่าของความยาวคลื่น")),
    ("ในท่อปลายปิดด้านหนึ่งที่เกิดการสั่นพ้อง ที่ปลายปิดเป็นตำแหน่งใดของการกระจัดของอนุภาคอากาศ", "บัพ (การกระจัดเป็นศูนย์)",
     ("ปฏิบัพ (การกระจัดมากที่สุด)", "ครึ่งทางระหว่างบัพกับปฏิบัพ", "เปลี่ยนตามความถี่")),
)


@question_type(
    "phys.sound_resonance_tube_foundation",
    display_name={"th": "บีต คลื่นนิ่ง ปรากฏการณ์ดอปเพลอร์ และคลื่นกระแทก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PIPE,
)
class SoundResonanceTubeFoundation(QuestionType):
    """What each effect is, and the beat frequency of two notes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(PIPE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_PIPE,
                             hint="บีตเกิดจากความถี่ใกล้กัน ดอปเพลอร์เกิดจากการเคลื่อนที่สัมพัทธ์ คลื่นกระแทกเกิดเมื่อเร็วกว่าเสียง")
        f1 = rng.randint(200, 520)
        f2 = f1 + rng.choice((-6, -5, -4, -3, -2, 2, 3, 4, 5, 6))
        what = rng.choice(("ส้อมเสียงสองอัน", "สายกีตาร์สองสาย", "ขลุ่ยสองเลา"))
        return numeric(
            stem=f"{what}ให้เสียงความถี่ {f1} Hz และ {f2} Hz พร้อมกัน ได้ยินบีตกี่ครั้งต่อวินาที",
            answer=abs(f1 - f2), wrongs=[f1 + f2, Fraction(f1 + f2, 2), abs(f1 - f2) * 2], unit="ครั้งต่อวินาที",
            topic=TOPIC_PIPE, hint="ความถี่บีต = ผลต่างของความถี่ทั้งสอง")


@question_type(
    "phys.sound_resonance_tube_fluency",
    display_name={"th": "การสั่นพ้องของอากาศในท่อปลายปิดด้านหนึ่งและคลื่นนิ่ง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PIPE,
)
class SoundResonanceTubeFluency(QuestionType):
    """L = (2n − 1)λ/4 in a closed pipe, and node spacing on a string."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            wl = Fraction(rng.randint(4, 40) * 4, 100)
            l1 = wl / 4
            l2 = 3 * wl / 4
            f = rng.choice([x for x in (256, 320, 400, 425, 500, 512, 850, 1000) if _exact(x * wl)])
            return numeric(
                stem=(f"ใช้ส้อมเสียงความถี่ {f} Hz ทำให้อากาศในท่อปลายปิดด้านหนึ่งสั่นพ้อง ได้ยินเสียงดังครั้งแรกและครั้งที่สอง"
                      f"เมื่อลำอากาศยาว {show(l1 * 100)} cm และ {show(l2 * 100)} cm อัตราเร็วเสียงเท่าใด"),
                answer=f * wl, wrongs=[f * (l2 - l1), f * l1 * 2, f * l2], unit="m/s", topic=TOPIC_PIPE,
                hint="ความยาวที่สั่นพ้องสองครั้งติดกันต่างกัน λ/2 ดังนั้น λ = 2(L₂ − L₁) แล้ว v = fλ")
        if shape == 1:
            t_c = rng.choice((0, 15, 20, 25, 30))
            v = speed_at(t_c)
            f = rng.choice([x for x in (100, 125, 200, 250, 400, 500, 1000) if _exact(v / x / 4 * 100)])
            n = rng.randint(1, 3)
            length = (2 * n - 1) * v / f / 4
            order = {1: "ครั้งแรก", 2: "ครั้งที่สอง", 3: "ครั้งที่สาม"}[n]
            return numeric(
                stem=(f"เสียงความถี่ {f} Hz ทำให้อากาศในท่อปลายปิดด้านหนึ่งสั่นพ้อง{order} ขณะอากาศมีอุณหภูมิ {t_c} °C "
                      "ลำอากาศยาวเท่าใด (v = 331 + 0.6T)"),
                answer=length * 100, wrongs=[n * v / f / 2 * 100, v / f * 100, n * v / f / 4 * 100], unit="cm",
                topic=TOPIC_PIPE, hint="ท่อปลายปิดด้านหนึ่งสั่นพ้องเมื่อ L = λ/4, 3λ/4, 5λ/4, … โดย λ = v/f")
        wl = Fraction(rng.randint(1, 20) * 10, 100)
        nodes = rng.randint(3, 7)
        span = wl / 2 * (nodes - 1)
        f = rng.choice([x for x in (10, 20, 25, 40, 50, 100) if _exact(x * wl)])
        return numeric(
            stem=(f"เกิดคลื่นนิ่งความถี่ {f} Hz ในเส้นเชือก มีบัพ {nodes} บัพ บัพแรกถึงบัพสุดท้ายห่างกัน {show(span)} m "
                  "อัตราเร็วของคลื่นในเชือกเท่าใด"),
            answer=f * wl, wrongs=[f * wl / 2, f * span, f * span / nodes], unit="m/s", topic=TOPIC_PIPE,
            hint="บัพที่อยู่ติดกันห่างกัน λ/2 หา λ ก่อน แล้ว v = fλ")


@question_type(
    "phys.sound_resonance_tube_application",
    display_name={"th": "คำนวณปรากฏการณ์ดอปเพลอร์และคลื่นกระแทกของเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PIPE,
)
class SoundResonanceTubeApplication(QuestionType):
    """f' = fv/(v ∓ vₛ) for a moving source, and the Mach number of a jet."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.7:
            v = 340
            toward = rng.random() < 0.5
            vs, f = rng.choice([(s, f) for s in (10, 20, 40, 60, 68, 85) for f in range(300, 1001, 10)
                                if _exact(Fraction(f * v, v - s if toward else v + s))])
            heard = Fraction(f * v, v - vs if toward else v + vs)
            other = Fraction(f * v, v + vs if toward else v - vs)
            what = rng.choice(("รถพยาบาล", "รถดับเพลิง", "รถตำรวจ"))
            return numeric(
                stem=(f"{what}เปิดไซเรนความถี่ {f} Hz วิ่งด้วยอัตราเร็ว {vs} m/s {'เข้าหา' if toward else 'ออกจาก'}"
                      "ผู้ฟังที่ยืนนิ่ง ผู้ฟังได้ยินเสียงความถี่เท่าใด (อัตราเร็วเสียง 340 m/s)"),
                answer=heard, wrongs=[other, f, f + vs if toward else f - vs], unit="Hz", topic=TOPIC_PIPE,
                hint="แหล่งกำเนิดเคลื่อนที่: f' = f·v ÷ (v − vₛ) เมื่อเข้าหา และ f·v ÷ (v + vₛ) เมื่อออกห่าง")
        mach = rng.choice((Fraction(3, 2), 2, Fraction(5, 2), 3))
        v = 340
        if rng.random() < 0.5:
            return numeric(
                stem=f"เครื่องบินบินด้วยอัตราเร็ว {show(v * mach)} m/s ในอากาศที่อัตราเร็วเสียง {v} m/s มีเลขมัคเท่าใด",
                answer=mach, wrongs=[1 / mach, mach * 2, v * mach - v], unit="", topic=TOPIC_PIPE,
                hint="เลขมัค = อัตราเร็วของแหล่งกำเนิด ÷ อัตราเร็วเสียง ถ้ามากกว่า 1 จะเกิดคลื่นกระแทก")
        return _labelled(
            stem=f"เครื่องบินบินด้วยอัตราเร็ว {show(v * mach)} m/s ในอากาศที่อัตราเร็วเสียง {v} m/s จะเกิดคลื่นกระแทกหรือไม่",
            correct="เกิด เพราะเครื่องบินเร็วกว่าเสียง",
            wrongs=("ไม่เกิด เพราะเครื่องบินช้ากว่าเสียง", "ไม่เกิด เพราะคลื่นกระแทกเกิดเฉพาะในน้ำ",
                    "เกิดเฉพาะเมื่อเครื่องบินบินเร็วเท่ากับเสียงพอดี"),
            topic=TOPIC_PIPE, hint="คลื่นกระแทกเกิดเมื่อแหล่งกำเนิดเคลื่อนที่เร็วกว่าเสียง (เลขมัคมากกว่า 1)")
