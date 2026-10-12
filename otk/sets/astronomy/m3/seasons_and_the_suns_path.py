"""ฤดูและการเคลื่อนที่ปรากฏของดวงอาทิตย์

ดาราศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.3/2

Sets moved here from: astronomy, science_wave_c5.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType, widen
from otk.sets._support.astronomy import SUBJECT, TOPIC
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_c5 import SEASON_FACTS, SEASON_SCENARIOS

PROVENANCE = Provenance("original")


SEASON_TOPIC = "ฤดูและการเคลื่อนที่ปรากฏของดวงอาทิตย์"


SEASON_MODEL = (
    "ครูวางโคมไฟไว้กลางโต๊ะแทนดวงอาทิตย์ แล้วถือลูกโลกที่มีแกนเอียงประมาณ 23.5 องศา "
    "เดินไปรอบโคมไฟหนึ่งรอบ โดยให้แกนเอียงชี้ไปทางเดิมตลอดทาง "
)


class SeasonPoint(NamedTuple):
    """One position on the orbit, and what it does to both named objects.

    ``season`` and ``sunrise`` are the two things ``ม.3/2`` names, so the answer
    that spans them is a single statement mentioning both.
    """
    position: str
    season: str
    sunrise: str


SEASON_POINTS = (
    SeasonPoint("ซีกโลกเหนือเอียงเข้าหาโคมไฟมากที่สุด",
                "ซีกโลกเหนือเป็นฤดูร้อน กลางวันยาวกว่ากลางคืน",
                "ดวงอาทิตย์ขึ้นเยื้องไปทางเหนือของทิศตะวันออก และขึ้นสูงที่สุดในรอบปี"),
    SeasonPoint("ซีกโลกเหนือเอียงออกจากโคมไฟมากที่สุด",
                "ซีกโลกเหนือเป็นฤดูหนาว กลางวันสั้นกว่ากลางคืน",
                "ดวงอาทิตย์ขึ้นเยื้องไปทางใต้ของทิศตะวันออก และขึ้นต่ำที่สุดในรอบปี"),
    SeasonPoint("แกนเอียงไม่ได้ชี้เข้าหาหรือออกจากโคมไฟ",
                "ทั้งสองซีกโลกได้รับแสงพอ ๆ กัน กลางวันและกลางคืนยาวเท่ากัน",
                "ดวงอาทิตย์ขึ้นตรงทิศตะวันออกพอดี"),
)


def _spans_both(item: SeasonPoint) -> str:
    return f"{item.season} และ{item.sunrise}"


@question_type(
    "astro.season_model_foundation",
    display_name={"th": "แกนเอียงของโลกกับฤดู"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SEASON_TOPIC,
)
class SeasonModelFoundation(QuestionType):
    """Know the tilt, and what a hemisphere leaning sunward receives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SEASON_FACTS,
            hint="นึกถึงแกนที่เอียงไปทางเดิมเสมอ แล้วดูว่าซีกใดเอียงเข้าหาดวงอาทิตย์",
        ), SEASON_TOPIC)


@question_type("astro.seasons",
               display_name={"th": "ฤดูของโลก"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class Seasons(ConceptBankType):
    """ฤดูกาลเกิดจากแกนโลกเอียงขณะโคจรรอบดวงอาทิตย์ ไม่ใช่ระยะห่างจากดวงอาทิตย์."""

    ITEMS = widen([
        Concept(
            "ฤดูกาลต่างๆ ของโลกเกิดจากสาเหตุใดเป็นสำคัญ",
            "การที่โลกโคจรรอบดวงอาทิตย์ในขณะที่แกนโลกเอียงประมาณ 23.5 องศา",
            ("การที่ระยะห่างระหว่างโลกกับดวงอาทิตย์เปลี่ยนไปมากในรอบปี",
             "การหมุนรอบตัวเองของโลกที่เร็วขึ้นและช้าลงในแต่ละช่วงของปี",
             "การที่ดวงอาทิตย์ส่องแสงแรงไม่เท่ากันในแต่ละวัน")),
        Concept(
            "แกนหมุนของโลกเอียงจากแนวตั้งฉากของระนาบวงโคจรประมาณเท่าใด",
            "ประมาณ 23.5 องศา",
            ("ประมาณ 90 องศา", "ประมาณ 45 องศา", "ประมาณ 10 องศา")),
        Concept(
            "เมื่อซีกโลกเหนือเป็นฤดูร้อน ซีกโลกใต้จะเป็นฤดูใด",
            "ฤดูหนาว",
            ("ฤดูร้อนเช่นเดียวกัน", "ฤดูฝนเสมอ", "ไม่มีการเปลี่ยนฤดูกาล")),
        Concept(
            "เพราะเหตุใดซีกโลกที่เอียงเข้าหาดวงอาทิตย์จึงเป็นฤดูร้อน",
            "แสงตกกระทบตรงกว่าและช่วงกลางวันยาวกว่า จึงได้รับพลังงานต่อพื้นที่มากกว่า",
            ("อยู่ใกล้ดวงอาทิตย์มากกว่าอีกซีกโลกอย่างชัดเจน",
             "หมุนรอบตัวเองเร็วกว่าซีกโลกอีกด้านหนึ่ง",
             "มีชั้นบรรยากาศบางกว่าซีกโลกอีกด้านหนึ่ง")),
        Concept(
            "ข้อใดกล่าวถูกต้องเกี่ยวกับสาเหตุการเกิดฤดูกาลของโลก",
            "ฤดูกาลเกิดจากการเอียงของแกนโลก ไม่ได้เกิดจากระยะห่างโลก–ดวงอาทิตย์",
            ("ฤดูร้อนเกิดเพราะโลกอยู่ใกล้ดวงอาทิตย์ที่สุด",
             "ฤดูกาลเกิดพร้อมกันทั้งสองซีกโลก เพราะโลกทั้งใบอยู่ห่างดวงอาทิตย์เท่ากัน",
             "ฤดูกาลเกิดจากการหมุนรอบตัวเองของโลกในหนึ่งวัน")),
    ], (
        ("การที่ดวงจันทร์บังแสงอาทิตย์เป็นช่วง ๆ ในรอบปี",
         "การที่ชั้นบรรยากาศของโลกหนาขึ้นและบางลงตามเดือน"),
        ("ประมาณ 0 องศา",
         "ประมาณ 66.5 องศา"),
        ("ฤดูใบไม้ผลิเสมอ",
         "ฤดูร้อนแต่มีอุณหภูมิสูงกว่า"),
        ("อยู่ใกล้ดวงอาทิตย์มากกว่าอีกซีกโลก จึงได้รับความร้อนจากดวงอาทิตย์มากกว่า",
         "หมุนรอบตัวเองช้ากว่า จึงหันเข้าหาดวงอาทิตย์นานกว่าและได้รับความร้อนมากกว่า"),
        ("ฤดูกาลเกิดเพราะดวงอาทิตย์ร้อนขึ้นและเย็นลงตามรอบปี",
         "ฤดูกาลเกิดจากระยะห่างโลก–ดวงอาทิตย์ ไม่ได้เกิดจากการเอียงของแกนโลก"),
    ))


@question_type("astro.sun_path",
               display_name={"th": "การเคลื่อนที่ปรากฏของดวงอาทิตย์บนท้องฟ้า"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class SunPath(ConceptBankType):
    """ดวงอาทิตย์ขึ้นทางตะวันออก ตกทางตะวันตก เพราะโลกหมุนรอบตัวเอง เส้นทางเปลี่ยนตามฤดู."""

    ITEMS = widen([
        Concept(
            "โดยทั่วไป เรามองเห็นดวงอาทิตย์ขึ้นทางด้านใดของขอบฟ้าและตกทางด้านใด",
            "ขึ้นทางด้านทิศตะวันออก และตกทางด้านทิศตะวันตก",
            ("ขึ้นทางทิศตะวันตก และตกทางทิศตะวันออก",
             "ขึ้นทางด้านทิศเหนือ และตกทางด้านทิศใต้ในทุกวัน",
             "ขึ้นทางด้านทิศตะวันตก และตกทางด้านทิศตะวันออก")),
        Concept(
            "การที่ดวงอาทิตย์ปรากฏเคลื่อนที่ข้ามท้องฟ้าจากทิศตะวันออกไปตะวันตกเกิดจากสาเหตุใด",
            "การหมุนรอบตัวเองของโลกจากทิศตะวันตกไปทิศตะวันออก",
            ("ดวงอาทิตย์เคลื่อนที่รอบโลกจริงในหนึ่งวัน",
             "การที่โลกโคจรรอบดวงอาทิตย์ในหนึ่งปี",
             "การเคลื่อนที่ของดวงจันทร์รอบโลกที่ดึงดวงอาทิตย์ไปด้วย")),
        Concept(
            "ในช่วงเวลาใดดวงอาทิตย์ปรากฏอยู่สูงที่สุดของวัน ณ ตำแหน่งผู้สังเกต",
            "ใกล้เวลาเที่ยงสุริยะท้องถิ่น ซึ่งไม่จำเป็นต้องตรง 12:00 น.",
            ("ทันทีที่ดวงอาทิตย์ขึ้น", "ทันทีก่อนดวงอาทิตย์ตก ซึ่งดวงอาทิตย์อยู่สูงที่สุดเหนือขอบฟ้า", "เวลาตรง 12:00 น. ตามนาฬิกา ไม่ว่าจะอยู่ที่ตำแหน่งใดบนโลก")),
        Concept(
            "สำหรับบริเวณส่วนใหญ่ในซีกโลกเหนือ เส้นทางปรากฏของดวงอาทิตย์ในฤดูร้อนเป็นอย่างไรเมื่อเทียบกับฤดูหนาว",
            "อยู่สูงกว่าและช่วงกลางวันยาวนานกว่า",
            ("อยู่ต่ำกว่าและช่วงกลางวันสั้นกว่า",
             "อยู่ในตำแหน่งเดิมและกลางวันเท่ากันทุกฤดู",
             "ดวงอาทิตย์ไม่ปรากฏขึ้นเลยตลอดฤดู")),
    ], (
        ("ขึ้นทางทิศใต้ และตกทางทิศเหนือ",
         "ขึ้นทางทิศตะวันออก และตกทางทิศเหนือเสมอ"),
        ("การที่โลกหมุนรอบตัวเองจากทิศตะวันออกไปทิศตะวันตก",
         "แรงลมในชั้นบรรยากาศที่พาดวงอาทิตย์เคลื่อนไป"),
        ("เวลาประมาณ 9:00 น. ทุกวัน",
         "เวลาตรง 12:00 น. ตามนาฬิกาทุกพื้นที่เสมอ"),
        ("อยู่สูงกว่าแต่ช่วงกลางวันสั้นกว่า",
         "อยู่ต่ำกว่าแต่ช่วงกลางวันยาวกว่า"),
    ))


@question_type(
    "astro.season_model_fluency",
    display_name={"th": "อธิบายฤดูและการเคลื่อนที่ปรากฏของดวงอาทิตย์"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SEASON_TOPIC,
)
class SeasonModelFluency(QuestionType):
    """Reach both of the indicator's objects from one position on the orbit.

    ``ม.3/2`` names the seasons and the sun's apparent motion under a single
    verb, so by the multi-object rule only an answer covering both is a
    defensible match. The two share a cause, which is what lets one answer do it.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SEASON_POINTS)
        others = [other for other in SEASON_POINTS if other.position != item.position]
        return _labelled(
            stem=f"{SEASON_MODEL}เมื่อลูกโลกมาถึงตำแหน่งที่{item.position} "
                 "จากแบบจำลองนี้ ข้อใดกล่าวถึงฤดูและตำแหน่งการขึ้นของดวงอาทิตย์"
                 "ที่ซีกโลกเหนือได้ถูกต้อง",
            correct=_spans_both(item),
            # Whole wrong positions, or one half borrowed from another position.
            wrongs=tuple([_spans_both(other) for other in others]
                + [f"{other.season} และ{item.sunrise}" for other in others]
                + [f"{item.season} และ{other.sunrise}" for other in others]
                + [f"{item.season} และดวงอาทิตย์ขึ้นตรงทิศตะวันตกพอดี"]),
            hint="ดูว่าซีกโลกเหนือเอียงเข้าหาหรือออกจากโคมไฟ แล้วตอบให้ครบทั้งสองเรื่อง",
            topic=SEASON_TOPIC,
        )


@question_type(
    "astro.season_model_application",
    display_name={"th": "วิเคราะห์ฤดูและเส้นทางของดวงอาทิตย์"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SEASON_TOPIC,
)
class SeasonModelApplication(QuestionType):
    """Judge the distance myth, a shadow measured twice, and the equator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SEASON_SCENARIOS,
            hint="ถามว่าซีกโลกนั้นเอียงเข้าหาหรือออกจากดวงอาทิตย์ ไม่ใช่ว่าอยู่ใกล้หรือไกล",
        ), SEASON_TOPIC)
