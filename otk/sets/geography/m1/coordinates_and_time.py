"""พิกัดภูมิศาสตร์และเวลาของโลก

ภูมิศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ส 5.1 ม.1/2
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.geography import M1, SUBJECT, choices, clock, number, stage

PROVENANCE = Provenance("original")


TOPIC = "พิกัดภูมิศาสตร์และเวลาของโลก"


def latitude(deg: int) -> str:
    """Signed degrees, north positive: -23 -> "23 องศาใต้"."""
    return f"{abs(deg)} องศา{'เหนือ' if deg > 0 else 'ใต้'}"


def longitude(deg: int) -> str:
    """Signed degrees, east positive: -75 -> "75 องศาตะวันตก"."""
    return f"{abs(deg)} องศา{'ตะวันออก' if deg > 0 else 'ตะวันตก'}"


def hemispheres(lat: int, lon: int) -> str:
    return (f"ซีกโลก{'เหนือ' if lat > 0 else 'ใต้'}"
            f"และซีกโลก{'ตะวันออก' if lon > 0 else 'ตะวันตก'}")


@question_type(
    "geog.hemisphere_m1",
    display_name={"th": "อ่านพิกัดละติจูดและลองจิจูดแล้วบอกซีกโลก"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class Hemisphere(QuestionType):
    def build(self, rng: Random, **params):
        if rng.random() < 0.6:
            lat = rng.randint(1, 80) * rng.choice((1, -1))
            lon = rng.randint(1, 179) * rng.choice((1, -1))
            return choices(
                stem=f"ตำแหน่งที่ละติจูด {latitude(lat)} ลองจิจูด {longitude(lon)} อยู่ในซีกโลกใด",
                correct=hemispheres(lat, lon),
                wrongs=[("direction.opposite", hemispheres(-lat, lon)),
                        ("direction.left_right_swapped", hemispheres(lat, -lon)),
                        hemispheres(-lat, -lon)],
                hint="ละติจูดบอกว่าอยู่เหนือหรือใต้เส้นศูนย์สูตร ลองจิจูดบอกว่าอยู่ตะวันออกหรือตะวันตกของเส้นเมริเดียนแรก",
                topic=TOPIC)
        # Which of four places is nearest the equator: the smallest latitude,
        # whatever the longitudes are.
        lats = [d * rng.choice((1, -1)) for d in rng.sample(range(2, 71), 4)]
        lons = [d * rng.choice((1, -1)) for d in rng.sample(range(2, 178), 4)]
        spots = [f"ละติจูด {latitude(a)} ลองจิจูด {longitude(o)}" for a, o in zip(lats, lons)]
        near = min(range(4), key=lambda i: abs(lats[i]))
        lon_slip = min(range(4), key=lambda i: abs(lons[i]))
        far = max(range(4), key=lambda i: abs(lats[i]))
        wrongs = []
        if lon_slip != near:
            wrongs.append(spots[lon_slip])
        wrongs += [spots[far], *(s for i, s in enumerate(spots) if i not in (near, far, lon_slip))]
        return choices(stem="ตำแหน่งใดอยู่ใกล้เส้นศูนย์สูตรมากที่สุด",
                       correct=spots[near], wrongs=wrongs,
                       hint="เส้นศูนย์สูตรคือละติจูด 0 องศา ดูเฉพาะค่าละติจูด ค่ายิ่งน้อยยิ่งใกล้เส้นศูนย์สูตร",
                       topic=TOPIC)


def _local_time(rng: Random, step: int):
    """Two longitudes ``step`` degrees apart at least, and a time at the first
    whose local time at the second falls on the same day."""
    while True:
        a = rng.randrange(-180 // step + 1, 180 // step + 1) * step
        b = rng.randrange(-180 // step + 1, 180 // step + 1) * step
        if a == b or a == 0 or b == 0:
            continue
        diff = (b - a) * 4                       # minutes: 1 degree is 4 minutes
        at_a = rng.randrange(6 * 4, 20 * 4) * 15  # 06.00-19.45
        if 0 <= at_a + diff < 24 * 60 and 0 <= at_a - diff < 24 * 60 and abs(diff) <= 10 * 60:
            return a, b, at_a, diff


TIME_HINT = ("โลกหมุนรอบตัวเองจากทิศตะวันตกไปทิศตะวันออก ที่อยู่ทางตะวันออกจึงเห็นดวงอาทิตย์ก่อนและมีเวลาเร็วกว่า "
             "ลองจิจูดต่างกัน 15 องศา เวลาต่างกัน 1 ชั่วโมง หรือ 1 องศา 4 นาที")


@question_type(
    "geog.local_time_hours_m1",
    display_name={"th": "หาเวลาท้องถิ่นจากลองจิจูดที่ต่างกันเป็นจำนวนเต็มชั่วโมง"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class LocalTimeHours(QuestionType):
    def build(self, rng: Random, **params):
        a, b, at_a, diff = _local_time(rng, 15)
        return choices(
            stem=(f"เมือง ก อยู่ที่ลองจิจูด {longitude(a)} เมือง ข อยู่ที่ลองจิจูด {longitude(b)} "
                  f"ขณะที่เวลาท้องถิ่นของเมือง ก เป็น {clock(at_a)} เวลาท้องถิ่นของเมือง ข เป็นเท่าใด"),
            correct=clock(at_a + diff),
            wrongs=[("time.east_west_reversed", clock(at_a - diff)),
                    clock(at_a + diff + 60), clock(at_a + diff - 60), clock(at_a + diff + 120)],
            hint=TIME_HINT, topic=TOPIC)


@question_type(
    "geog.local_time_minutes_m1",
    display_name={"th": "หาเวลาท้องถิ่นจากลองจิจูด โดย 1 องศาเท่ากับ 4 นาที"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class LocalTimeMinutes(QuestionType):
    def build(self, rng: Random, **params):
        while True:
            a, b, at_a, diff = _local_time(rng, 5)
            if (b - a) % 15:                     # not a whole number of hours
                break
        degrees = abs(b - a)
        return choices(
            stem=(f"เมือง ก อยู่ที่ลองจิจูด {longitude(a)} เมือง ข อยู่ที่ลองจิจูด {longitude(b)} "
                  f"ขณะที่เวลาท้องถิ่นของเมือง ก เป็น {clock(at_a)} เวลาท้องถิ่นของเมือง ข เป็นเท่าใด"),
            correct=clock(at_a + diff),
            wrongs=[("time.east_west_reversed", clock(at_a - diff)),
                    # Read 15 degrees an hour as 15 minutes a degree.
                    ("units.wrong_conversion", clock(at_a + (15 if diff > 0 else -15) * degrees)),
                    clock(at_a + diff + 20), clock(at_a + diff - 20)],
            hint=TIME_HINT, topic=TOPIC)


# Standard (not daylight-saving) offsets from UTC, in minutes. The stems state
# each city's offset, so the set practises the arithmetic, not the table.
CITIES = (
    ("ลอนดอน (สหราชอาณาจักร)", 0), ("ปารีส (ฝรั่งเศส)", 60), ("ไคโร (อียิปต์)", 120),
    ("มอสโก (รัสเซีย)", 180), ("ดูไบ (สหรัฐอาหรับเอมิเรตส์)", 240), ("นิวเดลี (อินเดีย)", 330),
    ("กรุงเทพมหานคร (ไทย)", 420), ("ปักกิ่ง (จีน)", 480), ("โตเกียว (ญี่ปุ่น)", 540),
    ("ซิดนีย์ (ออสเตรเลีย)", 600), ("โอ๊คแลนด์ (นิวซีแลนด์)", 720), ("โฮโนลูลู (สหรัฐอเมริกา)", -600),
    ("ลอสแอนเจลิส (สหรัฐอเมริกา)", -480), ("นิวยอร์ก (สหรัฐอเมริกา)", -300),
    ("รีโอเดจาเนโร (บราซิล)", -180),
)


def utc(offset: int) -> str:
    sign = "+" if offset >= 0 else "−"
    h, m = divmod(abs(offset), 60)
    return f"UTC{sign}{h}" + (f":{m:02d}" if m else "")


def when(day: int, minutes: int) -> str:
    """A day of the month and minutes after its midnight, rolled into range."""
    d, m = divmod(minutes, 24 * 60)
    return f"วันที่ {day + d} เวลา {clock(m)}"


@question_type(
    "geog.time_zone_m1",
    display_name={"th": "เปรียบเทียบวันและเวลามาตรฐานของเมืองต่าง ๆ ตามเขตเวลา"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class TimeZone(QuestionType):
    def build(self, rng: Random, **params):
        (here, off_a), (there, off_b) = rng.sample(CITIES, 2)
        day = rng.randint(2, 27)
        at_a = rng.randrange(0, 24 * 4) * 15
        diff = off_b - off_a
        wrongs = [("time.east_west_reversed", when(day, at_a - diff))]
        if (at_a + diff) // (24 * 60):
            wrongs.append(("time.date_not_changed", when(day, (at_a + diff) % (24 * 60))))
        wrongs += [when(day, at_a + diff + 60), when(day, at_a + diff - 60),
                   when(day, at_a + off_b)]
        return choices(
            stem=(f"เวลามาตรฐานของ{here}คือ {utc(off_a)} และของ{there}คือ {utc(off_b)} "
                  f"(ไม่คิดเวลาออมแสง) ขณะที่{here}เป็น{when(day, at_a)} "
                  f"ที่{there}เป็นวันที่และเวลาใด"),
            correct=when(day, at_a + diff), wrongs=wrongs,
            hint="หาผลต่างของ UTC ทั้งสองเมือง เมืองที่มีค่า UTC มากกว่ามีเวลาเร็วกว่า ถ้าเวลาเลยเที่ยงคืนต้องเปลี่ยนวันที่ด้วย",
            topic=TOPIC)


WEEKDAYS = ("วันอาทิตย์", "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์")
# (from, to, crossing eastward): eastward across the line the date goes back a day.
FLIGHTS = (
    ("โตเกียว (ญี่ปุ่น)", "โฮโนลูลู (รัฐฮาวาย สหรัฐอเมริกา)", True),
    ("ซิดนีย์ (ออสเตรเลีย)", "ลอสแอนเจลิส (สหรัฐอเมริกา)", True),
    ("โอ๊คแลนด์ (นิวซีแลนด์)", "ซานฟรานซิสโก (สหรัฐอเมริกา)", True),
    ("โฮโนลูลู (รัฐฮาวาย สหรัฐอเมริกา)", "โตเกียว (ญี่ปุ่น)", False),
    ("ลอสแอนเจลิส (สหรัฐอเมริกา)", "ซิดนีย์ (ออสเตรเลีย)", False),
    ("ซานฟรานซิสโก (สหรัฐอเมริกา)", "โอ๊คแลนด์ (นิวซีแลนด์)", False),
)


@question_type(
    "geog.date_line_m1",
    display_name={"th": "ปรับวันที่เมื่อเดินทางข้ามเส้นวันที่สากล"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class DateLine(QuestionType):
    def build(self, rng: Random, **params):
        origin, dest, east = rng.choice(FLIGHTS)
        weekday, date = rng.randrange(7), rng.randint(2, 27)

        def day(shift: int, date_shift: int | None = None) -> str:
            return f"{WEEKDAYS[(weekday + shift) % 7]}ที่ {date + (shift if date_shift is None else date_shift)}"

        step = -1 if east else 1
        way = "ทิศตะวันออก" if east else "ทิศตะวันตก"
        return choices(
            stem=(f"เครื่องบินออกจาก{origin} บินไปทาง{way}ข้ามเส้นวันที่สากลไปยัง{dest} "
                  f"ขณะบินข้ามเส้นเป็น{day(0)} ผู้โดยสารต้องปรับวันเป็นวันใด"),
            correct=day(step),
            wrongs=[("time.east_west_reversed", day(-step)),
                    ("time.date_not_changed", day(0)),
                    day(step, 0)],
            hint="ข้ามเส้นวันที่สากลไปทางทิศตะวันออก ให้ลดวันลง 1 วัน ข้ามไปทางทิศตะวันตก ให้เพิ่มวันขึ้น 1 วัน",
            topic=TOPIC)


KM_PER_DEGREE = 111


@question_type(
    "geog.latitude_distance_m1",
    display_name={"th": "หาระยะทางตามแนวเหนือใต้จากละติจูดที่ต่างกัน"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class LatitudeDistance(QuestionType):
    def build(self, rng: Random, **params):
        a, b = rng.sample(range(1, 61), 2)
        while abs(a - b) < 3:
            a, b = rng.sample(range(1, 61), 2)
        across = rng.random() < 0.5
        lat_b = -b if across else b
        degrees = abs(a - lat_b)
        slip = abs(a - b) if across else a + b
        lon = rng.randint(1, 179) * rng.choice((1, -1))
        return choices(
            stem=(f"เมือง ก และเมือง ข อยู่บนลองจิจูด {longitude(lon)} เท่ากัน เมือง ก อยู่ที่ละติจูด "
                  f"{latitude(a)} เมือง ข อยู่ที่ละติจูด {latitude(lat_b)} ถ้าละติจูด 1 องศาห่างกันประมาณ "
                  f"{KM_PER_DEGREE} กิโลเมตร สองเมืองนี้ห่างกันประมาณกี่กิโลเมตร"),
            correct=f"{number(degrees * KM_PER_DEGREE)} กิโลเมตร",
            wrongs=[("operation.reversed", f"{number(slip * KM_PER_DEGREE)} กิโลเมตร"),
                    f"{number(degrees * 60)} กิโลเมตร",
                    f"{number((degrees + 1) * KM_PER_DEGREE)} กิโลเมตร",
                    f"{number((degrees - 1) * KM_PER_DEGREE)} กิโลเมตร"],
            hint="ถ้าอยู่ซีกโลกเดียวกันให้ลบค่าละติจูด ถ้าอยู่คนละซีกโลกให้บวก แล้วคูณด้วยระยะทางต่อ 1 องศา",
            topic=TOPIC)
