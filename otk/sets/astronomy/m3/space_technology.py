"""เทคโนโลยีอวกาศ

ดาราศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.3/4

Sets moved here from: astronomy, science_wave_c5.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.astronomy import SUBJECT, TOPIC
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_c5 import SPACE_USE_SCENARIOS

PROVENANCE = Provenance("original")


SPACE_TOPIC = "เทคโนโลยีอวกาศ"


class Orbit(NamedTuple):
    """A kind of satellite, the orbit it needs, and why that orbit suits its job."""
    kind: str
    orbit: str
    because: str


# The job fixes the orbit, so each row answers to exactly one of the others.
ORBITS = (
    Orbit("ดาวเทียมสื่อสารและดาวเทียมออกอากาศ",
          "วงโคจรค้างฟ้าเหนือเส้นศูนย์สูตร ที่ความสูงประมาณ 36,000 กิโลเมตร",
          "คาบการโคจรเท่ากับคาบการหมุนรอบตัวเองของโลกพอดี จานรับสัญญาณบนพื้นจึงหันค้างไว้ที่เดิมได้"),
    Orbit("ดาวเทียมสำรวจทรัพยากรและดาวเทียมอุตุนิยมวิทยาวงโคจรต่ำ",
          "วงโคจรผ่านขั้วโลกที่ความสูงไม่กี่ร้อยกิโลเมตร",
          "โลกหมุนผ่านใต้วงโคจร ดาวเทียมจึงกวาดถ่ายภาพได้ครบทั้งผิวโลกและได้ภาพละเอียดเพราะอยู่ต่ำ"),
    Orbit("ดาวเทียมนำทาง",
          "วงโคจรระดับกลาง ที่ความสูงประมาณ 20,000 กิโลเมตร หลายดวงกระจายกันทั่วท้องฟ้า",
          "เครื่องรับต้องเห็นดาวเทียมพร้อมกันหลายดวงเสมอ จึงจะคำนวณตำแหน่งจากเวลาที่สัญญาณเดินทางได้"),
    Orbit("กล้องโทรทรรศน์อวกาศ",
          "วงโคจรรอบโลกเหนือชั้นบรรยากาศ หรือจุดสมดุลแรงโน้มถ่วงที่อยู่ไกลออกไป",
          "อยู่พ้นอากาศที่ไหวตัวและพ้นแสงรบกวน จึงเก็บภาพและคลื่นที่ชั้นบรรยากาศดูดกลืนไว้ได้"),
    Orbit("สถานีอวกาศที่มีมนุษย์อยู่อาศัย",
          "วงโคจรต่ำที่เอียงจากเส้นศูนย์สูตรเล็กน้อย ที่ความสูงประมาณ 400 กิโลเมตร",
          "อยู่ต่ำพอให้ยานขนส่งส่งคนและเสบียงขึ้นไปได้บ่อยและประหยัดเชื้อเพลิง"),
)


class Mission(NamedTuple):
    """One step forward for space exploration, as a collected record would list it."""
    period: str
    project: str
    advance: str


# Ordered, and each ``advance`` is a different kind of first.
MISSIONS = (
    Mission("ทศวรรษ 2500", "โครงการส่งดาวเทียมและยานที่มีมนุษย์ควบคุมรุ่นแรก",
            "พิสูจน์ว่าส่งวัตถุและมนุษย์ขึ้นสู่วงโคจรแล้วกลับลงมาได้"),
    Mission("ทศวรรษ 2510", "โครงการส่งมนุษย์ไปลงดวงจันทร์",
            "นำมนุษย์ไปลงบนวัตถุท้องฟ้าดวงอื่นและนำตัวอย่างหินกลับมาศึกษา"),
    Mission("ทศวรรษ 2520", "โครงการยานสำรวจที่เดินทางผ่านดาวเคราะห์ชั้นนอก",
            "ถ่ายภาพระยะใกล้ของดาวเคราะห์ชั้นนอกและดาวบริวารได้เป็นครั้งแรก"),
    Mission("ทศวรรษ 2530", "โครงการกล้องโทรทรรศน์อวกาศ",
            "สังเกตวัตถุที่อยู่ไกลมากได้คมชัดขึ้น เพราะพ้นชั้นบรรยากาศของโลก"),
    Mission("ทศวรรษ 2540", "โครงการสถานีอวกาศนานาชาติ",
            "ทำให้มนุษย์อาศัยและทำการทดลองในวงโคจรได้ต่อเนื่องเป็นเวลานาน"),
    Mission("ทศวรรษ 2550 เป็นต้นมา", "โครงการรถสำรวจดาวอังคารและจรวดที่นำกลับมาใช้ซ้ำ",
            "สำรวจพื้นผิวดาวเคราะห์ดวงอื่นได้ละเอียดขึ้น และลดค่าใช้จ่ายในการส่งของขึ้นสู่วงโคจร"),
)


def _missions() -> str:
    return " / ".join(f"{item.period}: {item.project}" for item in MISSIONS)


@question_type("astro.space_tech",
               display_name={"th": "เทคโนโลยีอวกาศและการสำรวจ"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class SpaceTechnology(ClassifyType):
    """โยงบทบาทหน้าที่เข้ากับเทคโนโลยี ดาวเทียม/ยานอวกาศและรถสำรวจ/กล้องโทรทรรศน์อวกาศ."""

    CLASSIFY_STEM = "บทบาทต่อไปนี้เป็นของเทคโนโลยีอวกาศประเภทใด: “{member}”"
    PICK_STEM = "ข้อใดคือบทบาทหน้าที่ของเทคโนโลยีประเภท{category}"

    CATEGORIES = [
        Category("ดาวเทียมที่ให้บริการหรือสำรวจโลก (Earth satellites)",
                 ("การถ่ายภาพกลุ่มเมฆและพายุเพื่อพยากรณ์อากาศ",
                  "การถ่ายทอดสัญญาณโทรทัศน์ โทรศัพท์ และอินเทอร์เน็ต",
                  "ระบบระบุพิกัดตำแหน่งบนโลกหรือระบบนำทาง (GPS)",
                  "การบินวนรอบโลกเพื่อสำรวจทรัพยากรธรรมชาติและไฟป่า")),
        Category("ยานสำรวจและรถสำรวจวัตถุอื่น (Exploration spacecraft & rovers)",
                 ("การส่งรถหุ่นยนต์ (Rover) ไปขับเคลื่อนสำรวจพื้นผิวดาวอังคาร",
                  "ยานสำรวจไร้คนขับที่บินผ่านและเก็บข้อมูลดาวเคราะห์วงนอก",
                  "ยานพาหนะสำหรับพามนุษย์เดินทางไปสำรวจดวงจันทร์")),
        Category("กล้องโทรทรรศน์อวกาศ (Space telescopes)",
                 ("การตรวจวัดแสงจากดาวฤกษ์เพื่อศึกษาดาวเคราะห์นอกระบบสุริยะ",
                  "การถ่ายภาพกาแล็กซีอันไกลโพ้นโดยไม่มีชั้นบรรยากาศโลกบดบัง",
                  "การศึกษาจุดกำเนิดของเอกภพผ่านการจับรังสีอินฟราเรดความไวสูง")),
    ]


@question_type("astro.satellite_uses",
               display_name={"th": "ประโยชน์ของดาวเทียมในชีวิตประจำวัน"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class SatelliteUses(ClassifyType):
    """โยงการใช้งานในชีวิตประจำวันเข้ากับประเภทของดาวเทียมที่ทำหน้าที่นั้น."""

    CLASSIFY_STEM = "การใช้งานต่อไปนี้เป็นของดาวเทียมประเภทใด: “{member}”"
    PICK_STEM = "ข้อใดคือประโยชน์หรือการใช้งานของ{category}"

    CATEGORIES = [
        Category("ดาวเทียมสื่อสาร (Communication)",
                 ("การถ่ายทอดสัญญาณโทรทัศน์ไปยังพื้นที่ห่างไกล",
                  "การเชื่อมต่อสัญญาณโทรศัพท์ระหว่างประเทศ",
                  "การให้บริการอินเทอร์เน็ตผ่านดาวเทียม")),
        Category("ดาวเทียมอุตุนิยมวิทยา (Weather)",
                 ("การถ่ายภาพกลุ่มเมฆและพายุเพื่อพยากรณ์อากาศ",
                  "การติดตามการก่อตัวและเส้นทางของพายุ",
                  "การตรวจวัดอุณหภูมิยอดเมฆและไอน้ำในบรรยากาศ")),
        Category("ดาวเทียมนำทาง (Navigation / GPS)",
                 ("การระบุพิกัดตำแหน่งบนพื้นโลก",
                  "การนำทางการเดินทางด้วยระบบ GPS",
                  "การบอกเวลามาตรฐานที่แม่นยำ")),
        Category("ดาวเทียมสำรวจทรัพยากร (Remote Sensing)",
                 ("การทำแผนที่พื้นที่ป่าไม้และการเปลี่ยนแปลงการใช้ที่ดิน",
                  "การติดตามสุขภาพพืชผลจากภาพถ่ายหลายช่วงคลื่น",
                  "การทำแผนที่ลักษณะพื้นผิวเพื่อช่วยสำรวจทรัพยากรธรรมชาติ")),
    ]


@question_type("astro.space_missions",
               display_name={"th": "โครงการสำรวจอวกาศ"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class SpaceMissions(ClassifyType):
    """โยงโครงการหรือยานสำรวจชื่อดังเข้ากับเป้าหมายหลักของภารกิจ."""

    CLASSIFY_STEM = "โครงการหรือยานสำรวจต่อไปนี้มีเป้าหมายหลักในเรื่องใด: “{member}”"
    PICK_STEM = "ข้อใดคือโครงการหรือยานสำรวจที่มีเป้าหมาย{category}"

    CATEGORIES = [
        Category("สำรวจและลงจอดบนดวงจันทร์",
                 ("โครงการอะพอลโล (Apollo)", "ยานสำรวจฉางเอ๋อ (Chang'e)")),
        Category("สำรวจพื้นผิวดาวอังคาร",
                 ("ยานคิวริออซิตี (Curiosity)", "ยานเพอร์เซเวียแรนซ์ (Perseverance)")),
        Category("สำรวจดาวเคราะห์วงนอก ดาวเคราะห์แคระ และวัตถุแถบไคเปอร์",
                 ("ยานวอยเอเจอร์ (Voyager)", "ยานนิวฮอไรซันส์ (New Horizons)")),
        Category("สังเกตการณ์วัตถุท้องฟ้าในห้วงอวกาศลึก",
                 ("กล้องโทรทรรศน์อวกาศฮับเบิล (Hubble)",
                  "กล้องโทรทรรศน์อวกาศเจมส์ เว็บบ์ (James Webb)")),
    ]


@question_type(
    "astro.space_tech_use_foundation",
    display_name={"th": "การใช้ประโยชน์ของเทคโนโลยีอวกาศ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SPACE_TOPIC,
)
class SpaceTechUseFoundation(QuestionType):
    """Explain what each kind of satellite is for and why its orbit suits it.

    ``อธิบายการใช้ประโยชน์ของเทคโนโลยีอวกาศ`` is the first of two verbs joined by
    ``และ``, each with an object of its own, so it earns an ``exact`` set.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ORBITS)
        others = [other for other in ORBITS if other.kind != item.kind]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=f"“{item.kind}” ต้องใช้วงโคจรแบบใด",
                correct=item.orbit,
                wrongs=tuple(other.orbit for other in others[:3]),
                hint="นึกว่างานของดาวเทียมชนิดนั้นต้องการอยู่นิ่งเหนือจุดเดิม "
                     "หรือกวาดผ่านทั่วโลก",
                topic=SPACE_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=f"เหตุใด “{item.kind}” จึงต้องใช้{item.orbit}",
                correct=item.because,
                wrongs=tuple(other.because for other in others[:3]),
                hint="อธิบายว่าวงโคจรนั้นให้อะไรที่งานของดาวเทียมชนิดนี้ต้องใช้",
                topic=SPACE_TOPIC,
            )
        return _labelled(
            stem=f"ดาวเทียมที่ใช้{item.orbit} เป็นดาวเทียมชนิดใด",
            correct=item.kind,
            wrongs=tuple(other.kind for other in others[:3]),
            hint="อ่านลักษณะของวงโคจร แล้วนึกว่างานแบบใดต้องใช้วงโคจรเช่นนั้น",
            topic=SPACE_TOPIC,
        )


@question_type(
    "astro.space_tech_use_fluency",
    display_name={"th": "ความก้าวหน้าของโครงการสำรวจอวกาศ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SPACE_TOPIC,
)
class SpaceTechUseFluency(QuestionType):
    """Give examples of how exploration advanced, from a collected record.

    ``ยกตัวอย่างความก้าวหน้าของโครงการสำรวจอวกาศ`` is the second free verb, so it
    earns the indicator's second ``exact`` set, answering ``จากข้อมูลที่รวบรวมได้``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = ("นักเรียนรวบรวมข้อมูลโครงการสำรวจอวกาศไว้ ดังนี้ "
                f"{_missions()} ")
        item = rng.choice(MISSIONS)
        others = [other for other in MISSIONS if other.period != item.period]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ใน{item.period} มีโครงการใด",
                correct=item.project,
                wrongs=tuple(other.project for other in others[:3]),
                hint="หาช่วงเวลาที่โจทย์ถามในรายการ แล้วอ่านชื่อโครงการ",
                topic=SPACE_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=stem + f"“{item.project}” ทำให้การสำรวจอวกาศก้าวหน้าขึ้นอย่างไร",
                correct=item.advance,
                wrongs=tuple(other.advance for other in others[:3]),
                hint="ถามว่าโครงการนั้นทำสิ่งใดได้เป็นครั้งแรก หรือทำได้ดีกว่าเดิมอย่างไร",
                topic=SPACE_TOPIC,
            )
        return _labelled(
            stem=stem + "จากข้อมูลนี้ ข้อใดสรุปความก้าวหน้าของการสำรวจอวกาศได้ถูกต้อง",
            correct="ก้าวจากการส่งวัตถุขึ้นวงโคจร ไปสู่การส่งมนุษย์ การสำรวจ"
                    "ดาวดวงอื่น และการอยู่อาศัยในวงโคจรได้ต่อเนื่อง",
            wrongs=("ก้าวจากการอยู่อาศัยในวงโคจร ย้อนกลับไปสู่การส่งดาวเทียมดวงแรก",
                    "ก้าวจากการสำรวจดาวอังคาร ไปสู่การส่งมนุษย์ขึ้นสู่วงโคจรครั้งแรก",
                    "ทุกโครงการเกิดขึ้นพร้อมกันในช่วงเวลาเดียว จึงไม่มีลำดับความก้าวหน้า"),
            hint="เรียงโครงการตามช่วงเวลา แล้วดูว่าทำอะไรได้เพิ่มขึ้นทีละขั้น",
            topic=SPACE_TOPIC,
        )


@question_type(
    "astro.space_tech_use_application",
    display_name={"th": "วิเคราะห์การใช้เทคโนโลยีอวกาศและการสำรวจ"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=SPACE_TOPIC,
)
class SpaceTechUseApplication(QuestionType):
    """Choose an orbit for a job, and weigh what exploration has returned."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SPACE_USE_SCENARIOS,
            hint="ถามว่างานนั้นต้องการอยู่นิ่งเหนือจุดเดิม อยู่ต่ำเพื่อความละเอียด "
                 "หรือเห็นหลายดวงพร้อมกัน",
        ), SPACE_TOPIC)
