"""ดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/9

Sets moved here from: science_wave_c8.
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
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c8 import SUN_SCENARIOS

PROVENANCE = Provenance("original")


SUN_TOPIC = "ดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ"


class Layer(NamedTuple):
    """One layer of the sun, where it sits and what happens there."""
    name: str
    where: str
    what: str


LAYERS = (
    Layer("แก่น", "ใจกลางของดวงอาทิตย์",
          "เกิดปฏิกิริยาหลอมนิวเคลียสของไฮโดรเจนเป็นฮีเลียม ซึ่งเป็นแหล่งพลังงานทั้งหมด"),
    Layer("เขตแผ่รังสี", "ถัดจากแก่นออกมา",
          "พลังงานเดินทางออกมาในรูปของรังสี โดยถูกดูดกลืนและปล่อยซ้ำนับครั้งไม่ถ้วน"),
    Layer("เขตพาความร้อน", "ถัดจากเขตแผ่รังสีออกมาจนถึงผิว",
          "แก๊สร้อนลอยขึ้นและแก๊สเย็นจมลงเป็นวง พาพลังงานขึ้นมาสู่ผิว"),
    Layer("โฟโตสเฟียร์", "ผิวที่เรามองเห็นเป็นดวงกลมสว่าง",
          "เป็นชั้นที่แสงหลุดออกมาสู่อวกาศได้ และเป็นที่ที่เห็นจุดมืดบนดวงอาทิตย์"),
    Layer("โครโมสเฟียร์", "เหนือโฟโตสเฟียร์ขึ้นไป",
          "เห็นเป็นขอบสีแดงจาง ๆ ขณะเกิดสุริยุปราคาเต็มดวง และเป็นที่เกิดพวยแก๊ส"),
    Layer("คอโรนา", "ชั้นนอกสุดที่แผ่ออกไปไกลมาก",
          "มีอุณหภูมิสูงนับล้านเคลวิน และเป็นแหล่งที่ลมสุริยะพัดออกไปสู่อวกาศ"),
)


STRUCTURE = "โครงสร้างของดวงอาทิตย์"


WIND = "การเกิดลมสุริยะ"


STORM = "พายุสุริยะ"


SUN_SPANNING = (
    f"{STRUCTURE}แบ่งเป็นแก่นที่เกิดปฏิกิริยาหลอมนิวเคลียส เขตแผ่รังสี เขตพาความร้อน "
    "แล้วจึงเป็นโฟโตสเฟียร์ โครโมสเฟียร์ และคอโรนา "
    f"{WIND}คือการที่อนุภาคมีประจุจากคอโรนาซึ่งร้อนจัดหลุดพ้นออกไปสู่อวกาศอย่างต่อเนื่อง "
    f"ส่วน{STORM}คือการปลดปล่อยพลังงานและมวลออกมาอย่างรุนแรงในช่วงสั้น ๆ "
    "ซึ่งสัมพันธ์กับจำนวนจุดมืดบนดวงอาทิตย์")


SUN_SPANNING_WRONGS = (
    f"{STRUCTURE}แบ่งเป็นคอโรนาที่ใจกลางแล้วจึงเป็นแก่นที่ผิวด้านนอก "
    f"{WIND}คือลมที่พัดจากโลกเข้าหาดวงอาทิตย์ "
    f"ส่วน{STORM}คือพายุฝนที่เกิดบนผิวดวงอาทิตย์",
    f"{STRUCTURE}มีเพียงชั้นเดียวที่เป็นแก๊สร้อนสม่ำเสมอ "
    f"{WIND}เกิดจากการหมุนรอบตัวเองของดวงอาทิตย์เพียงอย่างเดียว "
    f"ส่วน{STORM}ไม่เกี่ยวกับจุดมืดบนดวงอาทิตย์เลย",
    f"{STRUCTURE}แบ่งเป็นแก่น เขตแผ่รังสี และเขตพาความร้อน "
    f"{WIND}คือแสงที่ดวงอาทิตย์ส่องออกมา "
    f"ส่วน{STORM}คือช่วงที่ดวงอาทิตย์ดับแสงลงชั่วคราว",
)


class Effect(NamedTuple):
    """One effect of solar activity on Earth, and what it reaches."""
    event: str
    result: str
    why: str


EFFECTS = (
    Effect("อนุภาคมีประจุจากพายุสุริยะถูกสนามแม่เหล็กโลกนำลงไปยังบริเวณขั้วโลก",
           "เกิดแสงเหนือแสงใต้ที่บริเวณละติจูดสูงใกล้ขั้วโลกได้บ่อยขึ้น",
           "อนุภาคชนกับแก๊สในบรรยากาศชั้นบนจนแก๊สเปล่งแสงออกมา"),
    Effect("พายุสุริยะรบกวนบรรยากาศชั้นไอโอโนสเฟียร์",
           "สัญญาณวิทยุคลื่นสั้นและสัญญาณดาวเทียมนำทางคลาดเคลื่อนหรือขาดหาย",
           "คลื่นวิทยุต้องสะท้อนหรือเดินทางผ่านชั้นไอโอโนสเฟียร์ ซึ่งความหนาแน่นของประจุเปลี่ยนไป"),
    Effect("การเปลี่ยนแปลงของสนามแม่เหล็กโลกอย่างรวดเร็วระหว่างพายุแม่เหล็กโลก",
           "เกิดกระแสไฟฟ้าเหนี่ยวนำในสายส่งไฟฟ้าแรงสูงจนหม้อแปลงเสียหายได้",
           "สนามแม่เหล็กที่เปลี่ยนแปลงเหนี่ยวนำให้เกิดกระแสในตัวนำที่ยาวมาก"),
    Effect("อนุภาคพลังงานสูงพุ่งเข้าชนดาวเทียมที่โคจรอยู่นอกเกราะกำบัง",
           "วงจรอิเล็กทรอนิกส์ของดาวเทียมเสียหายและนักบินอวกาศได้รับรังสีเพิ่มขึ้น",
           "นอกสนามแม่เหล็กและบรรยากาศของโลกไม่มีอะไรกั้นอนุภาคพลังงานสูงไว้"),
)


THAI_EFFECT = ("ไทยอยู่ใกล้เส้นศูนย์สูตรแม่เหล็กจึงแทบไม่เห็นแสงเหนือ แต่ยังได้รับผลผ่านสัญญาณดาวเทียมนำทางและวิทยุคลื่นสั้น")


EFFECT_RESULT_DECOYS = ("เกิดแผ่นดินไหวรุนแรงทั่วโลกจากแรงกระแทกของอนุภาคที่พุ่งมาถึง",
                        "ระดับน้ำทะเลสูงขึ้นหลายเมตรในวันเดียว เพราะอนุภาคดึงดูดน้ำทะเล")


EFFECT_WHY_DECOYS = ("อนุภาคจากดวงอาทิตย์มีมวลมากจนดึงดูดน้ำทะเลขึ้นมา จนระดับน้ำทะเลเปลี่ยนไปทั่วโลก",
                     "ลมสุริยะพาความร้อนมาทำให้อากาศบนพื้นโลกร้อนจัด จนอุปกรณ์บนพื้นโลกเสียหาย")


@question_type(
    "astro.sun_structure_foundation",
    display_name={"th": "โครงสร้างดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ"},
    level=UPPER_SIX, subject=SUBJECT, topic=SUN_TOPIC,
)
class SunStructureFoundation(QuestionType):
    """Reach the structure, the solar wind and the storms in one set.

    The indicator's first verb governs all three, so by the multi-object rule the
    ``exact`` answer has to hold all three.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=f"ข้อใดอธิบาย{STRUCTURE} {WIND} และ{STORM}ได้ถูกต้อง",
                correct=SUN_SPANNING, wrongs=SUN_SPANNING_WRONGS,
                hint="ตอบให้ครบทั้งสามเรื่อง แล้วตรวจว่าลำดับชั้นจากในออกนอกถูกต้องหรือไม่",
                topic=SUN_TOPIC,
            )
        layer = rng.choice(LAYERS)
        others = [other for other in LAYERS if other.name != layer.name]
        rng.shuffle(others)
        if draw < 0.7:
            return _labelled(
                stem=f"ชั้น “{layer.name}” ของดวงอาทิตย์เกิดอะไรขึ้น",
                correct=layer.what,
                wrongs=tuple(other.what for other in others[:3]),
                hint="ไล่ลำดับจากแก่นออกมาจนถึงคอโรนา",
                topic=SUN_TOPIC,
            )
        return _labelled(
            stem=f"ชั้นใดของดวงอาทิตย์อยู่{layer.where}",
            correct=layer.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="ไล่ลำดับจากแก่นออกมาจนถึงคอโรนา",
            topic=SUN_TOPIC,
        )


@question_type(
    "astro.sun_structure_fluency",
    display_name={"th": "วิเคราะห์ผลของลมสุริยะและพายุสุริยะต่อโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=SUN_TOPIC,
)
class SunStructureFluency(QuestionType):
    """Analyse what solar activity does to Earth — the indicator's second verb.

    ``สืบค้นข้อมูล`` and ``นำเสนอ`` are things a learner does and earn nothing here;
    ``วิเคราะห์`` carries an object of its own, and this set assesses it.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.3:
            return _labelled(
                stem="พายุสุริยะรุนแรงส่งผลต่อประเทศไทยอย่างไร",
                correct=THAI_EFFECT,
                wrongs=tuple((
                    "ประเทศไทยจะเห็นแสงเหนือได้ชัดเจนกว่าประเทศในเขตละติจูดสูง เพราะอยู่ใกล้ดวงอาทิตย์มากกว่า และสัญญาณดาวเทียมจะดีขึ้น",
                    "ประเทศไทยไม่ได้รับผลใด ๆ เลย เพราะอยู่ใกล้เส้นศูนย์สูตร",
                    "ประเทศไทยจะมีอุณหภูมิอากาศสูงขึ้นหลายองศาในวันที่เกิดพายุ จนไฟฟ้าดับและสัญญาณวิทยุหายไปทั้งประเทศ",
                    "ประเทศไทยจะมีพายุฝนฟ้าคะนองรุนแรงทั่วประเทศในวันที่เกิดพายุสุริยะ",
                    "ประเทศไทยจะมืดลงในเวลากลางวันเพราะดวงอาทิตย์หรี่แสง",
                )),
                hint="ละติจูดกำหนดว่าจะเห็นแสงเหนือหรือไม่ แต่สัญญาณดาวเทียมใช้กันทุกละติจูด",
                topic=SUN_TOPIC,
            )
        item = rng.choice(EFFECTS)
        others = [other for other in EFFECTS if other.event != item.event]
        rng.shuffle(others)
        if draw < 0.65:
            return _labelled(
                stem=f"เมื่อ{item.event} จะเกิดผลใดตามมา",
                correct=item.result,
                wrongs=tuple([other.result for other in others[:3]]
                                        + list(EFFECT_RESULT_DECOYS)),
                hint="ไล่จากสิ่งที่ถูกรบกวนไปหาสิ่งที่ต้องอาศัยสิ่งนั้นทำงาน",
                topic=SUN_TOPIC,
            )
        return _labelled(
            stem=f"เหตุใด{item.event}จึงทำให้{item.result}",
            correct=item.why,
            wrongs=tuple([other.why for other in others[:3]] + list(EFFECT_WHY_DECOYS)),
            hint="อธิบายกลไกที่เชื่อมอนุภาคหรือสนามแม่เหล็กเข้ากับผลที่เกิดขึ้น",
            topic=SUN_TOPIC,
        )


@question_type(
    "astro.sun_structure_application",
    display_name={"th": "วิเคราะห์สภาพอวกาศและผลต่อโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=SUN_TOPIC,
)
class SunStructureApplication(QuestionType):
    """Decide who must prepare, and separate space weather from ordinary weather."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUN_SCENARIOS,
            hint="ถามว่าสิ่งที่ถูกกระทบคือบรรยากาศชั้นบน สนามแม่เหล็ก หรืออากาศใกล้พื้น",
        ), SUN_TOPIC)
