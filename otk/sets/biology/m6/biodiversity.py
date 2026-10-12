"""ความหลากหลายทางชีวภาพ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.6/1

Sets moved here from: science_wave_f52.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f52 import SUBJECT

PROVENANCE = Provenance("original")


UPPER_SIX = {"th": "ม.6"}


TOPIC_DIV = "ความหลากหลายทางชีวภาพ"


LEVELS = {
    "ความหลากหลายทางพันธุกรรม": ("ข้าวหอมมะลิ ข้าวเหนียว และข้าวไรซ์เบอร์รีมีลักษณะเมล็ดต่างกัน",
                                  "สุนัขพันธุ์ต่าง ๆ มีขนาดและสีขนแตกต่างกัน", "มะม่วงแต่ละพันธุ์มีรสชาติและรูปร่างผลต่างกัน",
                                  "ผู้คนมีหมู่เลือดและสีผิวแตกต่างกัน"),
    "ความหลากหลายของสปีชีส์": ("ป่าดิบชื้นแห่งหนึ่งพบนกหลายสิบชนิด", "แนวปะการังมีปลาหลายร้อยชนิดอาศัยอยู่ร่วมกัน",
                                "ในบ่อน้ำพบทั้งปลา กบ หอย และพืชน้ำหลายชนิด", "ประเทศไทยพบกล้วยไม้ป่ามากกว่าพันชนิด"),
    "ความหลากหลายของระบบนิเวศ": ("ประเทศไทยมีทั้งป่าชายเลน ป่าดิบเขา ทุ่งหญ้า และแนวปะการัง",
                                  "จังหวัดหนึ่งมีทั้งภูเขา แม่น้ำ และชายหาด", "มีทั้งระบบนิเวศบนบกและระบบนิเวศในน้ำจืดและน้ำเค็ม"),
}


DIV_HINT = ("ความหลากหลายทางพันธุกรรมคือความแตกต่างภายในสปีชีส์ ความหลากหลายของสปีชีส์คือจำนวนชนิด "
            "ความหลากหลายของระบบนิเวศคือจำนวนแบบของแหล่งที่อยู่ ทั้งสามระดับเกื้อหนุนกัน")


VALUE_FACTS = (
    ("ความหลากหลายทางพันธุกรรมภายในประชากรมีความสำคัญอย่างไร", "ทำให้ประชากรมีโอกาสอยู่รอดเมื่อสิ่งแวดล้อมเปลี่ยนหรือเกิดโรคระบาด",
     ("ทำให้ทุกตัวในประชากรเหมือนกัน จึงต้านทานโรคได้เท่ากันทุกตัว", "ทำให้ประชากรไม่ต้องสืบพันธุ์", "ไม่มีผลต่อการอยู่รอดของประชากร เพราะสิ่งแวดล้อมไม่เคยเปลี่ยน", "ทำให้ประชากรลดจำนวนลงเสมอ")),
    ("ความหลากหลายของระบบนิเวศเกี่ยวข้องกับความหลากหลายของสปีชีส์อย่างไร", "ระบบนิเวศที่หลากหลายมีแหล่งที่อยู่หลายแบบ จึงรองรับสปีชีส์ได้มาก",
     ("ระบบนิเวศที่หลากหลายทำให้สปีชีส์ลดลง เพราะแหล่งที่อยู่ถูกแบ่งย่อยเกินไป", "ทั้งสองไม่เกี่ยวข้องกัน", "ระบบนิเวศแต่ละแบบรองรับได้เพียงสปีชีส์เดียวเท่านั้น")),
    ("ข้อใดเป็นประโยชน์ทางตรงของความหลากหลายทางชีวภาพต่อมนุษย์", "เป็นแหล่งอาหาร ยารักษาโรค และวัตถุดิบ",
     ("ทำให้เกิดภัยธรรมชาติมากขึ้น", "ทำให้ดินเสื่อมโทรมและขาดธาตุอาหาร", "เพิ่มแก๊สเรือนกระจกในบรรยากาศ")),
    ("ข้อใดเป็นสาเหตุสำคัญที่ทำให้ความหลากหลายทางชีวภาพลดลง", "การทำลายแหล่งที่อยู่อาศัยของสิ่งมีชีวิต",
     ("การอนุรักษ์ป่าต้นน้ำ", "การจัดตั้งอุทยานแห่งชาติ", "การปลูกป่าชายเลนทดแทน", "การเก็บรักษาเมล็ดพันธุ์ในธนาคารเมล็ดพันธุ์")),
    ("การปลูกพืชพันธุ์เดียวกันทั้งหมดในพื้นที่กว้างมีความเสี่ยงอย่างไร", "ถ้าเกิดโรคที่พืชพันธุ์นั้นไม่ต้านทาน พืชอาจตายทั้งหมด",
     ("ทำให้ผลผลิตหลากหลายขึ้นและขายได้ราคาดีขึ้น", "ทำให้พืชทุกต้นต้านทานโรคได้ทุกชนิดเหมือนกันเสมอ", "ไม่มีความเสี่ยงใด ๆ")),
)


THREATS = ("การบุกรุกแผ้วถางป่าเพื่อทำไร่", "การนำสิ่งมีชีวิตต่างถิ่นที่รุกรานเข้ามาในแหล่งน้ำ", "การล่าสัตว์ป่าเพื่อการค้า",
           "การปล่อยน้ำเสียลงแม่น้ำ", "การปลูกพืชพันธุ์เดียวบนพื้นที่กว้าง")


CONSERVE = ("การจัดตั้งอุทยานแห่งชาติและเขตรักษาพันธุ์สัตว์ป่า", "การเก็บรักษาเมล็ดพันธุ์พื้นเมืองในธนาคารเมล็ดพันธุ์",
            "การปลูกป่าชายเลนทดแทนส่วนที่ถูกทำลาย", "การเพาะเลี้ยงสัตว์ใกล้สูญพันธุ์แล้วปล่อยคืนธรรมชาติ")


SITES = ("ป่าชายเลน", "ป่าดิบชื้น", "ทุ่งหญ้า", "แนวปะการัง", "ป่าเต็งรัง")


@question_type(
    "biology.biodiversity_foundation",
    display_name={"th": "ระดับของความหลากหลายทางชีวภาพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_DIV,
)
class BiodiversityFoundation(QuestionType):
    """Genes within a species, the number of species, the kinds of ecosystem."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        level = rng.choice(sorted(LEVELS))
        example = rng.choice(LEVELS[level])
        others = [lv for lv in LEVELS if lv != level]
        if rng.random() < 0.55:
            return _labelled(stem=f"\"{example}\" แสดงความหลากหลายทางชีวภาพระดับใด", correct=level,
                             wrongs=(*others, "ความหลากหลายทางวัฒนธรรม"), topic=TOPIC_DIV, hint=DIV_HINT)
        pool = [e for lv in others for e in LEVELS[lv]]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{level}", correct=example, wrongs=tuple(pool), topic=TOPIC_DIV,
                         hint=DIV_HINT)


@question_type(
    "biology.biodiversity_fluency",
    display_name={"th": "ความสำคัญและความเชื่อมโยงของความหลากหลายทางชีวภาพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_DIV,
)
class BiodiversityFluency(QuestionType):
    """Why each level matters, and what threatens it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            protect = rng.random() < 0.5
            right, wrong = (CONSERVE, THREATS) if protect else (THREATS, CONSERVE)
            return _labelled(stem=f"ข้อใด{'ช่วยรักษา' if protect else 'ทำให้สูญเสีย'}ความหลากหลายทางชีวภาพ", correct=rng.choice(right),
                             wrongs=tuple(wrong), topic=TOPIC_DIV, hint=DIV_HINT)
        stem, right, wrongs = rng.choice(VALUE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_DIV, hint=DIV_HINT)


@question_type(
    "biology.biodiversity_application",
    display_name={"th": "เปรียบเทียบความหลากหลายของสปีชีส์จากข้อมูลสำรวจ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_DIV,
)
class BiodiversityApplication(QuestionType):
    """More kinds, and more even numbers of each, mean more species diversity."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(SITES, 2)
        kinds = rng.randint(3, 5)
        total = rng.choice((60, 100, 120, 200))
        even = [total // kinds] * kinds
        even[0] += total - sum(even)
        skew = [total - (kinds - 1) * 2] + [2] * (kinds - 1)
        if rng.random() < 0.5:
            extra = rng.randint(1, 4)
            more = [total // (kinds + extra)] * (kinds + extra)
            more[0] += total - sum(more)
            return numeric(stem=f"สำรวจสิ่งมีชีวิตในพื้นที่ขนาดเท่ากันพบว่า {a} มีสิ่งมีชีวิต {len(more)} ชนิด ชนิดละ "
                                f"{', '.join(map(str, more))} ตัว และ{b} มี {kinds} ชนิด ชนิดละ {', '.join(map(str, even))} ตัว "
                                f"พื้นที่ที่มีความหลากหลายของสปีชีส์มากกว่ามีสิ่งมีชีวิตกี่ชนิด",
                           answer=len(more), wrongs=[kinds, total, len(more) + kinds], unit="ชนิด", topic=TOPIC_DIV,
                           hint="เมื่อจำนวนตัวทั้งหมดเท่ากัน พื้นที่ที่มีจำนวนชนิดมากกว่ามีความหลากหลายของสปีชีส์มากกว่า")
        return _labelled(stem=f"สำรวจพื้นที่ขนาดเท่ากัน {a} พบ {kinds} ชนิด จำนวน {', '.join(map(str, even))} ตัว "
                              f"ส่วน{b} พบ {kinds} ชนิด จำนวน {', '.join(map(str, skew))} ตัว ข้อสรุปใดถูกต้อง",
                         correct=f"{a}มีความหลากหลายของสปีชีส์มากกว่า เพราะจำนวนแต่ละชนิดกระจายสม่ำเสมอกว่า",
                         wrongs=(f"{b}มีความหลากหลายของสปีชีส์มากกว่า เพราะมีชนิดหนึ่งจำนวนมากกว่าชนิดอื่นมาก",
                                 "ทั้งสองพื้นที่มีความหลากหลายเท่ากันทุกด้าน เพราะมีจำนวนชนิดเท่ากัน",
                                 "สรุปไม่ได้ เพราะความหลากหลายไม่เกี่ยวกับจำนวนตัวของแต่ละชนิด"),
                         topic=TOPIC_DIV, hint="เมื่อจำนวนชนิดเท่ากัน พื้นที่ที่จำนวนแต่ละชนิดใกล้เคียงกันมีความหลากหลายมากกว่า")
