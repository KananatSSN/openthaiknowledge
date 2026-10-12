"""ซากดึกดำบรรพ์

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/3

Sets moved here from: science_wave_c14.
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
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c14 import FOSSIL_SCENARIOS

PROVENANCE = Provenance("original")


FOSSIL_TOPIC = "ซากดึกดำบรรพ์"


class Model(NamedTuple):
    """A classroom model, the kind of fossil it explains, and how that fossil forms."""
    activity: str
    fossil: str
    forms: str


MODELS = (
    Model("กดเปลือกหอยลงบนดินน้ำมันแล้วยกออก เหลือรอยบุ๋มเป็นรูปเปลือกหอย",
          "รอยพิมพ์",
          "ซากถูกตะกอนทับถม แล้วซากผุพังหายไป เหลือเพียงรอยประทับของรูปร่างไว้ในหิน"),
    Model("เทปูนปลาสเตอร์ลงในรอยบุ๋มบนดินน้ำมัน รอให้แข็งแล้วแกะออก ได้ชิ้นที่มีรูปร่างเหมือนเปลือกหอย",
          "รูปหล่อ",
          "แร่ในน้ำใต้ดินเข้าไปเติมเต็มช่องว่างที่ซากทิ้งไว้ในหิน แล้วแข็งตัวเป็นรูปร่างของซาก"),
    Model("หยดเทียนหลอมเหลวลงบนแมลงพลาสติก รอให้แข็งจนแมลงถูกหุ้มอยู่ภายในทั้งตัว",
          "ซากในอำพัน",
          "สิ่งมีชีวิตถูกยางไม้เหนียวหุ้มไว้ทั้งตัว ยางไม้แข็งตัวเป็นอำพัน ซากจึงยังคงสภาพเกือบสมบูรณ์"),
    Model("แช่กิ่งไม้ในน้ำเกลือเข้มข้นหลายวัน แล้วนำขึ้นมาตากให้แห้ง พบผลึกเกลือแทรกอยู่ในเนื้อไม้",
          "ไม้กลายเป็นหิน",
          "แร่ที่ละลายในน้ำค่อย ๆ แทรกเข้าไปแทนที่เนื้อไม้ทีละน้อย จนซากแข็งเป็นหินแต่ยังเห็นลายเนื้อไม้"),
)


FORMATION_STEPS = (
    "สิ่งมีชีวิตตายลงและถูกตะกอนทับถมอย่างรวดเร็ว",
    "ส่วนที่อ่อนนุ่มเน่าสลายไป เหลือส่วนแข็ง เช่น กระดูกหรือเปลือก",
    "ตะกอนที่ทับถมถูกอัดแน่นจนกลายเป็นหินตะกอน",
    "เปลือกโลกยกตัวและหินถูกกัดกร่อน ซากดึกดำบรรพ์จึงโผล่ให้เห็น",
)


class Find(NamedTuple):
    """Fossils found together in one layer, and the past environment they point to."""
    fossils: str
    environment: str


# Each environment is named by exactly one find, so a find has one answer.
FINDS = (
    Find("เปลือกหอยทะเลและปะการังในหินปูนบนยอดเขา", "ทะเลตื้นที่มีน้ำอุ่น"),
    Find("หอยขมและหอยน้ำจืดจำนวนมากอัดแน่นเป็นแผ่นหิน", "บึงหรือทะเลสาบน้ำจืด"),
    Find("ใบเฟิร์นและลำต้นพืชจำนวนมากในหินดินดานและถ่านหิน", "ป่าที่ชื้นแฉะและมีพืชขึ้นหนาแน่น"),
    Find("กระดูกและรอยเท้าไดโนเสาร์กินพืชในหินทราย", "พื้นดินริมแม่น้ำที่มีพืชเป็นอาหาร"),
    Find("รอยเท้าสัตว์เลื้อยคลานบนชั้นทรายที่วางตัวเอียงเป็นเนินในหินทราย",
         "ทะเลทรายที่มีเนินทรายและฝนน้อย"),
)


@question_type(
    "geo.fossil_foundation",
    display_name={"th": "อธิบายการเกิดซากดึกดำบรรพ์จากแบบจำลอง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=FOSSIL_TOPIC,
)
class FossilFoundation(QuestionType):
    """Explain how a fossil forms from a model, or put the steps in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.3:
            order = list(FORMATION_STEPS)
            wrong_orders: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrong_orders) < 3:
                shuffled = order[:]
                rng.shuffle(shuffled)
                if shuffled != order:
                    wrong_orders[" → ".join(shuffled)] = None
            return _labelled(
                stem="ข้อใดเรียงลำดับการเกิดซากดึกดำบรรพ์ในหินตะกอนได้ถูกต้อง",
                correct=" → ".join(order),
                wrongs=tuple(wrong_orders),
                hint="ซากต้องถูกฝังก่อน แล้วตะกอนจึงกลายเป็นหิน สุดท้ายจึงโผล่ให้เห็น",
                topic=FOSSIL_TOPIC,
            )
        model = rng.choice(MODELS)
        others = [other for other in MODELS if other.fossil != model.fossil]
        if draw < 0.65:
            return _labelled(
                stem=f"แบบจำลอง: {model.activity} แบบจำลองนี้อธิบายการเกิดซากดึกดำบรรพ์แบบใด",
                correct=model.fossil,
                wrongs=tuple(other.fossil for other in others),
                hint="เทียบสิ่งที่ทำในแบบจำลองกับสิ่งที่เกิดกับซากในธรรมชาติ",
                topic=FOSSIL_TOPIC,
            )
        return _labelled(
            stem=f"แบบจำลอง: {model.activity} แบบจำลองนี้อธิบายว่า{model.fossil}เกิดขึ้นอย่างไร",
            correct=model.forms,
            wrongs=tuple(other.forms for other in others),
            hint="เทียบสิ่งที่ทำในแบบจำลองกับสิ่งที่เกิดกับซากในธรรมชาติ",
            topic=FOSSIL_TOPIC,
        )


@question_type(
    "geo.fossil_fluency",
    display_name={"th": "คาดคะเนสภาพแวดล้อมในอดีตจากซากดึกดำบรรพ์"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=FOSSIL_TOPIC,
)
class FossilFluency(QuestionType):
    """Infer the past environment from what was found — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        find = rng.choice(FINDS)
        others = [other for other in FINDS if other.fossils != find.fossils]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"นักธรณีวิทยาพบ{find.fossils} "
                     "บริเวณนี้ในอดีตน่าจะมีสภาพแวดล้อมแบบใด",
                correct=find.environment,
                wrongs=tuple([other.environment for other in others]),
                hint="สิ่งมีชีวิตในซากเคยอาศัยอยู่ที่ใด บริเวณนั้นในอดีตก็น่าจะเป็นแบบนั้น",
                topic=FOSSIL_TOPIC,
            )
        return _labelled(
            stem=f"ถ้าบริเวณหนึ่งในอดีตเคยเป็น{find.environment} "
                 "นักธรณีวิทยาน่าจะพบซากดึกดำบรรพ์แบบใดในชั้นหินของบริเวณนั้น",
            correct=find.fossils,
            wrongs=tuple([other.fossils for other in others]),
            hint="สิ่งมีชีวิตแบบใดอาศัยอยู่ในสภาพแวดล้อมนั้น",
            topic=FOSSIL_TOPIC,
        )


@question_type(
    "geo.fossil_application",
    display_name={"th": "ใช้ซากดึกดำบรรพ์อธิบายประวัติของพื้นที่"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=FOSSIL_TOPIC,
)
class FossilApplication(QuestionType):
    """Read a sequence of layers, explain a sea shell on a mountain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FOSSIL_SCENARIOS,
            hint="ชั้นล่างเกิดก่อนชั้นบน และซากบอกว่าที่นั้นเคยมีสภาพแวดล้อมแบบใด",
        ), FOSSIL_TOPIC)
