"""อีเอ็มเอฟเหนี่ยวนำและกฎการเหนี่ยวนำของฟาราเดย์

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/4

Sets moved here from: science_wave_f13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f13 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_INDUCTION = "อีเอ็มเอฟเหนี่ยวนำและกฎการเหนี่ยวนำของฟาราเดย์"


INDUCTION_FACTS = (
    ("อีเอ็มเอฟเหนี่ยวนำเกิดในขดลวดเมื่อใด", "เมื่อฟลักซ์แม่เหล็กที่ผ่านขดลวดเปลี่ยนแปลง",
     ("เมื่อมีฟลักซ์แม่เหล็กคงตัวผ่านขดลวด", "เมื่อขดลวดอยู่นิ่งในสนามสม่ำเสมอ", "เมื่อขดลวดร้อนขึ้น")),
    ("ขนาดของอีเอ็มเอฟเหนี่ยวนำตามกฎของฟาราเดย์ขึ้นกับอะไร", "จำนวนรอบของขดลวดและอัตราการเปลี่ยนฟลักซ์แม่เหล็ก",
     ("ขนาดของฟลักซ์ที่ผ่านขดลวดเพียงอย่างเดียว", "ความต้านทานของขดลวดเท่านั้น ไม่ขึ้นกับจำนวนรอบ", "ชนิดของแม่เหล็กเท่านั้นที่ใช้เคลื่อนผ่านขดลวด")),
    ("กฎของเลนซ์กล่าวว่าอย่างไร", "กระแสเหนี่ยวนำสร้างสนามแม่เหล็กที่ต้านการเปลี่ยนฟลักซ์ที่ทำให้เกิดกระแสนั้น",
     ("กระแสเหนี่ยวนำเสริมการเปลี่ยนฟลักซ์ที่ทำให้เกิดกระแสนั้นเสมอ", "กระแสเหนี่ยวนำมีทิศเดียวกับสนามแม่เหล็กภายนอกเสมอ", "กระแสเหนี่ยวนำไม่มีทิศแน่นอน ขึ้นกับชนิดของลวดที่ใช้")),
    ("เลื่อนขั้วเหนือของแม่เหล็กเข้าหาขดลวด ปลายขดลวดด้านที่ใกล้แม่เหล็กจะเป็นขั้วใด", "ขั้วเหนือ เพื่อผลักแม่เหล็กที่กำลังเข้ามา",
     ("ขั้วใต้ เพื่อดูดแม่เหล็กเข้ามา", "ไม่เป็นขั้วแม่เหล็ก เพราะไม่มีกระแสไหล", "สลับขั้วเร็วมากตลอดเวลาที่แม่เหล็กเข้ามา")),
    ("ดึงขั้วเหนือของแม่เหล็กออกจากขดลวด ปลายขดลวดด้านที่ใกล้แม่เหล็กจะเป็นขั้วใด", "ขั้วใต้ เพื่อดึงแม่เหล็กที่กำลังออกไป",
     ("ขั้วเหนือ เพื่อผลักแม่เหล็กออกไป", "ไม่เป็นขั้วแม่เหล็ก เพราะไม่มีกระแสไหล", "เป็นขั้วเหนือเสมอไม่ว่าแม่เหล็กเคลื่อนที่ทางใด")),
)


DEVICES = (
    ("เตาแม่เหล็กไฟฟ้า", "สนามแม่เหล็กที่เปลี่ยนแปลงเหนี่ยวนำกระแสวนในก้นภาชนะโลหะจนร้อน"),
    ("เครื่องกำเนิดไฟฟ้า", "ขดลวดหมุนในสนามแม่เหล็กทำให้ฟลักซ์เปลี่ยนจึงเกิดอีเอ็มเอฟ"),
    ("ปิกอัพของกีตาร์ไฟฟ้า", "สายเหล็กที่สั่นเปลี่ยนฟลักซ์ผ่านขดลวดใต้สาย ได้สัญญาณไฟฟ้าตามการสั่น"),
    ("เครื่องชาร์จโทรศัพท์แบบไร้สาย", "กระแสสลับในขดลวดฐานเหนี่ยวนำอีเอ็มเอฟในขดลวดของโทรศัพท์"),
    ("เครื่องตรวจโลหะที่สนามบิน", "โลหะที่ผ่านทำให้สนามแม่เหล็กของขดลวดเปลี่ยน เครื่องจึงตรวจพบ"),
    ("เบรกแม่เหล็กของรถไฟฟ้า", "กระแสวนที่เหนี่ยวนำในจานโลหะสร้างแรงต้านการเคลื่อนที่"),
)


@question_type(
    "phys.faraday_induction_foundation",
    display_name={"th": "การเกิดอีเอ็มเอฟเหนี่ยวนำ กฎของเลนซ์ และเครื่องใช้ที่อาศัยการเหนี่ยวนำ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_INDUCTION,
)
class FaradayInductionFoundation(QuestionType):
    """When emf is induced, which way it pushes, and the devices that use it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(INDUCTION_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_INDUCTION,
                             hint="อีเอ็มเอฟเหนี่ยวนำเกิดเมื่อฟลักซ์เปลี่ยน และกระแสเหนี่ยวนำต้านการเปลี่ยนนั้น (กฎของเลนซ์)")
        chosen = rng.sample(DEVICES, 4)
        device, how = chosen[0]
        return _labelled(stem=f"{device}ทำงานโดยอาศัยการเหนี่ยวนำแม่เหล็กไฟฟ้าอย่างไร", correct=how,
                         wrongs=tuple(h for _, h in chosen[1:]), topic=TOPIC_INDUCTION,
                         hint="มองหาว่าฟลักซ์ที่ผ่านขดลวดหรือโลหะเปลี่ยนไปเพราะอะไร")


@question_type(
    "phys.faraday_induction_fluency",
    display_name={"th": "คำนวณอีเอ็มเอฟเหนี่ยวนำตามกฎของฟาราเดย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_INDUCTION,
)
class FaradayInductionFluency(QuestionType):
    """ε = N ΔΦ/Δt, with ΔΦ = ΔB × A."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n, db, area, dt = rng.choice([(n, Fraction(b, 10), Fraction(a, 100), Fraction(t, 100))
                                      for n in (10, 20, 50, 100, 200, 500) for b in (1, 2, 4, 5, 8, 10)
                                      for a in (1, 2, 4, 5, 10, 20) for t in (1, 2, 5, 10, 20, 50)
                                      if _exact(n * Fraction(b, 10) * Fraction(a, 100) / Fraction(t, 100))
                                      and n * Fraction(b, 10) * Fraction(a, 100) / Fraction(t, 100) <= 1000])
        emf = n * db * area / dt
        if rng.random() < 0.5:
            return numeric(
                stem=(f"ขดลวด {n} รอบ พื้นที่ {show(area)} m² วางตั้งฉากกับสนามแม่เหล็กที่เปลี่ยนไป {show(db)} T "
                      f"ในเวลา {show(dt)} s อีเอ็มเอฟเหนี่ยวนำเฉลี่ยมีขนาดเท่าใด"),
                answer=emf, wrongs=[db * area / dt, n * db * area, emf * 2], unit="V", topic=TOPIC_INDUCTION,
                hint="ε = N ΔΦ/Δt และ ΔΦ = ΔB × A")
        flux = db * area
        if not _exact(flux):
            # Keep the stated flux exact as shown: fall back to the field-change wording.
            return numeric(
                stem=(f"ขดลวด {n} รอบ พื้นที่ {show(area)} m² วางตั้งฉากกับสนามแม่เหล็กที่เปลี่ยนไป {show(db)} T "
                      f"ในเวลา {show(dt)} s อีเอ็มเอฟเหนี่ยวนำเฉลี่ยมีขนาดเท่าใด"),
                answer=emf, wrongs=[db * area / dt, n * db * area, emf * 2], unit="V", topic=TOPIC_INDUCTION,
                hint="ε = N ΔΦ/Δt และ ΔΦ = ΔB × A")
        return numeric(
            stem=(f"ฟลักซ์แม่เหล็กผ่านขดลวด {n} รอบลดลงจาก {show(flux)} Wb เป็นศูนย์ในเวลา {show(dt)} s "
                  "อีเอ็มเอฟเหนี่ยวนำเฉลี่ยมีขนาดเท่าใด"),
            answer=emf, wrongs=[flux / dt, n * flux, emf / 2], unit="V", topic=TOPIC_INDUCTION,
            hint="ε = N ΔΦ/Δt")


@question_type(
    "phys.faraday_induction_application",
    display_name={"th": "อีเอ็มเอฟเหนี่ยวนำในแท่งตัวนำที่เคลื่อนที่ตัดสนามแม่เหล็ก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_INDUCTION,
)
class FaradayInductionApplication(QuestionType):
    """ε = BLv for a rod on rails, the current it drives, and the force that resists it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        b, length, v, r = rng.choice([(Fraction(b, 10), Fraction(ell, 10), v, r) for b in (1, 2, 4, 5, 8, 10)
                                      for ell in (1, 2, 3, 4, 5, 10) for v in (1, 2, 4, 5, 10)
                                      for r in (Fraction(1, 2), 1, 2, 4, 5)
                                      if _exact(Fraction(b, 10) * Fraction(ell, 10) * v / r)
                                      and _exact(Fraction(b, 10) ** 2 * Fraction(ell, 10) ** 2 * v / r)])
        emf = b * length * v
        i = emf / r
        given = (f"แท่งตัวนำยาว {show(length)} m เลื่อนบนรางด้วยความเร็ว {v} m/s ตั้งฉากกับสนามแม่เหล็ก {show(b)} T "
                 f"วงจรมีความต้านทานรวม {show(r)} Ω")
        shape = rng.randrange(3)
        if shape == 0:
            return numeric(stem=f"{given} อีเอ็มเอฟเหนี่ยวนำเท่าใด", answer=emf, wrongs=[b * v, emf / r, emf * 2],
                           unit="V", topic=TOPIC_INDUCTION, hint="ε = BLv")
        if shape == 1:
            return numeric(stem=f"{given} กระแสเหนี่ยวนำเท่าใด", answer=i, wrongs=[emf, emf * r, i * 2],
                           unit="A", topic=TOPIC_INDUCTION, hint="ε = BLv แล้ว I = ε/R")
        return numeric(stem=f"{given} แรงแม่เหล็กที่ต้านการเคลื่อนที่ของแท่งเท่าใด", answer=i * length * b,
                       wrongs=[emf * length, i * b, i * length * b * 2], unit="N", topic=TOPIC_INDUCTION,
                       hint="หา I = BLv/R แล้วแรงบนแท่ง F = ILB (กฎของเลนซ์: แรงต้านการเคลื่อนที่)")
