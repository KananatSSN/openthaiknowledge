"""สารโคเวเลนต์โครงร่างตาข่าย

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/19

Sets moved here from: science_wave_f23.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f23 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_NETWORK = "สารโคเวเลนต์โครงร่างตาข่าย"


NETWORK_FACTS = {
    "เพชร": ("คาร์บอนแต่ละอะตอมสร้างพันธะโคเวเลนต์กับคาร์บอนอื่น 4 อะตอมเป็นทรงสี่หน้า",
             "เป็นสารที่แข็งที่สุดในธรรมชาติ และไม่นำไฟฟ้า"),
    "แกรไฟต์": ("เป็นชั้นของคาร์บอนหลายชั้นซ้อนกัน แต่ละชั้นยึดกันด้วยแรงแผ่กระจายลอนดอน",
                "ใช้ทำไส้ดินสอและสารหล่อลื่น เพราะชั้นเลื่อนไถลผ่านกันได้"),
    "แกรฟีน": ("เป็นแผ่นคาร์บอนแผ่นเดียวที่หนาเพียงหนึ่งอะตอม",),
    "ฟูลเลอรีน (C₆₀)": ("เป็นโมเลกุลรูปทรงคล้ายลูกฟุตบอล ไม่ใช่โครงร่างตาข่าย",),
    "ซิลิคอนไดออกไซด์": ("ซิลิคอนแต่ละอะตอมสร้างพันธะกับออกซิเจน 4 อะตอม และออกซิเจนแต่ละอะตอมสร้างพันธะกับซิลิคอน 2 อะตอม",
                         "เป็นองค์ประกอบหลักของทรายและผลึกควอตซ์"),
    "ซิลิคอนคาร์ไบด์": ("มีซิลิคอนและคาร์บอนในอัตราส่วนอะตอม 1 : 1 ต่อกันเป็นโครงร่างตาข่าย",),
    "ซิลิคอน": ("เป็นธาตุกึ่งโลหะที่ใช้ทำชิปคอมพิวเตอร์และเซลล์สุริยะ",),
}


# (substance, bonds per formula unit counted once, what the bond is, formula mass)
NETWORK_BONDS = (("เพชร", 2, "C–C", 12), ("แกรไฟต์", Fraction(3, 2), "C–C", 12), ("ซิลิคอนไดออกไซด์", 4, "Si–O", 60))


NETWORK_USES = (
    ("ทำหัวเจาะและมีดตัดกระจก", "เพชร", {"ซิลิคอนคาร์ไบด์"}),
    ("ทำไส้ดินสอ", "แกรไฟต์", set()),
    ("ทำขั้วไฟฟ้าในเซลล์ไฟฟ้าเคมีราคาถูก", "แกรไฟต์", {"แกรฟีน"}),
    ("ทำชิปคอมพิวเตอร์และเซลล์สุริยะ", "ซิลิคอน", set()),
    ("ทำแก้วและเส้นใยนำแสง", "ซิลิคอนไดออกไซด์", set()),
    ("ทำกระดาษทรายและหินเจียราคาถูก", "ซิลิคอนคาร์ไบด์", {"เพชร"}),
    ("ทำแผ่นวัสดุบางที่สุดที่แข็งแรงและนำไฟฟ้าได้ดี", "แกรฟีน", {"แกรไฟต์"}),
)


NETWORK_REASONS = (
    ("แกรไฟต์นำไฟฟ้าได้เพราะเหตุใด",
     "คาร์บอนแต่ละอะตอมสร้างพันธะ 3 พันธะ อิเล็กตรอนอีก 1 ตัวเคลื่อนที่ได้อิสระ"),
    ("เพชรไม่นำไฟฟ้าเพราะเหตุใด", "คาร์บอนใช้เวเลนซ์อิเล็กตรอนทั้ง 4 ตัวสร้างพันธะ จึงไม่มีอิเล็กตรอนอิสระ"),
    ("แกรไฟต์ลื่นและใช้เป็นสารหล่อลื่นได้เพราะเหตุใด",
     "ชั้นของคาร์บอนยึดกันด้วยแรงแผ่กระจายลอนดอนที่อ่อน จึงเลื่อนไถลผ่านกันได้"),
    ("เพชรและซิลิคอนไดออกไซด์มีจุดหลอมเหลวสูงมากเพราะเหตุใด",
     "การหลอมเหลวต้องสลายพันธะโคเวเลนต์จำนวนมากในโครงร่างตาข่าย"),
    ("CO₂ เป็นแก๊สที่อุณหภูมิห้อง แต่ SiO₂ เป็นของแข็งที่มีจุดหลอมเหลวสูงเพราะเหตุใด",
     "CO₂ เป็นโมเลกุลเดี่ยวที่ยึดกันด้วยแรงอ่อน ส่วน SiO₂ เป็นโครงร่างตาข่ายของพันธะโคเวเลนต์"),
    ("สารโคเวเลนต์โครงร่างตาข่ายส่วนใหญ่ไม่ละลายน้ำเพราะเหตุใด",
     "อะตอมยึดกันด้วยพันธะโคเวเลนต์ทั่วทั้งโครงสร้าง ซึ่งน้ำสลายไม่ได้"),
)


NETWORK_FALSE = ("มีไอออนบวกและไอออนลบที่เคลื่อนที่ได้อย่างอิสระในโครงผลึก", "มีพันธะโลหะและทะเลอิเล็กตรอนที่เคลื่อนที่ได้ทั่วโครงสร้าง",
                 "โมเลกุลยึดกันด้วยพันธะไฮโดรเจนที่แข็งแรงมากระหว่างโมเลกุล", "อะตอมยึดกันด้วยแรงแผ่กระจายลอนดอนเท่านั้น จึงแยกออกจากกันง่าย",
                 "เป็นโมเลกุลขนาดเล็กที่มีขั้ว ซึ่งดึงดูดกันด้วยแรงระหว่างโมเลกุล", "อะตอมยึดกันด้วยพันธะไอออนิกระหว่างไอออนบวกและไอออนลบ")


@question_type(
    "chem.network_covalent_foundation",
    display_name={"th": "โครงสร้างและสมบัติของสารโคเวเลนต์โครงร่างตาข่าย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NETWORK,
)
class NetworkCovalentFoundation(QuestionType):
    """Match each network solid to its structure or a property."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "เพชร: C ต่อ 4 อะตอม แกรไฟต์: ชั้นของ C ต่อ 3 อะตอม SiO₂: Si ต่อ O 4 อะตอม ฟูลเลอรีนเป็นโมเลกุลเดี่ยว"
        substance = rng.choice(sorted(NETWORK_FACTS))
        fact = rng.choice(NETWORK_FACTS[substance])
        others = sorted(set(NETWORK_FACTS) - {substance})
        if rng.random() < 0.5:
            other_facts = [f for s in others for f in NETWORK_FACTS[s]]
            return _labelled(stem=f"ข้อใดกล่าวถึง{substance}ได้ถูกต้อง", correct=fact,
                             wrongs=tuple(other_facts), topic=TOPIC_NETWORK, hint=hint)
        return _labelled(stem=f"\"{fact}\" เป็นลักษณะของสารใด", correct=substance,
                         wrongs=tuple(others), topic=TOPIC_NETWORK, hint=hint)


@question_type(
    "chem.network_covalent_fluency",
    display_name={"th": "นับพันธะในโครงร่างตาข่าย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NETWORK,
)
class NetworkCovalentFluency(QuestionType):
    """Each bond joins two atoms, so bonds per atom = neighbours ÷ 2 (4 Si–O per Si in SiO₂)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        substance, per, bond, mass = rng.choice(NETWORK_BONDS)
        unit_word = "หน่วยสูตร SiO₂" if bond == "Si–O" else "อะตอมคาร์บอน"
        wrongs = {"เพชร": [4, 1, 3], "แกรไฟต์": [3, 1, 2], "ซิลิคอนไดออกไซด์": [2, 8, 1]}[substance]
        hint = ("เพชร: C ต่อ 4 อะตอม แต่ละพันธะใช้ร่วมกัน 2 อะตอม จึงมี 2 พันธะต่อ C "
                "แกรไฟต์: 3 ÷ 2 = 1.5 พันธะต่อ C  SiO₂: Si หนึ่งอะตอมมีพันธะ Si–O 4 พันธะ")
        if rng.random() < 0.5:
            moles = rng.choice([Fraction(n, 4) for n in range(1, 25) if (per * Fraction(n, 4) * 100).denominator == 1])
            return numeric(stem=f"{substance}ที่มี{unit_word} {show(moles)} โมล มีพันธะ {bond} ทั้งหมดกี่โมล",
                           answer=per * moles, wrongs=[w * moles for w in wrongs], unit="โมล", topic=TOPIC_NETWORK,
                           hint=hint)
        # Masses that give a bond count exact to two places.
        grams = rng.choice([g for g in range(3, 241, 3) if (Fraction(g, mass) * per * 100).denominator == 1])
        return numeric(stem=f"{substance}หนัก {grams} กรัม มีพันธะ {bond} ทั้งหมดกี่โมล "
                            f"({'มวลอะตอม C' if mass == 12 else 'มวลสูตร SiO₂'} = {mass})",
                       answer=Fraction(grams, mass) * per, wrongs=[Fraction(grams, mass) * w for w in wrongs],
                       unit="โมล", topic=TOPIC_NETWORK, hint=hint)


@question_type(
    "chem.network_covalent_application",
    display_name={"th": "อธิบายสมบัติและการใช้ประโยชน์ของสารโคเวเลนต์โครงร่างตาข่าย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NETWORK,
)
class NetworkCovalentApplication(QuestionType):
    """Structure explains the property, and the property picks the use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right = rng.choice(NETWORK_REASONS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(NETWORK_FALSE), topic=TOPIC_NETWORK,
                             hint="สมบัติของสารโครงร่างตาข่ายมาจากพันธะโคเวเลนต์ที่ต่อกันทั้งโครงสร้าง "
                                  "และจากว่าเวเลนซ์อิเล็กตรอนถูกใช้สร้างพันธะหมดหรือไม่")
        use, right, also = rng.choice(NETWORK_USES)
        pool = sorted(set(NETWORK_FACTS) - {right} - also)
        return _labelled(stem=f"สารใดเหมาะนำมา{use}", correct=right, wrongs=tuple(pool),
                         topic=TOPIC_NETWORK, hint="เลือกจากสมบัติ: แข็งมาก นำไฟฟ้า ลื่น เป็นสารกึ่งตัวนำ หรือโปร่งใส")
