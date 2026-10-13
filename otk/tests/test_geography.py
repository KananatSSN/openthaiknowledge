"""Geography (ส 5): filing, and every computed answer checked by another route.

The sets compute their answers with the helpers in ``otk.sets._support.geography``.
These tests read each drawn question's stem back, recompute the answer without
those helpers (``datetime`` for clocks and time zones, ``atan2`` for directions,
``Fraction`` for scales), and require the marked choice to be it.
"""

from __future__ import annotations

import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path
from random import Random

import pytest

from otk.core import REGISTRY, catalog, generate
from otk.core.curriculum_geography import GEOGRAPHY_UNITS
from otk.sets._support.geography import GRID_MAP_SPECS

ROOT = Path(__file__).resolve().parents[2]
KEYS = sorted(k for k in REGISTRY if k.startswith("geog."))
SEEDS = range(300)
SPECS = {spec.asset_id: spec for spec in GRID_MAP_SPECS}

AZIMUTHS = {"ทิศเหนือ": 0, "ทิศตะวันออกเฉียงเหนือ": 45, "ทิศตะวันออก": 90,
            "ทิศตะวันออกเฉียงใต้": 135, "ทิศใต้": 180, "ทิศตะวันตกเฉียงใต้": 225,
            "ทิศตะวันตก": 270, "ทิศตะวันตกเฉียงเหนือ": 315}


def stem(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def answer(q) -> str:
    return q.choices[q.answer].content[0].text


def asset(q) -> str:
    return next(b.asset_id for b in q.stem if b.kind == "image")


def draws(key: str):
    for seed in SEEDS:
        yield generate(key, rng=Random(seed))


def num(s: str) -> Fraction:
    return Fraction(s.replace(",", ""))


def signed(deg: str, word: str) -> int:
    return int(deg) * (1 if word in ("เหนือ", "ตะวันออก") else -1)


def hhmm(s: str) -> tuple[int, int]:
    h, m = re.fullmatch(r"(\d\d)\.(\d\d) น\.", s).groups()
    return int(h), int(m)


# ── filing ───────────────────────────────────────────────────────────────────

def test_every_geography_set_is_filed_by_its_unit():
    rows = [r for r in catalog() if r["key"].startswith("geog.")]
    assert len(rows) == len(KEYS) >= 30
    official = {json.loads(line)["code"] for line in
                (ROOT / "docs/curriculum_sources/_md/indicators.jsonl").read_text("utf-8").splitlines()}
    for row in rows:
        assert row["subject"] == "ภูมิศาสตร์", row["key"]
        assert row["curriculum_node_id"].startswith("th-geo-2560-"), row["key"]
        assert row["indicator_codes"] and set(row["indicator_codes"]) <= official, row["key"]
        assert row["learning_stage"] in (1, 2, 3), row["key"]


def test_unit_docstrings_list_the_filed_indicators():
    for key in KEYS:
        qt = REGISTRY[key]
        doc = sys.modules[type(qt).__module__].__doc__
        listed = re.search(r"^Indicators: (.+)$", doc, re.M).group(1).split(", ")
        level = qt.level["th"]
        assert tuple(listed) == GEOGRAPHY_UNITS[(level, qt.topic)][1], key
        assert doc.splitlines()[0] == qt.topic, key


def test_every_unit_in_the_table_has_sets():
    filed = {(REGISTRY[k].level["th"], REGISTRY[k].topic) for k in KEYS}
    assert filed == set(GEOGRAPHY_UNITS)


def test_the_geography_indicators_are_indexed():
    rows = [json.loads(line) for line in
            (ROOT / "docs/curriculum_sources/_md/indicators.jsonl").read_text("utf-8").splitlines()]
    geo = [r for r in rows if r["subject"] == "geography"]
    assert len(geo) == 66
    assert {r["code"] for r in geo} >= {"ส 5.1 ป.1/1", "ส 5.1 ม.4-6/3", "ส 5.2 ม.3/5"}


# ── variety ──────────────────────────────────────────────────────────────────

# Fixed banks, and spaces that are small by nature: eight directions, each
# facing with three sides (24 questions) or two ways of asking its azimuth (16).
FINITE = {"geog.globe_and_map_p2", "geog.resource_wise_use_p2", "geog.contour_reading_m4",
          "geog.map_colour_p2", "geog.nature_benefit_p1", "geog.facing_direction_p3",
          "geog.azimuth_m2", "geog.weather_in_a_day_p1", "geog.earth_sun_moon_p2",
          "geog.region_landform_p6", "geog.region_livelihood_p6", "geog.disaster_asia_m1",
          "geog.disaster_europe_africa_m2", "geog.disaster_americas_m3",
          "geog.earth_sun_moon_reasoning_p2", "geog.season_plan_p2", "geog.disaster_kind_p6",
          "geog.environmental_organisation_m3", "geog.sun_direction_p2"}


@pytest.mark.parametrize("key", [k for k in KEYS if k not in FINITE])
def test_a_generator_offers_at_least_25_distinct_questions(key):
    seen = {stem(q) + "|" + "|".join(sorted(c.content[0].text for c in q.choices))
            for q in draws(key)}
    assert len(seen) >= 25, (key, len(seen))


# ── ป.1 ─────────────────────────────────────────────────────────────────────

def test_lineup_position():
    for q in draws("geog.lineup_position_p1"):
        s = stem(q)
        row = re.search(r"ได้แก่ (\S+) (\S+) (\S+) (\S+) (\S+) ใคร", s).groups()
        if m := re.search(r"ทางขวามือของ(\S+?)ติดกัน", s):
            want = row[row.index(m.group(1)) + 1]
        elif m := re.search(r"ทางซ้ายมือของ(\S+?)ติดกัน", s):
            want = row[row.index(m.group(1)) - 1]
        elif m := re.search(r"ระหว่าง(\S+?)กับ(\S+)$", s):
            i, j = row.index(m.group(1)), row.index(m.group(2))
            want = row[(i + j) // 2]
        else:
            want = row[0] if "ซ้ายสุด" in s else row[-1]
        assert answer(q) == want, s


def test_near_far():
    for q in draws("geog.near_far_p1"):
        s = stem(q)
        homes = {k: int(m.replace(",", "")) for k, m in re.findall(r"บ้านของ(\S+?)ห่าง ([\d,]+) เมตร", s)}
        pick = min if "ใกล้โรงเรียนที่สุด" in s else max
        assert answer(q) == pick(homes, key=homes.get), s


def test_classroom_plan():
    for q in draws("geog.classroom_plan_p1"):
        spec = SPECS[asset(q)]
        a, b = re.search(r"โต๊ะ ([A-H]) และหันหน้า.*โต๊ะ ([A-H]) อยู่", stem(q)).groups()
        (ax, ay), (bx, by) = spec.places["ABCDEFGH".index(a)], spec.places["ABCDEFGH".index(b)]
        # Facing the board (+y): right is +x.
        want = {(1, 0): "ทางขวามือ", (-1, 0): "ทางซ้ายมือ", (0, 1): "ข้างหน้า", (0, -1): "ข้างหลัง"}[
            ((bx > ax) - (bx < ax), (by > ay) - (by < ay))]
        assert answer(q) == want


def test_shadow_length():
    for q in draws("geog.shadow_length_p1"):
        hours = {c.content[0].text: int(c.content[0].text[:2]) for c in q.choices}
        # Solar noon in Thailand falls between 12.00 and 12.45: score each hour
        # by its distance from both ends, and the answer must win either way.
        for noon in (12.0, 12.75):
            dist = {t: abs(h - noon) for t, h in hours.items()}
            pick = min if "สั้นที่สุด" in stem(q) else max
            assert answer(q) == pick(dist, key=dist.get), stem(q)


# ── ป.3 ─────────────────────────────────────────────────────────────────────

def test_facing_direction():
    for q in draws("geog.facing_direction_p3"):
        facing, side = re.search(r"หันหน้าไปทาง(\S+) (\S+?)ของเรา", stem(q)).groups()
        turn = {"ขวามือ": 90, "ซ้ายมือ": -90, "ข้างหลัง": 180}[side]
        assert AZIMUTHS[answer(q)] == (AZIMUTHS[facing] + turn) % 360


def test_turning_direction():
    for q in draws("geog.turning_direction_p3"):
        facing, way, angle = re.search(r"หันหน้าไปทาง(\S+) แล้วหมุนตัว(\S+) (\d+) องศา", stem(q)).groups()
        sign = 1 if way == "ตามเข็มนาฬิกา" else -1
        assert AZIMUTHS[answer(q)] == (AZIMUTHS[facing] + sign * int(angle)) % 360


def _bearing(dx: int, dy: int) -> int:
    """Azimuth from north, clockwise, by trigonometry."""
    return round(math.degrees(math.atan2(dx, dy))) % 360


def test_map_direction():
    for q in draws("geog.map_direction_p3"):
        spec = SPECS[asset(q)]
        a, here, b, there = re.search(r"([A-H]) คือ(\S+) และ ([A-H]) คือ(\S+) ", stem(q)).groups()
        (ax, ay), (bx, by) = spec.places["ABCDEFGH".index(a)], spec.places["ABCDEFGH".index(b)]
        assert AZIMUTHS[answer(q)] == _bearing(bx - ax, by - ay)


def test_walk_route():
    steps = {"ทิศเหนือ": (0, 1), "ทิศใต้": (0, -1), "ทิศตะวันออก": (1, 0), "ทิศตะวันตก": (-1, 0)}
    for q in draws("geog.walk_route_p3"):
        spec = SPECS[asset(q)]
        s = stem(q)
        x, y = spec.places["ABCDEFGH".index(re.search(r"เริ่มที่ ([A-H])", s).group(1))]
        for way, n in re.findall(r"เดินไปทาง(\S+) (\d+) ช่อง", s):
            x, y = x + steps[way][0] * int(n), y + steps[way][1] * int(n)
        assert spec.places["ABCDEFGH".index(answer(q))] == (x, y), s


# ── ม.1 ─────────────────────────────────────────────────────────────────────

def test_hemisphere():
    for q in draws("geog.hemisphere_m1"):
        s = stem(q)
        if s.startswith("ตำแหน่งใด"):
            text = answer(q)
            lat = int(re.search(r"ละติจูด (\d+)", text).group(1))
            others = [int(re.search(r"ละติจูด (\d+)", c.content[0].text).group(1)) for c in q.choices]
            assert lat == min(others)
            continue
        lat, ns, lon, ew = re.search(r"ละติจูด (\d+) องศา(\S+) ลองจิจูด (\d+) องศา(\S+) อยู่", s).groups()
        assert answer(q) == f"ซีกโลก{ns}และซีกโลก{ew}"


def _local(q):
    s = stem(q)
    (da, wa), (db, wb) = re.findall(r"ลองจิจูด (\d+) องศา(ตะวันออก|ตะวันตก)", s)
    h, m = hhmm(re.search(r"เมือง ก เป็น (\d\d\.\d\d น\.)", s).group(1))
    # Local mean time is UTC shifted by 4 minutes a degree east.
    tz_a = timezone(timedelta(minutes=4 * signed(da, wa)))
    tz_b = timezone(timedelta(minutes=4 * signed(db, wb)))
    there = datetime(2026, 1, 15, h, m, tzinfo=tz_a).astimezone(tz_b)
    return f"{there:%H.%M} น."


@pytest.mark.parametrize("key", ["geog.local_time_hours_m1", "geog.local_time_minutes_m1"])
def test_local_time(key):
    for q in draws(key):
        assert answer(q) == _local(q), stem(q)


def test_time_zone():
    for q in draws("geog.time_zone_m1"):
        s = stem(q)
        offsets = [(1 if sign == "+" else -1) * (int(h) * 60 + int(m or 0))
                   for sign, h, m in re.findall(r"UTC([+−])(\d+)(?::(\d\d))?", s)]
        day, h, m = re.search(r"เป็นวันที่ (\d+) เวลา (\d\d)\.(\d\d) น\.", s).groups()
        here = datetime(2026, 1, int(day), int(h), int(m), tzinfo=timezone(timedelta(minutes=offsets[0])))
        there = here.astimezone(timezone(timedelta(minutes=offsets[1])))
        assert answer(q) == f"วันที่ {there.day} เวลา {there:%H.%M} น.", s


def test_date_line():
    weekdays = ("วันอาทิตย์", "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์")
    for q in draws("geog.date_line_m1"):
        s = stem(q)
        wd, date = re.search(r"ขณะบินข้ามเส้นเป็น(วัน\S+?)ที่ (\d+)", s).groups()
        shift = -1 if "บินไปทางทิศตะวันออก" in s else 1
        want = f"{weekdays[(weekdays.index(wd) + shift) % 7]}ที่ {int(date) + shift}"
        assert answer(q) == want, s


def test_latitude_distance():
    for q in draws("geog.latitude_distance_m1"):
        (a, wa), (b, wb) = re.findall(r"ละติจูด (\d+) องศา(เหนือ|ใต้)", stem(q))
        km = abs(signed(a, wa) - signed(b, wb)) * 111
        assert num(answer(q).split()[0]) == km


@pytest.mark.parametrize("key", ["geog.continent_landform_m1", "geog.continent_landform_m2",
                                 "geog.continent_landform_m3"])
def test_continent_landform(key):
    from otk.sets._support.geography import CONTINENTS
    home = {f: c for c, fs in CONTINENTS.items() for f in fs}
    assert len(home) == sum(len(fs) for fs in CONTINENTS.values())   # no landform twice
    for q in draws(key):
        s = stem(q)
        if m := re.search(r"“(.+)” อยู่ในทวีปใด", s):
            assert answer(q) == home[m.group(1)]
        else:
            continent = re.search(r"อยู่ใน(ทวีป.+)$", s).group(1)
            fits = [c.content[0].text for c in q.choices if home[c.content[0].text] == continent]
            assert fits == [answer(q)], s


# ── ม.2 ─────────────────────────────────────────────────────────────────────

def _scale(s: str) -> int:
    return int(re.search(r"1 : ([\d,]+)", s).group(1).replace(",", ""))


def test_map_to_ground():
    for q in draws("geog.map_to_ground_m2"):
        s = stem(q)
        cm = num(re.search(r"วัดได้ ([\d.,]+) เซนติเมตร", s).group(1))
        assert num(answer(q).split()[0]) * 1000 * 100 == cm * _scale(s)


def test_ground_to_map():
    for q in draws("geog.ground_to_map_m2"):
        s = stem(q)
        km = num(re.search(r"ห่างกันจริง ([\d.,]+) กิโลเมตร", s).group(1))
        assert num(answer(q).split()[0]) * _scale(s) == km * 1000 * 100


def test_find_scale():
    for q in draws("geog.find_scale_m2"):
        s = stem(q)
        km = num(re.search(r"สองเมือง ([\d.,]+) กิโลเมตร", s).group(1))
        cm = num(re.search(r"วัดได้ ([\d.,]+) เซนติเมตร", s).group(1))
        assert _scale(answer(q)) == km * 100_000 / cm


def test_scale_detail():
    for q in draws("geog.scale_detail_m2"):
        scales = [_scale(c.content[0].text) for c in q.choices]
        pick = min if "รายละเอียด" in stem(q) else max
        assert _scale(answer(q)) == pick(scales)


def test_azimuth():
    for q in draws("geog.azimuth_m2"):
        s = stem(q)
        if m := re.search(r"มุมอะซิมุท (\d+) องศา ชี้", s):
            assert AZIMUTHS[answer(q)] == int(m.group(1))
        else:
            way = re.match(r"(\S+?)มีมุมอะซิมุท", s).group(1)
            assert answer(q) == f"{AZIMUTHS[way]} องศา"


def test_back_azimuth():
    for q in draws("geog.back_azimuth_m2"):
        there = int(re.search(r"ได้มุมอะซิมุท (\d+) องศา", stem(q)).group(1))
        back = int(answer(q).split()[0])
        assert (back - there) % 360 == 180 and 0 <= back < 360


# ── ม.4 ─────────────────────────────────────────────────────────────────────

def test_contour_interval():
    for q in draws("geog.contour_interval_m4"):
        s = stem(q)
        low, high = (int(x.replace(",", "")) for x in re.findall(r"([\d,]+) เมตร", s)[:2])
        between = int(re.search(r"อีก (\d+) เส้น", s).group(1))
        assert num(answer(q).split()[0]) == Fraction(high - low, between + 1)


def test_contour_height():
    for q in draws("geog.contour_height_m4"):
        s = stem(q)
        interval = int(re.search(r"ช่วงชั้นความสูง (\d+) เมตร", s).group(1))
        base = int(re.search(r"จุด ก อยู่บนเส้นชั้นความสูง ([\d,]+) เมตร", s).group(1).replace(",", ""))
        lines = int(re.search(r"จุด ก ไป (\d+) เส้น", s).group(1))
        sign = 1 if "สูงกว่าจุด ก" in s else -1
        assert num(answer(q).split()[0]) == base + sign * lines * interval


def test_slope_gradient():
    for q in draws("geog.slope_gradient_m4"):
        s = stem(q)
        scale = _scale(s)
        a, b = (int(x.replace(",", "")) for x in re.findall(r"เส้นชั้นความสูง ([\d,]+) เมตร", s))
        cm = num(re.search(r"วัดได้ ([\d.]+) เซนติเมตร", s).group(1))
        run_m = cm * scale / 100
        rise, run = answer(q).split(" : ")
        assert Fraction(int(rise)) / num(run) == Fraction(b - a) / run_m, s


def test_population_density():
    for q in draws("geog.population_density_m4"):
        s = stem(q)
        area = num(re.search(r"พื้นที่ ([\d,]+) ตาราง", s).group(1))
        people = num(re.search(r"ประชากร ([\d,]+) คน", s).group(1))
        assert num(answer(q).split()[0]) == people / area


def test_natural_increase():
    for q in draws("geog.natural_increase_m4"):
        s = stem(q)
        people, births, deaths = (num(x) for x in re.findall(r"([\d,]{5,}) คน", s))
        assert num(answer(q).split()[1]) == (births - deaths) / people * 100, s


def test_doubling_time():
    for q in draws("geog.doubling_time_m4"):
        rate = num(re.search(r"ร้อยละ ([\d.]+) ต่อปี", stem(q)).group(1))
        assert num(answer(q).split()[0]) == 70 / rate
        assert all((num(c.content[0].text.split()[0]) * 100).denominator == 1 for c in q.choices)


def test_waste_count():
    from otk.sets.geography.p2.waste import WasteBin
    bin_of = {m: c.label for c in WasteBin.CATEGORIES for m in c.members}
    for q in draws("geog.waste_count_p2"):
        s = stem(q)
        listed = s.split(": ", 1)[1].split(" ขยะที่ต้องทิ้งลง")[0]
        colour = re.search(r"ทิ้งลง(ถังสี\S+?)มีทั้งหมด", s).group(1)
        total = 0
        for item in bin_of:
            if m := re.search(re.escape(item) + r" (\d+) ", listed + " "):
                if bin_of[item].startswith(colour):
                    total += int(m.group(1))
        assert answer(q) == f"{total} ชิ้น", s


def test_map_nearest():
    for q in draws("geog.map_nearest_p2"):
        spec = SPECS[asset(q)]
        here = spec.places["ABCDEFGH".index(re.search(r"ใกล้ ([A-H]) ", stem(q)).group(1))]
        dist = {L: math.dist(here, spec.places[i]) for i, L in enumerate("ABCDEFGH"[:len(spec.places)])
                if spec.places[i] != here}
        assert answer(q) == min(dist, key=dist.get)


def test_sun_direction():
    for q in draws("geog.sun_direction_p2"):
        s = stem(q)
        sun = 90 if s.startswith("ตอนเช้า") else 270
        facing = sun if "หันหน้าเข้าหา" in s else sun + 180
        side = re.search(r"ดวงอาทิตย์ (\S+?)ของเรา", s).group(1)
        turn = {"ข้างหน้า": 0, "ข้างหลัง": 180, "ขวามือ": 90, "ซ้ายมือ": -90}[side]
        assert AZIMUTHS[answer(q)] == (facing + turn) % 360, s
