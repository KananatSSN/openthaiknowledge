"""การเลือกวัสดุและการนำวัสดุกลับมาใช้ใหม่

เคมี · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.2/3

Sets moved here from: science_wave_d2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SECOND, SUBJECT

PROVENANCE = Provenance("original")


CHOOSING_TOPIC = "การเลือกวัสดุและการนำวัสดุกลับมาใช้ใหม่"


class Purpose(NamedTuple):
    """An object to make, the test that matters, and each material's result."""
    make: str
    test: str
    results: tuple[tuple[str, str], ...]
    best: str
    need: str


PURPOSES = (
    Purpose("หมวกกันฝน", "หยดน้ำลงบนวัสดุแล้วดูว่าน้ำซึมผ่านหรือไม่",
            (("ถุงพลาสติก", "น้ำไม่ซึมผ่าน"), ("ผ้าฝ้าย", "น้ำซึมผ่าน"), ("กระดาษ", "น้ำซึมผ่านและขาดยุ่ย")),
            "ถุงพลาสติก", "น้ำไม่ซึมผ่าน"),
    Purpose("หนังสติ๊ก", "ดึงวัสดุแล้วปล่อย ดูว่ายืดและหดกลับหรือไม่",
            (("ยางวง", "ยืดออกและหดกลับ"), ("เชือกฟาง", "ไม่ยืด"), ("เส้นลวด", "ไม่ยืดและงอค้าง")),
            "ยางวง", "ยืดออกและหดกลับ"),
    Purpose("หน้าต่างบ้านตุ๊กตาที่มองเห็นข้างในได้", "ส่องไฟฉายผ่านวัสดุแล้วดูว่ามองผ่านได้หรือไม่",
            (("แผ่นพลาสติกใส", "มองผ่านได้ชัดเจน"), ("กระดาษแข็ง", "มองผ่านไม่ได้"), ("ไม้อัด", "มองผ่านไม่ได้")),
            "แผ่นพลาสติกใส", "มองผ่านได้ชัดเจน"),
    Purpose("ผ้าเช็ดแว่นตา", "ถูวัสดุบนแผ่นกระจกแล้วดูว่าเกิดรอยขีดข่วนหรือไม่",
            (("ผ้านุ่ม", "ไม่เกิดรอย"), ("กระดาษทราย", "เกิดรอยมาก"), ("ฟองน้ำด้านสาก", "เกิดรอยเล็กน้อย")),
            "ผ้านุ่ม", "ไม่เกิดรอย"),
    Purpose("สายผูกว่าวที่ไม่ขาดง่าย", "แขวนถุงทรายไว้ที่ปลายวัสดุแล้วดูว่าขาดหรือไม่",
            (("เชือกไนลอน", "ไม่ขาด"), ("ด้ายเย็บผ้าเส้นเดียว", "ขาดทันที"), ("กระดาษม้วนเป็นเส้น", "ขาดและยุ่ย")),
            "เชือกไนลอน", "ไม่ขาด"),
    Purpose("ที่เช็ดมือในห้องน้ำ", "จุ่มวัสดุขนาดเท่ากันลงในน้ำแล้วดูว่าซับน้ำได้มากเพียงใด",
            (("ผ้าขนหนู", "ซับน้ำได้มาก"), ("แผ่นพลาสติก", "ไม่ซับน้ำ"), ("อะลูมิเนียมฟอยล์", "ไม่ซับน้ำ")),
            "ผ้าขนหนู", "ซับน้ำได้มาก"),
)


class Reuse(NamedTuple):
    """A used material, what is observed of it, a new use that fits, and other uses it could also serve."""
    used: str
    observed: str
    new_use: str
    defensible: frozenset[str] = frozenset()


POT, BOX, STRAP, CLOTH, PENCILS, WRAP, COUNTERS = (
    "กระถางปลูกต้นไม้", "กล่องเก็บของเล่น", "สายรัดของท้ายรถ", "ผ้าเช็ดโต๊ะ",
    "กระบอกใส่ดินสอ", "กระดาษห่อของขวัญ", "ตัวนับเลขในชั้นเรียน",
)


# ``defensible`` lists the other uses this material could reasonably serve too,
# so they are never offered as wrong: a tin can makes a fine plant pot.
REUSES = (
    Reuse("ขวดน้ำพลาสติกที่ใช้แล้ว", "น้ำไม่ซึมผ่าน และตัดให้เป็นรูปทรงต่าง ๆ ได้", POT,
          frozenset({PENCILS, BOX})),
    Reuse("กล่องกระดาษที่ใช้แล้ว", "แข็งพอที่จะตั้งเป็นรูปทรงได้ และพับได้", BOX,
          frozenset({PENCILS, WRAP})),
    Reuse("ยางในรถจักรยานที่ขาดแล้ว", "ดึงแล้วยืดออกและหดกลับได้", STRAP),
    Reuse("เสื้อยืดเก่า", "นุ่ม และซับน้ำได้ดี", CLOTH, frozenset({POT, STRAP, WRAP})),
    Reuse("กระป๋องโลหะที่ใช้แล้ว", "แข็ง ตั้งได้มั่นคง", PENCILS, frozenset({POT, BOX})),
    Reuse("หนังสือพิมพ์เก่า", "บาง พับและห่อหุ้มสิ่งของได้", WRAP, frozenset({CLOTH, PENCILS})),
    Reuse("ฝาขวดพลาสติกที่ใช้แล้ว", "ชิ้นเล็ก มีหลายสี หยิบนับและจัดกลุ่มได้ง่าย", COUNTERS),
)


CHOOSING_SCENARIOS = (
    ("นักเรียนจะทำกระเป๋าใส่ของที่ใช้ได้นานหลายครั้ง ระหว่างถุงกระดาษ กับถุงผ้า ควรเลือกแบบใด",
     "ถุงผ้า เพราะเหนียว พับเก็บได้ และไม่ฉีกขาดง่ายเหมือนถุงกระดาษ",
     ("ถุงกระดาษ เพราะฉีกขาดได้ง่ายจึงทิ้งได้สะดวก",
      "ถุงกระดาษ เพราะเมื่อเปียกน้ำจะแข็งแรงขึ้น",
      "เลือกแบบใดก็ได้ เพราะใช้ได้นานเท่ากัน",
      "ถุงผ้า เพราะใสมองผ่านได้",
      "ถุงกระดาษ เพราะยืดและหดกลับได้")),
    ("นักเรียนต้องการทำที่ใส่ดินสอจากวัสดุที่ใช้แล้ว ตัวเลือกใดเหมาะสมที่สุด",
     "ตัดขวดพลาสติกที่ใช้แล้วให้สั้นลง เพราะตั้งได้และใส่ดินสอได้หลายแท่ง",
     ("ใช้ถุงพลาสติกบาง ๆ เพราะตั้งเองได้มั่นคง",
      "ใช้กระดาษทิชชูที่ใช้แล้ว เพราะแข็งแรงที่สุด",
      "ใช้ลูกโป่งที่แตกแล้ว เพราะแข็งและตั้งได้",
      "ใช้กระดาษหนังสือพิมพ์แผ่นเดียวม้วนหลวม ๆ",
      "ใช้ฟองน้ำที่เปียกน้ำ")),
    ("นักเรียนทดสอบวัสดุสามชนิดเพื่อทำร่มให้ตุ๊กตา แต่หยดน้ำลงบนวัสดุแต่ละชนิดในปริมาณไม่เท่ากัน ควรปรับการทดสอบอย่างไร",
     "หยดน้ำปริมาณเท่ากันลงบนวัสดุขนาดเท่ากัน เพื่อให้เปรียบเทียบผลได้ยุติธรรม",
     ("ทดสอบวัสดุเพียงชนิดเดียวก็พอ",
      "ไม่ต้องใช้น้ำ ให้ดูสีของวัสดุแทน",
      "หยดน้ำมากที่สุดบนวัสดุที่คิดว่าดีที่สุด",
      "ทดสอบวัสดุแต่ละชนิดคนละวันโดยไม่สนใจปริมาณน้ำ",
      "ให้เพื่อนเดาว่าวัสดุใดกันน้ำได้")),
    ("นักเรียนจะทำป้ายชื่อที่ใช้กลางแจ้งและโดนฝนบ่อย ระหว่างกระดาษแข็งกับแผ่นพลาสติก ควรเลือกแบบใด",
     "แผ่นพลาสติก เพราะน้ำไม่ซึมผ่าน จึงไม่เปื่อยเมื่อโดนฝน",
     ("กระดาษแข็ง เพราะซับน้ำฝนได้ดี",
      "กระดาษแข็ง เพราะเปื่อยง่ายจึงทิ้งได้สะดวก",
      "เลือกแบบใดก็ได้ เพราะโดนฝนเหมือนกัน",
      "แผ่นพลาสติก เพราะฉีกขาดง่าย",
      "กระดาษแข็ง เพราะใสมองผ่านได้")),
    ("ข้อใดเป็นการนำวัสดุที่ใช้แล้วมาทำของใหม่ได้เหมาะสมกับสมบัติของวัสดุ",
     "นำยางในรถจักรยานที่ขาดมาตัดเป็นสายรัดของ เพราะยืดและหดกลับได้",
     ("นำกระดาษทิชชูที่ใช้แล้วมาทำร่ม",
      "นำถุงพลาสติกบาง ๆ มาทำขาเก้าอี้",
      "นำเปลือกไข่มาทำสายรัดของ",
      "นำหนังสือพิมพ์เก่ามาทำแก้วใส่น้ำ",
      "นำลูกโป่งที่แตกมาทำกล่องใส่ของหนัก")),
)


@question_type(
    "chem.material_choice_foundation",
    display_name={"th": "เปรียบเทียบสมบัติของวัสดุเพื่อเลือกทำวัตถุตามวัตถุประสงค์"},
    level=SECOND, subject=SUBJECT, topic=CHOOSING_TOPIC,
)
class MaterialChoiceFoundation(QuestionType):
    """Test results for three materials; choose one for a purpose, comparing all three."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        purpose = rng.choice(PURPOSES)
        results = list(purpose.results)
        rng.shuffle(results)
        record = " / ".join(f"{name}: {result}" for name, result in results)
        others = [name for name, _ in purpose.results if name != purpose.best]
        result_of = dict(purpose.results)
        return _labelled(
            stem=(f"นักเรียนจะทำ{purpose.make} จึงทดสอบโดย{purpose.test} ได้ผลดังนี้ — {record} "
                  "ควรเลือกวัสดุใด เพราะเหตุใด"),
            correct=f"{purpose.best} เพราะ{purpose.need} ต่างจาก{others[0]}และ{others[1]}",
            wrongs=(f"{others[0]} เพราะ{result_of[others[0]]} ต่างจาก{purpose.best}และ{others[1]}",
                    f"{others[1]} เพราะ{result_of[others[1]]} ต่างจาก{purpose.best}และ{others[0]}",
                    f"เลือกวัสดุใดก็ได้ เพราะทั้งสามชนิด{purpose.need}เหมือนกัน",
                    f"{purpose.best} เพราะมีราคาถูกที่สุด โดยไม่ต้องดูผลการทดสอบ"),
            hint="ถามก่อนว่าวัตถุนี้ต้องการสมบัติใด แล้วหาวัสดุที่ผลการทดสอบแสดงสมบัตินั้น",
            topic=CHOOSING_TOPIC,
        )


@question_type(
    "chem.material_choice_fluency",
    display_name={"th": "อธิบายการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่จากสมบัติที่สังเกตได้"},
    level=SECOND, subject=SUBJECT, topic=CHOOSING_TOPIC,
)
class MaterialChoiceFluency(QuestionType):
    """A used material and what is observed of it; the reuse its properties suit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reuse = rng.choice(REUSES)
        others = [other for other in REUSES
                  if other.new_use != reuse.new_use and other.new_use not in reuse.defensible]
        return _labelled(
            stem=(f"นักเรียนสังเกต{reuse.used} พบว่า{reuse.observed} "
                  f"จากหลักฐานนี้ ข้อใดอธิบายการนำ{reuse.used}กลับมาใช้ใหม่ได้เหมาะสมที่สุด"),
            correct=f"ทำเป็น{reuse.new_use} เพราะ{reuse.observed}",
            wrongs=tuple(f"ทำเป็น{other.new_use} เพราะ{other.observed}" for other in rng.sample(others, 3)),
            hint="ใช้สมบัติที่สังเกตได้ของวัสดุที่ใช้แล้ว เลือกของใหม่ที่ต้องการสมบัตินั้น",
            topic=CHOOSING_TOPIC,
        )


@question_type(
    "chem.material_choice_application",
    display_name={"th": "เลือกและนำวัสดุกลับมาใช้ใหม่ในสถานการณ์จริง"},
    level=SECOND, subject=SUBJECT, topic=CHOOSING_TOPIC,
)
class MaterialChoiceApplication(QuestionType):
    """A lasting shopping bag, a pencil holder from waste, and a fair test."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CHOOSING_SCENARIOS,
            hint="จับคู่สมบัติของวัสดุกับสิ่งที่งานนั้นต้องการ และให้การทดสอบเปรียบเทียบได้ยุติธรรม",
        ), CHOOSING_TOPIC)
