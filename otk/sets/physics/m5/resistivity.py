"""สภาพต้านทานและความต้านทานของลวด

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/8

Sets moved here from: electricity, science_wave_a6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.electricity import LEVEL, SUBJECT, TOPIC
from otk.sets._support.science_wave_a6 import LEVEL as LEVEL_science_wave_a6

PROVENANCE = Provenance("original")


# (ρ ×10⁻⁶ Ω·m, L₁ m, A₁ ×10⁻⁶ m², L₂ m, A₂ ×10⁻⁶ m²). Only the wires are
# listed; both resistances, their series sum and their parallel equivalent are
# computed from them, so no stated number can drift from the geometry. The rows
# are chosen so all four of those values are whole, and R₁ ≠ R₂ — equal wires
# would let a learner halve R₁ without ever combining anything.
WIRE_PAIRS = (
    (2, 2, 1, 6, 1),
    (2, 3, 1, 3, 2),
    (2, 6, 1, 8, 4),
    (2, 10, 1, 10, 4),
    (3, 1, 1, 2, 1),
    (3, 2, 1, 10, 1),
    (4, 1, 1, 3, 1),
    (4, 3, 2, 6, 2),
    (5, 1, 1, 4, 1),
    (5, 2, 1, 3, 1),
    (6, 1, 1, 2, 1),
    (8, 1, 1, 3, 1),
    # Wave H: more unequal pairs, each still whole in series and in parallel.
    (10, 2, 1, 3, 1),
    (2, 3, 1, 6, 1),
    (8, 2, 1, 6, 1),
    (3, 5, 1, 10, 1),
    (3, 3, 1, 6, 1),
    (6, 2, 1, 4, 1),
    (2, 5, 1, 20, 1),
    (6, 1, 1, 5, 1),
    (4, 3, 1, 9, 1),
    (4, 2, 1, 6, 1),
    (7, 1, 1, 6, 1),
)


RHO_UNIT = "×10⁻⁶ โอห์ม·เมตร"


AREA_UNIT = "×10⁻⁶ ตารางเมตร"


def wire_resistance(rho: int, length: int, area: int) -> int:
    """R = ρL/A, in whole โอห์ม for every row of :data:`WIRE_PAIRS`."""
    return rho * length // area


def _wire_text(index: int, length: int, area: int) -> str:
    return (f"เส้นที่ {index} ยาว {length} เมตร พื้นที่หน้าตัด {area}{AREA_UNIT}")


@question_type("elec.resistance_factors",
               display_name={"th": "สิ่งที่มีผลต่อความต้านทานของลวดตัวนำ"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class ResistanceFactors(ClassifyType):
    """จาก R = ρL/A: ยาวขึ้นหรือวัสดุต้านทานสูงขึ้น → R เพิ่ม, หน้าตัดโตขึ้น → R ลด.

    หมวด "เท่าเดิม" คือหัวใจของเรื่อง — ความต้านทานขึ้นกับตัวลวดเท่านั้น ไม่ได้ขึ้นกับ
    ความต่างศักย์หรือกระแสที่จ่ายให้มัน ซึ่งเป็นความเข้าใจผิดที่พบบ่อยที่สุด.
    """

    CLASSIFY_STEM = "ถ้า “{member}” ความต้านทานของลวดจะเปลี่ยนไปอย่างไร"
    PICK_STEM = "การกระทำในข้อใดทำให้{category}"

    CATEGORIES = [
        Category("ความต้านทานของลวดเพิ่มขึ้น",
                 ("เปลี่ยนไปใช้ลวดชนิดเดียวกันที่ยาวเป็น 2 เท่าของเดิม",
                  "เปลี่ยนไปใช้ลวดที่ทำจากวัสดุซึ่งมีสภาพต้านทานสูงกว่าเดิม",
                  "รีดลวดเส้นเดิมให้เล็กลงจนพื้นที่หน้าตัดเหลือครึ่งหนึ่ง",
                  "นำลวดเส้นเดิมอีกหนึ่งเส้นมาต่ออนุกรมกับเส้นเดิม")),
        Category("ความต้านทานของลวดลดลง",
                 ("ตัดลวดเส้นเดิมออกจนเหลือความยาวครึ่งหนึ่ง",
                  "เปลี่ยนไปใช้ลวดชนิดเดียวกันที่หนาขึ้นจนพื้นที่หน้าตัดเป็น 2 เท่า",
                  "เปลี่ยนไปใช้ลวดที่ทำจากวัสดุซึ่งมีสภาพต้านทานต่ำกว่าเดิม",
                  "นำลวดเส้นเดิมอีกหนึ่งเส้นมาต่อขนานกับเส้นเดิม")),
        Category("ความต้านทานของลวดเท่าเดิม",
                 ("เพิ่มความต่างศักย์ที่ปลายลวดเป็น 2 เท่าโดยยังใช้ลวดเส้นเดิมและอุณหภูมิคงที่",
                  "ลดความต่างศักย์และกระแสไฟฟ้าผ่านลวดเส้นเดิมลงในสัดส่วนเดียวกันโดยอุณหภูมิคงที่",
                  "สลับปลายทั้งสองของลวดเส้นเดิมที่ต่อเข้ากับแหล่งจ่ายไฟ")),
    ]


@question_type("elec.resistivity",
               display_name={"th": "ความต้านทานของลวดตัวนำ (R = ρL/A)"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class Resistivity(PhysCalc):
    """R = ρL/A — ถามหา R, หา ρ และหา L.

    ทั้ง ρ และ A ให้เป็นตัวคูณของ 10⁻⁶ ในหน่วยของมันเอง ตัวเลข 10⁻⁶ จึงตัดกันหมด
    และคำตอบเป็นจำนวนเต็มโอห์ม โดยที่รูปสมการยังเป็นสูตรจริงตามชีท.
    """

    # (ρ ×10⁻⁶ Ω·m, L เมตร, A ×10⁻⁶ m²) เลือกให้ ρL/A ลงตัว
    _WIRES = [(2, 4, 2), (5, 2, 1), (4, 3, 2), (3, 4, 6), (8, 5, 2), (6, 4, 8),
              (2, 9, 3), (5, 8, 4), (9, 2, 3), (4, 6, 8), (7, 4, 2), (2, 6, 4)]
    _RHO = "×10⁻⁶ โอห์ม·เมตร"
    _AREA = "×10⁻⁶ ตารางเมตร"

    def draw(self, rng: Random) -> Calc:
        a, ell, b = rng.choice(self._WIRES)
        r = a * ell // b
        which = rng.random()
        if which < 0.5:                      # ให้ ρ, L, A → หา R
            return Calc(
                f"ลวดตัวนำมีสภาพต้านทาน {a}{self._RHO} ยาว {ell} เมตร "
                f"พื้นที่หน้าตัด {b}{self._AREA} จงหาความต้านทานของลวด (โอห์ม)",
                fmt(r), wrongs=slips(fmt(r), a * ell, a * ell * b, b * ell),
                hint=r"R = \frac{\rho L}{A}")
        if which < 0.75:                     # ให้ R, L, A → หา ρ
            return Calc(
                f"ลวดตัวนำยาว {ell} เมตร พื้นที่หน้าตัด {b}{self._AREA} "
                f"วัดความต้านทานได้ {r} โอห์ม จงหาสภาพต้านทานของวัสดุ ({self._RHO})",
                fmt(a), wrongs=slips(fmt(a), r * b, r * ell / b, r / ell),
                hint=r"\rho = \frac{RA}{L}")
        return Calc(                         # ให้ R, ρ, A → หา L
            f"ลวดตัวนำมีสภาพต้านทาน {a}{self._RHO} พื้นที่หน้าตัด {b}{self._AREA} "
            f"ความต้านทาน {r} โอห์ม จงหาความยาวของลวด (เมตร)",
            fmt(ell), wrongs=slips(fmt(ell), r * b, r * a / b, r / a),
            hint=r"L = \frac{RA}{\rho}")


@question_type("elec.resistance_ratio",
               display_name={"th": "การเปลี่ยนความยาวและพื้นที่หน้าตัดของลวด"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class ResistanceRatio(PhysCalc):
    """R เป็นกี่เท่าของเดิม เมื่อ L และ A เปลี่ยนไป — R = ρL/A ในเชิงสัดส่วน.

    ไม่มีหน่วยเข้ามาเกี่ยวข้อง จึงวัดความเข้าใจว่า R แปรผันตรงกับ L และแปรผกผันกับ A
    ล้วน ๆ ตัวลวงคือการสลับทิศของการแปรผัน (คูณ A แทนที่จะหาร).
    """

    # (ตัวคูณความยาว, ตัวคูณพื้นที่หน้าตัด). When the area *grows* the answer is a
    # ratio, so those pairs are listed by hand — only ones giving a clean value,
    # and never 1, which would make "กี่เท่า" a trick question rather than a test.
    _GROW = [(2, 4), (3, 2), (3, 4), (4, 2)]
    _SHRINK = [(lf, af) for lf in (2, 3, 4) for af in (2, 4)]

    def draw(self, rng: Random) -> Calc:
        if rng.random() < 0.5:               # พื้นที่หน้าตัดโตขึ้น → R ลดลง
            lf, af = rng.choice(self._GROW)
            ans, area = lf / af, f"พื้นที่หน้าตัดเป็น {af} เท่าของเดิม"
            other = lf * af
        else:                                # พื้นที่หน้าตัดเล็กลง → R เพิ่มขึ้น
            lf, af = rng.choice(self._SHRINK)
            ans, area = lf * af, f"พื้นที่หน้าตัดเหลือ 1 ใน {af} ของเดิม"
            other = lf / af
        return Calc(
            f"ลวดชนิดเดิมเส้นใหม่ยาวเป็น {lf} เท่าของเดิม และมี{area} "
            f"ความต้านทานของเส้นใหม่เป็นกี่เท่าของเดิม",
            fmt(ans), wrongs=slips(fmt(ans), other, lf, af),
            hint=r"R \propto \frac{L}{A}")


@question_type(
    "elec.resistance_network_application",
    display_name={"th": "ความต้านทานสมมูลของลวดตัวนำสองเส้น"},
    level=LEVEL_science_wave_a6, subject=SUBJECT, topic=TOPIC,
)
class ResistanceNetworkApplication(PhysCalc):
    """Find each wire's resistance from its geometry, then combine the two.

    ``ม.5/8`` asks for R = ρL/A *and* for the equivalent resistance of resistors
    in series and in parallel. `elec.resistivity` covers the first half and
    `elec.resistance_ratio` the proportionality; nothing until now made a learner
    do both in one item, which is the whole difficulty of the outcome.
    """

    def draw(self, rng: Random) -> Calc:
        rho, l1, a1, l2, a2 = rng.choice(WIRE_PAIRS)
        r1 = wire_resistance(rho, l1, a1)
        r2 = wire_resistance(rho, l2, a2)
        wires = (f"ลวดโลหะชนิดเดียวกันสองเส้นมีสภาพต้านทาน {rho}{RHO_UNIT} "
                 f"{_wire_text(1, l1, a1)} และ{_wire_text(2, l2, a2)} ")
        if rng.random() < 0.5:
            total = r1 + r2
            return Calc(
                wires + "นำลวดทั้งสองเส้นมาต่ออนุกรมกัน จงหาความต้านทานสมมูล (โอห์ม)",
                fmt(total),
                # The classic slips: use the parallel rule by mistake, combine the
                # geometry instead of the resistances, or answer with one wire.
                wrongs=slips(fmt(total), r1 * r2 / total, r1 * r2, max(r1, r2)),
                hint=r"R = \frac{\rho L}{A},\ R_{\text{อนุกรม}} = R_1 + R_2")
        total = r1 * r2 // (r1 + r2)
        return Calc(
            wires + "นำลวดทั้งสองเส้นมาต่อขนานกัน จงหาความต้านทานสมมูล (โอห์ม)",
            fmt(total),
            wrongs=slips(fmt(total), r1 + r2, r1 * r2, min(r1, r2)),
            hint=r"R = \frac{\rho L}{A},\ \frac{1}{R_{\text{ขนาน}}} "
                 r"= \frac{1}{R_1} + \frac{1}{R_2}")
