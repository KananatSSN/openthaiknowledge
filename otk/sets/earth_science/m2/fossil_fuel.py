"""เชื้อเพลิงซากดึกดำบรรพ์

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/1

Sets moved here from: science_wave_c19.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c19 import FUEL_SCENARIOS

PROVENANCE = Provenance("original")


FUEL_TOPIC = "เชื้อเพลิงซากดึกดำบรรพ์"


class Fuel(NamedTuple):
    """A fossil fuel on the three aspects the indicator compares, and its emissions."""
    name: str
    forms: str
    property: str
    use: str
    co2: tuple[int, int]
    so2: tuple[int, int]


# Emissions per the same amount of heat, in rounded relative units. The bands do
# not overlap and keep the real order: coal > crude oil > natural gas.
FUELS = (
    Fuel("ถ่านหิน",
         "ซากพืชทับถมในแอ่งน้ำจืดนานหลายล้านปีภายใต้ความร้อนและความดัน",
         "เป็นของแข็งสีดำ เมื่อเผาให้เขม่าและแก๊สซัลเฟอร์ไดออกไซด์มาก",
         "ใช้เป็นเชื้อเพลิงผลิตไฟฟ้าในโรงไฟฟ้าและในโรงงานปูนซีเมนต์",
         (95, 105), (40, 60)),
    Fuel("น้ำมันดิบ",
         "ซากสิ่งมีชีวิตขนาดเล็กในทะเลทับถมในชั้นหินตะกอน ได้รับความร้อนและความดันพอเหมาะ",
         "เป็นของเหลวข้น ต้องนำไปกลั่นลำดับส่วนก่อนใช้",
         "กลั่นเป็นน้ำมันเบนซินและดีเซลสำหรับยานพาหนะ",
         (70, 80), (10, 25)),
    Fuel("แก๊สธรรมชาติ",
         "ซากสิ่งมีชีวิตขนาดเล็กในทะเลทับถมในชั้นหินตะกอน ได้รับความร้อนและความดันสูงกว่า",
         "เป็นแก๊สไม่มีสี ติดไฟง่าย เผาไหม้ได้สมบูรณ์และมีเขม่าน้อย",
         "แยกเป็นแก๊สหุงต้มและใช้เป็นเชื้อเพลิงรถยนต์ประเภทเอ็นจีวี",
         (50, 60), (0, 3)),
)


EMISSION_EFFECTS = {
    "co2": "แก๊สคาร์บอนไดออกไซด์เพิ่มปรากฏการณ์เรือนกระจก ทำให้โลกร้อนขึ้น",
    "so2": "แก๊สซัลเฟอร์ไดออกไซด์ทำให้เกิดฝนกรด ซึ่งทำลายพืชและสิ่งปลูกสร้าง",
}


def emissions_record(rng: Random) -> list[tuple[Fuel, int, int]]:
    rows = [(fuel, rng.randint(*fuel.co2), rng.randint(*fuel.so2)) for fuel in FUELS]
    rng.shuffle(rows)
    return rows


ASPECTS = ("forms", "property", "use")


def _fuel_line(names: list[str], table: dict[str, list[str]]) -> str:
    return " / ".join(
        f"{name} — การเกิด: {table['forms'][i]}; สมบัติ: {table['property'][i]}; การใช้ประโยชน์: {table['use'][i]}"
        for i, name in enumerate(names))


@question_type(
    "geo.fossil_fuel_foundation",
    display_name={"th": "ผลกระทบจากการใช้เชื้อเพลิงซากดึกดำบรรพ์จากข้อมูล"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_TOPIC,
)
class FossilFuelFoundation(QuestionType):
    """Explain an effect of burning fuel from an emissions record — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = emissions_record(rng)
        record = " / ".join(
            f"{fuel.name}: คาร์บอนไดออกไซด์ {co2} หน่วย ซัลเฟอร์ไดออกไซด์ {so2} หน่วย"
            for fuel, co2, so2 in rows)
        gas = rng.choice(("co2", "so2"))
        index = 1 if gas == "co2" else 2
        worst = max(rows, key=lambda row: row[index])[0]
        best = min(rows, key=lambda row: row[index])[0]
        name = "คาร์บอนไดออกไซด์" if gas == "co2" else "ซัลเฟอร์ไดออกไซด์"
        other_effect = EMISSION_EFFECTS["so2" if gas == "co2" else "co2"]
        return _labelled(
            stem=f"ข้อมูลแก๊สที่เกิดจากการเผาเชื้อเพลิงเพื่อให้ได้ความร้อนเท่ากัน — {record} "
                 f"จากข้อมูลนี้ ข้อใดอธิบายผลกระทบจากแก๊ส{name}ได้ถูกต้อง",
            correct=f"{worst.name}ปล่อยมากที่สุด และ{EMISSION_EFFECTS[gas]}",
            wrongs=(f"{best.name}ปล่อยมากที่สุด และ{EMISSION_EFFECTS[gas]}",
                    f"{worst.name}ปล่อยมากที่สุด และ{other_effect}",
                    f"{worst.name}ปล่อยมากที่สุด แต่แก๊สนี้ไม่มีผลกระทบต่อสิ่งแวดล้อม",
                    # The wrong fuel and the wrong effect.
                    f"{best.name}ปล่อยมากที่สุด และ{other_effect}",
                    f"{best.name}ปล่อยมากที่สุด แต่แก๊สนี้ไม่มีผลกระทบต่อสิ่งแวดล้อม"),
            hint="หาเชื้อเพลิงที่ตัวเลขของแก๊สนั้นมากที่สุด แล้วนึกว่าแก๊สนั้นทำให้เกิดปัญหาใด",
            topic=FUEL_TOPIC,
        )


@question_type(
    "geo.fossil_fuel_fluency",
    display_name={"th": "เปรียบเทียบการเกิด สมบัติ และการใช้ประโยชน์ของเชื้อเพลิงซากดึกดำบรรพ์"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_TOPIC,
)
class FossilFuelFluency(QuestionType):
    """Compare all three fuels on all three aspects; each wrong choice swaps one aspect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # One fuel: each wrong borrows one aspect from another fuel.
            fuel = rng.choice(FUELS)
            others = [f for f in FUELS if f is not fuel]

            def one(row: dict[str, str]) -> str:
                return f"การเกิด: {row['forms']}; สมบัติ: {row['property']}; การใช้ประโยชน์: {row['use']}"

            own = {aspect: getattr(fuel, aspect) for aspect in ASPECTS}
            wrongs = [one({**own, aspect: getattr(other, aspect)})
                      for aspect in ASPECTS for other in others
                      if getattr(other, aspect) != own[aspect]]
            return _labelled(
                stem=f"ข้อใดบอกการเกิด สมบัติ และการใช้ประโยชน์ของ{fuel.name}ได้ถูกต้องทั้งหมด",
                correct=one(own),
                wrongs=tuple(rng.sample(wrongs, min(5, len(wrongs)))),
                hint="ตรวจทีละส่วน: เกิดจากซากพืชหรือสิ่งมีชีวิตในทะเล อยู่ในสถานะใด และนำไปใช้ทำอะไร",
                topic=FUEL_TOPIC,
            )
        names = [fuel.name for fuel in FUELS]
        table = {aspect: [getattr(fuel, aspect) for fuel in FUELS] for aspect in ASPECTS}
        # Any aspect with any pair of fuels swapped: nine wrong tables, three drawn.
        swaps = [(aspect, pair) for aspect in ASPECTS for pair in _swaps(rng, 3, 3)]
        wrongs = []
        for aspect, (i, j) in rng.sample(swaps, 3):
            changed = dict(table)
            changed[aspect] = _swapped(table[aspect], i, j)
            wrongs.append(_fuel_line(names, changed))
        # Two aspects swapped at once, so the answer is not the table every
        # wrong differs from in a single aspect.
        for _ in range(2):
            (a1, (i1, j1)), (a2, (i2, j2)) = rng.sample(swaps, 2)
            if a1 == a2:
                continue
            changed = dict(table)
            changed[a1] = _swapped(table[a1], i1, j1)
            changed[a2] = _swapped(table[a2], i2, j2)
            wrongs.append(_fuel_line(names, changed))
        wrongs = list(dict.fromkeys(wrongs))
        return _labelled(
            stem="ข้อมูลที่รวบรวมได้เกี่ยวกับถ่านหิน น้ำมันดิบ และแก๊สธรรมชาติ "
                 "ข้อใดเปรียบเทียบกระบวนการเกิด สมบัติ และการใช้ประโยชน์ได้ถูกต้องทั้งหมด",
            correct=_fuel_line(names, table),
            wrongs=tuple(wrongs),
            hint="ตรวจทีละเชื้อเพลิง: เกิดจากซากพืชหรือสิ่งมีชีวิตในทะเล เป็นของแข็ง ของเหลว หรือแก๊ส และใช้ทำอะไร",
            topic=FUEL_TOPIC,
        )


@question_type(
    "geo.fossil_fuel_application",
    display_name={"th": "วิเคราะห์การเกิดและผลกระทบของเชื้อเพลิงซากดึกดำบรรพ์"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=FUEL_TOPIC,
)
class FossilFuelApplication(QuestionType):
    """Why fuels run out, why plants switch to gas, and where each fuel is found."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FUEL_SCENARIOS,
            hint="นึกว่าเชื้อเพลิงนั้นเกิดจากอะไร ในที่ใด และเผาแล้วให้อะไรออกมา",
        ), FUEL_TOPIC)
