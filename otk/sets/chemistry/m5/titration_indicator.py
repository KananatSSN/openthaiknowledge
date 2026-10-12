"""หลักการไทเทรตและการเลือกอินดิเคเตอร์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/20

Sets moved here from: science_wave_f37.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, show
from otk.sets._support.science_wave_f37 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_TITRATION = "หลักการไทเทรตและการเลือกอินดิเคเตอร์"


# (indicator, low pH, high pH, acid colour, base colour)
INDICATORS = (
    ("เมทิลออเรนจ์", Fraction(31, 10), Fraction(44, 10), "แดง", "เหลือง"),
    ("เมทิลเรด", Fraction(44, 10), Fraction(62, 10), "แดง", "เหลือง"),
    ("โบรมอไทมอลบลู", Fraction(6), Fraction(76, 10), "เหลือง", "น้ำเงิน"),
    ("ฟีนอล์ฟทาลีน", Fraction(83, 10), Fraction(10), "ไม่มีสี", "ชมพู"),
)


# (acid, base, rough pH at the equivalence point, which indicator suits)
TITRATIONS = (
    ("HCl", "NaOH", 7, "โบรมอไทมอลบลู"), ("HNO₃", "KOH", 7, "โบรมอไทมอลบลู"),
    ("CH₃COOH", "NaOH", Fraction(87, 10), "ฟีนอล์ฟทาลีน"), ("HCOOH", "KOH", Fraction(84, 10), "ฟีนอล์ฟทาลีน"),
    ("HF", "NaOH", Fraction(9), "ฟีนอล์ฟทาลีน"), ("HCl", "NH₃", Fraction(53, 10), "เมทิลเรด"),
    ("HNO₃", "NH₃", Fraction(52, 10), "เมทิลเรด"), ("H₂SO₄", "NH₃", Fraction(51, 10), "เมทิลเรด"),
)


TERMS = (
    ("จุดสมมูลของการไทเทรตคืออะไร", "จุดที่กรดและเบสทำปฏิกิริยากันพอดีตามอัตราส่วนโมลในสมการ",
     ("จุดที่อินดิเคเตอร์เปลี่ยนสี", "จุดที่สารละลายมี pH เท่ากับ 7 เสมอ", "จุดที่เริ่มหยดสารจากบิวเรตต์")),
    ("จุดยุติของการไทเทรตคืออะไร", "จุดที่อินดิเคเตอร์เปลี่ยนสี ซึ่งควรอยู่ใกล้จุดสมมูลมากที่สุด",
     ("จุดที่กรดและเบสทำปฏิกิริยากันพอดีเสมอ", "จุดที่สารในบิวเรตต์หมด", "จุดที่สารละลายเดือด")),
    ("อินดิเคเตอร์ที่เหมาะสมกับการไทเทรตต้องมีสมบัติอย่างไร", "ช่วง pH ที่เปลี่ยนสีครอบคลุม pH ที่จุดสมมูล",
     ("เปลี่ยนสีที่ pH 7 เสมอ", "มีสีเข้มที่สุด", "ทำปฏิกิริยากับกรดได้ดีที่สุด")),
    ("สารละลายมาตรฐานในการไทเทรตคืออะไร", "สารละลายที่ทราบความเข้มข้นแน่นอน",
     ("สารละลายที่ไม่ทราบความเข้มข้น", "น้ำกลั่นที่ใช้ล้างอุปกรณ์", "อินดิเคเตอร์ที่หยดลงไป")),
)


def indicator_by_name(name):
    return next(i for i in INDICATORS if i[0] == name)


@question_type(
    "chem.titration_indicator_foundation",
    display_name={"th": "หลักการไทเทรตและช่วงการเปลี่ยนสีของอินดิเคเตอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TITRATION,
)
class TitrationIndicatorFoundation(QuestionType):
    """Equivalence point, end point, and what colour an indicator shows at a pH."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, right, wrongs = rng.choice(TERMS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_TITRATION,
                             hint="จุดสมมูลคือจุดที่ทำปฏิกิริยาพอดี จุดยุติคือจุดที่อินดิเคเตอร์เปลี่ยนสี")
        name, low, high, acid_colour, base_colour = rng.choice(INDICATORS)
        ph = rng.choice([Fraction(x, 2) for x in range(2, 27)])
        if low <= ph <= high:
            return self.build(rng)
        right = acid_colour if ph < low else base_colour
        colours = sorted(({i[3] for i in INDICATORS} | {i[4] for i in INDICATORS} | {"ส้ม", "เขียว"}) - {right})
        return _labelled(stem=f"{name} เปลี่ยนสีในช่วง pH {show(low)}-{show(high)} ({acid_colour} → {base_colour}) "
                              f"ในสารละลาย pH {show(ph)} จะมีสีใด",
                         correct=right, wrongs=tuple(colours), topic=TOPIC_TITRATION,
                         hint="pH ต่ำกว่าช่วงเปลี่ยนสีได้สีด้านกรด pH สูงกว่าช่วงได้สีด้านเบส")


@question_type(
    "chem.titration_indicator_fluency",
    display_name={"th": "เลือกอินดิเคเตอร์ให้เหมาะกับการไทเทรต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TITRATION,
)
class TitrationIndicatorFluency(QuestionType):
    """The indicator's range must hold the equivalence pH."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, base, eq_ph, best = rng.choice(TITRATIONS)
        ranges = ", ".join(f"{n} {show(lo)}-{show(hi)}" for n, lo, hi, _, _ in INDICATORS)
        if rng.random() < 0.4:
            name, lo, hi, _, _ = rng.choice(INDICATORS)
            point = rng.choice([Fraction(x, 10) for x in range(int(lo * 10) + 1, int(hi * 10))])
            return _labelled(stem=f"การไทเทรตครั้งหนึ่งมี pH ที่จุดสมมูลเท่ากับ {show(point)} ควรใช้อินดิเคเตอร์ใด (ช่วง pH: {ranges})",
                             correct=name, wrongs=tuple(i[0] for i in INDICATORS if i[0] != name), topic=TOPIC_TITRATION,
                             hint="เลือกอินดิเคเตอร์ที่ช่วง pH การเปลี่ยนสีครอบคลุม pH ที่จุดสมมูล")
        if rng.random() < 0.5:
            return _labelled(stem=f"ไทเทรต {acid} ด้วย {base} (pH ที่จุดสมมูลประมาณ {show(eq_ph)}) ควรใช้อินดิเคเตอร์ใด "
                                  f"(ช่วง pH: {ranges})",
                             correct=best, wrongs=tuple(i[0] for i in INDICATORS if i[0] != best), topic=TOPIC_TITRATION,
                             hint="เลือกอินดิเคเตอร์ที่ช่วง pH การเปลี่ยนสีครอบคลุม pH ที่จุดสมมูล")
        kind = ("กรดแก่กับเบสแก่" if eq_ph == 7 else "กรดอ่อนกับเบสแก่" if eq_ph > 7 else "กรดแก่กับเบสอ่อน")
        right = "ประมาณ 7" if eq_ph == 7 else "มากกว่า 7" if eq_ph > 7 else "น้อยกว่า 7"
        return _labelled(stem=f"การไทเทรต {acid} ด้วย {base} ({kind}) ที่จุดสมมูลสารละลายมี pH เป็นอย่างไร", correct=right,
                         wrongs=tuple(x for x in ("ประมาณ 7", "มากกว่า 7", "น้อยกว่า 7", "เท่ากับ 0") if x != right),
                         topic=TOPIC_TITRATION,
                         hint="ที่จุดสมมูลมีแต่เกลือกับน้ำ เกลือของกรดอ่อน+เบสแก่เป็นเบส ของกรดแก่+เบสอ่อนเป็นกรด")


@question_type(
    "chem.titration_indicator_application",
    display_name={"th": "สีที่จุดยุติของการไทเทรต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TITRATION,
)
class TitrationIndicatorApplication(QuestionType):
    """Which way the colour turns at the end point, depending on what is in the flask."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, base, _, best = rng.choice(TITRATIONS)
        name, _, _, acid_colour, base_colour = indicator_by_name(best)
        acid_in_flask = rng.random() < 0.5
        if acid_in_flask:
            right = f"จาก{acid_colour}เป็น{base_colour}"
            setup = f"ใส่ {acid} ในขวดรูปกรวยและหยด {base} จากบิวเรตต์"
        else:
            right = f"จาก{base_colour}เป็น{acid_colour}"
            setup = f"ใส่ {base} ในขวดรูปกรวยและหยด {acid} จากบิวเรตต์"
        flipped = f"จาก{base_colour}เป็น{acid_colour}" if acid_in_flask else f"จาก{acid_colour}เป็น{base_colour}"
        if rng.random() < 0.5:
            end = rng.randrange(15, 41)
            added = rng.choice([v for v in range(5, 51) if v != end])
            flask_colour = acid_colour if acid_in_flask else base_colour
            other_colour = base_colour if acid_in_flask else acid_colour
            now = flask_colour if added < end else other_colour
            return _labelled(stem=f"ไทเทรตโดย{setup} ใช้{name}เป็นอินดิเคเตอร์ จุดสมมูลอยู่ที่ {end} cm³ "
                                  f"เมื่อหยดไปแล้ว {added} cm³ สารละลายในขวดมีสีใด",
                             correct=now, wrongs=tuple(c for c in (flask_colour, other_colour, "ส้ม", "เขียว", "ม่วง")
                                                       if c != now)[:3],
                             topic=TOPIC_TITRATION, hint="ก่อนจุดสมมูลสีเป็นของสารในขวด เลยจุดสมมูลสีเปลี่ยนตามสารจากบิวเรตต์")
        return _labelled(stem=f"ไทเทรตโดย{setup} ใช้{name}เป็นอินดิเคเตอร์ ที่จุดยุติสีของสารละลายเปลี่ยนอย่างไร",
                         correct=right, wrongs=(flipped, "ไม่เปลี่ยนสีเลย", f"จาก{acid_colour}เป็นไม่มีสี"
                                                if acid_colour != "ไม่มีสี" else "จากชมพูเป็นน้ำเงิน"),
                         topic=TOPIC_TITRATION, hint="สารในขวดกำหนดสีตั้งต้น เมื่อเลยจุดสมมูลสารจากบิวเรตต์ทำให้สีเปลี่ยน")
