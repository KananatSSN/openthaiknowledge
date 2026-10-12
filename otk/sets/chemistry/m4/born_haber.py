"""พลังงานกับการเกิดสารประกอบไอออนิกและวัฏจักรบอร์น-ฮาเบอร์

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/11

Sets moved here from: science_wave_f21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f21 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_BORN = "พลังงานกับการเกิดสารประกอบไอออนิกและวัฏจักรบอร์น-ฮาเบอร์"


# (metal, halogen, compound): the textbook's order of steps.
BORN_SALTS = (("Na", "Cl", "NaCl"), ("K", "Cl", "KCl"), ("Li", "F", "LiF"), ("Na", "Br", "NaBr"), ("K", "Br", "KBr"),
              ("Na", "F", "NaF"), ("Li", "Cl", "LiCl"), ("K", "I", "KI"))


STEP_FACTS = (
    ("ขั้นการระเหิดโลหะของแข็งเป็นแก๊สอะตอม เป็นกระบวนการแบบใด", "ดูดพลังงาน"),
    ("ขั้นการทำให้อะตอมแก๊สของโลหะกลายเป็นไอออนบวก (พลังงานไอออไนเซชัน) เป็นกระบวนการแบบใด", "ดูดพลังงาน"),
    ("ขั้นการสลายพันธะของแก๊สฮาโลเจนให้เป็นอะตอม เป็นกระบวนการแบบใด", "ดูดพลังงาน"),
    ("ขั้นอะตอมฮาโลเจนรับอิเล็กตรอนเป็นไอออนลบ (สัมพรรคภาพอิเล็กตรอน) เป็นกระบวนการแบบใด", "คายพลังงาน"),
    ("ขั้นไอออนบวกและไอออนลบในสถานะแก๊สรวมกันเป็นผลึก (พลังงานโครงผลึก) เป็นกระบวนการแบบใด", "คายพลังงาน"),
)


def _born_steps(rng: Random) -> dict[str, int]:
    return {"sub": rng.randint(70, 110), "ie": rng.randint(400, 520), "half_d": rng.randint(70, 130),
            "ea": -rng.randint(320, 360), "lattice": -rng.randint(650, 1050)}


def _born_text(s: dict[str, int], hide: str | None = None) -> str:
    labels = (("sub", "พลังงานการระเหิดของโลหะ"), ("ie", "พลังงานไอออไนเซชันของโลหะ"),
              ("half_d", "พลังงานสลายพันธะของฮาโลเจน (ครึ่งโมล)"), ("ea", "พลังงานสัมพรรคภาพอิเล็กตรอน"),
              ("lattice", "พลังงานโครงผลึก (รวมไอออนเป็นผลึก)"))
    return " ".join(f"{text} {'?' if key == hide else f'{s[key]:+d}'} kJ/mol" for key, text in labels)


@question_type(
    "chem.born_haber_foundation",
    display_name={"th": "ขั้นตอนดูดและคายพลังงานในวัฏจักรบอร์น-ฮาเบอร์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BORN,
)
class BornHaberFoundation(QuestionType):
    """Which steps take energy in and which give it out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, halogen, salt = rng.choice(BORN_SALTS)
        stem, right = rng.choice(STEP_FACTS)
        if rng.random() < 0.6:
            return _labelled(stem=f"ในการเกิด {salt} จาก {metal} และ {halogen}₂ {stem}", correct=right,
                             wrongs=("คายพลังงาน" if right == "ดูดพลังงาน" else "ดูดพลังงาน", "ไม่มีการเปลี่ยนพลังงาน",
                                     "ขึ้นกับปริมาณสาร"),
                             topic=TOPIC_BORN, hint="การแยกหรือดึงอิเล็กตรอนออกต้องใช้พลังงาน การรับอิเล็กตรอนของฮาโลเจนและการรวมเป็นผลึกคายพลังงาน")
        order = ("ระเหิดโลหะ", "ทำให้โลหะเป็นไอออนบวก", "สลายพันธะฮาโลเจน", "ฮาโลเจนรับอิเล็กตรอน", "ไอออนรวมกันเป็นผลึก")
        right_text = " → ".join(order)
        wrongs = set()
        while len(wrongs) < 3:
            shuffled = list(order)
            rng.shuffle(shuffled)
            if shuffled != list(order):
                wrongs.add(" → ".join(shuffled))
        return _labelled(stem=f"ลำดับขั้นตอนในวัฏจักรบอร์น-ฮาเบอร์ของการเกิด {salt} ข้อใดถูกต้อง", correct=right_text,
                         wrongs=tuple(sorted(wrongs)), topic=TOPIC_BORN,
                         hint="เริ่มจากทำให้ทั้งสองธาตุเป็นอะตอมแก๊ส แล้วเป็นไอออน สุดท้ายรวมเป็นผลึก")


@question_type(
    "chem.born_haber_fluency",
    display_name={"th": "คำนวณพลังงานของการเกิดสารประกอบไอออนิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BORN,
)
class BornHaberFluency(QuestionType):
    """ΔH of formation is the sum of the five steps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, halogen, salt = rng.choice(BORN_SALTS)
        steps = _born_steps(rng)
        total = sum(steps.values())
        return numeric(
            stem=f"การเกิด {salt} จาก {metal}(s) และ {halogen}₂ มีพลังงานแต่ละขั้น: {_born_text(steps)} พลังงานของการเกิดสารประกอบเท่าใด",
            answer=total, wrongs=[total - 2 * steps["lattice"], total - 2 * steps["ea"], total + steps["half_d"]],
            unit="kJ/mol", topic=TOPIC_BORN, allow_negative=True,
            hint="พลังงานของการเกิดสารประกอบ = ผลรวมพลังงานทุกขั้น (คิดเครื่องหมายด้วย)")


@question_type(
    "chem.born_haber_application",
    display_name={"th": "หาพลังงานโครงผลึกจากวัฏจักรบอร์น-ฮาเบอร์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BORN,
)
class BornHaberApplication(QuestionType):
    """The unknown step is whatever makes the cycle add up to ΔH of formation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, halogen, salt = rng.choice(BORN_SALTS)
        steps = _born_steps(rng)
        total = sum(steps.values())
        hide = rng.choice(("lattice", "ea", "ie"))
        return numeric(
            stem=(f"การเกิด {salt} มีพลังงานของการเกิดสารประกอบ {total:+d} kJ/mol และพลังงานแต่ละขั้น: {_born_text(steps, hide)} "
                  "ค่าที่เป็น ? เท่าใด"),
            answer=steps[hide], wrongs=[-steps[hide], steps[hide] + 2 * total, steps[hide] - steps["sub"]],
            unit="kJ/mol", topic=TOPIC_BORN, allow_negative=True,
            hint="ผลรวมของทุกขั้นเท่ากับพลังงานของการเกิดสารประกอบ ย้ายข้างหาค่าที่ไม่รู้")
