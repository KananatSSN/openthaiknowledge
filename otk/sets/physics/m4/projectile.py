"""การเคลื่อนที่แบบโพรเจกไทล์

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/16

Sets moved here from: science_wave_f6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, _labelled, numeric, show
from otk.sets._support.science_wave_f6 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_PROJECTILE = "การเคลื่อนที่แบบโพรเจกไทล์"


PROJECTILE_FACTS = (
    ("ในการเคลื่อนที่แบบโพรเจกไทล์ ความเร็วในแนวระดับเป็นอย่างไร (ไม่คิดแรงต้านอากาศ)", "คงตัวตลอดการเคลื่อนที่",
     ("เพิ่มขึ้นอย่างสม่ำเสมอ", "ลดลงจนเป็นศูนย์ที่จุดสูงสุด", "เปลี่ยนทิศทุกขณะ")),
    ("ในการเคลื่อนที่แบบโพรเจกไทล์ ความเร่งของวัตถุเป็นอย่างไร", "มีขนาด g ทิศลงในแนวดิ่งตลอดการเคลื่อนที่",
     ("มีขนาด g ทิศตามแนวการเคลื่อนที่", "เป็นศูนย์ที่จุดสูงสุด", "มีทั้งแนวระดับและแนวดิ่ง")),
    ("ที่จุดสูงสุดของการเคลื่อนที่แบบโพรเจกไทล์ ข้อใดถูกต้อง", "ความเร็วแนวดิ่งเป็นศูนย์ แต่ความเร็วแนวระดับไม่เป็นศูนย์",
     ("ความเร็วทั้งสองแนวเป็นศูนย์", "ความเร่งเป็นศูนย์", "ความเร็วแนวระดับเป็นศูนย์")),
    ("ขว้างลูกบอลออกในแนวระดับ พร้อมกับปล่อยลูกบอลอีกลูกจากความสูงเดียวกัน ลูกใดถึงพื้นก่อน",
     "ถึงพื้นพร้อมกัน เพราะการเคลื่อนที่แนวดิ่งเหมือนกัน",
     ("ลูกที่ขว้างถึงก่อน เพราะเร็วกว่า", "ลูกที่ปล่อยถึงก่อน เพราะเดินทางสั้นกว่า", "ขึ้นกับมวลของลูกบอล")),
    ("ยิงวัตถุด้วยอัตราเร็วเท่ากัน มุมใดทำให้ได้ระยะในแนวระดับไกลที่สุด (บนพื้นราบ)", "45°",
     ("30°", "60°", "90°")),
    ("ยิงวัตถุด้วยอัตราเร็วเท่ากันที่มุม 37° และ 53° กับพื้นราบ ระยะในแนวระดับเป็นอย่างไร", "เท่ากัน แต่ที่ 53° ขึ้นได้สูงกว่า",
     ("ที่ 53° ไกลกว่า", "ที่ 37° ไกลกว่าและสูงกว่า", "เท่ากันและสูงเท่ากัน")),
)


# (time of flight in s, height in m) with h = ½gt².
FALLS = tuple((Fraction(t), Fraction(5) * Fraction(t) ** 2) for t in
              (Fraction(2, 5), Fraction(1, 2), Fraction(3, 5), Fraction(4, 5), 1, Fraction(6, 5),
               Fraction(3, 2), 2, Fraction(5, 2), 3, 4))


# (time, launch speed, landing speed) with (gt)² + u² a perfect square.
LANDINGS = ((Fraction(1, 2), 12, 13), (Fraction(4, 5), 6, 10), (Fraction(6, 5), 5, 13), (Fraction(6, 5), 9, 15),
            (Fraction(6, 5), 16, 20), (Fraction(3, 2), 20, 25), (Fraction(3, 2), 8, 17), (1, 24, 26),
            (2, 15, 25), (3, 40, 50), (4, 30, 50), (2, 21, 29))


def _edge(rng: Random, height: Fraction) -> str:
    """Somewhere a ball could roll off at this height."""
    return "โต๊ะ" if height <= Fraction(9, 5) else rng.choice(("หน้าผา", "ดาดฟ้าอาคาร", "สะพาน"))


@question_type(
    "phys.projectile_foundation",
    display_name={"th": "ลักษณะการเคลื่อนที่แบบโพรเจกไทล์ในแนวระดับและแนวดิ่ง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROJECTILE,
)
class ProjectileFoundation(QuestionType):
    """Two motions at once: steady across, free fall down."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        hint = "แยกคิดสองแนว: แนวระดับความเร็วคงตัว แนวดิ่งตกอิสระด้วยความเร่ง g และใช้เวลาเดียวกัน"
        if shape == 0:
            stem, correct, wrongs = rng.choice(PROJECTILE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_PROJECTILE, hint=hint)
        if shape == 1:
            t, h = rng.choice(FALLS)
            where = _edge(rng, h)
            return numeric(
                stem=f"ขว้างลูกบอลออกจากขอบ{where}สูง {show(h)} m ในแนวระดับ ลูกบอลใช้เวลาเท่าใดจึงถึงพื้น (g = 10 m/s²)",
                answer=t, wrongs=[h / 5, t * 2, h / 10], unit="s", topic=TOPIC_PROJECTILE,
                hint="แนวดิ่งเริ่มจากความเร็วศูนย์: h = ½gt² ความเร็วแนวระดับไม่มีผลต่อเวลา")
        u = rng.randint(2, 30)
        t = rng.randint(1, 4)
        return numeric(
            stem=(f"ขว้างวัตถุออกในแนวระดับด้วยความเร็ว {u} m/s เมื่อผ่านไป {t} s (ยังไม่ถึงพื้น) "
                  "ความเร็วในแนวระดับของวัตถุเท่าใด (ไม่คิดแรงต้านอากาศ)"),
            answer=u, wrongs=[u + G * t, G * t, u * t], unit="m/s", topic=TOPIC_PROJECTILE, hint=hint)


@question_type(
    "phys.projectile_fluency",
    display_name={"th": "คำนวณการเคลื่อนที่แบบโพรเจกไทล์ที่ขว้างในแนวระดับ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROJECTILE,
)
class ProjectileFluency(QuestionType):
    """Launched level: how far out, how fast down, and how fast overall."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            t, h = rng.choice(FALLS)
            u = rng.randint(2, 25)
            return numeric(
                stem=(f"ขว้างวัตถุออกจากขอบ{_edge(rng, h)}สูง {show(h)} m ในแนวระดับด้วยความเร็ว {u} m/s "
                      "วัตถุตกห่างจากจุดที่อยู่ใต้ขอบลงมาในแนวระดับเท่าใด (g = 10 m/s²)"),
                answer=u * t, wrongs=[u * t * 2, u * h / 10, u + t], unit="m", topic=TOPIC_PROJECTILE,
                hint="หาเวลาจากแนวดิ่ง h = ½gt² ก่อน แล้วระยะแนวระดับ = ut")
        if shape == 1:
            t, h = rng.choice(FALLS)
            u = rng.randint(2, 25)
            return numeric(
                stem=(f"ลูกบอลกลิ้งตกจากขอบ{_edge(rng, h)}สูง {show(h)} m ด้วยความเร็ว {u} m/s ในแนวระดับ "
                      "ขณะกระทบพื้นลูกบอลมีความเร็วในแนวดิ่งเท่าใด (g = 10 m/s²)"),
                answer=G * t, wrongs=[G * t + u, u, 2 * G * h], unit="m/s", topic=TOPIC_PROJECTILE,
                hint="ความเร็วแนวดิ่งเริ่มจากศูนย์: v = gt โดย t หาได้จาก h = ½gt²")
        t, u, v = rng.choice(LANDINGS)
        h = 5 * Fraction(t) ** 2
        return numeric(
            stem=(f"ขว้างวัตถุออกในแนวระดับด้วยความเร็ว {u} m/s จากที่สูง {show(h)} m "
                  "ขณะกระทบพื้นวัตถุมีอัตราเร็วเท่าใด (g = 10 m/s²)"),
            answer=v, wrongs=[u + G * Fraction(t), G * Fraction(t), u], unit="m/s", topic=TOPIC_PROJECTILE,
            hint="หาความเร็วแนวดิ่ง gt แล้วรวมแบบเวกเตอร์กับความเร็วแนวระดับ: v = √(u² + (gt)²)")


@question_type(
    "phys.projectile_application",
    display_name={"th": "การเคลื่อนที่แบบโพรเจกไทล์ที่ยิงทำมุมกับพื้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROJECTILE,
)
class ProjectileApplication(QuestionType):
    """Launched at 37° or 53°: time aloft, top height and range."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        k = rng.randint(1, 8)
        u = 5 * k
        angle = rng.choice((37, 53))
        ux, uy = (4 * k, 3 * k) if angle == 37 else (3 * k, 4 * k)
        flight = Fraction(2 * uy, G)
        thing = rng.choice(("ลูกฟุตบอล", "ลูกกอล์ฟ", "ลูกบาสเกตบอล", "ลูกเปตอง"))
        launch = (f"เตะ{thing}" if thing == "ลูกฟุตบอล" else f"ยิง{thing}" if thing == "ลูกกอล์ฟ" else f"โยน{thing}")
        given = (f"{launch}จากพื้นราบด้วยความเร็ว {u} m/s ทำมุม {angle}° กับพื้น "
                 "(g = 10 m/s², sin 37° = 0.6, cos 37° = 0.8)")
        shape = rng.randrange(3)
        if shape == 0:
            return numeric(
                stem=f"{given} ลูกลอยอยู่ในอากาศนานเท่าใด",
                answer=flight, wrongs=[Fraction(uy, G), Fraction(2 * ux, G), Fraction(2 * u, G)],
                unit="s", topic=TOPIC_PROJECTILE,
                hint="ใช้ความเร็วแนวดิ่ง u sin θ: เวลาขึ้น = u sin θ ÷ g และเวลาทั้งหมดเป็นสองเท่า")
        if shape == 1:
            return numeric(
                stem=f"{given} ลูกขึ้นไปได้สูงสุดเท่าใด",
                answer=Fraction(uy * uy, 2 * G), wrongs=[Fraction(u * u, 2 * G), Fraction(ux * ux, 2 * G),
                                                         Fraction(uy * uy, G)],
                unit="m", topic=TOPIC_PROJECTILE, hint="ที่จุดสูงสุดความเร็วแนวดิ่งเป็นศูนย์: H = (u sin θ)² ÷ 2g")
        return numeric(
            stem=f"{given} ลูกตกห่างจากจุดเริ่มต้นในแนวระดับเท่าใด",
            answer=ux * flight, wrongs=[u * flight, uy * flight, ux * flight / 2], unit="m",
            topic=TOPIC_PROJECTILE, hint="ระยะแนวระดับ = u cos θ × เวลาทั้งหมด โดยเวลาทั้งหมด = 2u sin θ ÷ g")
