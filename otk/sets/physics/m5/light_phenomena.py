"""ปรากฏการณ์ธรรมชาติที่เกี่ยวกับแสง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/12

Sets moved here from: science_wave_f9.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f9 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SKY = "ปรากฏการณ์ธรรมชาติที่เกี่ยวกับแสง"


PHENOMENA = (
    ("รุ้ง", "แสงหักเห กระจาย และสะท้อนกลับหมดในหยดน้ำ"),
    ("การทรงกลด", "แสงหักเหผ่านผลึกน้ำแข็งในเมฆชั้นสูง"),
    ("มิราจ", "แสงหักเหผ่านชั้นอากาศที่มีอุณหภูมิต่างกันจนสะท้อนกลับหมด"),
    ("ท้องฟ้าเป็นสีฟ้าตอนกลางวัน", "อนุภาคในอากาศกระเจิงแสงความยาวคลื่นสั้นได้มากกว่า"),
    ("ท้องฟ้าเป็นสีแดงส้มตอนเย็น", "แสงผ่านอากาศเป็นระยะทางยาว แสงสีน้ำเงินถูกกระเจิงออกไปก่อน"),
    ("เมฆเป็นสีขาว", "หยดน้ำในเมฆกระเจิงแสงทุกความยาวคลื่นพอ ๆ กัน"),
    ("เพชรเป็นประกายแวววาว", "แสงสะท้อนกลับหมดหลายครั้งภายในเพชรที่มีมุมวิกฤตเล็ก"),
)


SITUATIONS = (
    ("หลังฝนตก หันหลังให้ดวงอาทิตย์แล้วเห็นแถบสีโค้งบนท้องฟ้า", "รุ้ง"),
    ("เห็นวงแสงสีจาง ๆ ล้อมรอบดวงอาทิตย์ในวันที่มีเมฆบางสีขาวลอยสูง", "การทรงกลด"),
    ("ขับรถกลางแดดจัด เห็นถนนข้างหน้าเหมือนมีน้ำนองสะท้อนภาพรถคันหน้า", "มิราจ"),
    ("นักเดินทางในทะเลทรายเห็นเหมือนมีแอ่งน้ำอยู่ไกล ๆ แต่ไปถึงแล้วไม่มี", "มิราจ"),
    ("มองท้องฟ้าเวลาเที่ยงวันที่อากาศแจ่มใส เห็นเป็นสีฟ้า", "ท้องฟ้าเป็นสีฟ้าตอนกลางวัน"),
    ("มองดวงอาทิตย์ขณะตกดิน เห็นท้องฟ้าบริเวณนั้นเป็นสีแดงส้ม", "ท้องฟ้าเป็นสีแดงส้มตอนเย็น"),
    ("เห็นแถบสีเหมือนรุ้งในละอองน้ำจากน้ำตก เมื่อยืนหันหลังให้ดวงอาทิตย์", "รุ้ง"),
    ("เห็นวงแสงล้อมรอบดวงจันทร์ในคืนที่มีเมฆซีร์รัสบาง ๆ", "การทรงกลด"),
)


SKY_CONDITIONS = (
    ("จะเห็นรุ้งได้ ผู้สังเกตต้องอยู่ตำแหน่งใดเทียบกับดวงอาทิตย์", "หันหลังให้ดวงอาทิตย์ โดยมีละอองน้ำอยู่ด้านหน้า",
     ("หันหน้าเข้าหาดวงอาทิตย์", "ดวงอาทิตย์อยู่เหนือศีรษะพอดี", "อยู่ในที่ร่มที่ไม่มีแสง")),
    ("ในรุ้งปฐมภูมิ แสงสีใดอยู่ขอบนอกสุดของแถบโค้ง", "แสงสีแดง",
     ("แสงสีม่วง", "แสงสีเขียว", "แสงสีเหลือง")),
    ("มิราจบนถนนเกิดได้ง่ายในวันแบบใด", "วันที่แดดจัด อากาศใกล้ถนนร้อนกว่าอากาศด้านบนมาก",
     ("วันที่ฝนตกหนักและถนนเปียกทั้งสาย", "คืนที่อากาศเย็นและมีหมอกลงจัด", "วันที่อุณหภูมิอากาศเท่ากันทุกระดับความสูงเหนือถนน")),
    ("ถ้าโลกไม่มีบรรยากาศ ท้องฟ้าตอนกลางวันจะเป็นสีใด", "สีดำ เพราะไม่มีอนุภาคกระเจิงแสง",
     ("สีฟ้าเข้มกว่าเดิม เพราะใกล้ดวงอาทิตย์", "สีขาว", "สีแดงส้ม เพราะแสงเดินทางผ่านอากาศไกล")),
    ("แสงสีใดถูกอนุภาคในอากาศกระเจิงได้มากที่สุด", "แสงสีน้ำเงิน ซึ่งมีความยาวคลื่นสั้น",
     ("แสงสีแดง ซึ่งมีความยาวคลื่นยาว", "แสงสีเหลือง", "ทุกสีถูกกระเจิงเท่ากัน")),
    ("การทรงกลดมักเห็นเมื่อใด", "เมื่อมีเมฆชั้นสูงที่ประกอบด้วยผลึกน้ำแข็ง",
     ("เมื่อฝนกำลังตกหนักและมีลมแรง", "เมื่อท้องฟ้าไม่มีเมฆเลยและอากาศแห้งมาก", "เมื่อดวงอาทิตย์อยู่ใต้ขอบฟ้าแล้ว")),
)


@question_type(
    "phys.light_phenomena_foundation",
    display_name={"th": "สาเหตุของรุ้ง การทรงกลด มิราจ และสีของท้องฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SKY,
)
class LightPhenomenaFoundation(QuestionType):
    """Each phenomenon and the behaviour of light behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(PHENOMENA, 4)
        name, cause = chosen[0]
        if rng.random() < 0.5:
            return _labelled(stem=f"ปรากฏการณ์ \"{name}\" เกิดจากข้อใด", correct=cause,
                             wrongs=tuple(c for _, c in chosen[1:]), topic=TOPIC_SKY,
                             hint="รุ้ง ทรงกลด และมิราจเกิดจากการหักเห สีของท้องฟ้าเกิดจากการกระเจิงของแสง")
        return _labelled(stem=f"ปรากฏการณ์ใดเกิดจาก{cause}", correct=name,
                         wrongs=tuple(n for n, _ in chosen[1:]), topic=TOPIC_SKY,
                         hint="รุ้ง ทรงกลด และมิราจเกิดจากการหักเห สีของท้องฟ้าเกิดจากการกระเจิงของแสง")


@question_type(
    "phys.light_phenomena_fluency",
    display_name={"th": "ระบุปรากฏการณ์ของแสงจากสิ่งที่สังเกตเห็น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SKY,
)
class LightPhenomenaFluency(QuestionType):
    """A scene described; name the phenomenon."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        scene, name = rng.choice(SITUATIONS)
        others = [n for n, _ in PHENOMENA if n != name]
        return _labelled(stem=f"{scene} เป็นปรากฏการณ์ใด", correct=name, wrongs=tuple(others),
                         topic=TOPIC_SKY, hint="นึกถึงตำแหน่งของดวงอาทิตย์ สิ่งที่แสงผ่าน (หยดน้ำ ผลึกน้ำแข็ง อากาศร้อน) และสีที่เห็น")


@question_type(
    "phys.light_phenomena_application",
    display_name={"th": "เงื่อนไขการเกิดปรากฏการณ์ของแสงในธรรมชาติ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SKY,
)
class LightPhenomenaApplication(QuestionType):
    """When and where each can be seen, and what would change without air."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.35:
            stem, correct, wrongs = rng.choice(SKY_CONDITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SKY,
                             hint="แสงความยาวคลื่นสั้นกระเจิงมาก รุ้งต้องมีดวงอาทิตย์อยู่ด้านหลังผู้สังเกต")
        if shape < 0.75:
            # The primary bow sits 42° from the point opposite the Sun, so its top is 42° − the Sun's altitude.
            sun = rng.randint(0, 41) if rng.random() < 0.8 else rng.randint(45, 60)
            if sun > 42:
                return _labelled(
                    stem=(f"ดวงอาทิตย์อยู่สูงจากขอบฟ้า {sun}° ผู้สังเกตบนพื้นราบจะเห็นรุ้งปฐมภูมิหรือไม่ "
                          "(รุ้งปฐมภูมิทำมุม 42° กับแนวที่ตรงข้ามกับดวงอาทิตย์)"),
                    correct="ไม่เห็น รุ้งอยู่ใต้ขอบฟ้า",
                    wrongs=(f"เห็น ยอดรุ้งสูง {sun - 42}°", f"เห็น ยอดรุ้งสูง {sun + 42}°", "เห็น ยอดรุ้งสูง 42°"),
                    topic=TOPIC_SKY, hint="ยอดรุ้งสูง 42° ลบด้วยมุมเงยของดวงอาทิตย์ ถ้าได้ค่าไม่เกินศูนย์รุ้งจะอยู่ใต้ขอบฟ้า")
            return numeric(
                stem=(f"ดวงอาทิตย์อยู่สูงจากขอบฟ้า {sun}° ยอดของรุ้งปฐมภูมิที่ผู้สังเกตบนพื้นราบเห็นจะสูงจากขอบฟ้ากี่องศา "
                      "(รุ้งปฐมภูมิทำมุม 42° กับแนวที่ตรงข้ามกับดวงอาทิตย์)"),
                answer=42 - sun, wrongs=[42 + sun, 42, abs(sun - 21) + 1], unit="องศา", topic=TOPIC_SKY,
                hint="จุดตรงข้ามดวงอาทิตย์อยู่ใต้ขอบฟ้าเท่ากับมุมเงยของดวงอาทิตย์ ยอดรุ้งจึงสูง 42° − มุมเงยของดวงอาทิตย์")
        # Rayleigh scattering goes as 1/λ⁴: compare two wavelengths.
        k = rng.choice((2, 3))
        short = rng.choice((200, 250, 300, 350, 400, 450) if k == 2 else (150, 200, 250))
        long_ = short * k
        return numeric(
            stem=(f"การกระเจิงของแสงโดยโมเลกุลอากาศแปรผกผันกับความยาวคลื่นยกกำลังสี่ แสงความยาวคลื่น {short} nm "
                  f"ถูกกระเจิงมากกว่าแสงความยาวคลื่น {long_} nm กี่เท่า"),
            answer=k ** 4, wrongs=[k, k * k, k ** 3], unit="เท่า", topic=TOPIC_SKY,
            hint="ความยาวคลื่นสั้นลง k เท่า การกระเจิงเพิ่มเป็น k⁴ เท่า")
