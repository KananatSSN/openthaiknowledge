"""สมดุลเคมีในสิ่งมีชีวิต ธรรมชาติ และอุตสาหกรรม

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/13

Sets moved here from: science_wave_f35.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f35 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LIFE = "สมดุลเคมีในสิ่งมีชีวิต ธรรมชาติ และอุตสาหกรรม"


RIGHT, LEFT = "เลื่อนไปทางขวา", "เลื่อนไปทางซ้าย"


# (setting, equilibrium, what changes, which way it shifts, what follows)
CASES = (
    ("ขึ้นไปบนภูเขาสูงที่มีแก๊สออกซิเจนน้อย", "Hb(aq) + O₂(aq) ⇌ HbO₂(aq)", "O₂ ลดลง", LEFT,
     "HbO₂ ลดลง ร่างกายได้ออกซิเจนน้อยลงจึงเหนื่อยง่าย"),
    ("สูดดมแก๊ส CO จากไอเสียรถยนต์ในห้องปิด", "Hb(aq) + O₂(aq) ⇌ HbO₂(aq)", "CO จับกับ Hb แทน ทำให้ Hb อิสระลดลง", LEFT,
     "HbO₂ ลดลง เนื้อเยื่อขาดออกซิเจน"),
    ("หายใจเร็วและลึกเกินไปจนขับ CO₂ ออกมาก", "CO₂(aq) + H₂O(l) ⇌ H₂CO₃(aq) ⇌ H⁺(aq) + HCO₃⁻(aq)",
     "CO₂ ในเลือดลดลง", LEFT, "H⁺ ในเลือดลดลง เลือดเป็นเบสมากขึ้น"),
    ("น้ำที่มีแก๊ส CO₂ ละลายหยดลงในถ้ำแล้ว CO₂ ระเหยออกไป", "CaCO₃(s) + CO₂(aq) + H₂O(l) ⇌ Ca²⁺(aq) + 2HCO₃⁻(aq)",
     "CO₂ ลดลง", LEFT, "CaCO₃ ตกตะกอนสะสมเป็นหินงอกหินย้อย"),
    ("น้ำฝนที่มี CO₂ ละลายไหลผ่านหินปูน", "CaCO₃(s) + CO₂(aq) + H₂O(l) ⇌ Ca²⁺(aq) + 2HCO₃⁻(aq)",
     "CO₂ เพิ่มขึ้น", RIGHT, "หินปูนละลายกลายเป็นถ้ำ"),
    ("เปิดฝาขวดน้ำอัดลม", "CO₂(g) ⇌ CO₂(aq)", "ความดันของแก๊สเหนือของเหลวลดลง", LEFT,
     "CO₂ ออกจากสารละลายเกิดฟองแก๊ส"),
    ("ทานอาหารรสหวานและเปรี้ยวบ่อย จนในปากมีกรดมาก",
     "Ca₅(PO₄)₃OH(s) ⇌ 5Ca²⁺(aq) + 3PO₄³⁻(aq) + OH⁻(aq)", "กรดทำปฏิกิริยากับ OH⁻ ทำให้ OH⁻ ลดลง", RIGHT,
     "สารเคลือบฟันละลาย ฟันผุง่ายขึ้น"),
    ("มหาสมุทรดูดซับ CO₂ จากอากาศมากขึ้น", "CO₂(aq) + H₂O(l) ⇌ H₂CO₃(aq) ⇌ H⁺(aq) + HCO₃⁻(aq)", "CO₂ เพิ่มขึ้น", RIGHT,
     "H⁺ เพิ่มขึ้น น้ำทะเลเป็นกรดมากขึ้นและกัดกร่อนเปลือกหอยและปะการัง"),
)


INDUSTRY = (
    ("กระบวนการฮาเบอร์ N₂(g) + 3H₂(g) ⇌ 2NH₃(g) ΔH < 0 ใช้ความดันสูงประมาณ 200 atm เพราะเหตุใด",
     "สมดุลเลื่อนไปทางที่มีจำนวนโมลแก๊สน้อยกว่า ได้ NH₃ มากขึ้น",
     ("ทำให้ค่า K เพิ่มขึ้น จึงได้ NH₃ มากขึ้น", "ทำให้ปฏิกิริยาดูดความร้อนเกิดได้ดีขึ้นที่ความดันสูงมาก", "เพื่อลดพลังงานก่อกัมมันต์ให้ปฏิกิริยาเกิดเร็วขึ้น")),
    ("กระบวนการฮาเบอร์ใช้อุณหภูมิประมาณ 450 °C แม้ว่าอุณหภูมิต่ำจะให้ NH₃ ที่สมดุลมากกว่า เพราะเหตุใด",
     "อุณหภูมิต่ำทำให้ปฏิกิริยาช้ามาก จึงเลือกอุณหภูมิที่ได้ผลผลิตพอเหมาะในเวลาไม่นาน",
     ("อุณหภูมิสูงทำให้สมดุลเลื่อนไปทาง NH₃ จึงได้ผลผลิตมากที่สุด", "อุณหภูมิสูงทำให้ค่า K เพิ่มขึ้น จึงได้ NH₃ มากที่สุด", "ตัวเร่งปฏิกิริยาทำงานเฉพาะที่ 450 °C เท่านั้น จึงใช้อุณหภูมิอื่นไม่ได้")),
    ("กระบวนการฮาเบอร์ใช้เหล็กเป็นตัวเร่งปฏิกิริยาเพื่ออะไร", "ให้ปฏิกิริยาเข้าสู่สมดุลเร็วขึ้น โดยไม่เปลี่ยนตำแหน่งสมดุล",
     ("ให้ได้ NH₃ ที่สมดุลมากขึ้นโดยเลื่อนสมดุลไปทางขวา", "ให้ค่า K เพิ่มขึ้น จึงได้ผลผลิตมากขึ้น", "ให้ปฏิกิริยากลายเป็นดูดความร้อนจึงเกิดได้เร็วขึ้น")),
    ("กระบวนการฮาเบอร์ทำให้ NH₃ กลายเป็นของเหลวแยกออกจากระบบตลอดเวลาเพื่ออะไร",
     "ให้สมดุลเลื่อนไปทางขวาเพื่อสร้าง NH₃ เพิ่ม", ("ให้ค่า K เพิ่มขึ้น จึงได้ผลผลิตมากขึ้น", "ลดความดันในระบบให้สมดุลเลื่อนไปทางซ้าย", "ทำให้ปฏิกิริยาหยุดเพื่อเก็บ NH₃ ไว้")),
    ("กระบวนการสัมผัส 2SO₂(g) + O₂(g) ⇌ 2SO₃(g) ΔH < 0 ใช้อากาศมากเกินพอเพื่ออะไร",
     "เพิ่มความเข้มข้นของ O₂ ให้สมดุลเลื่อนไปทางขวา ได้ SO₃ มากขึ้น",
     ("เพื่อลดอุณหภูมิของระบบให้ปฏิกิริยาคายความร้อนเกิดดีขึ้น", "เพื่อให้ค่า K เพิ่มขึ้น จึงได้ SO₃ มากขึ้น", "เพื่อเจือจาง SO₃ ไม่ให้สมดุลเลื่อนกลับทางซ้าย")),
    ("กระบวนการสัมผัสใช้ V₂O₅ เพื่ออะไร", "เป็นตัวเร่งปฏิกิริยาให้เข้าสู่สมดุลเร็วขึ้น",
     ("เพิ่มปริมาณ SO₃ ที่สมดุลโดยเลื่อนสมดุลไปทางขวา", "ดูดซับ SO₃ ออกจากระบบให้สมดุลเลื่อนไปทางขวา", "เพิ่มความดันของระบบให้ได้ SO₃ มากขึ้น")),
)


@question_type(
    "chem.equilibrium_life_foundation",
    display_name={"th": "สมดุลเคมีที่เกี่ยวข้องกับปรากฏการณ์ในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LIFE,
)
class EquilibriumLifeFoundation(QuestionType):
    """Name the equilibrium behind a familiar effect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        setting, equilibrium, _, _, result = rng.choice(CASES)
        others = sorted({c[1] for c in CASES if c[1] != equilibrium})
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{setting}\" เกี่ยวข้องกับสมดุลใด", correct=equilibrium,
                             wrongs=tuple(others), topic=TOPIC_LIFE,
                             hint="ดูว่าสารที่เปลี่ยนไปในสถานการณ์นี้ปรากฏในสมการสมดุลใด")
        results = [c[4] for c in CASES if c[4] != result]
        return _labelled(stem=f"สมดุล {equilibrium}: เมื่อ{setting} จะเกิดผลอย่างไร", correct=result,
                         wrongs=tuple(results), topic=TOPIC_LIFE,
                         hint="หาว่าสารใดเพิ่มหรือลด แล้วใช้หลักของเลอชาเตอลิเอหาทิศทางและผลที่ตามมา")


@question_type(
    "chem.equilibrium_life_fluency",
    display_name={"th": "ทิศทางการเลื่อนของสมดุลในสิ่งมีชีวิตและธรรมชาติ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LIFE,
)
class EquilibriumLifeFluency(QuestionType):
    """The change, the shift, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        setting, equilibrium, change, direction, _ = rng.choice(CASES)
        other = LEFT if direction == RIGHT else RIGHT
        if rng.random() < 0.6:
            right = f"{change} สมดุล{direction}"
            pool = {f"{c[2]} สมดุล{d}" for c in CASES for d in (RIGHT, LEFT)} - {right}
            return _labelled(stem=f"สมดุล {equilibrium} เมื่อ{setting} เกิดการเปลี่ยนแปลงใด", correct=right,
                             wrongs=(f"{change} สมดุล{other}", *rng.sample(sorted(pool - {f'{change} สมดุล{other}'}), 2)),
                             topic=TOPIC_LIFE,
                             hint="ระบุก่อนว่าสารใดในสมการเพิ่มหรือลด แล้วหาทิศทางการเลื่อนของสมดุล")
        return _labelled(stem=f"สมดุล {equilibrium} เมื่อ{setting} ({change}) สมดุลจะเลื่อนไปทางใด",
                         correct=f"{direction} เพื่อลดผลของการเปลี่ยนแปลง",
                         wrongs=(f"{other} เพื่อลดผลของการเปลี่ยนแปลง", "ไม่เลื่อน เพราะค่า K คงที่",
                                 "ไม่เลื่อน เพราะเป็นระบบในร่างกายหรือธรรมชาติ"),
                         topic=TOPIC_LIFE, hint="สารฝั่งใดลดลง สมดุลเลื่อนไปสร้างสารฝั่งนั้น สารฝั่งใดเพิ่ม สมดุลเลื่อนไปใช้สารฝั่งนั้น")


@question_type(
    "chem.equilibrium_life_application",
    display_name={"th": "สมดุลเคมีในกระบวนการอุตสาหกรรม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LIFE,
)
class EquilibriumLifeApplication(QuestionType):
    """Why the Haber and contact processes run as they do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(INDUSTRY)
        wrongs = tuple(wrongs)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_LIFE,
                         hint="ภาวะในอุตสาหกรรมต้องคุ้มทั้งปริมาณผลิตภัณฑ์ที่สมดุล (เลอชาเตอลิเอ) และความเร็ว (อัตรา)")

# More items: these tables held six or fewer, so a learner met them all in
# a few tries. Each added item has wrong readings of its own.
INDUSTRY = (*INDUSTRY,
    ('กระบวนการฮาเบอร์ เมื่อเพิ่มความเข้มข้นของ H₂ ในระบบที่อยู่ในสมดุล ผลที่ได้คือข้อใด',
     'สมดุลเลื่อนไปทางขวา ได้ NH₃ มากขึ้น โดยค่า K คงเดิม',
     ('ค่า K เพิ่มขึ้น จึงได้ NH₃ มากขึ้นตามไปด้วย', 'สมดุลเลื่อนไปทางซ้าย NH₃ สลายตัวเป็น N₂ และ H₂', 'ไม่มีผลใด ๆ เพราะ H₂ ไม่เกี่ยวกับตำแหน่งสมดุล')),
    ('กระบวนการสัมผัส ถ้าเพิ่มอุณหภูมิของระบบที่อยู่ในสมดุล ปริมาณ SO₃ จะเป็นอย่างไร',
     'ลดลง เพราะสมดุลของปฏิกิริยาคายความร้อนเลื่อนไปทางซ้าย',
     ('เพิ่มขึ้น เพราะอุณหภูมิสูงทำให้สมดุลเลื่อนไปทางขวาเสมอ', 'เท่าเดิม เพราะอุณหภูมิไม่มีผลต่อสมดุลเคมีใด ๆ', 'เพิ่มขึ้น เพราะค่า K ของปฏิกิริยาคายความร้อนเพิ่มขึ้น')),
)
