"""ดรรชนีหักเหและการหักเหของแสง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/10

Sets moved here from: physics, science_wave_a7.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.physics import SUBJECT, TOPIC, _n
from otk.sets._support.science_wave_a7 import UPPER, WAVES

PROVENANCE = Provenance("original")


# (ดรรชนีหักเหของตัวกลาง, ความลึกจริง ซม.) โดยความลึกปรากฏเป็นจำนวนเต็ม.
# The index is kept as a fraction (numerator, denominator) so the apparent depth
# is exact; only fractions whose decimal form terminates in two places are used,
# because a stem reading "ดรรชนีหักเห 1.33333" is a rounding artefact, not a
# measurement. All of them fall in the range real liquids and glass occupy.
DEPTH_SETUPS = (
    ((3, 2), 30), ((3, 2), 45), ((3, 2), 60), ((3, 2), 90),
    ((5, 4), 40), ((5, 4), 80), ((5, 4), 100),
    ((8, 5), 40), ((8, 5), 80),
    ((6, 5), 30), ((6, 5), 60), ((6, 5), 90),
)


# (ดรรชนีหักเหตัวกลางที่แสงเดินทางอยู่, ดรรชนีหักเหตัวกลางที่แสงจะออกไป).
# n₁ > n₂ ≥ 1 — the second condition matters as much as the first, since no real
# medium slows light less than a vacuum does. sin θc comes out exact for each row.
CRITICAL_PAIRS = (
    (1.5, 1.2), (2.0, 1.0), (2.0, 1.2), (2.0, 1.5), (2.0, 1.6),
    (1.6, 1.0), (1.6, 1.2), (1.25, 1.0), (2.5, 1.0), (2.5, 1.5), (2.5, 2.0),
)


# (n₁, sin θ₁, n₂) โดย n₁·sin θ₁ / n₂ ไม่เกิน 1 และเป็นทศนิยมที่ลงตัว.
SNELL_SETUPS = (
    (1.5, 0.4, 1.2), (1.5, 0.6, 1.0), (2.0, 0.3, 1.5), (1.6, 0.5, 1.0),
    (1.0, 0.9, 1.5), (1.0, 0.6, 1.2), (1.2, 0.5, 1.5), (1.25, 0.8, 2.0),
)


def _num(value: float) -> str:
    """A refractive index or sine as it should read in a stem: 1.5, not 1.50."""
    return f"{value:g}"


@question_type(
    "phys.refraction_index_foundation",
    display_name={"th": "ความหมายของดรรชนีหักเหและทิศทางการหักเหของแสง"},
    level=UPPER, subject=SUBJECT, topic=WAVES,
)
class RefractionIndexFoundation(ConceptBankType):
    """What the refractive index is, and which way the ray bends.

    `phys.refraction` computes n = c/v. It never says which way a ray turns at a
    boundary, nor that the frequency is the one thing refraction leaves alone —
    both of which the ``ม.5/10`` calculations quietly assume.
    """

    ITEMS = [
        Concept(
            "ดรรชนีหักเหของตัวกลางหนึ่งมีความหมายว่าอย่างไร",
            "อัตราส่วนของอัตราเร็วแสงในสุญญากาศต่ออัตราเร็วแสงในตัวกลางนั้น",
            ("อัตราส่วนของอัตราเร็วแสงในตัวกลางนั้นต่ออัตราเร็วแสงในสุญญากาศ",
             "อัตราส่วนของมุมตกกระทบต่อมุมหักเหเสมอ",
             "อัตราส่วนของความหนาแน่นของตัวกลางต่อความหนาแน่นของอากาศ"),
        ),
        Concept(
            "เหตุใดดรรชนีหักเหของตัวกลางใด ๆ จึงมีค่าไม่น้อยกว่า 1",
            "เพราะแสงเดินทางในตัวกลางได้ช้ากว่าหรือเท่ากับในสุญญากาศเสมอ",
            ("เพราะดรรชนีหักเหเป็นอัตราส่วนของมุมสองมุมซึ่งเป็นบวกเสมอ",
             "เพราะตัวกลางทุกชนิดมีความหนาแน่นมากกว่าสุญญากาศ",
             "เพราะกำหนดให้อากาศมีดรรชนีหักเหเท่ากับ 1 เป็นค่าต่ำสุด"),
        ),
        Concept(
            "แสงเดินทางจากอากาศเข้าสู่แก้ว รังสีหักเหจะเบนไปทางใด",
            "เบนเข้าหาเส้นแนวฉาก เพราะแสงเดินทางในแก้วได้ช้ากว่า",
            ("เบนออกจากเส้นแนวฉาก เพราะแสงเดินทางในแก้วได้ช้ากว่า",
             "เบนเข้าหาเส้นแนวฉาก เพราะแสงเดินทางในแก้วได้เร็วกว่า",
             "ไม่เบน เพราะแสงเดินทางเป็นเส้นตรงเสมอเมื่อผ่านตัวกลางโปร่งใส"),
        ),
        Concept(
            "เมื่อแสงหักเหจากตัวกลางหนึ่งไปยังอีกตัวกลางหนึ่ง ปริมาณใดไม่เปลี่ยนแปลง",
            "ความถี่ของแสง",
            ("ความยาวคลื่นของแสง", "อัตราเร็วของแสง", "ทิศทางการเดินทางของแสง"),
        ),
        Concept(
            "เมื่อมองเหรียญที่ก้นสระน้ำจากด้านบน จะเห็นเหรียญอยู่ที่ตำแหน่งใด",
            "ตื้นกว่าตำแหน่งจริง เพราะแสงหักเหออกจากเส้นแนวฉากเมื่อออกจากน้ำสู่อากาศ",
            ("ลึกกว่าตำแหน่งจริง เพราะแสงหักเหเข้าหาเส้นแนวฉากเมื่อออกจากน้ำสู่อากาศ",
             "ตรงตำแหน่งจริง เพราะการหักเหเปลี่ยนเฉพาะความสว่างไม่ใช่ตำแหน่ง",
             "เยื้องไปด้านข้างของตำแหน่งจริง เพราะน้ำทำให้ภาพเลื่อนในแนวราบ"),
        ),
        Concept(
            "การสะท้อนกลับหมดของแสงเกิดขึ้นได้ในกรณีใด",
            "เมื่อแสงเดินทางจากตัวกลางที่มีดรรชนีหักเหมากไปยังตัวกลางที่มีดรรชนีหักเหน้อยกว่า "
            "ด้วยมุมตกกระทบมากกว่ามุมวิกฤต",
            ("เมื่อแสงเดินทางจากตัวกลางที่มีดรรชนีหักเหน้อยไปยังตัวกลางที่มีดรรชนีหักเหมากกว่า "
             "ด้วยมุมตกกระทบมากกว่ามุมวิกฤต",
             "เมื่อแสงตกกระทบผิวรอยต่อในแนวตั้งฉากพอดี",
             "เมื่อแสงตกกระทบผิวรอยต่อของตัวกลางสองชนิดที่มีดรรชนีหักเหเท่ากัน"),
        ),
        Concept(
            "มุมวิกฤตของรอยต่อระหว่างตัวกลางสองชนิดหมายถึงมุมใด",
            "มุมตกกระทบที่ทำให้มุมหักเหเท่ากับ 90 องศาพอดี",
            ("มุมหักเหที่ทำให้มุมตกกระทบเท่ากับ 90 องศาพอดี",
             "มุมตกกระทบที่ทำให้มุมหักเหเท่ากับมุมตกกระทบพอดี",
             "มุมตกกระทบที่ทำให้แสงไม่สะท้อนกลับเลย"),
        ),
        Concept("ดรรชนีหักเหของแก้วประมาณ 1.5 หมายความว่าอย่างไร",
                "แสงในสุญญากาศเดินทางเร็วกว่าแสงในแก้ว 1.5 เท่า",
                (
                 "แสงในแก้วเดินทางเร็วกว่าแสงในสุญญากาศ 1.5 เท่า",
                 "แก้วมีความหนาแน่นมากกว่าน้ำ 1.5 เท่า",
                 "แสงหักเหในแก้วเป็นมุม 1.5 องศา",
                 "ความยาวคลื่นแสงในแก้วยาวขึ้น 1.5 เท่า",
                 "ความถี่ของแสงในแก้วลดลง 1.5 เท่า")),
        Concept("แสงเดินทางจากแก้วออกสู่อากาศในแนวเฉียง รังสีหักเหจะเบนไปทางใด",
                "เบนออกจากเส้นแนวฉาก เพราะแสงเดินทางในอากาศได้เร็วกว่า",
                (
                 "เบนเข้าหาเส้นแนวฉาก เพราะแสงเดินทางในอากาศได้เร็วกว่า",
                 "ไม่เบนเลย เพราะแสงเดินทางเป็นเส้นตรงเสมอ",
                 "เบนเข้าหาเส้นแนวฉาก เพราะอากาศมีดรรชนีหักเหมากกว่า",
                 "สะท้อนกลับหมดทุกกรณี",
                 "เบนออกจากเส้นแนวฉาก เพราะแสงเดินทางในอากาศได้ช้ากว่า")),
        Concept("แสงตกกระทบรอยต่อระหว่างตัวกลางสองชนิดตามแนวเส้นแนวฉากพอดี จะเป็นอย่างไร",
                "ผ่านเข้าไปโดยไม่เปลี่ยนทิศ แต่อัตราเร็วเปลี่ยนไป",
                (
                 "เบนเข้าหาเส้นแนวฉาก",
                 "สะท้อนกลับหมด",
                 "ผ่านเข้าไปโดยทั้งทิศและอัตราเร็วไม่เปลี่ยน",
                 "เบนออกจากเส้นแนวฉาก",
                 "หยุดอยู่ที่รอยต่อ")),
        Concept("เมื่อแสงเดินทางจากอากาศเข้าสู่น้ำ ความยาวคลื่นเปลี่ยนไปอย่างไร",
                "สั้นลง เพราะอัตราเร็วลดลงแต่ความถี่คงเดิม",
                (
                 "ยาวขึ้น เพราะอัตราเร็วเพิ่มขึ้น",
                 "เท่าเดิม เพราะเป็นแสงเดิม",
                 "สั้นลง เพราะความถี่ลดลง",
                 "ยาวขึ้น เพราะความถี่เพิ่มขึ้น",
                 "เป็นศูนย์ เพราะแสงหยุดในน้ำ")),
    ]


@question_type("phys.refraction",
               display_name={"th": "การหักเหของแสง (ดัชนีหักเห)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class Refraction(PhysCalc):
    """ดัชนีหักเห n = c/v — อัตราเร็วแสงในสุญญากาศต่ออัตราเร็วในตัวกลาง."""

    # (n, v) with v in units of ×10^8 m/s and c = 3×10^8 m/s, so n·v = 3.
    _PAIRS = [(1.5, 2.0), (2.0, 1.5), (2.5, 1.2), (3.0, 1.0), (1.2, 2.5), (1.25, 2.4), (2.4, 1.25)]
    _C = "กำหนดให้อัตราเร็วแสงในสุญญากาศเท่ากับ 3×10⁸ เมตร/วินาที"
    def draw(self, rng: Random) -> Calc:
        if rng.random() < 0.35:
            # Two media whose speed ratio n₂/n₁ is exact to two places.
            indices = [n for n, _ in self._PAIRS]
            ratios = [(a, b) for a in indices for b in indices
                      if b > a and round(b / a * 100, 9) == int(round(b / a * 100, 9))]
            n1, n2 = rng.choice(ratios)
            ratio = n2 / n1
            return Calc(
                f"ตัวกลาง A มีดัชนีหักเห {_n(n1)} และตัวกลาง B มีดัชนีหักเห {_n(n2)} "
                "อัตราเร็วของแสงในตัวกลาง A เป็นกี่เท่าของอัตราเร็วในตัวกลาง B",
                _n(ratio), wrongs=(_n(round(n1 / n2, 2)), _n(n2 - n1), _n(n1 * n2)),
                hint=r"rac{v_A}{v_B} = rac{n_B}{n_A}")
        n, v = rng.choice(self._PAIRS)
        if rng.random() < 0.5:
            return Calc(
                f"แสงมีอัตราเร็วในตัวกลางหนึ่งเท่ากับ {_n(v)}×10⁸ เมตร/วินาที "
                f"จงหาดัชนีหักเหของตัวกลาง ({self._C})",
                _n(n), wrongs=(_n(v), _n(2 * n), _n(n / 2)),
                hint=r"n = \frac{c}{v}")
        return Calc(
            f"ตัวกลางหนึ่งมีดัชนีหักเห {_n(n)} จงหาอัตราเร็วของแสงในตัวกลางนี้ "
            f"(หน่วย ×10⁸ เมตร/วินาที) ({self._C})",
            _n(v), wrongs=(_n(n), _n(2 * v), _n(v / 2)),
            hint=r"v = \frac{c}{n}")


@question_type(
    "phys.refraction_index_application",
    display_name={"th": "ความลึกปรากฏ มุมวิกฤต และกฎของสเนลล์"},
    level=UPPER, subject=SUBJECT, topic=WAVES,
)
class RefractionIndexApplication(PhysCalc):
    """The three calculations ``ม.5/10`` names beyond n = c/v.

    Real versus apparent depth, the critical angle, and the relation between the
    two angles are all listed in the outcome and none of them is reachable from
    `phys.refraction`, which only converts between an index and a speed.
    """

    def draw(self, rng: Random) -> Calc:
        which = rng.random()
        if which < 0.4:
            return self._depth(rng)
        if which < 0.7:
            return self._critical(rng)
        return self._snell(rng)

    def _depth(self, rng: Random) -> Calc:
        (top, bottom), real = rng.choice(DEPTH_SETUPS)
        apparent = real * bottom // top
        index = _num(top / bottom)
        return Calc(
            f"ภาชนะใสบรรจุของเหลวที่มีดรรชนีหักเห {index} ลึกจริง {real} เซนติเมตร "
            "เมื่อมองจากด้านบนในแนวดิ่ง จะเห็นก้นภาชนะลึกเท่าใด (เซนติเมตร)",
            fmt(apparent),
            # คูณแทนหาร, ตอบความลึกจริง, หรือตอบผลต่างของสองความลึก
            wrongs=slips(fmt(apparent), real * top / bottom, real, real - apparent),
            hint=r"n = \frac{\text{ความลึกจริง}}{\text{ความลึกปรากฏ}}")

    def _critical(self, rng: Random) -> Calc:
        dense, sparse = rng.choice(CRITICAL_PAIRS)
        sine = round(sparse / dense, 4)
        return Calc(
            f"แสงเดินทางอยู่ในตัวกลางที่มีดรรชนีหักเห {_num(dense)} "
            f"และจะออกสู่ตัวกลางที่มีดรรชนีหักเห {_num(sparse)} "
            "ไซน์ของมุมวิกฤตที่รอยต่อนี้มีค่าเท่าใด",
            fmt(sine),
            # กลับเศษกับส่วน, ใช้ผลต่างของดรรชนีหักเห, หรือใช้ผลคูณ
            wrongs=slips(fmt(sine), dense / sparse, dense - sparse, dense * sparse),
            hint=r"\sin\theta_c = \frac{n_2}{n_1}")

    def _snell(self, rng: Random) -> Calc:
        first, sine_in, second = rng.choice(SNELL_SETUPS)
        sine_out = round(first * sine_in / second, 4)
        return Calc(
            f"แสงเดินทางจากตัวกลางที่มีดรรชนีหักเห {_num(first)} "
            f"เข้าสู่ตัวกลางที่มีดรรชนีหักเห {_num(second)} "
            f"ถ้าไซน์ของมุมตกกระทบเท่ากับ {_num(sine_in)} "
            "ไซน์ของมุมหักเหมีค่าเท่าใด",
            fmt(sine_out),
            # ใช้ดรรชนีหักเหกลับด้าน, ลืมหาร, หรือตอบไซน์ของมุมตกกระทบเดิม
            wrongs=slips(fmt(sine_out), second * sine_in / first,
                         first * sine_in, sine_in),
            hint=r"n_1\sin\theta_1 = n_2\sin\theta_2")
