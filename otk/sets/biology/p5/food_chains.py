"""โซ่อาหารและบทบาทของสิ่งมีชีวิต

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.5/3

Sets moved here from: biology, science_pilots.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.biology import SUBJECT, TOPIC_ECOLOGY

PROVENANCE = Provenance("original")


BIOLOGY = "ชีวะ"


ECOLOGY = "สิ่งมีชีวิตกับสิ่งแวดล้อม"


class FoodChain(NamedTuple):
    habitat: str
    producer: str
    primary: str
    secondary: str
    tertiary: str

    @property
    def members(self) -> tuple[str, str, str, str]:
        return self.producer, self.primary, self.secondary, self.tertiary

    @property
    def diagram(self) -> str:
        return " → ".join(self.members)


FOOD_CHAINS = (
    FoodChain("นาข้าว", "ต้นข้าว", "ตั๊กแตน", "กบ", "งู"),
    FoodChain("ทุ่งหญ้า", "หญ้า", "ตั๊กแตน", "กบ", "เหยี่ยว"),
    FoodChain("สวนผลไม้", "ใบไม้", "หนอนผีเสื้อ", "นกกินแมลง", "เหยี่ยว"),
    FoodChain("สระน้ำ", "สาหร่าย", "ลูกน้ำยุง", "ปลาหางนกยูง", "นกยาง"),
    FoodChain("ทะเลเปิด", "แพลงก์ตอนพืช", "แพลงก์ตอนสัตว์", "ปลาขนาดเล็ก", "ปลาทูน่า"),
    FoodChain("ไร่ข้าวโพด", "ต้นข้าวโพด", "หนูนา", "งูเห่า", "เหยี่ยวแดง"),
    FoodChain("ป่าชายเลน", "ใบโกงกาง", "ปูแสม", "ปลากะพง", "นกกระสา"),
    FoodChain("สวนผัก", "ผักกาด", "หนอนกระทู้", "คางคก", "งูสิง"),
)


ROLES = (
    "ผู้ผลิต",
    "ผู้บริโภคลำดับที่ 1",
    "ผู้บริโภคลำดับที่ 2",
    "ผู้บริโภคลำดับที่ 3",
)


def _question(
    *, stem: str, correct: str, wrongs: tuple[str, str, str], hint: str,
) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=ECOLOGY,
        hint=[text(hint)],
    )


@question_type("ecology.feeding",
               display_name={"th": "การจัดกลุ่มสิ่งมีชีวิต (ตามพฤติกรรมการกิน)"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_ECOLOGY)
class FeedingGroups(ClassifyType):
    """แบ่งสัตว์ตามพฤติกรรมการกิน: กินพืช / กินสัตว์ / กินทั้งพืชและสัตว์."""

    CLASSIFY_STEM = "“{member}” จัดอยู่ในกลุ่มใดเมื่อแบ่งตามพฤติกรรมการกิน"
    PICK_STEM = "สัตว์ในข้อใดจัดเป็น{category}"

    CATEGORIES = [
        Category("สัตว์กินพืช (Herbivore)",
                 ("วัว", "ควาย", "ม้า", "ช้าง", "กระต่าย", "กวาง", "ยีราฟ",
                  "แพะ", "แกะ", "ม้าลาย", "หนอนผีเสื้อ", "ตั๊กแตน")),
        Category("สัตว์กินสัตว์ (Carnivore)",
                 ("เสือ", "สิงโต", "งู", "จระเข้", "เหยี่ยว", "หมาป่า",
                  "แมงมุม", "นกฮูก", "ปลาฉลาม", "กบ")),
        Category("สัตว์กินทั้งพืชและสัตว์ (Omnivore)",
                 ("มนุษย์", "หมู", "สุนัข", "ไก่", "เป็ด", "หมี", "ลิง", "กา")),
    ]


@question_type(
    "ecology.food_chain_foundation",
    display_name={"th": "โซ่อาหาร: ระบุผู้ผลิตและผู้บริโภค"},
    level={"th": "ป.5"}, subject=BIOLOGY, topic=ECOLOGY,
)
class FoodChainFoundation(QuestionType):
    """Identify one organism's role in an explicit four-organism food chain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(FOOD_CHAINS)
        role_index = rng.randrange(4)
        return GeneratedQuestion(
            stem=[text(
                f"โซ่อาหารใน{chain.habitat}: {chain.diagram}\n"
                f"สิ่งมีชีวิตใดทำหน้าที่เป็น{ROLES[role_index]}"
            )],
            correct=[text(chain.members[role_index])],
            distractors=label_pool(list(chain.members)),
            topic=self.topic,
            hint=[text(
                "ลูกศรชี้จากสิ่งที่ถูกกินไปยังผู้กิน เริ่มจากผู้ผลิต แล้วนับลำดับผู้บริโภค"
            )],
        )


@question_type(
    "ecology.food_chain_fluency",
    display_name={"th": "โซ่อาหาร: สร้างและอธิบายความสัมพันธ์"},
    level={"th": "ป.5"}, subject=BIOLOGY, topic=ECOLOGY,
)
class FoodChainFluency(QuestionType):
    """Build a chain from feeding facts and predict one direct relationship."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(FOOD_CHAINS)
        which = rng.randrange(5)
        a, b, c, d = chain.members

        if which == 0:
            return _question(
                stem=(
                    f"ใน{chain.habitat} {b}กิน{a}, {c}กิน{b} และ{d}กิน{c} "
                    "ข้อใดเขียนโซ่อาหารได้ถูกต้อง"
                ),
                correct=chain.diagram,
                wrongs=(
                    f"{d} → {c} → {b} → {a}",
                    f"{a} → {c} → {b} → {d}",
                    f"{b} → {a} → {d} → {c}",
                ),
                hint="ลูกศรในโซ่อาหารชี้ตามทิศทางการถ่ายทอดพลังงาน จากสิ่งที่ถูกกินไปยังผู้กิน",
            )
        if which == 1:
            return _question(
                stem=(
                    f"กำหนดโซ่อาหาร {chain.diagram} ถ้า{b}ลดจำนวนลงมาก "
                    "และปัจจัยอื่นคงเดิม แนวโน้มระยะสั้นใดสมเหตุสมผลที่สุด"
                ),
                correct=f"{a}มีแนวโน้มเพิ่มขึ้น และ{c}มีแนวโน้มลดลง",
                wrongs=(
                    f"{a}และ{c}มีแนวโน้มเพิ่มขึ้นทั้งคู่",
                    f"{a}มีแนวโน้มลดลง และ{c}มีแนวโน้มเพิ่มขึ้น",
                    f"{a}และ{c}ไม่เกี่ยวข้องกับการเปลี่ยนแปลงของ{b}",
                ),
                hint="พิจารณาทั้งอาหารของสิ่งมีชีวิตที่ลดลง และผู้บริโภคที่กินสิ่งมีชีวิตนั้น",
            )
        if which == 2:
            return _question(
                stem=(
                    f"กำหนดโซ่อาหาร {chain.diagram} ถ้า{c}ลดจำนวนลงมาก "
                    "และปัจจัยอื่นคงเดิม แนวโน้มระยะสั้นใดสมเหตุสมผลที่สุด"
                ),
                correct=f"{b}มีแนวโน้มเพิ่มขึ้น ทำให้{a}ถูกกินมากขึ้น",
                wrongs=(
                    f"{b}มีแนวโน้มลดลง ทำให้{a}ถูกกินน้อยลง",
                    f"{b}หยุดกิน{a}ทันที เพราะไม่มีผู้ล่าคอยกระตุ้นให้หาอาหาร",
                    f"{a}มีแนวโน้มเพิ่มขึ้น เพราะ{c}ที่ลดลงเคยกิน{a}โดยตรง",
                    f"{a}เปลี่ยนบทบาทเป็นผู้บริโภคลำดับที่ 1 แทน{b}",
                ),
                hint="เมื่อผู้ล่าลดลง เหยื่อของผู้ล่านั้นอาจเพิ่มขึ้นและกินอาหารของมันมากขึ้น",
            )
        if which == 3:
            return _question(
                stem=f"ในโซ่อาหาร {chain.diagram} พลังงานที่{d}ได้รับมีจุดเริ่มต้นจากข้อใด",
                correct=f"พลังงานแสงที่{a}สะสมไว้ แล้วถ่ายทอดผ่าน{b}และ{c}",
                wrongs=(
                    f"พลังงานที่{d}สร้างขึ้นเองโดยไม่รับจากสิ่งมีชีวิตอื่น",
                    f"พลังงานที่{c}สร้างขึ้นเอง แล้วส่งต่อให้{d}โดยไม่ผ่าน{a}",
                    "พลังงานความร้อนที่ไหลย้อนจากผู้บริโภคไปยังผู้ผลิต",
                ),
                hint="ติดตามลูกศรย้อนกลับไปยังผู้ผลิต ซึ่งรับพลังงานเริ่มต้นจากแสง",
            )
        return _question(
            stem=f"ข้อใดระบุบทบาทในโซ่อาหาร {chain.diagram} ได้ถูกต้องครบถ้วน",
            correct=f"{b}เป็นผู้บริโภคลำดับที่ 1, {c}ลำดับที่ 2 และ{d}ลำดับที่ 3",
            # Every choice names three roles, as the answer does; the wrong
            # ones count from the wrong end or start at the producer.
            wrongs=(
                f"{a}เป็นผู้บริโภคลำดับที่ 1, {b}ลำดับที่ 2 และ{c}ลำดับที่ 3",
                f"{d}เป็นผู้บริโภคลำดับที่ 1, {c}ลำดับที่ 2 และ{b}ลำดับที่ 3",
                f"{b}เป็นผู้ผลิต, {c}เป็นผู้บริโภคลำดับที่ 1 และ{d}ลำดับที่ 2",
                f"{b}, {c} และ{d}เป็นผู้บริโภคลำดับที่ 1 เหมือนกันทั้งหมด",
            ),
            hint="เริ่มที่ผู้ผลิต แล้วนับจำนวนขั้นของผู้บริโภคตามทิศลูกศร",
        )


@question_type(
    "ecology.food_chain_application",
    display_name={"th": "โซ่อาหาร: วิเคราะห์หลักฐานการเปลี่ยนแปลง"},
    level={"th": "ป.5"}, subject=BIOLOGY, topic=ECOLOGY,
)
class FoodChainApplication(QuestionType):
    """Use before/after evidence to explain a multi-step trophic cascade."""

    @staticmethod
    def _drop(rng: Random) -> tuple[int, int]:
        before = rng.randrange(80, 141, 10)
        return before, rng.randrange(25, 61, 5)

    @staticmethod
    def _rise(rng: Random) -> tuple[int, int]:
        before = rng.randrange(25, 61, 5)
        return before, rng.randrange(80, 141, 10)

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(FOOD_CHAINS)
        a, b, c, d = chain.members
        which = rng.randrange(4)

        if which == 0:
            b0, b1 = self._drop(rng)
            c0, c1 = self._drop(rng)
            a0, a1 = self._rise(rng)
            return _question(
                stem=(
                    f"โซ่อาหารใน{chain.habitat}: {chain.diagram}\n"
                    f"หลังใช้วิธีควบคุมที่ลด{b}โดยตรง ดัชนีความอุดมสมบูรณ์ก่อน→หลังเป็น "
                    f"{b} {b0}→{b1}, {c} {c0}→{c1}, {a} {a0}→{a1}\n"
                    "ข้อสรุปใดใช้หลักฐานและกลไกของโซ่อาหารได้ดีที่สุด"
                ),
                correct=(
                    f"เมื่อ{b}ลดลง {c}มีอาหารน้อยลงจึงลดลง ส่วน{a}ถูกกินน้อยลงจึงเพิ่มขึ้น"
                ),
                wrongs=(
                    f"เมื่อ{b}ลดลง {c}ย้ายไปกิน{a}แทน จึงลดลงเพราะ{a}ไม่ใช่อาหารที่ดี",
                    f"{a}เพิ่มขึ้นก่อน จึงทำให้{b}ลดลงโดยตรง และ{c}ลดลงตาม{b}",
                    f"{c}ลดลงเพราะถูก{b}ล่า เมื่อ{b}ลดลง {c}จึงจะเพิ่มขึ้นในภายหลัง",
                    "ข้อมูลพิสูจน์ว่าสิ่งมีชีวิตทั้งสามชนิดไม่สัมพันธ์กัน เพราะเปลี่ยนไปคนละทิศทาง",
                ),
                hint="เริ่มจากสิ่งมีชีวิตที่ถูกลดโดยตรง แล้วติดตามผลไปหนึ่งขั้นทั้งสองด้านของมัน",
            )
        if which == 1:
            d0, d1 = self._drop(rng)
            c0, c1 = self._rise(rng)
            b0, b1 = self._drop(rng)
            return _question(
                stem=(
                    f"โซ่อาหารใน{chain.habitat}: {chain.diagram}\n"
                    f"หลัง{d}หายไปจากพื้นที่ส่วนใหญ่ ดัชนีก่อน→หลังเป็น "
                    f"{d} {d0}→{d1}, {c} {c0}→{c1}, {b} {b0}→{b1}\n"
                    "คำอธิบายใดสอดคล้องกับหลักฐานมากที่สุด"
                ),
                correct=f"{d}ลดลงทำให้{c}ถูกล่าน้อยลง; {c}จึงเพิ่มและกิน{b}มากขึ้น",
                wrongs=(
                    f"{d}ลดลงทำให้{c}ขาดอาหาร เพราะ{d}เป็นอาหารของ{c}",
                    f"{b}ลดลงเพราะเปลี่ยนไปเป็น{c} จำนวน{c}จึงเพิ่มขึ้นตาม",
                    "การเปลี่ยนแปลงทั้งสามค่าอธิบายด้วยโซ่อาหารนี้ไม่ได้เลย",
                    f"{c}เพิ่มขึ้นเพราะได้กินซากของ{d} จึงกิน{b}น้อยลงแต่{b}ยังลดลง",
                ),
                hint="ตรวจทิศลูกศรก่อนว่าใครกินใคร แล้วติดตามผลของผู้ล่าที่ลดลงสองขั้น",
            )
        if which == 2:
            a0, a1 = self._drop(rng)
            b0, b1 = self._drop(rng)
            c0, c1 = self._drop(rng)
            return _question(
                stem=(
                    f"โซ่อาหารใน{chain.habitat}: {chain.diagram}\n"
                    f"โรคทำให้{a}ลดลงมาก ดัชนีก่อน→หลังเป็น "
                    f"{a} {a0}→{a1}, {b} {b0}→{b1}, {c} {c0}→{c1}\n"
                    "ข้อใดอธิบายแนวโน้มนี้ได้ครบที่สุด"
                ),
                correct=f"พลังงานเริ่มที่{a}; เมื่อผู้ผลิตลดลง {b}ขาดอาหารและส่งผลต่อเนื่องถึง{c}",
                wrongs=(
                    f"{c}ลดลงเพราะ{c}เป็นผู้ผลิตแทน{a} เมื่อ{a}ป่วยจึงผลิตอาหารไม่ได้",
                    f"{b}และ{c}ลดลงเพราะได้รับพลังงานจากดวงอาทิตย์โดยตรงน้อยลงเท่านั้น",
                    f"{a}ลดลงเพราะ{c}กิน{a}โดยตรง ไม่เกี่ยวกับโรคที่เกิดขึ้น",
                ),
                hint="หาจุดเริ่มต้นของพลังงานในโซ่อาหาร แล้วติดตามผลเมื่อจุดเริ่มต้นลดลง",
            )

        c0, c1 = self._rise(rng)
        b0, b1 = self._drop(rng)
        a0, a1 = self._rise(rng)
        return _question(
            stem=(
                f"โซ่อาหารใน{chain.habitat}: {chain.diagram}\n"
                f"โครงการฟื้นฟูเพิ่มจำนวน{c} ดัชนีก่อน→หลังเป็น "
                f"{c} {c0}→{c1}, {b} {b0}→{b1}, {a} {a0}→{a1}\n"
                "ข้อเสนอใดเชื่อมหลักฐานกับโซ่อาหารได้สมเหตุสมผลที่สุด"
            ),
            correct=f"{c}ที่เพิ่มขึ้นกิน{b}มากขึ้น; เมื่อ{b}ลดลง {a}จึงถูกกินน้อยลงและเพิ่มขึ้น",
            wrongs=(
                f"{a}เพิ่มขึ้นเพราะ{c}ที่เพิ่มขึ้นช่วยผลิตอาหารให้{a}โดยตรง",
                f"{b}ลดลงเพราะเปลี่ยนบทบาทไปเป็นผู้ผลิต จึงไม่ได้กิน{a}อีกต่อไป",
                f"ข้อมูลแสดงว่า{c}สร้างพลังงานให้{a}โดยไม่ผ่าน{b}",
                f"{c}เพิ่มขึ้นทำให้{b}มีอาหารมากขึ้น แต่{b}ลดลงเพราะแย่งอาหารกับ{a}",
            ),
            hint="ใช้เหตุการณ์ที่กำหนดเป็นจุดเริ่ม แล้วตรวจว่าค่าถัดไปเปลี่ยนตามความสัมพันธ์ผู้ล่า–เหยื่อหรือไม่",
        )
