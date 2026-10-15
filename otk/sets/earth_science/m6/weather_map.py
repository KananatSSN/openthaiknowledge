"""แผนที่อากาศและการวางแผนการดำเนินชีวิต

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/14

Sets moved here from: science_wave_c26.
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
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c22 import _matching_item
from otk.sets._support.science_wave_c26 import WEATHER_MAP_SCENARIOS

PROVENANCE = Provenance("original")


WEATHER_MAP_TOPIC = "แผนที่อากาศและการวางแผนการดำเนินชีวิต"


class Symbol(NamedTuple):
    meaning: str
    look: str


SYMBOLS = (
    Symbol("หย่อมความกดอากาศสูง",
           "ตัวอักษร H สีน้ำเงินที่มีเส้นโค้งปิดล้อมรอบ ค่าความกดอากาศบนเส้นเพิ่มขึ้นเข้าหาศูนย์กลาง"),
    Symbol("หย่อมความกดอากาศต่ำ",
           "ตัวอักษร L สีแดงที่มีเส้นโค้งปิดล้อมรอบ ค่าความกดอากาศบนเส้นลดลงเข้าหาศูนย์กลาง"),
    Symbol("เส้นไอโซบาร์",
           "เส้นโค้งที่ลากผ่านจุดที่มีความกดอากาศเท่ากัน และมีตัวเลขค่าความกดอากาศกำกับ"),
    Symbol("แนวปะทะอากาศเย็น",
           "เส้นสีน้ำเงินที่มีรูปสามเหลี่ยมทึบเรียงอยู่ด้านเดียวของเส้น"),
    Symbol("แนวปะทะอากาศอุ่น",
           "เส้นสีแดงที่มีรูปครึ่งวงกลมทึบเรียงอยู่ด้านเดียวของเส้น"),
    Symbol("พายุหมุนเขตร้อน",
           "วงกลมที่มีหางโค้งยื่นออกไปสองข้างในทิศตรงข้ามกันคล้ายกังหัน"),
)


class Situation(NamedTuple):
    """What a weather map shows, who is affected, and the plan that fits."""
    shows: str
    who: str
    plan: str


SITUATIONS = (
    Situation("หย่อมความกดอากาศสูงกำลังแรงจากประเทศจีนแผ่ลงมาปกคลุมประเทศไทยตอนบน",
              "นักเรียนในจังหวัดเชียงรายจะไปเข้าค่ายพักแรมบนดอยในสัปดาห์หน้า",
              "เตรียมเสื้อผ้ากันหนาวและถุงนอนที่อุ่นพอ ดื่มน้ำให้เพียงพอ และระวังการก่อไฟเพราะอากาศแห้ง"),
    Situation("พายุหมุนเขตร้อนในทะเลจีนใต้กำลังเคลื่อนเข้าหาชายฝั่งภาคตะวันออกของประเทศไทย",
              "ชาวประมงเรือเล็กในจังหวัดระยอง",
              "งดนำเรือออกจากฝั่ง ผูกเรือให้แน่นหนา เก็บสิ่งของที่อาจปลิว และติดตามประกาศเตือนภัย"),
    Situation("ร่องความกดอากาศต่ำพาดผ่านภาคเหนือตอนล่าง และมีเส้นไอโซบาร์ห่างกัน",
              "ครอบครัวที่จะไปเที่ยวน้ำตกในหุบเขาของจังหวัดตาก",
              "เลื่อนการเที่ยวน้ำตกออกไป หรือหลีกเลี่ยงลำธารในหุบเขาที่อาจเกิดน้ำป่าไหลหลาก และเตรียมเสื้อกันฝน"),
    Situation("ลมมรสุมตะวันตกเฉียงใต้กำลังแรงพัดปกคลุมทะเลอันดามัน เส้นไอโซบาร์บริเวณนั้นอยู่ชิดกัน",
              "นักท่องเที่ยวที่จองทัวร์ดำน้ำนอกชายฝั่งจังหวัดภูเก็ต",
              "เลื่อนทัวร์ดำน้ำออกไปและงดเล่นน้ำทะเล เพราะคลื่นลมแรง"),
    Situation("แนวปะทะอากาศเย็นกำลังเคลื่อนผ่านภาคตะวันออกเฉียงเหนือตอนบน",
              "ชาวนาในจังหวัดอุดรธานีที่วางแผนตากข้าวเปลือกกลางลานในบ่ายวันพรุ่งนี้",
              "เก็บข้าวเปลือกเข้าที่ร่มก่อนบ่าย เพราะอาจมีฝนฟ้าคะนองและลมกระโชกแรง แล้วอากาศจะเย็นลงหลังแนวปะทะผ่าน"),
    Situation("หย่อมความกดอากาศสูงแผ่ปกคลุมภาคกลาง ลมสงบ และท้องฟ้าโปร่งติดต่อกันหลายวัน",
              "ชาวสวนในจังหวัดสุพรรณบุรีที่ต้องการตากกล้วยให้แห้งเพื่อทำกล้วยตาก",
              "ใช้ช่วงที่ท้องฟ้าโปร่งและแดดดีตากกล้วย และปิดคลุมเมื่อมีฝุ่นละอองสะสมเพราะลมสงบ"),
)


# More situations. Each plan answers its own reader and weather only.
SITUATIONS = (*SITUATIONS,
    Situation("หย่อมความกดอากาศต่ำกำลังแรงอยู่กลางทะเลอันดามัน และเส้นไอโซบาร์รอบหย่อมนั้นอยู่ชิดกันมาก",
              "ผู้ที่จะเดินทางโดยเรือเฟอร์รีจากจังหวัดกระบี่ไปเกาะลันตาในวันพรุ่งนี้",
              "ตรวจประกาศของท่าเรือก่อนออกเดินทาง เตรียมเลื่อนการเดินทางทางเรือ และหาที่พักบนฝั่งสำรองไว้"),
    Situation("มวลอากาศเย็นจากประเทศจีนแผ่ลงมาถึงภาคใต้ตอนบน ทำให้คลื่นลมในอ่าวไทยแรงขึ้น",
              "ผู้เลี้ยงปลาในกระชังริมชายฝั่งจังหวัดสุราษฎร์ธานี",
              "ผูกยึดกระชังให้แน่นหนา ลดการให้อาหารช่วงคลื่นแรง และเตรียมย้ายปลาบางส่วนเข้าบ่อบนฝั่ง"),
    Situation("ร่องมรสุมพาดผ่านภาคกลางและภาคตะวันออกติดต่อกันหลายวัน",
              "ผู้รับเหมาที่กำลังจะเทพื้นคอนกรีตลานจอดรถกลางแจ้งในกรุงเทพมหานคร",
              "เลื่อนการเทคอนกรีตไปวันที่ฝนน้อย หรือเตรียมผ้าใบคลุมพื้นที่เทไว้ เพราะฝนจะตกชุกหลายวัน"),
    Situation("หย่อมความกดอากาศสูงแผ่ปกคลุมภาคเหนือ ลมสงบ และอากาศเย็นแห้งติดต่อกันหลายวัน",
              "ชาวบ้านในจังหวัดเชียงใหม่ที่วางแผนเผาเศษซังข้าวโพดในไร่",
              "งดการเผาในที่โล่ง เพราะลมสงบทำให้ควันและฝุ่นสะสมอยู่ในพื้นที่ แล้วใช้วิธีไถกลบแทน"),
    Situation("พายุดีเปรสชันกำลังเคลื่อนเข้าสู่ภาคตะวันออกเฉียงเหนือ และคาดว่าจะมีฝนตกหนักถึงหนักมาก",
              "เจ้าหน้าที่ดูแลอ่างเก็บน้ำขนาดกลางในจังหวัดขอนแก่น",
              "เร่งระบายน้ำในอ่างลงล่วงหน้าเพื่อรองรับน้ำฝนที่จะไหลเข้ามา และแจ้งเตือนชุมชนท้ายน้ำ"),
)

@question_type(
    "geo.weather_map_foundation",
    display_name={"th": "แปลความหมายสัญลักษณ์ลมฟ้าอากาศในแผนที่อากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=WEATHER_MAP_TOPIC,
)
class WeatherMapFoundation(QuestionType):
    """Five symbols described; the answer places every one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(SYMBOLS, 5)
        return _matching_item(
            rng, [symbol.meaning for symbol in chosen], [symbol.look for symbol in chosen],
            intro="ลักษณะของสัญลักษณ์ในแผนที่อากาศ",
            question="ข้อใดจับคู่ความหมายกับสัญลักษณ์ได้ถูกต้องทั้งหมด",
            hint="แนวปะทะอากาศเย็นใช้สามเหลี่ยมสีน้ำเงิน แนวปะทะอากาศอุ่นใช้ครึ่งวงกลมสีแดง H คือความกดอากาศสูง L คือความกดอากาศต่ำ",
            topic=WEATHER_MAP_TOPIC,
        )


@question_type(
    "geo.weather_map_fluency",
    display_name={"th": "วางแผนการดำเนินชีวิตจากข้อมูลในแผนที่อากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=WEATHER_MAP_TOPIC,
)
class WeatherMapFluency(QuestionType):
    """What the map shows and who is affected; the plan that fits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(SITUATIONS))
        situation = SITUATIONS[index]
        return _labelled(
            stem=(f"แผนที่อากาศวันนี้แสดง{situation.shows} ถ้า{situation.who} "
                  "ควรวางแผนอย่างไรจึงสอดคล้องกับสภาพลมฟ้าอากาศมากที่สุด"),
            correct=situation.plan,
            wrongs=tuple([other.plan for i, other in enumerate(SITUATIONS) if i != index]),
            hint="แปลสัญลักษณ์ก่อนว่าจะเกิดลมฟ้าอากาศแบบใดในบริเวณนั้น แล้วเลือกแผนที่รับมือกับสภาพนั้น",
            topic=WEATHER_MAP_TOPIC,
        )


@question_type(
    "geo.weather_map_application",
    display_name={"th": "วิเคราะห์แผนที่อากาศเพื่อคาดการณ์และตัดสินใจ"},
    level=UPPER_SIX, subject=SUBJECT, topic=WEATHER_MAP_TOPIC,
)
class WeatherMapApplication(QuestionType):
    """Isobar spacing, a passing cold front, and a storm weakened to a low."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WEATHER_MAP_SCENARIOS,
            hint="แปลสัญลักษณ์ให้เป็นลมฟ้าอากาศที่จะเกิดก่อน แล้วจึงตัดสินใจ",
        ), WEATHER_MAP_TOPIC)
