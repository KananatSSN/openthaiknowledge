"""หินและการใช้ประโยชน์

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/9

Sets moved here from: science_wave_f76.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f76 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_ROCK = "หินและการใช้ประโยชน์"


ROCKS = (
    ("หินแกรนิต", "หินอัคนีแทรกซอน", "เนื้อหยาบ เห็นผลึกแร่ควอตซ์ เฟลด์สปาร์ และไมกาชัดเจน", "ทำหินปูพื้นและท็อปโต๊ะ"),
    ("หินบะซอลต์", "หินอัคนีพุ", "สีเข้ม เนื้อละเอียด อาจมีรูพรุน", "ทำหินโรยทางรถไฟและเป็นแหล่งพลอยในบางพื้นที่"),
    ("หินพัมมิซ", "หินอัคนีพุ", "มีรูพรุนมากจนลอยน้ำได้", "ใช้ขัดผิวและขัดภาชนะ"),
    ("หินออบซิเดียน", "หินอัคนีพุ", "เนื้อเป็นแก้ว สีดำ แตกเป็นรูปก้นหอย", "ใช้ทำเครื่องมือมีคมในสมัยโบราณ"),
    ("หินทราย", "หินตะกอน", "เนื้อเป็นเม็ดทรายยึดติดกัน", "ใช้ก่อสร้างและแกะสลัก"),
    ("หินดินดาน", "หินตะกอน", "เนื้อละเอียดมาก แยกเป็นแผ่นบาง ๆ ได้", "เป็นวัตถุดิบทำอิฐและเครื่องปั้นดินเผา"),
    ("หินปูน", "หินตะกอน", "ทำปฏิกิริยากับกรดเจือจางเกิดฟองแก๊ส อาจพบซากดึกดำบรรพ์", "ใช้ทำปูนซีเมนต์"),
    ("หินกรวดมน", "หินตะกอน", "มีกรวดกลมมนขนาดต่าง ๆ ยึดติดกันด้วยตะกอนละเอียด", "ใช้ตกแต่งสวนและอาคาร"),
    ("หินอ่อน", "หินแปร", "แปรสภาพจากหินปูน ทำปฏิกิริยากับกรดเจือจางเกิดฟองแก๊ส", "ใช้ทำรูปปั้นและปูพื้น"),
    ("หินชนวน", "หินแปร", "แปรสภาพจากหินดินดาน แยกเป็นแผ่นเรียบได้ดี", "ใช้ทำกระเบื้องมุงหลังคาและกระดานชนวน"),
    ("หินควอร์ตไซต์", "หินแปร", "แปรสภาพจากหินทราย แข็งมาก", "ใช้ทำวัสดุทนการสึกกร่อน"),
    ("หินไนส์", "หินแปร", "มีแถบแร่สีอ่อนสลับสีเข้มเป็นริ้ว", "ใช้เป็นหินประดับและหินก่อสร้าง"),
)


PARENTS = (("หินปูน", "หินอ่อน"), ("หินดินดาน", "หินชนวน"), ("หินทราย", "หินควอร์ตไซต์"), ("หินแกรนิต", "หินไนส์"))


ROCK_HINT = ("หินอัคนีเกิดจากแมกมาเย็นตัว แทรกซอนเนื้อหยาบ พุเนื้อละเอียดหรือมีรูพรุน หินตะกอนเกิดจากตะกอนอัดตัว "
             "หินแปรเกิดจากหินเดิมถูกความร้อนและความดัน เช่น หินปูน → หินอ่อน หินดินดาน → หินชนวน")


@question_type(
    "geo.rock_id_foundation",
    display_name={"th": "ประเภทของหินและการใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ROCK,
)
class RockIdFoundation(QuestionType):
    """Igneous, sedimentary or metamorphic; and what each rock is used for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, kind, _, use = rng.choice(ROCKS)
        roll = rng.random()
        if roll < 0.45:
            kinds = ("หินอัคนีแทรกซอน", "หินอัคนีพุ", "หินตะกอน", "หินแปร")
            return _labelled(stem=f"{name}จัดเป็นหินประเภทใด", correct=kind, wrongs=tuple(k for k in kinds if k != kind), topic=TOPIC_ROCK, hint=ROCK_HINT)
        others = rng.sample([r for r in ROCKS if r[0] != name], 3)
        if roll < 0.75:
            return _labelled(stem=f"{name}ใช้ประโยชน์อย่างไร", correct=use, wrongs=tuple(r[3] for r in others), topic=TOPIC_ROCK, hint=ROCK_HINT)
        return _labelled(stem=f"หินใด{use}", correct=name, wrongs=tuple(r[0] for r in others), topic=TOPIC_ROCK, hint=ROCK_HINT)


@question_type(
    "geo.rock_id_fluency",
    display_name={"th": "ระบุชื่อหินจากลักษณะที่สังเกตได้"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ROCK,
)
class RockIdFluency(QuestionType):
    """Name the rock from what the specimen shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, looks, _ = rng.choice(ROCKS)
        # A lookalike with the same kind makes the better distractor.
        others = rng.sample([r[0] for r in ROCKS if r[0] != name], 3)
        return _labelled(stem=f"ตัวอย่างหินมีลักษณะ \"{looks}\" น่าจะเป็นหินใด", correct=name, wrongs=tuple(others), topic=TOPIC_ROCK, hint=ROCK_HINT)


@question_type(
    "geo.rock_id_application",
    display_name={"th": "หินต้นกำเนิดของหินแปรและการจำแนกหิน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ROCK,
)
class RockIdApplication(QuestionType):
    """Which rock a metamorphic rock came from, and sorting a set."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        parent, meta = rng.choice(PARENTS)
        if rng.random() < 0.5:
            others = [p for p, _ in PARENTS if p != parent] + ["หินบะซอลต์"]
            return _labelled(stem=f"{meta}แปรสภาพมาจากหินใด", correct=parent, wrongs=tuple(others), topic=TOPIC_ROCK, hint=ROCK_HINT)
        others = [m for _, m in PARENTS if m != meta] + ["หินพัมมิซ"]
        return _labelled(stem=f"เมื่อ{parent}ได้รับความร้อนและความดันสูงจะแปรสภาพเป็นหินใด", correct=meta, wrongs=tuple(others),
                         topic=TOPIC_ROCK, hint=ROCK_HINT)
