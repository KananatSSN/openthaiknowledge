"""เวลาสุริยคติปรากฏ

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/15

Sets moved here from: science_wave_f85.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f85 import SUBJECT, UPPER_SIX, _clock

PROVENANCE = Provenance("original")


TOPIC_SOLAR = "เวลาสุริยคติปรากฏ"


SOLAR_FACTS = (
    ("เวลาสุริยคติปรากฏ 12:00 น. คือขณะใด", "ขณะที่ดวงอาทิตย์ผ่านเส้นเมริเดียนของผู้สังเกต",
     ("ขณะที่ดวงอาทิตย์ขึ้นจากขอบฟ้า", "ขณะที่นาฬิกาทุกเรือนบอก 12:00 น.", "ขณะที่ดวงอาทิตย์อยู่สูงที่สุดตามนาฬิกา 12:00 น.", "ขณะที่ดวงอาทิตย์ผ่านเส้นศูนย์สูตรท้องฟ้าพอดี")),
    ("นาฬิกาแดดบอกเวลาแบบใด", "เวลาสุริยคติปรากฏของสถานที่นั้น",
     ("เวลามาตรฐานของประเทศนั้น", "เวลาสากลเชิงพิกัด (UTC)", "เวลาดาราคติของสถานที่นั้น", "เวลาของเส้นลองจิจูด 0°")),
    ("เหตุใดความยาวของวันสุริยคติปรากฏจึงไม่เท่ากันตลอดปี", "วงโคจรของโลกเป็นวงรีและแกนโลกเอียง",
     ("โลกหมุนรอบตัวเองเร็วช้าต่างกันทุกวัน", "ดวงอาทิตย์เคลื่อนเข้าใกล้และไกลโลกทุกวัน", "ดวงจันทร์บังดวงอาทิตย์", "นาฬิกาแต่ละเรือนเดินไม่เท่ากัน")),
    ("ถ้าบันทึกเวลาตามนาฬิกาขณะดวงอาทิตย์ผ่านเมริเดียนทุกวันตลอดปี จะพบอะไร", "เวลาที่บันทึกได้เปลี่ยนไปเล็กน้อยทุกวัน ไม่ตรง 12:00 น. เสมอ",
     ("ตรงกับ 12:00 น. ทุกวันพอดี เพราะดวงอาทิตย์ผ่านเมริเดียนเวลาเดิม", "ดวงอาทิตย์ไม่ผ่านเมริเดียนในบางวัน", "เวลาที่บันทึกได้เปลี่ยนไปวันละหลายชั่วโมงตามฤดูกาล", "ดวงอาทิตย์ผ่านเมริเดียนวันละสองครั้ง")),
    ("ขณะดวงอาทิตย์ผ่านเส้นเมริเดียน เงาของแท่งไม้ที่ปักตั้งตรงมีลักษณะอย่างไร", "สั้นที่สุดของวันและชี้ไปในแนวเหนือ-ใต้",
     ("ยาวที่สุดของวันและชี้ไปทางทิศเหนือ", "สั้นที่สุดของวันและชี้ไปทางทิศตะวันออก", "ไม่มีเงาเลยทุกวันตลอดปี", "ชี้ไปทางทิศตะวันตกเสมอ")),
    ("วันสุริยคติปรากฏหนึ่งวันคือช่วงเวลาใด", "ช่วงเวลาที่ดวงอาทิตย์ผ่านเมริเดียนครั้งหนึ่งจนถึงครั้งถัดไป",
     ("ช่วงเวลาที่ดาวฤกษ์ผ่านเมริเดียนสองครั้ง", "ช่วงเวลาจากดวงอาทิตย์ขึ้นถึงดวงอาทิตย์ตก", "ช่วงเวลาตั้งแต่ดวงอาทิตย์ขึ้นจนถึงดวงอาทิตย์ขึ้นครั้งถัดไป", "ช่วงเวลาที่ดาวฤกษ์ดวงหนึ่งผ่านเมริเดียนครั้งหนึ่งจนถึงครั้งถัดไป")),
    ("สถานที่ที่อยู่ทางตะวันออกของประเทศไทยจะเห็นดวงอาทิตย์ผ่านเมริเดียนก่อนหรือหลังกรุงเทพมหานคร", "ก่อน เพราะโลกหมุนจากทิศตะวันตกไปทิศตะวันออก",
     ("หลัง เพราะโลกหมุนจากทิศตะวันออกไปทิศตะวันตก", "พร้อมกันทุกแห่งที่อยู่ละติจูดเดียวกัน", "หลัง เพราะอยู่ทางทิศตะวันออกไกลกว่า", "หลัง เพราะอยู่ใกล้ดวงอาทิตย์มากกว่า")),
)


SOLAR_HINT = ("เวลาสุริยคติปรากฏยึดดวงอาทิตย์จริง ผ่านเมริเดียนเมื่อ 12:00 น. ดวงอาทิตย์ปรากฏเคลื่อน 15° ต่อชั่วโมง "
              "ความยาววันสุริยคติปรากฏเปลี่ยนตลอดปีเพราะวงโคจรเป็นวงรีและแกนโลกเอียง")


@question_type(
    "astro.apparent_solar_time_foundation",
    display_name={"th": "ความหมายของเวลาสุริยคติปรากฏ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOLAR,
)
class ApparentSolarTimeFoundation(QuestionType):
    """Noon at the meridian; sundials; why the day's length changes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(SOLAR_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SOLAR, hint=SOLAR_HINT)


@question_type(
    "astro.apparent_solar_time_fluency",
    display_name={"th": "หาเวลาสุริยคติปรากฏจากตำแหน่งดวงอาทิตย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOLAR,
)
class ApparentSolarTimeFluency(QuestionType):
    """15° from the meridian is one hour; east is before noon, west after."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        degrees = rng.randrange(5, 81, 5)
        west = rng.random() < 0.5
        minutes = 4 * degrees
        right = _clock(12 * 60 + (minutes if west else -minutes))
        return _labelled(stem=f"ดวงอาทิตย์อยู่ห่างจากเส้นเมริเดียนไปทาง{'ตะวันตก' if west else 'ตะวันออก'} {degrees}° ขณะนั้นเป็นเวลาสุริยคติปรากฏเท่าใด "
                              f"(ดวงอาทิตย์ปรากฏเคลื่อน 15° ต่อชั่วโมง)",
                         correct=right, wrongs=(_clock(12 * 60 + (-minutes if west else minutes)), _clock(12 * 60 + (degrees if west else -degrees)),
                                                _clock(12 * 60 + (15 * degrees if west else -15 * degrees))), topic=TOPIC_SOLAR,
                         hint=SOLAR_HINT + " ทางตะวันออกของเมริเดียนคือก่อนเที่ยง ทางตะวันตกคือหลังเที่ยง")


@question_type(
    "astro.apparent_solar_time_application",
    display_name={"th": "วิเคราะห์เวลาที่ดวงอาทิตย์ผ่านเมริเดียน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOLAR,
)
class ApparentSolarTimeApplication(QuestionType):
    """Clock time of the Sun's transit on different days; apparent time from the clock."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        transit = 12 * 60 + rng.choice([d for d in range(-10, 31) if d])
        if rng.random() < 0.5:
            other = transit + rng.choice([d for d in range(-25, 26) if d])
            return numeric(stem=f"นักเรียนบันทึกว่าดวงอาทิตย์ผ่านเมริเดียนเวลา {_clock(transit)} ในวันหนึ่ง และเวลา {_clock(other)} ในอีกวันหนึ่ง "
                                f"เวลาทั้งสองต่างกันกี่นาที", answer=abs(other - transit),
                           wrongs=[abs(other - transit) + 60, abs(other - transit) * 2, 60 - abs(other - transit) if abs(other - transit) != 30 else 45],
                           unit="นาที", topic=TOPIC_SOLAR, hint="หาผลต่างของเวลาเป็นนาที")
        later = rng.randint(1, 5) * 60 + rng.choice((0, 15, 30, 45))
        right = _clock(12 * 60 + later)
        clock = transit + later
        return _labelled(stem=f"วันหนึ่งดวงอาทิตย์ผ่านเมริเดียนเวลา {_clock(transit)} ตามนาฬิกา เมื่อนาฬิกาบอกเวลา {_clock(clock)} "
                              f"เวลาสุริยคติปรากฏเป็นเท่าใด", correct=right,
                         wrongs=(_clock(clock), _clock(12 * 60 - later), _clock(12 * 60 + later + 60)),
                         topic=TOPIC_SOLAR, hint="เวลาสุริยคติปรากฏ = 12:00 น. + เวลาที่ผ่านไปหลังดวงอาทิตย์ผ่านเมริเดียน")
