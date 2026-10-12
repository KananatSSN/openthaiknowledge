"""พันธะโลหะและสมบัติของโลหะ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/20

Sets moved here from: science_wave_f23.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f23 import SUBJECT, UPPER_FOUR, _order_choices

PROVENANCE = Provenance("original")


TOPIC_METAL = "พันธะโลหะและสมบัติของโลหะ"


METAL_REASONS = (
    ("พันธะโลหะเกิดจากอะไร", "แรงดึงดูดระหว่างไอออนบวกของโลหะกับเวเลนซ์อิเล็กตรอนที่เคลื่อนที่อิสระ"),
    ("โลหะนำไฟฟ้าได้ดีเพราะเหตุใด", "เวเลนซ์อิเล็กตรอนเคลื่อนที่ได้อย่างอิสระทั่วทั้งก้อนโลหะ"),
    ("โลหะนำความร้อนได้ดีเพราะเหตุใด", "อิเล็กตรอนอิสระรับพลังงานแล้วถ่ายโอนต่อกันได้อย่างรวดเร็ว"),
    ("โลหะตีแผ่เป็นแผ่นบางหรือดึงเป็นเส้นได้เพราะเหตุใด", "ไอออนบวกเลื่อนไถลผ่านกันได้ โดยยังมีทะเลอิเล็กตรอนยึดไว้"),
    ("ผิวโลหะมันวาวเพราะเหตุใด", "อิเล็กตรอนอิสระรับแสงที่ตกกระทบแล้วปล่อยแสงกลับออกมา"),
    ("โลหะส่วนใหญ่มีจุดหลอมเหลวสูงเพราะเหตุใด", "ไอออนบวกกับทะเลอิเล็กตรอนดึงดูดกันแข็งแรงทั่วทั้งก้อนโลหะ"),
)


METAL_FALSE = ("ไอออนบวกและไอออนลบเคลื่อนที่ได้อย่างอิสระทั่วทั้งก้อนโลหะ",
               "อะตอมโลหะใช้อิเล็กตรอนร่วมกันเป็นคู่ระหว่างสองอะตอม เกิดเป็นโมเลกุลแยกกัน",
               "อะตอมโลหะยึดกันด้วยพันธะไฮโดรเจนระหว่างอะตอมที่อยู่ติดกัน",
               "นิวเคลียสของโลหะเคลื่อนที่ได้อย่างอิสระ ส่วนอิเล็กตรอนอยู่กับที่",
               "โปรตอนเคลื่อนที่ไปทั่วก้อนโลหะแล้วถ่ายโอนพลังงานต่อกัน",
               "ไอออนบวกผลักกันจนแยกออกเป็นชั้นที่ไม่ยึดติดกัน")


# symbol: (Thai name, valence electrons, molar mass, melting point °C)
METALS = {
    "Li": ("ลิเทียม", 1, 7, 181), "Na": ("โซเดียม", 1, 23, 98), "K": ("โพแทสเซียม", 1, 39, 63),
    "Rb": ("รูบิเดียม", 1, 85, 39), "Cs": ("ซีเซียม", 1, 133, 28), "Be": ("เบริลเลียม", 2, 9, 1287),
    "Mg": ("แมกนีเซียม", 2, 24, 650), "Ca": ("แคลเซียม", 2, 40, 842), "Al": ("อะลูมิเนียม", 3, 27, 660),
}


# Each chain rises in melting point: down group 1 the ions grow; along a period the charge grows.
METAL_CHAINS = (("Cs", "Rb", "K", "Na", "Li"), ("Na", "Mg", "Al"), ("K", "Na", "Mg", "Al"), ("Rb", "K", "Ca"),
                ("Li", "Be"))


METAL_USES = (
    ("สายไฟฟ้าในบ้าน", "ทองแดง", "นำไฟฟ้าได้ดีและดึงเป็นเส้นได้"),
    ("กระดาษห่ออาหาร (ฟอยล์)", "อะลูมิเนียม", "ตีแผ่เป็นแผ่นบางได้และเบา"),
    ("ไส้หลอดไฟแบบไส้", "ทังสเตน", "มีจุดหลอมเหลวสูงมาก"),
    ("เครื่องประดับ", "ทองคำ", "มันวาวและไม่ทำปฏิกิริยากับอากาศ"),
    ("เทอร์มอมิเตอร์แบบดั้งเดิม", "ปรอท", "เป็นของเหลวที่อุณหภูมิห้องและขยายตัวสม่ำเสมอ"),
)


def metal_pairs():
    return sorted({(a, b) for chain in METAL_CHAINS for a, b in combinations(chain, 2)})


@question_type(
    "chem.metallic_bond_foundation",
    display_name={"th": "การเกิดพันธะโลหะและสมบัติของโลหะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METAL,
)
class MetallicBondFoundation(QuestionType):
    """Positive ions in a sea of free valence electrons explain each property."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right = rng.choice(METAL_REASONS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(METAL_FALSE), topic=TOPIC_METAL,
                         hint="อะตอมโลหะปล่อยเวเลนซ์อิเล็กตรอนออกมาเป็นทะเลอิเล็กตรอนที่เคลื่อนที่ได้ทั่วก้อน "
                              "ล้อมรอบไอออนบวกที่เรียงชิดกัน")


@question_type(
    "chem.metallic_bond_fluency",
    display_name={"th": "เวเลนซ์อิเล็กตรอนในทะเลอิเล็กตรอนและจุดหลอมเหลวของโลหะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METAL,
)
class MetallicBondFluency(QuestionType):
    """Count the electrons each atom gives to the sea, or compare two melting points."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            symbol = rng.choice(sorted(METALS))
            name, valence, mass, _ = METALS[symbol]
            moles = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, Fraction(5, 2), 3, 4, Fraction(1, 4)))
            if rng.random() < 0.5:
                amount = f"{show(moles)} โมล"
            else:
                amount = f"{show(moles * mass)} กรัม (มวลอะตอม {symbol} = {mass})"
            return numeric(stem=f"โลหะ{name} ({symbol}) {amount} ปล่อยเวเลนซ์อิเล็กตรอนเข้าสู่ทะเลอิเล็กตรอนได้กี่โมล",
                           answer=moles * valence, wrongs=[moles, moles * (valence + 1), moles * 8], unit="โมล",
                           topic=TOPIC_METAL,
                           hint="แต่ละอะตอมปล่อยอิเล็กตรอนเท่ากับจำนวนเวเลนซ์อิเล็กตรอน (หมู่ 1 = 1 หมู่ 2 = 2 Al = 3)")
        low, high = rng.choice(metal_pairs())
        pair = [low, high]
        rng.shuffle(pair)
        label = lambda s: f"{METALS[s][0]} ({s})"
        return _labelled(stem=f"{label(pair[0])} กับ {label(pair[1])} โลหะใดมีจุดหลอมเหลวสูงกว่า", correct=label(high),
                         wrongs=(label(low), "มีจุดหลอมเหลวเท่ากัน", "บอกไม่ได้เพราะเป็นโลหะทั้งคู่"), topic=TOPIC_METAL,
                         hint="พันธะโลหะแข็งแรงขึ้นเมื่อจำนวนเวเลนซ์อิเล็กตรอนมากขึ้นและไอออนเล็กลง "
                              "(ในหมู่ 1 จากบนลงล่างจุดหลอมเหลวลดลง)")


@question_type(
    "chem.metallic_bond_application",
    display_name={"th": "เรียงความแข็งแรงของพันธะโลหะและเลือกโลหะตามการใช้งาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_METAL,
)
class MetallicBondApplication(QuestionType):
    """Order three metals by melting point, or match a metal to a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            chain = rng.choice([c for c in METAL_CHAINS if len(c) >= 3])
            trio = tuple(reversed(sorted(rng.sample(chain, 3), key=chain.index)))
            shown = rng.sample(trio, 3)
            right, wrongs = _order_choices(rng, trio)
            return _labelled(stem=f"เรียงจุดหลอมเหลวของ {', '.join(shown)} จากสูงไปต่ำ", correct=right, wrongs=wrongs,
                             topic=TOPIC_METAL,
                             hint="ตามคาบ เวเลนซ์อิเล็กตรอนมากขึ้น พันธะโลหะแข็งแรงขึ้น "
                                  "ตามหมู่ 1 จากบนลงล่าง ไอออนใหญ่ขึ้น พันธะอ่อนลง")
        use, metal, why = rng.choice(METAL_USES)
        others = [u for u in METAL_USES if u[1] != metal]
        return _labelled(stem=f"ควรเลือกโลหะใดทำ{use} เพราะเหตุใด", correct=f"{metal} เพราะ{why}",
                         wrongs=tuple(f"{u[1]} เพราะ{u[2]}" for u in rng.sample(others, 3)), topic=TOPIC_METAL,
                         hint="เลือกสมบัติของโลหะที่งานนั้นต้องการที่สุด")
