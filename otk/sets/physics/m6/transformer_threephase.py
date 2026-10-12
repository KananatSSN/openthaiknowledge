"""เครื่องกำเนิดไฟฟ้ากระแสสลับ 3 เฟสและหม้อแปลง

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/6

Sets moved here from: science_wave_f14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f14 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_TRANSFORMER = "เครื่องกำเนิดไฟฟ้ากระแสสลับ 3 เฟสและหม้อแปลง"


TRANSFORMER_FACTS = (
    ("เครื่องกำเนิดไฟฟ้ากระแสสลับ 3 เฟสมีลักษณะอย่างไร", "มีขดลวด 3 ชุดวางทำมุม 120° กัน ให้อีเอ็มเอฟ 3 ชุดที่เฟสต่างกัน 120°",
     ("มีขดลวดชุดเดียวหมุน 3 รอบต่อวินาที", "มีแม่เหล็ก 3 อันต่อขนานกัน", "ให้ไฟฟ้ากระแสตรง 3 ระดับ")),
    ("ข้อดีของระบบไฟฟ้า 3 เฟสคือข้อใด", "ส่งกำลังได้สม่ำเสมอและใช้สายไฟน้อยกว่าเมื่อเทียบกับกำลังที่ส่งเท่ากัน",
     ("ใช้กับไฟฟ้ากระแสตรงได้ดีกว่า", "ไม่ต้องใช้หม้อแปลงเลย", "ความต่างศักย์เป็นศูนย์ตลอดเวลา")),
    ("หม้อแปลงไฟฟ้าทำงานได้กับไฟฟ้าชนิดใด", "ไฟฟ้ากระแสสลับ เพราะต้องมีฟลักซ์ที่เปลี่ยนแปลงในแกนเหล็ก",
     ("ไฟฟ้ากระแสตรง เพราะฟลักซ์คงตัว", "ทั้งสองชนิดได้ดีเท่ากัน", "ไฟฟ้าสถิตเท่านั้น")),
    ("การส่งไฟฟ้าระยะไกลใช้ความต่างศักย์สูง เพราะเหตุใด", "กระแสในสายน้อยลง ความร้อนที่สูญเสียในสาย I²R จึงลดลง",
     ("สายไฟจะเย็นลงเพราะความต่างศักย์สูง", "ความต้านทานของสายลดลง", "ไฟฟ้าเดินทางเร็วขึ้น")),
    ("หม้อแปลงขึ้น (เพิ่มแรงดัน) มีจำนวนรอบของขดลวดอย่างไร", "ขดทุติยภูมิมีจำนวนรอบมากกว่าขดปฐมภูมิ",
     ("ขดปฐมภูมิมีจำนวนรอบมากกว่าขดทุติยภูมิ", "จำนวนรอบเท่ากัน", "ไม่มีขดทุติยภูมิ")),
)


@question_type(
    "phys.transformer_threephase_foundation",
    display_name={"th": "เครื่องกำเนิดไฟฟ้า 3 เฟส หลักการของหม้อแปลง และการส่งไฟฟ้าระยะไกล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRANSFORMER,
)
class TransformerThreePhaseFoundation(QuestionType):
    """Three phases, why AC, and why high voltage on the lines."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(TRANSFORMER_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_TRANSFORMER,
                             hint="หม้อแปลงอาศัยฟลักซ์ที่เปลี่ยน จึงใช้กับไฟกระแสสลับ ส่งไฟแรงดันสูงเพื่อลดกระแสและความร้อนในสาย")
        np_, ns = rng.choice([(p, s) for p in (100, 200, 250, 400, 500, 1000, 2000) for s in (50, 100, 200, 500, 1000, 4000)
                              if p != s])
        return _labelled(
            stem=f"หม้อแปลงมีขดปฐมภูมิ {np_:,} รอบ และขดทุติยภูมิ {ns:,} รอบ เป็นหม้อแปลงชนิดใด",
            correct="หม้อแปลงขึ้น (เพิ่มความต่างศักย์)" if ns > np_ else "หม้อแปลงลง (ลดความต่างศักย์)",
            wrongs=("หม้อแปลงลง (ลดความต่างศักย์)" if ns > np_ else "หม้อแปลงขึ้น (เพิ่มความต่างศักย์)",
                    "ไม่เปลี่ยนความต่างศักย์", "เปลี่ยนไฟกระแสสลับเป็นกระแสตรง"),
            topic=TOPIC_TRANSFORMER, hint="V_s/V_p = N_s/N_p ขดทุติยภูมิรอบมากกว่าจะได้ความต่างศักย์สูงขึ้น")


@question_type(
    "phys.transformer_threephase_fluency",
    display_name={"th": "คำนวณความต่างศักย์และจำนวนรอบของหม้อแปลง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRANSFORMER,
)
class TransformerThreePhaseFluency(QuestionType):
    """V_s/V_p = N_s/N_p, both ways round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        vp, np_, ns = rng.choice([(v, p, s) for v in (110, 220, 240, 1000, 11000, 22000) for p in (50, 100, 200, 500, 1000, 2000)
                                  for s in (10, 20, 50, 100, 200, 500, 1000, 4000) if p != s and _exact(Fraction(v * s, p))])
        vs = Fraction(vp * ns, np_)
        if rng.random() < 0.6:
            return numeric(
                stem=f"หม้อแปลงอุดมคติมีขดปฐมภูมิ {np_:,} รอบ ขดทุติยภูมิ {ns:,} รอบ ป้อนไฟกระแสสลับ {vp:,} V ความต่างศักย์ขาออกเท่าใด",
                answer=vs, wrongs=[Fraction(vp * np_, ns), vp, vs * 2], unit="V", topic=TOPIC_TRANSFORMER,
                hint="V_s = V_p × N_s/N_p")
        return numeric(
            stem=f"หม้อแปลงอุดมคติแปลงไฟ {vp:,} V เป็น {show(vs)} V ขดปฐมภูมิมี {np_:,} รอบ ขดทุติยภูมิต้องมีกี่รอบ",
            answer=ns, wrongs=[Fraction(np_ * vp) / vs, np_, ns * 2], unit="รอบ", topic=TOPIC_TRANSFORMER,
            hint="N_s = N_p × V_s/V_p")


@question_type(
    "phys.transformer_threephase_application",
    display_name={"th": "กระแสในหม้อแปลง ประสิทธิภาพ และการสูญเสียพลังงานในสายส่ง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRANSFORMER,
)
class TransformerThreePhaseApplication(QuestionType):
    """Ideal V_pI_p = V_sI_s, real efficiency, and line loss falling as 1/V²."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            vp, vs, is_ = rng.choice([(p, s, i) for p in (220, 240, 1100, 2200) for s in (6, 12, 24, 110)
                                      for i in (1, 2, 5, 10, 11, 20) if _exact(Fraction(s * i, p))])
            return numeric(
                stem=f"หม้อแปลงอุดมคติแปลงไฟ {vp:,} V เป็น {vs} V จ่ายกระแสด้านทุติยภูมิ {is_} A กระแสด้านปฐมภูมิเท่าใด",
                answer=Fraction(vs * is_, vp), wrongs=[Fraction(vp * is_, vs), is_, Fraction(vs, vp)], unit="A",
                topic=TOPIC_TRANSFORMER, hint="หม้อแปลงอุดมคติกำลังเข้าเท่ากำลังออก: V_pI_p = V_sI_s")
        if shape == 1:
            p_in = rng.choice((200, 400, 500, 1000, 2000, 5000))
            eff = rng.choice((80, 85, 90, 95, 96, 98))
            return numeric(
                stem=f"หม้อแปลงรับกำลังไฟฟ้า {p_in:,} W มีประสิทธิภาพร้อยละ {eff} จ่ายกำลังไฟฟ้าออกได้เท่าใด",
                answer=Fraction(p_in * eff, 100), wrongs=[Fraction(p_in * (100 - eff), 100), p_in, p_in * 2],
                unit="W", topic=TOPIC_TRANSFORMER, hint="กำลังออก = ประสิทธิภาพ × กำลังเข้า")
        loss = rng.randint(2, 50) * 100
        k = rng.choice((2, 5, 10, 20))
        return numeric(
            stem=(f"ส่งกำลังไฟฟ้าเท่าเดิมผ่านสายส่งเส้นเดิม สูญเสียพลังงานในสาย {loss:,} W ถ้าเพิ่มความต่างศักย์ในการส่งเป็น "
                  f"{k} เท่า กำลังที่สูญเสียในสายจะเหลือเท่าใด"),
            answer=Fraction(loss, k * k), wrongs=[Fraction(loss, k), loss * k, Fraction(loss, 2 * k)], unit="W",
            topic=TOPIC_TRANSFORMER,
            hint="กำลังเท่าเดิม P = VI ความต่างศักย์เพิ่ม k เท่า กระแสลด k เท่า การสูญเสีย I²R ลด k² เท่า")
