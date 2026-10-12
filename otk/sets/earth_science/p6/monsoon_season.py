"""มรสุมและฤดูของประเทศไทย

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/5

Sets moved here from: science_wave_c15.
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
from otk.sets._support.science_wave_c15 import MONSOON_SCENARIOS

PROVENANCE = Provenance("original")


MONSOON_TOPIC = "มรสุมและฤดูของประเทศไทย"


class Season(NamedTuple):
    """A Thai season, the wind that marks it, and why the monsoon makes it so."""
    name: str
    wind: str
    months: tuple[str, ...]
    rain: tuple[int, int]
    temperature: tuple[int, int]
    because: str


SEASONS = (
    Season("ฤดูหนาว", "ลมมรสุมตะวันออกเฉียงเหนือ", ("ธันวาคม", "มกราคม"),
           (2, 20), (20, 24),
           "มรสุมตะวันออกเฉียงเหนือพัดพามวลอากาศเย็นและแห้งมาจากประเทศจีน อากาศจึงเย็นและฝนน้อย"),
    Season("ฤดูร้อน", "ลมใต้และลมแปรปรวน ไม่มีลมมรสุม", ("มีนาคม", "เมษายน"),
           (25, 70), (29, 32),
           "เป็นช่วงเปลี่ยนมรสุม ไม่มีมรสุมพัดพาความเย็นหรือความชื้นมา อากาศจึงร้อนที่สุดในรอบปี"),
    Season("ฤดูฝน", "ลมมรสุมตะวันตกเฉียงใต้", ("กรกฎาคม", "สิงหาคม", "กันยายน"),
           (180, 320), (26, 28),
           "มรสุมตะวันตกเฉียงใต้พัดผ่านมหาสมุทรอินเดียนำความชื้นมา จึงมีฝนตกชุก"),
)


# Wrong readings for the season questions, one drawn per question.
SEASON_DECOYS = ("ไม่มีฤดูใดเกี่ยวข้องกับลม", "ฤดูใบไม้ร่วง")


WIND_DECOYS = ("ลมบกและลมทะเลเท่านั้น", "ลมที่พัดมาจากขั้วโลกใต้โดยตรง")


BECAUSE_DECOYS = ("โลกอยู่ใกล้และไกลดวงอาทิตย์สลับกันในแต่ละเดือน",
                  "ดวงจันทร์บังแสงอาทิตย์ในบางเดือนของปี",
                  "มหาสมุทรหยุดระเหยน้ำในช่วงนั้นของปี")


def season_record(rng: Random) -> list[tuple[Season, str, int, int]]:
    """One month per season, shuffled: (season, month, rainfall mm, temperature °C)."""
    rows = [(season, rng.choice(season.months), rng.randint(*season.rain),
             rng.randint(*season.temperature)) for season in SEASONS]
    rng.shuffle(rows)
    return rows


def _record_text(rows) -> str:
    return " / ".join(
        f"{month}: {season.wind} ปริมาณฝน {rain} มิลลิเมตร อุณหภูมิเฉลี่ย {temperature} องศาเซลเซียส"
        for season, month, rain, temperature in rows)


def _season_answer(season: Season) -> str:
    return f"{season.name} เพราะ{season.because}"


@question_type(
    "geo.monsoon_season_foundation",
    display_name={"th": "มรสุมกับฤดูของประเทศไทย"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=MONSOON_TOPIC,
)
class MonsoonSeasonFoundation(QuestionType):
    """Match each season to its wind and why, without data."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        season = rng.choice(SEASONS)
        others = [other for other in SEASONS if other.name != season.name]
        ask = rng.randrange(4)
        if ask == 2:
            return _labelled(
                stem=f"เดือน{rng.choice(season.months)}ของประเทศไทยส่วนใหญ่อยู่ในฤดูใด",
                correct=season.name,
                wrongs=tuple(other.name for other in others) + (rng.choice(SEASON_DECOYS[1:]),),
                hint="นึกว่าเดือนนั้นมีมรสุมใดพัดผ่านประเทศไทย",
                topic=MONSOON_TOPIC,
            )
        if ask == 3:
            return _labelled(
                stem=f"ในช่วง{season.name} ประเทศไทยได้รับลมใดเป็นหลัก",
                correct=season.wind,
                wrongs=tuple(other.wind for other in others) + (rng.choice(WIND_DECOYS),),
                hint="ลมที่พัดผ่านทะเลนำความชื้นมา ลมที่พัดมาจากแผ่นดินใหญ่นำความเย็นและแห้งมา",
                topic=MONSOON_TOPIC,
            )
        if ask == 0:
            return _labelled(
                stem=f"ช่วงที่ประเทศไทยได้รับ{season.wind} เป็นฤดูใด",
                correct=season.name,
                wrongs=tuple(other.name for other in others) + (rng.choice(SEASON_DECOYS),),
                hint="ลมที่พัดผ่านทะเลนำความชื้นมา ลมที่พัดมาจากแผ่นดินใหญ่นำความเย็นและแห้งมา",
                topic=MONSOON_TOPIC,
            )
        return _labelled(
            stem=f"เหตุใดประเทศไทยจึงมี{season.name}",
            correct=season.because,
            wrongs=tuple(other.because for other in others)
                   + (rng.choice(BECAUSE_DECOYS),),
            hint="นึกว่าช่วงนั้นมีมรสุมใดพัดมา และลมนั้นพัดผ่านบริเวณใด",
            topic=MONSOON_TOPIC,
        )


@question_type(
    "geo.monsoon_season_fluency",
    display_name={"th": "อธิบายผลของมรสุมต่อฤดูของประเทศไทยจากข้อมูล"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=MONSOON_TOPIC,
)
class MonsoonSeasonFluency(QuestionType):
    """Explain a month's season from the wind, rain and temperature on its row."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = season_record(rng)
        record = _record_text(rows)
        season, month, _, _ = rng.choice(rows)
        stem = f"ข้อมูลลมฟ้าอากาศของจังหวัดหนึ่งที่รวบรวมได้ — {record}"
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{stem} จากข้อมูลนี้ เดือน{month}อยู่ในฤดูใด และเพราะเหตุใด",
                correct=_season_answer(season),
                wrongs=tuple(_season_answer(other) for other in SEASONS if other.name != season.name)
                       + (f"{season.name} เพราะโลกอยู่ใกล้ดวงอาทิตย์มากที่สุดในเดือนนี้",),
                hint="ดูลมที่พัดในเดือนนั้น แล้วตรวจกับปริมาณฝนและอุณหภูมิในแถวเดียวกัน",
                topic=MONSOON_TOPIC,
            )
        return _labelled(
            stem=f"{stem} จากข้อมูลนี้ เดือนใดได้รับผลจาก{season.wind}",
            correct=f"เดือน{month}",
            wrongs=tuple(f"เดือน{other_month}" for _, other_month, _, _ in rows if other_month != month)
                   + ("ไม่มีเดือนใดในข้อมูล",),
            hint="หาแถวที่มีชื่อลมตรงกับคำถาม",
            topic=MONSOON_TOPIC,
        )


@question_type(
    "geo.monsoon_season_application",
    display_name={"th": "ใช้ความรู้เรื่องมรสุมในชีวิตจริง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=MONSOON_TOPIC,
)
class MonsoonSeasonApplication(QuestionType):
    """The southern east coast's winter rain, a late monsoon, and choosing data."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MONSOON_SCENARIOS,
            hint="นึกว่ามรสุมพัดมาจากที่ใด ผ่านทะเลหรือแผ่นดิน และนำอะไรมาด้วย",
        ), MONSOON_TOPIC)
